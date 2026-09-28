"""Optional browser templates are inert during adoption and conflict-aware updates."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from distribution import adopt, package_files, update
from state import StateError
from workflow import selection


class BrowserModuleTests(unittest.TestCase):
    def test_adoption_copies_inert_templates_without_replacing_project_tooling(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'existing'; target.mkdir()
            originals = {'AGENTS.md': b'Keep existing instructions', 'package.json': b'{"private":true}',
                         'package-lock.json': b'{"lockfileVersion":3}', 'playwright.config.mjs': b'// Existing runner config',
                         'project/PROFILE.md': b'Keep choices', '.github/workflows/web.yml': b'# Existing CI',
                         'app/data.json': b'{"existing":"data"}'}
            for name, data in originals.items():
                path = target/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
            # Any attempted package install is a real test failure; Git inspection remains allowed.
            import subprocess
            original_run = subprocess.run
            def guarded(command, *args, **kwargs):
                self.assertEqual(command[0], 'git', f'Unexpected executable during adoption: {command[0]}')
                return original_run(command, *args, **kwargs)
            with patch('subprocess.run', side_effect=guarded):
                adopt(target, selection('feature', True))
            for name, data in originals.items(): self.assertEqual((target/name).read_bytes(), data)
            self.assertEqual((target/'.workflow/templates/browser/playwright.config.mjs').read_bytes(), (ROOT/'templates/browser/playwright.config.mjs').read_bytes())
            self.assertTrue((target/'.workflow/templates/browser/journey.spec.mjs').is_file())
            self.assertTrue((target/'.workflow/templates/github/playwright-ci.yml').is_file())
            self.assertFalse((target/'node_modules').exists())
            self.assertFalse((target/'.local').exists())

    def test_module_update_preserves_choices_and_rejects_template_collision(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); upstream = base/'previous'; upstream.mkdir()
            release, files = package_files(ROOT)
            # Synthetic prior source lacks only the new optional module.
            release['version'] = 'synthetic-before-browser-module'
            release['include'].remove('templates/browser/*.mjs')
            for name, data in files.items():
                name = name.removeprefix('.workflow/')
                if name.startswith('templates/browser/') or name == 'templates/github/playwright-ci.yml': continue
                path = upstream/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
            (upstream/'foundation.json').write_text(json.dumps(release), encoding='utf-8')
            target = base/'target'; adopt(target, selection('bug'), upstream)
            (target/'project/PROFILE.md').write_text('Keep chosen runner', encoding='utf-8')
            before = {p:(target/p).read_bytes() for p in ['AGENTS.md','project/PROFILE.md','project/state.json']}
            collision = target/'.workflow/templates/browser/journey.spec.mjs'
            collision.parent.mkdir(parents=True); collision.write_text('Existing unrelated template')
            manifest = (target/'.workflow/installed.json').read_bytes()
            with self.assertRaisesRegex(StateError, 'before writes'): update(target, ROOT)
            self.assertEqual((target/'.workflow/installed.json').read_bytes(), manifest)
            collision.rename(collision.with_suffix('.saved'))
            update(target, ROOT)
            for p, data in before.items(): self.assertEqual((target/p).read_bytes(), data)
            self.assertTrue((target/'.workflow/templates/browser/playwright.config.mjs').is_file())
            self.assertEqual(collision.with_suffix('.saved').read_text(), 'Existing unrelated template')
            self.assertFalse((target/'node_modules').exists())


if __name__ == '__main__': unittest.main()
