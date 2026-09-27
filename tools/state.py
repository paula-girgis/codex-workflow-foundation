"""Versioned state validation and durable local checkpoints (standard library only)."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((PACKAGE / "schema/state.schema.json").read_text(encoding="utf-8"))


class StateError(ValueError):
    """An actionable input, consistency, or persistence error."""


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise StateError(f"Cannot read JSON at {path.name}: {exc}") from exc


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(root: Path, relative: str) -> Path:
    """Reject traversal, Windows absolute paths, symlinks escaping the project."""
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise StateError(f"Use a portable relative path: {relative!r}")
    candidate = root / relative
    resolved = candidate.resolve()
    if Path(relative).is_absolute() or ".." in Path(relative).parts or not resolved.is_relative_to(root.resolve()):
        raise StateError(f"Path escapes project: {relative!r}")
    return resolved


def schema_errors(value, rule=None, location="$", errors=None):
    """Validate exactly the JSON Schema subset used by our published schema."""
    errors = [] if errors is None else errors
    rule = SCHEMA if rule is None else rule
    if "$ref" in rule:
        rule = SCHEMA["$defs"][rule["$ref"].split("/")[-1]]
    expected = rule.get("type")
    types = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool, "null": type(None)}
    if expected:
        accepted = expected if isinstance(expected, list) else [expected]
        if not any(type(value) is types[name] for name in accepted):
            errors.append(f"{location}: expected {expected}")
            return errors
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{location}: expected one of {rule['enum']}")
    if isinstance(value, str):
        import re
        if len(value) < rule.get("minLength", 0):
            errors.append(f"{location}: must not be empty")
        if "pattern" in rule and not re.fullmatch(rule["pattern"], value):
            errors.append(f"{location}: invalid format")
    if type(value) is int and value < rule.get("minimum", value):
        errors.append(f"{location}: below minimum")
    if isinstance(value, dict):
        properties = rule.get("properties", {})
        for key in rule.get("required", []):
            if key not in value:
                errors.append(f"{location}.{key}: missing required field")
        for key, item in value.items():
            if key in properties:
                schema_errors(item, properties[key], f"{location}.{key}", errors)
            elif rule.get("additionalProperties") is False:
                errors.append(f"{location}.{key}: unknown field")
            elif isinstance(rule.get("additionalProperties"), dict):
                schema_errors(item, rule["additionalProperties"], f"{location}.{key}", errors)
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"{location}: too few items")
        for index, item in enumerate(value):
            schema_errors(item, rule.get("items", {}), f"{location}[{index}]", errors)
    return errors


def validate(state: dict, root: Path, *, allow_synthetic=False, check_files=True) -> list[str]:
    if isinstance(state, dict) and state.get("schema_version") != "1.0":
        return ["Unsupported schema_version. Keep the original file; use a matching helper or an explicit reviewed migration to 1.0. Do not relabel the version."]
    errors = schema_errors(state)
    if errors:
        return errors
    if state.get("synthetic", False) and not allow_synthetic:
        errors.append("Synthetic state requires --allow-synthetic and must remain in an isolated fixture.")
    tasks = {task["id"]: task for task in state["tasks"]}
    if len(tasks) != len(state["tasks"]):
        errors.append("Duplicate task IDs")
    approvals = {item["id"]: item for item in state["approvals"]}
    if len(approvals) != len(state["approvals"]):
        errors.append("Duplicate approval IDs")
    artifacts = state["artifacts"]

    def check_file(path, expected=None, label="artifact"):
        try:
            actual = local_path(root, path)
            if not check_files:
                return
            if not actual.is_file():
                errors.append(f"{label}: missing artifact {path}")
            elif expected and digest(actual) != expected:
                errors.append(f"{label}: stale hash for {path}; previous evidence no longer applies")
        except StateError as exc:
            errors.append(f"{label}: {exc}")

    check_file(state["decisions_file"], label="decisions")
    for path in state["portable_files"]:
        check_file(path, label="portable file")
    for key, item in artifacts.items():
        check_file(item["path"], item["sha256"], key)
    for approval in approvals.values():
        if approval["source"] == "synthetic" and not (allow_synthetic and state.get("synthetic")):
            errors.append(f"approval {approval['id']}: synthetic approval is forbidden in real state")
        if approval["task_id"] not in tasks:
            errors.append(f"approval {approval['id']}: unknown task")
        check_file(approval["decision_path"], approval["decision_sha256"], "approval provenance")
        if not approval["artifact_hashes"]:
            errors.append(f"approval {approval['id']}: missing versioned artifacts")
        for key, expected in approval["artifact_hashes"].items():
            if key not in artifacts or artifacts[key]["sha256"] != expected:
                errors.append(f"approval {approval['id']}: stale or unknown artifact {key}")
    for task in tasks.values():
        label = task["id"]
        for dependency in task["depends_on"]:
            if dependency not in tasks:
                errors.append(f"{label}: missing dependency {dependency}")
            elif task["status"] in {"Ready", "Running", "Verified complete"} and tasks[dependency]["status"] != "Verified complete":
                errors.append(f"{label}: dependency {dependency} has not passed its gate")
        for key in task["artifacts"]:
            if key not in artifacts:
                errors.append(f"{label}: unknown artifact {key}")
        for record in task["evidence"]:
            check_file(record["path"], record["sha256"], f"{label} evidence")
            for key, expected in record["inputs"].items():
                if key not in artifacts or artifacts[key]["sha256"] != expected:
                    errors.append(f"{label}: stale evidence input {key}")
                elif artifacts[key]["path"] == record["path"]:
                    errors.append(f"{label}: evidence cannot use itself as an input")
        if task["status"] == "Verified complete":
            if not task["artifacts"]:
                errors.append(f"{label}: completion requires explicit task artifacts")
            if not task["evidence"]:
                errors.append(f"{label}: completion requires evidence")
            for record in task["evidence"]:
                if record["result"] != "passed":
                    errors.append(f"{label}: completion has non-passing evidence")
                if not record["inputs"]:
                    errors.append(f"{label}: evidence must identify its input artifacts/code state")
            covered = set().union(*(set(e["inputs"]) for e in task["evidence"]))
            if set(task["artifacts"]) - covered:
                errors.append(f"{label}: evidence does not cover task artifacts")
            for kind in task["requires_approvals"]:
                matched = [a for a in approvals.values() if a["task_id"] == label and a["type"] == kind]
                if not matched:
                    errors.append(f"{label}: missing required {kind} approval")
                elif not any(set(task["artifacts"]).issubset(a["artifact_hashes"]) for a in matched):
                    errors.append(f"{label}: approval does not cover task artifacts")
    visiting, visited = set(), set()

    def visit(key):
        if key in visiting:
            errors.append(f"Circular dependency involving {key}")
            return
        if key in visited or key not in tasks:
            return
        visiting.add(key)
        for other in tasks[key]["depends_on"]:
            visit(other)
        visiting.remove(key)
        visited.add(key)

    for key in tasks:
        visit(key)
    if state["ui"]:
        for key, kind in [("wireframes", "wireframe"), ("polished", "polished")]:
            if key not in tasks or kind not in tasks[key]["requires_approvals"]:
                errors.append(f"UI workflow requires {key} task and {kind} approval gate")
            elif tasks[key]["status"] == "Verified complete":
                if not any(artifacts.get(a, {}).get("kind") == "image" for a in tasks[key]["artifacts"]):
                    errors.append(f"{key}: actual registered image required")
        if "polished" in tasks and "wireframes" not in tasks["polished"]["depends_on"]:
            errors.append("polished must depend on wireframes")
        if "implement" in tasks and "polished" not in ancestors("implement", tasks):
            errors.append("UI implement must depend on the polished approval gate")
    for operation in state["external_operations"]:
        if operation["task_id"] not in tasks:
            errors.append(f"external operation {operation['id']}: unknown task")
        elif operation["status"] != "confirmed" and tasks[operation["task_id"]]["status"] == "Verified complete":
            errors.append(f"{operation['task_id']}: external operation is unresolved")
    for item in state["saved_unverified"]:
        check_file(item["path"], label="saved unverified")
        if item["task_id"] not in tasks:
            errors.append("saved_unverified: unknown task")
        elif tasks[item["task_id"]]["status"] == "Verified complete":
            errors.append(f"{item['task_id']}: saved unverified work cannot be complete")
    for item in state["delegations"]:
        if item["task_id"] not in tasks:
            errors.append("delegation: unknown task")
        if item["report_path"]:
            check_file(item["report_path"], label="delegated result")
    return errors


def ancestors(key, tasks, seen=None):
    seen = set() if seen is None else seen
    for dependency in tasks.get(key, {}).get("depends_on", []):
        if dependency not in seen:
            seen.add(dependency)
            ancestors(dependency, tasks, seen)
    return seen


def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def checkpoint(candidate: dict, root: Path, state_path: Path, *, expected_revision=None, allow_synthetic=False):
    root = root.resolve()
    try:
        state_path = local_path(root, state_path.resolve().relative_to(root).as_posix())
    except ValueError as exc:
        raise StateError("Checkpoint destination must be inside the project root") from exc
    errors = validate(candidate, root, allow_synthetic=allow_synthetic)
    if errors:
        raise StateError("Checkpoint rejected:\n" + "\n".join(errors))
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lock = state_path.with_suffix(state_path.suffix + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise StateError("Checkpoint lock exists. Confirm no writer is running before manually removing the stale lock; do not retry blindly.") from exc
    os.close(fd)
    try:
        actual_git = git_state(root)
        if actual_git.get("repository") and candidate["git"].get("head") != actual_git.get("head"):
            raise StateError("Candidate git.head does not match the live repository; inspect Git and record the actual code state first.")
        if state_path.exists():
            previous = read_json(state_path)
            # Validate the previous record's internal integrity independently of
            # files deliberately changed/deleted since that checkpoint.
            if validate(previous, root, allow_synthetic=allow_synthetic, check_files=False):
                raise StateError("Current state is invalid or unsupported. Preserve it and inspect the .prev snapshot before explicit recovery.")
            if expected_revision is None or previous["revision"] != expected_revision:
                raise StateError("Revision conflict: pass --expected-revision matching the current state; re-read and reconcile first.")
            if candidate["revision"] != previous["revision"] + 1:
                raise StateError("New revision must be exactly current revision + 1")
            # A snapshot can be structurally valid yet its old artifact hashes stale.
            # Preserve this last accepted record without pretending its evidence is current.
            atomic_write(state_path.with_suffix(state_path.suffix + ".prev"), state_path.read_bytes())
        elif candidate["revision"] != 1:
            raise StateError("The first checkpoint must have revision 1")
        atomic_write(state_path, (json.dumps(candidate, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    finally:
        lock.unlink(missing_ok=True)


def git_state(root: Path):
    try:
        inside = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if inside.returncode:
            return {"available": True, "repository": False}
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "HEAD"], capture_output=True, text=True, timeout=10)
        status = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all", "--", str(root)], capture_output=True, text=True, timeout=10)
        if status.returncode:
            return {"available": True, "repository": True, "inspection_failed": True, "note": "Git status failed; inspect manually"}
        changes = status.stdout.splitlines()
        return {"available": True, "repository": True, "head": head.stdout.strip() if head.returncode == 0 else None, "changes": changes}
    except (OSError, subprocess.TimeoutExpired):
        return {"available": False, "repository": None, "note": "Inspect Git manually; no completion inferred"}


def resume(state: dict, root: Path, *, allow_synthetic=False):
    errors = validate(state, root, allow_synthetic=allow_synthetic)
    if schema_errors(state) or state.get("schema_version") != "1.0":
        raise StateError("Cannot interpret state safely:\n" + "\n".join(errors))
    actual_git = git_state(root)
    git_changed = (actual_git.get("repository") and actual_git.get("head") != state["git"]["head"]) or (state["git"]["head"] is not None and not actual_git.get("repository"))
    git_needs_review = bool(actual_git.get("changes")) or bool(actual_git.get("inspection_failed")) or not actual_git.get("available")
    # Conservative: any consistency/freshness failure withholds all completion claims.
    recorded = [t["id"] for t in state["tasks"] if t["status"] == "Verified complete"]
    verified = recorded if not errors and not git_changed and not git_needs_review else []
    uncertain = [t["id"] for t in state["tasks"] if t["id"] not in verified]
    return {"structurally_and_freshness_valid": not errors, "errors": errors,
            "verified_recorded_work": verified, "uncertain_tasks": uncertain,
            "saved_unverified": state["saved_unverified"],
            "external_operations_to_inspect": [o for o in state["external_operations"] if o["status"] in {"unknown", "running"}],
            "git": actual_git, "git_head_changed": bool(git_changed),
            "git_requires_review": git_needs_review, "recorded_complete_tasks": recorded,
            "next_action": state["next_action"],
            "limits": "Recorded passing evidence is not re-executed. Unregistered files are not hash-verified. Inspect Git changes and relevant files. Never replay external operations automatically."}
