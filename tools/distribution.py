"""Explicit local adoption, conflict-aware updates, and portable milestone archives."""
from __future__ import annotations

import io
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from state import PACKAGE, StateError, atomic_write, checkpoint, digest, git_state, local_path, read_json, validate


def package_files(source=PACKAGE):
    release = read_json(source / "foundation.json")
    result = {}
    for pattern in release["include"]:
        matches = list(source.glob(pattern))
        if not matches:
            raise StateError(f"Package input is missing: {pattern}; use the complete upstream source package")
        for path in matches:
            if path.is_file() and "__pycache__" not in path.parts:
                relative = path.relative_to(source).as_posix()
                destination = relative if relative.startswith(".agents/skills/") else f".workflow/{relative}"
                result[destination] = path.read_bytes()
    if not result:
        raise StateError("No reusable package files found")
    return release, result


def bytes_hash(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


def adopt(target: Path, chosen: dict, source=PACKAGE):
    target = target.resolve()
    release, files = package_files(source)
    if (target / ".workflow").exists():
        raise StateError(".workflow already exists. Inspect it; use update for a managed adoption, or choose a clean destination.")
    collisions = [name for name in files if local_path(target, name).exists()]
    if collisions:
        raise StateError("Adoption would overwrite existing files; resolve explicitly: " + ", ".join(collisions))
    target.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        atomic_write(local_path(target, name), data)
    preserved = []
    for name in ["PROFILE.md", "DECISIONS.md", "LESSONS.md"]:
        destination = local_path(target, f"project/{name}")
        if destination.exists():
            preserved.append(f"project/{name}")
        else:
            atomic_write(destination, (source / "templates/project" / name).read_bytes())
    current = local_path(target, "project/state.json")
    if current.exists():
        preserved.append("project/state.json (inspect format manually)")
    else:
        state = read_json(source / "templates/project/state.json")
        state.update(chosen)
        state["portable_files"] = sorted([*files, "AGENTS.md", "project/PROFILE.md", "project/DECISIONS.md", "project/LESSONS.md"])
        # Existing instructions are authoritative; never append or replace them silently.
        state["next_action"] = "Read project/PROFILE.md and existing instructions; agree scope and configure relevant verification commands"
        if not (target / "AGENTS.md").exists():
            atomic_write(target / "AGENTS.md", b"# Project instructions\n\nRead `.workflow/START.md` and `.workflow/AGENTS.md` before work. Project choices live in `project/PROFILE.md`; current execution state is `project/state.json`.\n")
        else:
            preserved.append("AGENTS.md (explicitly reference .workflow/START.md until routing is reviewed)")
        state["git"]["head"] = git_state(target).get("head")
        checkpoint(state, target, current)
    manifest = {"version": release["version"], "managed": {name: bytes_hash(data) for name, data in files.items()}}
    atomic_write(target / ".workflow/installed.json", (json.dumps(manifest, indent=2) + "\n").encode())
    return {"version": release["version"], "entry": ".workflow/START.md", "preserved": preserved,
            "note": "No Git or services changed. Project templates require editing; existing AGENTS is never replaced. Inspect partial files if an OS interruption occurred during adoption."}


def update(target: Path, source=PACKAGE):
    target = target.resolve()
    old = read_json(target / ".workflow/installed.json")
    release, files = package_files(source)
    removed = set(old["managed"]) - set(files)
    conflicts = []
    for name, previous_hash in old["managed"].items():
        path = local_path(target, name)
        if not path.is_file() or digest(path) != previous_hash:
            conflicts.append(name)
    for name in set(files) - set(old["managed"]):
        if local_path(target, name).exists():
            conflicts.append(name)
    if conflicts or removed:
        raise StateError("Update stopped before writes. Review local changes/collisions or removed upstream files: " + ", ".join(sorted(set(conflicts) | removed)))
    # Preflight all conflicts first; individual writes are atomic, the full update is not.
    for name, data in files.items():
        atomic_write(local_path(target, name), data)
    atomic_write(target / ".workflow/installed.json", (json.dumps({"version": release["version"], "managed": {name: bytes_hash(data) for name, data in files.items()}}, indent=2) + "\n").encode())
    return {"updated_to": release["version"], "preserved": ["AGENTS.md", "project/", "application files"],
            "next": "Review upstream changes, refresh portable file inventory, reconcile evidence and run relevant checks before accepting this update."}


def bundle(root: Path, state_name: str, output: Path):
    root = root.resolve()
    data = read_json(local_path(root, state_name))
    problems = validate(data, root)
    if problems:
        raise StateError("Cannot export inconsistent milestone:\n" + "\n".join(problems))
    names = set(data["portable_files"]) | {state_name, data["decisions_file"]}
    # A restored adoption needs its ownership/version manifest to update safely.
    if (root / ".workflow/installed.json").is_file():
        names.add(".workflow/installed.json")
    names |= {item["path"] for item in data["artifacts"].values()}
    names |= {e["path"] for task in data["tasks"] for e in task["evidence"]}
    names |= {item["decision_path"] for item in data["approvals"]}
    names |= {item["path"] for item in data["saved_unverified"]}
    names |= {item["report_path"] for item in data["delegations"] if item["report_path"]}
    contents = {}
    for name in sorted(names):
        parts = Path(name).parts
        if any(p in {".git", ".local", "node_modules", "__pycache__"} or p == ".env" or p.startswith(".env.") or p.endswith((".pem", ".key")) for p in parts):
            raise StateError(f"Refusing sensitive/runtime path {name}; review the portable inventory")
        path = local_path(root, name)
        if path.resolve() == output.resolve() or name == "BUNDLE-MANIFEST.json":
            raise StateError("Bundle output or reserved manifest cannot be an input")
        contents[name] = path.read_bytes()
    manifest = {"format": "1.0", "state": state_name, "files": {name: bytes_hash(raw) for name, raw in contents.items()}}
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, raw in contents.items():
            archive.writestr(name, raw)
        archive.writestr("BUNDLE-MANIFEST.json", json.dumps(manifest, indent=2))
    if output.exists():
        raise StateError("Bundle destination exists; choose a new milestone name")
    atomic_write(output, stream.getvalue())
    return {"files": len(contents), "note": "Local archive only. File names are screened, not secret contents. An off-device backup destination remains unconfigured."}


def restore(archive_path: Path, target: Path):
    if any(p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction()) for p in [target, *target.parents]):
        raise StateError("Restore target and its parents must not be symlinks or junctions")
    target = target.resolve()
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise StateError("Restore requires a new or empty directory")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory(prefix="workflow-restore-", dir=target.parent) as temp:
            stage = Path(temp)
            manifest = json.loads(archive.read("BUNDLE-MANIFEST.json"))
            if not isinstance(manifest, dict) or manifest.get("format") != "1.0" or not isinstance(manifest.get("files"), dict) or not isinstance(manifest.get("state"), str):
                raise StateError("Unsupported bundle format")
            if len(archive.namelist()) != len(set(archive.namelist())) or set(archive.namelist()) != set(manifest["files"]) | {"BUNDLE-MANIFEST.json"}:
                raise StateError("Bundle entries do not match manifest")
            for name, expected in manifest["files"].items():
                if not isinstance(name, str) or not isinstance(expected, str) or len(expected) != 64:
                    raise StateError("Bundle manifest has an invalid file/hash entry")
                path = local_path(stage, name)
                raw = archive.read(name)
                if bytes_hash(raw) != expected:
                    raise StateError(f"Bundle hash mismatch: {name}")
                atomic_write(path, raw)
            state = read_json(local_path(stage, manifest["state"]))
            problems = validate(state, stage)
            if problems:
                raise StateError("Restored state failed validation: " + "; ".join(problems))
            shutil.copytree(stage, target, dirs_exist_ok=True)
        return {"restored": True, "state": manifest["state"], "next": "Run resume, inspect actual files and Git, restore required runtimes/access. No process was restarted."}
    except (zipfile.BadZipFile, KeyError, json.JSONDecodeError) as exc:
        raise StateError(f"Invalid milestone archive: {exc}") from exc
