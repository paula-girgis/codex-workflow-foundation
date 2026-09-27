"""Behavior and failure cases. All approvals and external operations here are synthetic."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from distribution import adopt, bundle, restore, update
from state import StateError, atomic_write, checkpoint, digest, git_state, read_json, resume, validate
from workflow import selection


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / "tests/.tmp"
        parent.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.root = Path(self.temp.name)
        # Fixtures must not inherit the source checkout's Git HEAD. Explicit
        # repositories created inside a fixture still use real Git normally.
        isolation = patch.dict(os.environ, {"GIT_CEILING_DIRECTORIES": str(parent.resolve())})
        isolation.start()
        self.addCleanup(isolation.stop)
        self.put("project/DECISIONS.md", "Synthetic test decisions. No real user approval.\n")
        self.put("src/rule.txt", "rule version one\n")
        self.put("evidence/check.txt", "Synthetic check of rule version one passed\n")
        self.state = read_json(ROOT / "templates/project/state.json")
        self.state["objective"] = "ISOLATED TEST FIXTURE"
        self.state["portable_files"] = ["project/DECISIONS.md", "src/rule.txt", "evidence/check.txt"]
        self.state["artifacts"] = {"rule": {"path": "src/rule.txt", "sha256": digest(self.root / "src/rule.txt"), "kind": "contract"}}
        evidence = {"path": "evidence/check.txt", "sha256": digest(self.root / "evidence/check.txt"), "kind": "test", "command": "synthetic local check", "result": "passed", "inputs": {"rule": self.state["artifacts"]["rule"]["sha256"]}}
        self.state["tasks"] = [
            {"id": "checked", "status": "Verified complete", "owner": "test", "depends_on": [], "requires_approvals": [], "artifacts": ["rule"], "evidence": [evidence]},
            {"id": "pending", "status": "Running", "owner": "test", "depends_on": ["checked"], "requires_approvals": [], "artifacts": [], "evidence": []}]

    def tearDown(self):
        self.temp.cleanup()

    def put(self, name, content):
        atomic_write(self.root / name, content.encode())

    def errors(self, **kwargs):
        return "\n".join(validate(self.state, self.root, **kwargs))

    def test_small_bug_selects_lightweight(self):
        route = selection("bug")
        self.assertEqual(route["workflow"], "lightweight")
        self.assertEqual([t["id"] for t in route["tasks"]], ["reproduce", "fix", "verify"])

    def test_fixture_does_not_inherit_source_repository(self):
        self.assertFalse(git_state(self.root)["repository"])
        checkpoint(self.state, self.root, self.root / "project/state.json")
        self.assertEqual(resume(self.state, self.root)["verified_recorded_work"], ["checked"])

    def test_ui_feature_has_separate_sequential_approval_gates(self):
        route = selection("feature", True)
        tasks = {t["id"]: t for t in route["tasks"]}
        self.assertEqual(tasks["wireframes"]["requires_approvals"], ["wireframe"])
        self.assertEqual(tasks["polished"]["requires_approvals"], ["polished"])
        self.assertEqual(tasks["polished"]["depends_on"], ["wireframes"])
        self.state.update(route)
        self.assertEqual(self.errors(), "")

    @unittest.skipUnless(importlib.util.find_spec("PIL"), "Optional image export check needs Pillow; core checks remain available")
    def test_image_fixture_export_and_manifest_registration(self):
        output = self.root / "wireframes/v001/fixture.png"
        manifest = self.root / "wireframes/v001/manifest.json"
        run = subprocess.run([sys.executable, str(ROOT / "tools/render_fixture.py"), "--output", str(output), "--manifest", str(manifest)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(output.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n")
        registration = json.loads(manifest.read_text())
        self.assertFalse(registration["approved"])
        self.assertEqual(registration["files"][output.name]["sha256"], digest(output))
        self.assertEqual(registration["files"][output.name]["path"], "fixture.png")
        from PIL import Image
        with Image.open(output) as actual:
            self.assertEqual(actual.size, (960, 540))
            actual.verify()

    def test_valid_state(self):
        self.assertEqual(self.errors(), "")

    def test_invalid_status_and_unknown_fields(self):
        self.state["tasks"][0]["status"] = "done"
        self.state["magic"] = True
        self.assertIn("expected one of", self.errors())
        self.assertIn("unknown field", self.errors())

    def test_missing_evidence(self):
        self.state["tasks"][0]["evidence"] = []
        self.assertIn("completion requires evidence", self.errors())

    def test_evidence_cannot_certify_itself(self):
        self.state['artifacts']['log'] = {'path':'evidence/check.txt','sha256':digest(self.root/'evidence/check.txt'),'kind':'document'}
        self.state['tasks'][0]['evidence'][0]['inputs']['log'] = digest(self.root/'evidence/check.txt')
        self.assertIn('cannot use itself', self.errors())

    def test_incomplete_task_evidence_references_are_checked(self):
        self.state['tasks'][0]['status']='Running'
        self.state['tasks'][1]['status']='Not started'
        self.state['tasks'][0]['evidence'][0]['inputs']={'missing':'a'*64}
        self.assertIn('stale evidence input', self.errors())

    def test_evidence_must_cover_inputs(self):
        self.state["tasks"][0]["evidence"][0]["inputs"] = {}
        self.assertIn("evidence must identify", self.errors())

    def test_failed_evidence_cannot_complete(self):
        self.state["tasks"][0]["evidence"][0]["result"] = "failed"
        self.assertIn("non-passing evidence", self.errors())

    def test_broken_dependency(self):
        self.state["tasks"][1]["depends_on"] = ["absent"]
        self.assertIn("missing dependency", self.errors())

    def test_cycle(self):
        self.state["tasks"][0]["depends_on"] = ["pending"]
        self.assertIn("Circular dependency", self.errors())

    def test_duplicate_task(self):
        self.state["tasks"].append(copy.deepcopy(self.state["tasks"][0]))
        self.assertIn("Duplicate task", self.errors())

    def test_dependent_work_cannot_start_before_gate(self):
        self.state["tasks"][0]["status"] = "Running"
        self.assertIn("has not passed its gate", self.errors())

    def test_missing_approval(self):
        self.state["tasks"][0]["requires_approvals"] = ["product"]
        self.assertIn("missing required product approval", self.errors())

    def synthetic_approval(self):
        self.state["synthetic"] = True
        self.state["tasks"][0]["requires_approvals"] = ["product"]
        self.state["approvals"] = [{"id": "SYNTHETIC-NOT-USER", "type": "product", "task_id": "checked", "source": "synthetic", "scope": "Fixture only", "artifact_hashes": {"rule": self.state["artifacts"]["rule"]["sha256"]}, "decision_path": "project/DECISIONS.md", "decision_sha256": digest(self.root / "project/DECISIONS.md")}]

    def test_synthetic_approval_requires_isolated_opt_in(self):
        self.synthetic_approval()
        self.assertIn("Synthetic state requires", self.errors())
        self.assertEqual(self.errors(allow_synthetic=True), "")

    def test_synthetic_approval_cannot_leak_to_real_state(self):
        self.synthetic_approval()
        self.state["synthetic"] = False
        self.assertIn("forbidden in real state", self.errors(allow_synthetic=True))

    def test_changed_artifact_withholds_completion(self):
        self.put("src/rule.txt", "changed rule\n")
        self.assertIn("stale hash", self.errors())
        self.assertEqual(resume(self.state, self.root)["verified_recorded_work"], [])

    def test_rehash_alone_does_not_refresh_evidence_or_approval(self):
        self.synthetic_approval()
        self.put("src/rule.txt", "changed contract\n")
        self.state["artifacts"]["rule"]["sha256"] = digest(self.root / "src/rule.txt")
        errors = self.errors(allow_synthetic=True)
        self.assertIn("stale evidence input", errors)
        self.assertIn("stale or unknown artifact", errors)

    def test_missing_artifact_and_tampered_evidence(self):
        (self.root / "src/rule.txt").unlink()
        self.put("evidence/check.txt", "different evidence")
        self.assertIn("missing artifact", self.errors())
        self.assertIn("stale hash", self.errors())

    def test_path_escape_rejected(self):
        for path in ["../outside", "C:/secret", "/absolute", "folder\\file"]:
            self.state["artifacts"]["rule"]["path"] = path
            self.assertTrue(validate(self.state, self.root), path)

    def test_resume_three_distinct_categories(self):
        self.put("src/partial.txt", "saved unfinished work")
        self.state["saved_unverified"] = [{"task_id": "pending", "path": "src/partial.txt", "reason": "Interrupted before verification"}]
        self.state["external_operations"] = [{"id": "SIMULATED-NO-SERVICE", "task_id": "pending", "status": "unknown", "description": "Simulated external request", "check_next": "Inspect the synthetic receipt; never replay"}]
        report = resume(self.state, self.root)
        self.assertEqual(report["verified_recorded_work"], ["checked"])
        self.assertEqual(report["saved_unverified"][0]["path"], "src/partial.txt")
        self.assertEqual(report["external_operations_to_inspect"][0]["status"], "unknown")
        self.assertIn("pending", report["uncertain_tasks"])

    def test_unknown_external_operation_blocks_completion(self):
        self.state["external_operations"] = [{"id": "SIMULATED", "task_id": "checked", "status": "unknown", "description": "No actual service", "check_next": "Inspect receipt"}]
        self.assertIn("external operation is unresolved", self.errors())

    def test_invalid_checkpoint_preserves_current_and_previous(self):
        path = self.root / "project/state.json"
        checkpoint(self.state, self.root, path)
        self.state["revision"] = 2
        checkpoint(self.state, self.root, path, expected_revision=1)
        old, previous = path.read_bytes(), path.with_suffix(".json.prev").read_bytes()
        self.state["revision"] = 3
        self.state["tasks"][0]["evidence"] = []
        with self.assertRaisesRegex(StateError, "Checkpoint rejected"):
            checkpoint(self.state, self.root, path, expected_revision=2)
        self.assertEqual(path.read_bytes(), old)
        self.assertEqual(path.with_suffix(".json.prev").read_bytes(), previous)

    def test_corrupt_current_cannot_replace_previous_usable_snapshot(self):
        path=self.root/'project/state.json'
        checkpoint(self.state,self.root,path)
        self.state['revision']=2
        checkpoint(self.state,self.root,path,expected_revision=1)
        previous=path.with_suffix('.json.prev').read_bytes()
        corrupted=copy.deepcopy(self.state)
        corrupted['tasks'][1]['depends_on']=['missing']
        atomic_write(path,json.dumps(corrupted).encode())
        self.state['revision']=3
        with self.assertRaisesRegex(StateError,'Current state is invalid'):
            checkpoint(self.state,self.root,path,expected_revision=2)
        self.assertEqual(path.with_suffix('.json.prev').read_bytes(),previous)

    def test_saved_changed_files_allow_reconciled_checkpoint(self):
        path=self.root/'project/state.json'
        checkpoint(self.state,self.root,path)
        (self.root/'src/rule.txt').unlink()
        self.state['revision']=2
        self.state['artifacts']={}
        self.state['portable_files']=['project/DECISIONS.md']
        self.state['tasks'][0].update(status='Running',artifacts=[],evidence=[])
        self.state['tasks'][1]['status']='Not started'
        checkpoint(self.state,self.root,path,expected_revision=1)
        self.assertEqual(read_json(path)['revision'],2)
        self.assertIn('rule',read_json(path.with_suffix('.json.prev'))['artifacts'])

    def test_checkpoint_write_failure_keeps_current_usable(self):
        path=self.root/'project/state.json'
        checkpoint(self.state,self.root,path)
        original=path.read_bytes()
        self.state['revision']=2
        from state import os as state_os
        real_replace=state_os.replace
        def fail_current(source,destination):
            if Path(destination)==path:
                raise OSError('simulated disk write failure')
            return real_replace(source,destination)
        with patch('state.os.replace',side_effect=fail_current):
            with self.assertRaisesRegex(OSError,'simulated'):
                checkpoint(self.state,self.root,path,expected_revision=1)
        self.assertEqual(path.read_bytes(),original)
        self.assertFalse(path.with_suffix('.json.lock').exists())

    def test_first_checkpoint_rejects_stale_git_head(self):
        with patch('state.git_state',return_value={'available':True,'repository':True,'head':'a'*40,'changes':[]}):
            with self.assertRaisesRegex(StateError,'git.head'):
                checkpoint(self.state,self.root,self.root/'project/state.json')
        self.assertFalse((self.root/'project/state.json').exists())

    def test_unregistered_git_changes_with_same_status_remain_uncertain(self):
        subprocess.run(['git','init','--quiet',str(self.root)],check=True,capture_output=True)
        self.put('unregistered.txt','version one')
        first=resume(self.state,self.root)
        self.put('unregistered.txt','version two')
        second=resume(self.state,self.root)
        self.assertEqual(first['git']['changes'],second['git']['changes'])
        self.assertTrue(second['git_requires_review'])
        self.assertEqual(second['verified_recorded_work'],[])
        self.assertEqual(second['recorded_complete_tasks'],['checked'])

    def test_unsupported_schema_actionable(self):
        self.state["schema_version"] = "99.0"
        self.assertIn("explicit reviewed migration", self.errors())
        with self.assertRaisesRegex(StateError, "Cannot interpret"):
            resume(self.state, self.root)

    def test_revision_conflict_and_writer_lock(self):
        path = self.root / "project/state.json"
        checkpoint(self.state, self.root, path)
        self.state["revision"] = 2
        with self.assertRaisesRegex(StateError, "Revision conflict"):
            checkpoint(self.state, self.root, path, expected_revision=0)
        path.with_suffix(".json.lock").write_text("simulated interrupted writer")
        with self.assertRaisesRegex(StateError, "Confirm no writer"):
            checkpoint(self.state, self.root, path, expected_revision=1)

    def test_missing_or_corrupt_state_does_not_guess(self):
        with self.assertRaisesRegex(StateError, "Cannot read JSON"):
            read_json(self.root / "missing.json")
        self.put("project/state.json", "{partial")
        with self.assertRaises(StateError):
            checkpoint(self.state, self.root, self.root / "project/state.json", expected_revision=1)
        self.assertEqual((self.root / "project/state.json").read_text(), "{partial")

    def test_saved_unverified_cannot_be_complete(self):
        self.state["saved_unverified"] = [{"task_id": "checked", "path": "src/rule.txt", "reason": "needs review"}]
        self.assertIn("cannot be complete", self.errors())

    def test_local_portability_and_stop_resume_drill(self):
        # Persist files, close/reload all in-memory state, restore into another directory.
        path = self.root / "project/state.json"
        checkpoint(self.state, self.root, path)
        archive = self.root / "milestone.zip"
        bundle(self.root, "project/state.json", archive)
        clean = self.root / "restored"
        restore(archive, clean)
        result = resume(read_json(clean / "project/state.json"), clean)
        self.assertEqual(result["verified_recorded_work"], ["checked"])
        self.assertEqual(digest(clean / "src/rule.txt"), digest(self.root / "src/rule.txt"))
        self.assertTrue((clean / "evidence/check.txt").is_file())
        # Fresh process as well as a fresh directory; no claim of cross-machine recovery.
        run = subprocess.run([sys.executable, str(ROOT / "tools/workflow.py"), "resume", "--root", str(clean)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("checked", json.loads(run.stdout)["verified_recorded_work"])

    def test_bundle_rejects_secret_paths_and_existing_target(self):
        self.put(".env", "SYNTHETIC_SECRET=not-real")
        self.state["portable_files"].append(".env")
        checkpoint(self.state, self.root, self.root / "project/state.json")
        with self.assertRaisesRegex(StateError, "sensitive/runtime"):
            bundle(self.root, "project/state.json", self.root / "milestone.zip")
        with self.assertRaisesRegex(StateError, "empty directory"):
            restore(self.root / "absent.zip", self.root)

    def test_archive_tampering_detected(self):
        checkpoint(self.state, self.root, self.root / "project/state.json")
        bundle(self.root, "project/state.json", self.root / "milestone.zip")
        with zipfile.ZipFile(self.root / "milestone.zip") as original:
            entries = {n: original.read(n) for n in original.namelist()}
        entries["src/rule.txt"] = b"tampered"
        with zipfile.ZipFile(self.root / "tampered.zip", "w") as modified:
            for name, content in entries.items():
                modified.writestr(name, content)
        with self.assertRaisesRegex(StateError, "hash mismatch"):
            restore(self.root / "tampered.zip", self.root / "clean")
        self.assertFalse((self.root / "clean").exists())

    def test_malformed_bundle_manifest_is_actionable(self):
        archive = self.root / "malformed.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("BUNDLE-MANIFEST.json", json.dumps({"format": "1.0", "files": [], "state": "state.json"}))
        with self.assertRaisesRegex(StateError, "Unsupported bundle format"):
            restore(archive, self.root / "clean")

    def test_restore_checks_symlink_before_resolving_target(self):
        target=self.root/'linked'
        original=Path.is_symlink
        with patch.object(Path,'is_symlink',lambda path: True if path==target else original(path)):
            with self.assertRaisesRegex(StateError,'symlinks'):
                restore(self.root/'unused.zip',target)

    def test_bundle_rejects_dotenv_variants(self):
        self.put('.env.production','SYNTHETIC=not-real')
        self.state['portable_files'].append('.env.production')
        checkpoint(self.state,self.root,self.root/'project/state.json')
        with self.assertRaisesRegex(StateError,'sensitive/runtime'):
            bundle(self.root,'project/state.json',self.root/'secret.zip')

    def test_adoption_and_update_preserve_existing_repo(self):
        target = self.root / "existing"
        target.mkdir()
        subprocess.run(["git", "init", "--quiet", str(target)], check=True, capture_output=True)
        (target / "AGENTS.md").write_text("Existing authoritative instructions\n")
        (target / "app.txt").write_text("Existing application\n")
        (target / "project").mkdir()
        (target / "project/PROFILE.md").write_text("Existing project choices\n")
        (target / "project/DECISIONS.md").write_text("Existing decisions\n")
        before = {name: (target / name).read_bytes() for name in ["AGENTS.md", "app.txt", "project/PROFILE.md", "project/DECISIONS.md"]}
        result = adopt(target, selection("bug"))
        self.assertTrue(result["preserved"])
        # Actual changed upstream version, not merely a no-op update.
        upstream = self.root / "upstream"
        shutil.copytree(ROOT, upstream, ignore=shutil.ignore_patterns(".tmp", "__pycache__", "development", ".git", ".local", "dist"))
        release = read_json(upstream / "foundation.json")
        release["version"] = "0.1.1-test-only"
        atomic_write(upstream / "foundation.json", json.dumps(release).encode())
        atomic_write(upstream / "docs/RECOVERY.md", (upstream / "docs/RECOVERY.md").read_bytes() + b"\nSynthetic update note.\n")
        state_before = (target / "project/state.json").read_bytes()
        update(target, upstream)
        for name, raw in before.items():
            self.assertEqual((target / name).read_bytes(), raw)
        self.assertEqual((target / "project/state.json").read_bytes(), state_before)
        self.assertIn("Synthetic update", (target / ".workflow/docs/RECOVERY.md").read_text())
        self.assertEqual(read_json(target / ".workflow/installed.json")["version"], "0.1.1-test-only")
        status = resume(read_json(target / "project/state.json"), target)
        self.assertTrue(status["git"]["repository"])
        self.assertTrue(status["git"]["changes"])

    def test_update_conflict_stops_before_any_writes(self):
        target = self.root / "new"
        adopt(target, selection())
        (target / ".workflow/START.md").write_text("Local custom changes")
        before = (target / ".workflow/installed.json").read_bytes()
        with self.assertRaisesRegex(StateError, "before writes"):
            update(target)
        self.assertEqual((target / ".workflow/installed.json").read_bytes(), before)
        self.assertEqual((target / ".workflow/START.md").read_text(), "Local custom changes")

    def test_restored_adoption_retains_manifest_and_can_update(self):
        target = self.root / 'adopted'
        adopt(target, selection('feature', True))
        profile = (target / 'project/PROFILE.md').read_bytes()
        snapshot = self.root / 'adopted.zip'
        bundle(target, 'project/state.json', snapshot)
        restored = self.root / 'restored-adoption'
        restore(snapshot, restored)
        self.assertTrue((restored / '.workflow/installed.json').is_file())
        self.assertEqual(read_json(restored / '.workflow/installed.json'), read_json(target / '.workflow/installed.json'))
        update(restored)
        self.assertEqual((restored / 'project/PROFILE.md').read_bytes(), profile)
        state = read_json(restored / 'project/state.json')
        self.assertEqual(state['approvals'], [])
        self.assertFalse(any(t['status'] == 'Verified complete' for t in state['tasks']))

    def test_existing_skill_collision_is_not_overwritten(self):
        target = self.root / "collision"
        path = target / ".agents/skills/resume-project/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("Existing skill")
        with self.assertRaisesRegex(StateError, "overwrite"):
            adopt(target, selection())
        self.assertFalse((target / ".workflow").exists())
        self.assertEqual(path.read_text(), "Existing skill")


if __name__ == "__main__":
    unittest.main(verbosity=2)
