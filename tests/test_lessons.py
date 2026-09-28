"""Project knowledge is seeded cleanly, preserved and portable; fixtures are synthetic."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from distribution import adopt, bundle, package_files, restore, update
from state import read_json
from workflow import selection


class LessonAdoptionTests(unittest.TestCase):
    def upstream(self, base):
        source = base / 'source'
        _, files = package_files(ROOT)
        for name, data in files.items():
            path = source / name.removeprefix('.workflow/')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        return source

    def test_new_adoption_excludes_maintainer_history_and_has_no_inherited_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); source = self.upstream(base)
            private = source / 'development/LESSONS.md'
            private.parent.mkdir(); private.write_text('SYNTHETIC_PRIVATE_INCIDENT_NOT_FOR_ADOPTION')
            target = base / 'project'; adopt(target, selection('bug'), source)
            self.assertEqual((target / 'project/LESSONS.md').read_bytes(),
                             (source / 'templates/project/LESSONS.md').read_bytes())
            self.assertNotIn('SYNTHETIC_PRIVATE_INCIDENT', (target / 'project/LESSONS.md').read_text())
            self.assertFalse((target / '.workflow/development').exists())
            state = read_json(target / 'project/state.json')
            self.assertIn('project/LESSONS.md', state['portable_files'])
            self.assertEqual(state['approvals'], [])
            self.assertTrue(all(not task['evidence'] and task['status'] != 'Verified complete'
                                for task in state['tasks']))
            self.assertNotIn('project/LESSONS.md', read_json(target / '.workflow/installed.json')['managed'])

    def test_existing_lessons_survive_adoption_milestone_restore_and_update(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); target = base / 'existing'
            record = target / 'project/LESSONS.md'; record.parent.mkdir(parents=True)
            original = b'## L-0001 | Synthetic fixture only | active | tags: recovery\nKeep project knowledge.\n'
            record.write_bytes(original)
            result = adopt(target, selection('bug'))
            self.assertIn('project/LESSONS.md', result['preserved'])
            self.assertEqual(record.read_bytes(), original)
            archive = base / 'milestone.zip'; bundle(target, 'project/state.json', archive)
            restored = base / 'restored'; restore(archive, restored)
            state_before = (restored / 'project/state.json').read_bytes()
            update(restored)
            self.assertEqual((restored / 'project/LESSONS.md').read_bytes(), original)
            self.assertEqual((restored / 'project/state.json').read_bytes(), state_before)
            self.assertEqual(read_json(restored / 'project/state.json')['approvals'], [])

    def test_changed_upstream_template_never_replaces_project_lessons_or_existing_state(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory); source = self.upstream(base)
            target = base / 'existing'; adopt(target, selection('bug'), source)
            record = target / 'project/LESSONS.md'
            original = b'SYNTHETIC project knowledge with active and superseded entries.\n'
            record.write_bytes(original)
            untouched = {name: (target/name).read_bytes() for name in
                         ['AGENTS.md', 'project/PROFILE.md', 'project/DECISIONS.md', 'project/state.json']}
            release = read_json(source / 'foundation.json'); release['version'] = 'synthetic-lessons-update'
            (source / 'foundation.json').write_text(json.dumps(release))
            template = source / 'templates/project/LESSONS.md'
            template.write_bytes(template.read_bytes() + b'\nSynthetic clean template revision.\n')
            update(target, source)
            self.assertEqual(record.read_bytes(), original)
            self.assertEqual((target / '.workflow/templates/project/LESSONS.md').read_bytes(), template.read_bytes())
            for name, data in untouched.items(): self.assertEqual((target/name).read_bytes(), data)
            # Older projects may have no live record: update must not silently create one or edit state.
            record.unlink()
            update(target, source)
            self.assertFalse(record.exists())
            self.assertEqual((target/'project/state.json').read_bytes(), untouched['project/state.json'])


if __name__ == '__main__': unittest.main()
