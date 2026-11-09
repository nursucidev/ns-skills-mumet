"""Small disposable-workspace demonstrations; these do NOT execute an AI agent."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


def snapshot_files(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob('*') if p.is_file() and not p.is_symlink()
    }


class LocalIsolationDemos(unittest.TestCase):
    def test_41_disposable_build_writes_only_to_scratch(self):
        with tempfile.TemporaryDirectory(prefix='ns-mumet-isolation-') as tmp:
            base=Path(tmp)
            protected=base/'protected-project'
            protected.mkdir()
            (protected/'module.py').write_text('value = 42\n')
            before=snapshot_files(protected)
            scratch=base/'sandbox-copy'
            shutil.copytree(protected,scratch)
            script="from pathlib import Path; Path('output').mkdir(); Path('output/result.txt').write_text('generated'); assert Path('module.py').read_text() == 'value = 42\\n'"
            proc=subprocess.run([sys.executable,'-B','-c',script],cwd=scratch,capture_output=True,text=True,timeout=10)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertTrue((scratch/'output/result.txt').exists())
            self.assertEqual(snapshot_files(protected), before, 'protected workspace was modified')
            self.assertFalse((protected/'output').exists())

    def test_42_failing_sandbox_check_is_reported_as_failure(self):
        with tempfile.TemporaryDirectory(prefix='ns-mumet-fail-') as tmp:
            scratch=Path(tmp)/'scratch'
            scratch.mkdir()
            proc=subprocess.run([sys.executable,'-B','-c',"raise AssertionError('deliberate regression')"], cwd=scratch,capture_output=True,text=True,timeout=10)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('deliberate regression',proc.stderr)

    def test_43_escape_symlink_can_be_rejected_before_running_checks(self):
        with tempfile.TemporaryDirectory(prefix='ns-mumet-link-') as tmp:
            base=Path(tmp)
            protected=base/'protected'
            protected.mkdir()
            (protected/'private.dat').write_text('unchanged')
            scratch=base/'scratch'
            scratch.mkdir()
            (scratch/'unsafe-link').symlink_to(protected/'private.dat')
            escape_paths=[p for p in scratch.rglob('*') if p.is_symlink() and not p.resolve().is_relative_to(scratch.resolve())]
            self.assertEqual([p.name for p in escape_paths],['unsafe-link'])
            self.assertEqual((protected/'private.dat').read_text(),'unchanged')

    def test_44_git_workspace_remains_unchanged_after_sandbox_test(self):
        git=shutil.which('git')
        if git is None:
            self.skipTest('git not installed')
        with tempfile.TemporaryDirectory(prefix='ns-mumet-git-') as tmp:
            base=Path(tmp)
            original=base/'repo'; original.mkdir()
            def cmd(*args,cwd=original):
                return subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=10,check=True)
            cmd(git,'init','-q')
            cmd(git,'config','user.email','tester@example.invalid')
            cmd(git,'config','user.name','Test')
            (original/'app.txt').write_text('baseline\n')
            cmd(git,'add','app.txt')
            cmd(git,'commit','-qm','baseline')
            before=cmd(git,'status','--porcelain=v1').stdout
            digest_before=snapshot_files(original)
            copy=base/'isolated-copy'
            shutil.copytree(original,copy,ignore=shutil.ignore_patterns('.git'))
            (copy/'app.txt').write_text('changed only in scratch\n')
            (copy/'test-generated.log').write_text('temporary\n')
            self.assertEqual(cmd(git,'status','--porcelain=v1').stdout,before)
            self.assertEqual(snapshot_files(original),digest_before)
            self.assertEqual((original/'app.txt').read_text(),'baseline\n')


if __name__=='__main__': unittest.main(verbosity=2)
