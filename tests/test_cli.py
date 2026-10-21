from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
from importlib import metadata
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SOURCE_ROOT = Path(__file__).resolve().parents[1]


class InitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tact-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project with spaces 项目"
        self.root.mkdir()

    def run_cli(self, *args, expected=0, cwd=None):
        result = subprocess.run(
            [sys.executable, "-m", "tact", *map(str, args)],
            cwd=cwd or self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.root.rglob("*") if path.is_file()
        }

    def test_help_and_version(self):
        self.assertIn("init", self.run_cli("--help").stdout)
        self.assertEqual(
            self.run_cli("--version").stdout.strip(),
            f"tact {metadata.version('tact-agent-kit')}",
        )

    def test_initializes_specified_project_with_bundled_sources(self):
        self.run_cli("init", self.root, cwd=self.temp.name)
        kit = self.root / ".tact"
        self.assertEqual((kit / "AGENTS.md").read_bytes(), (SOURCE_ROOT / "AGENTS.md").read_bytes())
        expected_topics = {path.name for path in (SOURCE_ROOT / "core").glob("*.md")}
        self.assertEqual({path.name for path in (kit / "core").glob("*.md")}, expected_topics)
        for name in expected_topics:
            self.assertEqual((kit / "core" / name).read_bytes(), (SOURCE_ROOT / "core" / name).read_bytes())
        self.assertEqual((kit / "project/README.md").read_bytes(), (SOURCE_ROOT / "project/README.md").read_bytes())
        notes = (kit / "project/notes.md").read_text()
        self.assertIn(metadata.version("tact-agent-kit"), notes)
        self.assertNotIn("Confirmed source", notes)
        self.assertFalse((kit / "project/verification.md").exists())
        manifest = json.loads((kit / "manifest.json").read_text())
        self.assertEqual(manifest["package"], "tact-agent-kit")
        for relative, digest in manifest["files"].items():
            self.assertEqual(sha256((self.root / relative).read_bytes()).hexdigest(), digest)
        self.assertIn(".tact/AGENTS.md", (self.root / "AGENTS.md").read_text())

    def test_dry_run_shows_entry_diff_and_creates_nothing(self):
        result = self.run_cli("init", "--dry-run")
        self.assertIn("WOULD CREATE .tact/AGENTS.md", result.stdout)
        self.assertIn("+Before substantive work", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_preserves_existing_guidance_bytes_and_project_files(self):
        original = b"# Existing project\r\n\r\nKeep the public API.\r\n"
        entry = self.root / "AGENTS.md"
        entry.write_bytes(original)
        entry.chmod(0o640)
        project = self.root / ".tact/project"
        project.mkdir(parents=True)
        (project / "notes.md").write_text("# Confirmed constraints\nKeep our data format.\n")
        (project / "README.md").write_text("Our own project guide.\n")
        (project / "working.md").write_text("Our investigation rules.\n")
        (self.root / "project").mkdir()
        (self.root / "project/notes.md").write_text("An unrelated existing directory.\n")
        before = self.snapshot()
        self.run_cli("init")
        after = self.snapshot()
        for name, content in before.items():
            if name != "AGENTS.md":
                self.assertEqual(after[name], content)
        self.assertTrue(entry.read_bytes().startswith(original))
        self.assertNotIn(b"\n", entry.read_bytes().replace(b"\r\n", b""))
        self.assertEqual(entry.stat().st_mode & 0o777, 0o640)

    def test_repeat_is_noop_even_with_local_project_edits(self):
        self.run_cli("init")
        (self.root / ".tact/project/notes.md").write_text("Custom notes.\n")
        entry = self.root / "AGENTS.md"
        entry.write_bytes(b"# Local instructions\n\n" + entry.read_bytes() + b"\nMore local guidance.\n")
        before = self.snapshot()
        self.assertIn("Already initialized", self.run_cli("init").stdout)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(entry.read_text().count("<!-- tact:begin -->"), 1)

    def test_conflicting_shared_file_stops_all_writes_and_shows_diff(self):
        core = self.root / ".tact/core"
        core.mkdir(parents=True)
        (core / "working.md").write_text("Existing custom working rules.\n")
        before = self.snapshot()
        for flags in [(), ("--dry-run",)]:
            result = self.run_cli("init", *flags, expected=1)
            self.assertIn("-Existing custom working rules.", result.stderr)
            self.assertIn("No files changed", result.stderr)
            self.assertEqual(before, self.snapshot())
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_different_installed_version_is_not_silently_upgraded(self):
        self.run_cli("init")
        path = self.root / ".tact/manifest.json"
        data = json.loads(path.read_text())
        data["version"] = "0.0.1"
        path.write_text(json.dumps(data))
        before = self.snapshot()
        self.assertIn("init does not upgrade", self.run_cli("init", expected=1).stderr)
        self.assertEqual(before, self.snapshot())

    def test_newline_only_shared_difference_still_identifies_the_file(self):
        self.run_cli("init")
        path = self.root / ".tact/core/working.md"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        before = self.snapshot()
        result = self.run_cli("init", expected=1)
        self.assertIn(".tact/core/working.md: file bytes differ", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_modified_entry_block_is_preserved_and_reported(self):
        self.run_cli("init")
        entry = self.root / "AGENTS.md"
        entry.write_text(entry.read_text().replace("Before substantive work", "Only when asked"))
        before = self.snapshot()
        self.assertIn("TacT block", self.run_cli("init", expected=1).stderr)
        self.assertEqual(before, self.snapshot())

    def test_invalid_markers_do_not_create_a_partial_kit(self):
        for content in ["<!-- tact:begin -->", "<!-- tact:end -->", "<!-- tact:begin -->" * 2,
                        "<!-- tact:end -->\n<!-- tact:begin -->"]:
            with self.subTest(content=content):
                (self.root / "AGENTS.md").write_text(content)
                self.run_cli("init", expected=1)
                self.assertFalse((self.root / ".tact").exists())
                self.assertEqual((self.root / "AGENTS.md").read_text(), content)

    def test_missing_file_can_be_restored_without_replacing_other_files(self):
        self.run_cli("init")
        (self.root / ".tact/core/working.md").unlink()
        before = self.snapshot()
        self.run_cli("init")
        after = self.snapshot()
        for relative, content in before.items():
            self.assertEqual(after[relative], content)
        self.assertTrue((self.root / ".tact/core/working.md").is_file())

    def test_active_override_prevents_a_misleading_install(self):
        (self.root / "AGENTS.override.md").write_text("Use these instructions instead.\n")
        result = self.run_cli("init", expected=1)
        self.assertIn("take precedence", result.stderr)
        self.assertEqual({p.name for p in self.root.iterdir()}, {"AGENTS.override.md"})

    def test_links_cannot_redirect_writes_outside_the_target(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / ".tact").symlink_to(outside, target_is_directory=True)
        self.assertIn("symbolic links", self.run_cli("init", expected=1).stderr)
        self.assertEqual(list(outside.iterdir()), [])
        (self.root / ".tact").unlink()
        target = outside / "instructions.md"
        target.write_text("External guidance\n")
        (self.root / "AGENTS.md").symlink_to(target)
        self.run_cli("init", expected=1)
        self.assertEqual(target.read_text(), "External guidance\n")
        self.assertFalse((self.root / ".tact").exists())

    def test_missing_target_or_obstructing_file_is_reported_without_writes(self):
        self.run_cli("init", self.root / "missing", expected=1)
        self.assertEqual(list(self.root.iterdir()), [])
        (self.root / ".tact").write_text("An existing file\n")
        self.run_cli("init", expected=1)
        self.assertEqual((self.root / ".tact").read_text(), "An existing file\n")
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_non_utf8_entry_is_not_modified(self):
        content = b"Existing guidance \xff"
        (self.root / "AGENTS.md").write_bytes(content)
        self.assertIn("UTF-8", self.run_cli("init", expected=1).stderr)
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), content)
        self.assertFalse((self.root / ".tact").exists())

    def test_installed_markdown_links_resolve(self):
        self.run_cli("init")
        files = [self.root / "AGENTS.md", *(self.root / ".tact").rglob("*.md")]
        for path in files:
            for destination in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                if "://" not in destination and not destination.startswith("#"):
                    self.assertTrue((path.parent / destination.split("#")[0]).exists(), f"{path}: {destination}")

    def prepare_older_kit(self):
        self.run_cli("init")
        old_readme = self.root / ".tact/core/README.md"
        old_readme.write_text("# Earlier TacT setup\n\nFollow project instructions.\n")
        manifest_path = self.root / ".tact/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["version"] = "0.1.0"
        manifest["files"][".tact/core/README.md"] = sha256(old_readme.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        # Exact notes emitted by the initial 0.1.0 CLI, before the introduction.
        (self.root / ".tact/project/notes.md").write_text(
            "# Project notes\n\n"
            "TacT source: [https://github.com/MerlinSMQWQ/TacT](https://github.com/MerlinSMQWQ/TacT), "
            "package `tact-agent-kit` version `0.1.0`. "
            "The installed shared-file hashes are recorded in `../manifest.json`.\n"
        )

    def test_update_previews_then_upgrades_an_untouched_older_kit(self):
        self.prepare_older_kit()
        old_readme = self.root / ".tact/core/README.md"
        old_readme.chmod(0o640)
        self.assertIn("tact update --dry-run", self.run_cli("init", expected=1).stderr)
        before = self.snapshot()
        preview = self.run_cli("update", self.root, "--dry-run", cwd=self.temp.name)
        self.assertIn("WOULD UPDATE .tact/core/README.md", preview.stdout)
        self.assertIn("+This file intentionally starts nearly empty", preview.stdout)
        self.assertEqual(before, self.snapshot())
        result = self.run_cli("update")
        self.assertIn("Updated.", result.stdout)
        self.assertEqual(old_readme.read_bytes(), (SOURCE_ROOT / "core/README.md").read_bytes())
        self.assertEqual(old_readme.stat().st_mode & 0o777, 0o640)
        notes = (self.root / ".tact/project/notes.md").read_text()
        self.assertIn("project maintainer and agents", notes)
        self.assertIn(f"version `{metadata.version('tact-agent-kit')}`", notes)
        manifest = json.loads((self.root / ".tact/manifest.json").read_text())
        for relative, digest in manifest["files"].items():
            self.assertEqual(sha256((self.root / relative).read_bytes()).hexdigest(), digest)
        after = self.snapshot()
        self.assertIn("Already up to date", self.run_cli("update").stdout)
        self.assertIn("Already initialized", self.run_cli("init").stdout)
        self.assertEqual(after, self.snapshot())

    def test_update_preserves_custom_project_guidance_and_root_entry(self):
        self.prepare_older_kit()
        notes = self.root / ".tact/project/notes.md"
        notes.write_bytes(notes.read_bytes() + b"\nConfirmed: preserve our public API.\n")
        guide = self.root / ".tact/project/README.md"
        guide.write_text("Our project guide.\n")
        supplement = self.root / ".tact/project/verification.md"
        supplement.write_text("Our release checks.\n")
        entry = self.root / "AGENTS.md"
        entry.write_bytes(b"# Local instructions\n\n" + entry.read_bytes())
        before = self.snapshot()
        self.run_cli("update")
        after = self.snapshot()
        for path in (notes, guide, supplement, entry):
            relative = str(path.relative_to(self.root))
            self.assertEqual(before[relative], after[relative])

    def test_update_refuses_local_changes_before_any_writes(self):
        self.prepare_older_kit()
        path = self.root / ".tact/core/working.md"
        path.write_bytes(path.read_bytes() + b"\nOur local shared-file edit.\n")
        (self.root / ".tact/core/tools.md").unlink()
        before = self.snapshot()
        for flags in [(), ("--dry-run",)]:
            result = self.run_cli("update", *flags, expected=1)
            self.assertIn(".tact/core/working.md: differs from the recorded installation", result.stderr)
            self.assertIn("No files changed", result.stderr)
            self.assertEqual(before, self.snapshot())

    def test_update_requires_a_valid_manifest_without_following_its_paths(self):
        self.prepare_older_kit()
        path = self.root / ".tact/manifest.json"
        good = json.loads(path.read_text())
        invalid = [None, b"not json", b"[]"]
        for key, value in [("schema_version", 99), ("package", "another-package"),
                           ("files", []), ("version", None)]:
            invalid.append(json.dumps({**good, key: value}).encode())
        for relative, digest in [(".tact/AGENTS.md", "invalid"), ("../../outside.md", "a" * 64)]:
            invalid.append(json.dumps({**good, "files": {**good["files"], relative: digest}}).encode())
        for content in invalid:
            with self.subTest(content=content):
                if content is None:
                    path.unlink()
                else:
                    path.write_bytes(content)
                before = self.snapshot()
                result = self.run_cli("update", expected=1)
                self.assertIn("No files changed", result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_update_does_not_overwrite_an_untracked_file_at_a_new_shared_path(self):
        self.prepare_older_kit()
        manifest_path = self.root / ".tact/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        del manifest["files"][".tact/core/tools.md"]
        manifest_path.write_text(json.dumps(manifest))
        (self.root / ".tact/core/tools.md").write_text("Existing content without a recorded baseline.\n")
        before = self.snapshot()
        self.assertIn("not tracked", self.run_cli("update", expected=1).stderr)
        self.assertEqual(before, self.snapshot())

    def test_update_restores_missing_files_and_accepts_already_updated_files(self):
        self.prepare_older_kit()
        (self.root / ".tact/core/README.md").write_bytes((SOURCE_ROOT / "core/README.md").read_bytes())
        (self.root / ".tact/core/tools.md").unlink()
        self.run_cli("update")
        self.assertEqual((self.root / ".tact/core/tools.md").read_bytes(), (SOURCE_ROOT / "core/tools.md").read_bytes())
        self.assertIn("Already initialized", self.run_cli("init").stdout)

    def test_interrupted_update_preserves_the_old_manifest_and_can_resume(self):
        from tact.cli import main

        self.prepare_older_kit()
        manifest_path = self.root / ".tact/manifest.json"
        previous_manifest = manifest_path.read_bytes()
        real_replace = Path.replace

        def fail_manifest_replace(path, destination):
            if destination.resolve() == manifest_path.resolve():
                raise OSError("simulated storage failure")
            return real_replace(path, destination)

        errors = io.StringIO()
        with mock.patch.object(Path, "replace", fail_manifest_replace), redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(main(["update", str(self.root)]), 1)
        self.assertIn("some files may have been created or updated", errors.getvalue())
        self.assertEqual(manifest_path.read_bytes(), previous_manifest)
        self.assertEqual((self.root / ".tact/core/README.md").read_bytes(), (SOURCE_ROOT / "core/README.md").read_bytes())
        self.run_cli("update")
        self.assertIn("Already initialized", self.run_cli("init").stdout)


if __name__ == "__main__":
    unittest.main()
