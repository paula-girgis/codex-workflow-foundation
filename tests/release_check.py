"""Build and verify a clean local source distribution. Maintainer check, not a project runtime helper."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from distribution import package_files, adopt, update
from state import StateError, atomic_write, digest, read_json, validate
from workflow import selection


def run(root, *arguments):
    result = subprocess.run([sys.executable, *arguments], cwd=root, capture_output=True, text=True, encoding='utf-8',
                            env={**os.environ, 'GIT_CEILING_DIRECTORIES': str(root.parent.resolve())})
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout


def links(root):
    checked = 0
    for path in root.rglob('*.md'):
        if any(part in {'.tmp', '__pycache__', 'development', '.local', 'dist'} for part in path.relative_to(root).parts):
            continue
        content = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content):
            target = target.strip('<>').split('#')[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            assert (path.parent / unquote(target)).exists(), f'Broken Markdown link: {path.relative_to(root)} -> {target}'
            checked += 1
    return checked


def main():
    release, adopted = package_files(ROOT)
    files = {name.removeprefix('.workflow/'): data for name, data in adopted.items()}
    files['.gitignore'] = (ROOT / '.gitignore').read_bytes()
    files.update({p.relative_to(ROOT).as_posix(): p.read_bytes() for p in (ROOT / 'tests').glob('*.py')})
    forbidden = ['development/', 'project/', 'app/', 'artifacts/', '.local/', 'dist/']
    for name, data in files.items():
        assert not any(name.startswith(prefix) for prefix in forbidden), name
        assert not re.search(r'(?:[A-Z]:[\\/](?:Users|Under test)[\\/])', data.decode('utf-8'), re.I), name
        assert not any(word in name.lower() for word in ['.env', 'credentials', 'private-key'])
    template = json.loads(files['templates/project/state.json'])
    assert template['approvals'] == [] and template['artifacts'] == {}
    assert all(not t['evidence'] and t['status'] != 'Verified complete' for t in template['tasks'])
    for name, data in files.items():
        if name.endswith('SKILL.md'):
            content = data.decode('utf-8')
            assert content.startswith('---\n') or content.startswith('---\r\n')
            frontmatter = content.split('---', 2)[1]
            assert re.search(r'^name:\s*\S+', frontmatter, re.M)
            assert re.search(r'^description:\s*\S+', frontmatter, re.M)
    manifest = {'format': 'foundation-source-1', 'version': release['version'],
                'requirements': {'python': '3.10+', 'tested_python': sys.version.split()[0], 'core_dependencies': 'standard library', 'optional_png_fixture': 'Pillow'},
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}}
    dist = ROOT / 'dist'; dist.mkdir(exist_ok=True)
    archive = dist / f'codex-workflow-foundation-v{release["version"]}.zip'
    # Never replace a different already-released archive. A failed verification can be inspected first.
    if archive.exists():
        with zipfile.ZipFile(archive) as existing:
            assert json.loads(existing.read('DISTRIBUTION-MANIFEST.json')) == manifest, 'Existing distribution differs; preserve it and choose a new release version'
    else:
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as output:
            for name, data in sorted(files.items()):
                output.writestr(name, data)
            output.writestr('DISTRIBUTION-MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
    atomic_write(dist / f'{archive.name}.sha256', f'{digest(archive)}  {archive.name}\n'.encode())
    atomic_write(dist / f'v{release["version"]}-manifest.json', (json.dumps(manifest, indent=2) + '\n').encode())
    (ROOT / 'tests/.tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / 'tests/.tmp') as temp:
        temp = Path(temp); extracted = temp / 'source'; extracted.mkdir()
        with zipfile.ZipFile(archive) as zipped:
            assert set(zipped.namelist()) == set(files) | {'DISTRIBUTION-MANIFEST.json'}
            for name, expected in manifest['files'].items():
                data = zipped.read(name); assert hashlib.sha256(data).hexdigest() == expected
                path = extracted / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
            (extracted / 'DISTRIBUTION-MANIFEST.json').write_bytes(zipped.read('DISTRIBUTION-MANIFEST.json'))
        checked_links = links(extracted)
        fresh = temp / 'fresh'
        run(extracted, 'tools/workflow.py', 'adopt', '--target', str(fresh), '--ui')
        state = read_json(fresh / 'project/state.json')
        assert (fresh / 'project/LESSONS.md').read_bytes() == files['templates/project/LESSONS.md']
        assert 'project/LESSONS.md' in state['portable_files']
        assert state['approvals'] == [] and not state['artifacts']
        assert all(t['status'] != 'Verified complete' and not t['evidence'] for t in state['tasks'])
        assert (fresh / '.agents/skills/resume-project/SKILL.md').is_file()
        assert not validate(state, fresh)
        run(fresh, '.workflow/tools/workflow.py', 'resume')
        run(fresh, '.workflow/tools/workflow.py', 'validate')
        route = json.loads(run(fresh, '.workflow/tools/workflow.py', 'select', '--kind', 'bug'))
        assert [t['id'] for t in route['tasks']] == ['reproduce', 'fix', 'verify']
        checked_links += links(fresh)
        # Existing instructions/choices are retained, including on documented update.
        existing = temp / 'existing'; (existing / 'project').mkdir(parents=True)
        original = {'AGENTS.md': b'Existing instructions\n', 'project/PROFILE.md': b'Existing decisions\n',
                    'project/LESSONS.md': b'Synthetic existing project knowledge\n', 'existing.txt': b'Pre-existing work\n'}
        for name, data in original.items(): (existing / name).write_bytes(data)
        run(extracted, 'tools/workflow.py', 'adopt', '--target', str(existing), '--kind', 'bug')
        state_before = (existing / 'project/state.json').read_bytes()
        run(extracted, 'tools/workflow.py', 'update', '--target', str(existing))
        assert (existing / 'project/state.json').read_bytes() == state_before
        assert all((existing / name).read_bytes() == data for name, data in original.items())
        # Run only existing helper tests relevant to the release/update boundary.
        result = subprocess.run([sys.executable, '-m', 'unittest',
            'test_workflow.WorkflowTests.test_adoption_and_update_preserve_existing_repo',
            'test_workflow.WorkflowTests.test_update_conflict_stops_before_any_writes',
            'test_workflow.WorkflowTests.test_restored_adoption_retains_manifest_and_can_update',
            'test_workflow.WorkflowTests.test_existing_skill_collision_is_not_overwritten',
            'test_workflow.WorkflowTests.test_rehash_alone_does_not_refresh_evidence_or_approval',
            'test_lessons.LessonAdoptionTests'],
            cwd=extracted / 'tests', capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
    report = {'passed': True, 'version': release['version'], 'files': len(files), 'archive': archive.relative_to(ROOT).as_posix(), 'archive_sha256': digest(archive),
              'markdown_links_checked': checked_links, 'targeted_helper_tests': 8, 'inputs': manifest['files'],
              'checks': ['Clean inclusion allowlist and no concrete host paths', 'Clean templates and skill frontmatter', 'Archive extracted and every manifest hash verified', 'Fresh visual adoption and target-local validate/resume/select', 'Existing instructions/choices/application file/state preserved through adoption/update', 'Conflict, restored-manifest and stale-approval regressions'],
              'limits': ['Standard-library format checks are not automatic skill discovery', 'Local extraction/adoption only, not another-machine or off-device backup', 'Filename/path scan is not a general secret scanner; included text was also reviewed']}
    atomic_write(ROOT / f'development/evidence/release-v{release["version"]}.json', (json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps({key: value for key, value in report.items() if key != 'inputs'}, indent=2))


if __name__ == '__main__':
    main()
