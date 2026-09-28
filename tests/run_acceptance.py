"""Run helper behavior tests and persist their actual outcome as evidence."""
import hashlib
import json
from pathlib import Path
import sys
import time
import unittest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "tools"))
from state import atomic_write

def source_hashes():
    paths = [root / name for name in ["START.md", "AGENTS.md", "foundation.json", ".gitignore"]]
    for directory in ["tools", "tests", "schema", "docs", "examples", "templates", ".agents", ".github"]:
        paths.extend(p for p in (root / directory).rglob("*") if p.is_file() and p.suffix in {".py", ".md", ".json", ".yml", ".mjs"} and ".tmp" not in p.parts and "__pycache__" not in p.parts)
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}

inputs = source_hashes()
suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_*.py")
started = time.monotonic()
result = unittest.TextTestRunner(verbosity=2).run(suite)
unchanged = inputs == source_hashes()
report = {"command": "python tests/run_acceptance.py", "tests_run": result.testsRun,
          "passed": result.wasSuccessful() and unchanged, "failures": len(result.failures), "errors": len(result.errors),
          "skipped": [(str(test), reason) for test, reason in result.skipped], "elapsed_seconds": round(time.monotonic() - started, 3),
          "inputs": inputs, "inputs_unchanged_during_run": unchanged,
          "runtime": sys.version.split()[0],
          "scope": "Local isolated fixtures; synthetic approvals and external operations; no application, real deployment or cross-machine recovery tested"}
destination = root / "development/evidence/acceptance.json"
destination.parent.mkdir(parents=True, exist_ok=True)
atomic_write(destination, (json.dumps(report, indent=2) + "\n").encode("utf-8"))
sys.exit(0 if report["passed"] else 1)
