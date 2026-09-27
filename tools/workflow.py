#!/usr/bin/env python3
"""Small local workflow CLI. No network calls, service execution, or scheduler."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from state import StateError, checkpoint, local_path, read_json, resume, validate


def selection(kind="feature", ui=False):
    route = "visual" if ui else "lightweight" if kind == "bug" else "standard"
    sequence = ["reproduce", "fix", "verify"] if route == "lightweight" else ["discover", "plan", "implement", "verify"]
    if ui:
        sequence = ["discover", "wireframes", "polished", "plan", "implement", "verify"]
    tasks = []
    for index, name in enumerate(sequence):
        tasks.append({"id": name, "status": "Ready" if index == 0 else "Not started", "owner": "coordinator",
                      "depends_on": sequence[index - 1:index],
                      "requires_approvals": ["wireframe"] if name == "wireframes" else ["polished"] if name == "polished" else [],
                      "artifacts": [], "evidence": []})
    return {"workflow": route, "ui": ui, "tasks": tasks}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    choose = commands.add_parser("select", help="Print workflow tasks; does not mutate state")
    choose.add_argument("--kind", choices=["bug", "feature"], default="feature")
    choose.add_argument("--ui", action="store_true", help="Changes UI layout/product journeys; requires both visual gates")
    for name in ["validate", "resume", "checkpoint"]:
        command = commands.add_parser(name)
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--state", default="project/state.json")
        command.add_argument("--allow-synthetic", action="store_true", help="Isolated test fixtures only")
        if name == "checkpoint":
            command.add_argument("--candidate", type=Path, required=True)
            command.add_argument("--expected-revision", type=int)
    for name in ["adopt", "update"]:
        command = commands.add_parser(name)
        command.add_argument("--target", type=Path, required=True)
        if name == "adopt":
            command.add_argument("--kind", choices=["bug", "feature"], default="feature")
            command.add_argument("--ui", action="store_true")
    bundle = commands.add_parser("bundle", help="Export an explicit portable file list; never uploads")
    bundle.add_argument("--root", type=Path, default=Path.cwd())
    bundle.add_argument("--state", default="project/state.json")
    bundle.add_argument("--output", type=Path, required=True)
    restore = commands.add_parser("restore")
    restore.add_argument("--bundle", type=Path, required=True)
    restore.add_argument("--target", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "select":
            result = selection(args.kind, args.ui)
        elif args.command in {"adopt", "update", "bundle", "restore"}:
            from distribution import adopt, update, bundle, restore
            if args.command == "adopt":
                result = adopt(args.target, selection(args.kind, args.ui))
            elif args.command == "update":
                result = update(args.target)
            elif args.command == "bundle":
                result = bundle(args.root, args.state, args.output)
            else:
                result = restore(args.bundle, args.target)
        else:
            root = args.root.resolve()
            path = local_path(root, args.state)
            data = read_json(args.candidate if args.command == "checkpoint" else path)
            if args.command == "checkpoint":
                checkpoint(data, root, path, expected_revision=args.expected_revision, allow_synthetic=args.allow_synthetic)
                result = {"saved": args.state, "revision": data["revision"]}
            elif args.command == "resume":
                result = resume(data, root, allow_synthetic=args.allow_synthetic)
            else:
                errors = validate(data, root, allow_synthetic=args.allow_synthetic)
                result = {"valid": not errors, "errors": errors, "note": "Structure and registered hashes only; not proof of functional correctness"}
                if errors:
                    print(json.dumps(result, indent=2))
                    return 1
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if args.command == "resume" and (result["errors"] or result["git_head_changed"] or result["git_requires_review"]) else 0
    except (StateError, OSError, ValueError) as exc:
        print(f"workflow: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
