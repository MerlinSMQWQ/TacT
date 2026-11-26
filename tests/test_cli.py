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

# Historical installation fixture; keep independent of the current CLI template.
LEGACY_ENTRY = """<!-- tact:begin -->
## TacT Agent Kit

Before substantive work, read the [TacT entry](.tact/AGENTS.md) and
[project notes](.tact/project/notes.md). Follow the entry's topic-reading triggers
and check matching project supplements.

The Kit root is `.tact/` in this repository. Resolve paths inside the Kit from
that directory, even when working in a subdirectory. Keep the existing repository
instructions in force. Resolve conflicts using the host's instruction hierarchy;
ask about consequential unresolved conflicts before taking dependent actions.
<!-- tact:end -->
"""

# Generated after first-response reading became mandatory, before completeness checks.
INITIAL_READING_ENTRY = """<!-- tact:begin -->
## TacT Agent Kit

Before your first response in each new session, read the [TacT entry](.tact/AGENTS.md),
[project notes](.tact/project/notes.md), and
[communication guidance](.tact/core/communication.md). Also read
`.tact/project/communication.md` if it exists. This applies to short questions
and casual conversation as well as engineering work; do not defer it until a
substantive task. Reuse their current contents if already supplied in this
session; otherwise read the files. Follow the entry's remaining topic-reading
triggers and check matching project supplements.

The Kit root is `.tact/` in this repository. Resolve paths inside the Kit from
that directory, even when working in a subdirectory. Keep the existing repository
instructions in force. Resolve conflicts using the host's instruction hierarchy;
ask about consequential unresolved conflicts before taking dependent actions.
<!-- tact:end -->
"""

# Generated with completeness checks, before the communication/style split.
COMPLETE_READING_ENTRY = """<!-- tact:begin -->
## TacT Agent Kit

Before your first response in each new session, read the [TacT entry](.tact/AGENTS.md),
[project notes](.tact/project/notes.md), and
[communication guidance](.tact/core/communication.md). Also read
`.tact/project/communication.md` if it exists. This applies to short questions
and casual conversation as well as engineering work; do not defer it until a
substantive task. Reuse their current contents if already supplied in this
session; otherwise read the files. Follow the entry's remaining topic-reading
triggers and check matching project supplements.

Read each required file in full before the response or action it governs.
Check the text actually returned: successful commands can still yield truncated
output. Keep reads within individual and combined output limits; read long files
separately in consecutive ranges and recover every missing range, including
partly returned lines. If coverage is unclear, reread that file in smaller
ranges. Reuse complete current contents already in context. If required content
remains unavailable, report the gap and pause dependent actions.

The Kit root is `.tact/` in this repository. Resolve paths inside the Kit from
that directory, even when working in a subdirectory. Keep the existing repository
instructions in force. Resolve conflicts using the host's instruction hierarchy;
ask about consequential unresolved conflicts before taking dependent actions.
<!-- tact:end -->
"""

# Generated after the style split, before post-compaction rereading.
STYLE_READING_ENTRY = """<!-- tact:begin -->
## TacT Agent Kit

Before your first response in each new session, read the [TacT entry](.tact/AGENTS.md),
[project notes](.tact/project/notes.md),
[communication guidance](.tact/core/communication.md), and
[language and conversational style](.tact/core/style.md). Also read
`.tact/project/communication.md` and `.tact/project/style.md` if present.
This applies to short questions
and casual conversation as well as engineering work; do not defer it until a
substantive task. Reuse their current contents if already supplied in this
session; otherwise read the files. Follow the entry's remaining topic-reading
triggers and check matching project supplements.

Read each required file in full before the response or action it governs.
Check the text actually returned: successful commands can still yield truncated
output. Keep reads within individual and combined output limits; read long files
separately in consecutive ranges and recover every missing range, including
partly returned lines. If coverage is unclear, reread that file in smaller
ranges. Reuse complete current contents already in context. If required content
remains unavailable, report the gap and pause dependent actions.

The Kit root is `.tact/` in this repository. Resolve paths inside the Kit from
that directory, even when working in a subdirectory. Keep the existing repository
instructions in force. Resolve conflicts using the host's instruction hierarchy;
ask about consequential unresolved conflicts before taking dependent actions.
<!-- tact:end -->
"""

# Generated after post-compaction rereading was added.
POST_COMPACTION_STYLE_ENTRY = STYLE_READING_ENTRY.replace(
    "The Kit root is `.tact/` in this repository.",
    """After context compaction, check which of `.tact/core/communication.md`,
`.tact/core/style.md`, and `.tact/core/communication-examples.md` you still
have in full. Before your next reply to the developer, reread any missing text.
If only a summary, a path, or a record of an earlier read remains for a file,
reread that file in full.

The Kit root is `.tact/` in this repository.""",
)


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
        help_text = self.run_cli("--help").stdout
        self.assertIn("init", help_text)
        self.assertIn("refresh", help_text)
        self.assertNotIn("update", help_text)
        self.assertIn("installed TacT package", self.run_cli("refresh", "--help").stdout)
        self.assertIn("invalid choice", self.run_cli("update", expected=2).stderr)
        self.assertEqual(self.snapshot(), {})
        self.assertEqual(
            self.run_cli("--version").stdout.strip(),
            f"tact {metadata.version('tact-agent-kit')}",
        )

    def test_initializes_specified_project_with_bundled_sources(self):
        self.run_cli("init", self.root, cwd=self.temp.name)
        kit = self.root / ".tact"
        source_entry = (SOURCE_ROOT / "AGENTS.md").read_bytes()
        shared_rules = source_entry.partition(b"\n<!-- tact:begin -->")[0]
        self.assertEqual((kit / "AGENTS.md").read_bytes(), shared_rules)
        self.assertNotIn(b"<!-- tact:begin -->", (kit / "AGENTS.md").read_bytes())
        self.assertEqual((kit / "LICENSE").read_bytes(), (SOURCE_ROOT / "LICENSE").read_bytes())
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
        self.assertIn(".tact/core/communication.md", (self.root / "AGENTS.md").read_text())
        self.assertNotIn(".tact/core/style.md", (self.root / "AGENTS.md").read_text())
        for entry in (kit / "AGENTS.md", self.root / "AGENTS.md"):
            recovery = entry.read_text().split("After context compaction", 1)[1].split("\n\n", 1)[0]
            for name in ("communication.md", "communication-examples.md"):
                self.assertIn(f"core/{name}", recovery)
        skill = self.root / ".agents/skills/tact"
        for relative in ("SKILL.md", "agents/openai.yaml"):
            self.assertEqual((skill / relative).read_bytes(), (SOURCE_ROOT / "skills/tact" / relative).read_bytes())
            self.assertIn(f".agents/skills/tact/{relative}", manifest["files"])

    def test_dry_run_shows_entry_diff_and_creates_nothing(self):
        result = self.run_cli("init", "--dry-run")
        self.assertIn("WOULD CREATE .tact/AGENTS.md", result.stdout)
        self.assertIn("WOULD CREATE .agents/skills/tact/SKILL.md", result.stdout)
        self.assertIn("WOULD CREATE .agents/skills/tact/agents/openai.yaml", result.stdout)
        self.assertIn("+Before your first response", result.stdout)
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

    def test_modified_entry_block_blocks_init_but_allows_refresh(self):
        self.run_cli("init")
        entry = self.root / "AGENTS.md"
        entry.write_text(entry.read_text().replace("Before your first response", "Only when asked"))
        before = self.snapshot()
        self.assertIn("TacT block", self.run_cli("init", expected=1).stderr)
        self.assertEqual(before, self.snapshot())
        self.assertIn("Already up to date", self.run_cli("refresh").stdout)
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

    def test_skill_path_links_cannot_redirect_writes_outside_the_target(self):
        from tact.cli import bundled_files

        shared, _ = bundled_files()
        manifest = self.root / ".tact/manifest.json"
        manifest.parent.mkdir()
        manifest.write_bytes(shared[".tact/manifest.json"])
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        for relative in (".agents", ".agents/skills", ".agents/skills/tact",
                         ".agents/skills/tact/agents", ".agents/skills/tact/SKILL.md",
                         ".agents/skills/tact/agents/openai.yaml"):
            with self.subTest(relative=relative):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(outside, target_is_directory=True)
                for command in ("init", "refresh"):
                    before = self.snapshot()
                    self.assertIn("symbolic links", self.run_cli(command, expected=1).stderr)
                    self.assertEqual(before, self.snapshot())
                    self.assertEqual(list(outside.iterdir()), [])
                path.unlink()

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
        files = [self.root / "AGENTS.md", *(self.root / ".tact").rglob("*.md"),
                 *(self.root / ".agents/skills/tact").rglob("*.md")]
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
        # Older releases installed no skill; refresh must add it.
        for relative in list(manifest["files"]):
            if relative.startswith(".agents/"):
                (self.root / relative).unlink()
                del manifest["files"][relative]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        # Exact notes emitted by the initial 0.1.0 CLI, before the introduction.
        (self.root / ".tact/project/notes.md").write_text(
            "# Project notes\n\n"
            "TacT source: [https://github.com/MerlinSMQWQ/TacT](https://github.com/MerlinSMQWQ/TacT), "
            "package `tact-agent-kit` version `0.1.0`. "
            "The installed shared-file hashes are recorded in `../manifest.json`.\n"
        )

    def test_refresh_previews_then_upgrades_an_untouched_older_kit(self):
        self.prepare_older_kit()
        old_readme = self.root / ".tact/core/README.md"
        old_readme.chmod(0o640)
        self.assertIn("tact refresh --dry-run", self.run_cli("init", expected=1).stderr)
        before = self.snapshot()
        preview = self.run_cli("refresh", self.root, "--dry-run", cwd=self.temp.name)
        self.assertIn("WOULD UPDATE .tact/core/README.md", preview.stdout)
        self.assertIn("WOULD CREATE .agents/skills/tact/SKILL.md", preview.stdout)
        self.assertIn("+This file intentionally starts nearly empty", preview.stdout)
        self.assertEqual(before, self.snapshot())
        result = self.run_cli("refresh")
        self.assertIn("Refreshed.", result.stdout)
        self.assertEqual(old_readme.read_bytes(), (SOURCE_ROOT / "core/README.md").read_bytes())
        self.assertEqual(old_readme.stat().st_mode & 0o777, 0o640)
        self.assertTrue((self.root / ".agents/skills/tact/agents/openai.yaml").is_file())
        notes = (self.root / ".tact/project/notes.md").read_text()
        self.assertIn("project maintainer and agents", notes)
        self.assertIn(f"version `{metadata.version('tact-agent-kit')}`", notes)
        manifest = json.loads((self.root / ".tact/manifest.json").read_text())
        for relative, digest in manifest["files"].items():
            self.assertEqual(sha256((self.root / relative).read_bytes()).hexdigest(), digest)
        after = self.snapshot()
        self.assertIn("Already up to date", self.run_cli("refresh").stdout)
        self.assertIn("Already initialized", self.run_cli("init").stdout)
        self.assertEqual(after, self.snapshot())

    def test_refresh_preserves_custom_project_guidance_and_root_entry(self):
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
        self.run_cli("refresh")
        after = self.snapshot()
        for path in (notes, guide, supplement, entry):
            relative = str(path.relative_to(self.root))
            self.assertEqual(before[relative], after[relative])

    def test_refresh_migrates_generated_legacy_entry_preserving_newlines(self):
        self.run_cli("init")
        current_template = (self.root / "AGENTS.md").read_bytes()
        for legacy, newline in (
            (LEGACY_ENTRY, b"\n"), (LEGACY_ENTRY, b"\r\n"),
            (INITIAL_READING_ENTRY, b"\n"), (INITIAL_READING_ENTRY, b"\r\n"),
            (COMPLETE_READING_ENTRY, b"\n"), (COMPLETE_READING_ENTRY, b"\r\n"),
            (STYLE_READING_ENTRY, b"\n"), (STYLE_READING_ENTRY, b"\r\n"),
            (POST_COMPACTION_STYLE_ENTRY, b"\n"), (POST_COMPACTION_STYLE_ENTRY, b"\r\n"),
        ):
            with self.subTest(legacy=legacy, newline=newline):
                self.prepare_older_kit()
                entry = self.root / "AGENTS.md"
                current = current_template.replace(b"\n", newline)
                prefix = newline
                suffix = newline + b" \t"
                entry.write_bytes(prefix + legacy.encode().replace(b"\n", newline) + suffix)
                entry.chmod(0o640)
                supplement = self.root / ".tact/project/communication.md"
                supplement.write_bytes(b"# Our communication preferences\nUse plain language.\n")
                style_supplement = self.root / ".tact/project/style.md"
                style_supplement.write_bytes(b"# Our style preferences\nUse familiar technical terms.\n")
                before = self.snapshot()

                self.assertIn("tact refresh --dry-run", self.run_cli("init", expected=1).stderr)
                self.assertEqual(before, self.snapshot())
                preview = self.run_cli("refresh", "--dry-run")
                self.assertIn("WOULD UPDATE AGENTS.md", preview.stdout)
                self.assertEqual(before, self.snapshot())

                self.run_cli("refresh")
                self.assertEqual(entry.read_bytes(), prefix + current + suffix)
                self.assertEqual(entry.stat().st_mode & 0o777, 0o640)
                self.assertEqual(self.snapshot()[".tact/project/communication.md"],
                                 before[".tact/project/communication.md"])
                self.assertEqual(self.snapshot()[".tact/project/style.md"],
                                 before[".tact/project/style.md"])
                after = self.snapshot()
                self.assertIn("Already up to date", self.run_cli("refresh").stdout)
                self.assertIn("Already initialized", self.run_cli("init").stdout)
                self.assertEqual(after, self.snapshot())

    def test_refresh_preserves_custom_root_entries_while_updating_shared_files(self):
        self.run_cli("init")
        entry = self.root / "AGENTS.md"
        current = entry.read_bytes()
        cases = {
            "project instructions only": b"# Project instructions\nKeep our public API.\n",
            "project prefix": b"# Project instructions\n\n" + current,
            "project suffix": current + b"\nKeep our public API.",
            "legacy block with project content": (
                b"# Project instructions\r\n\r\n"
                + LEGACY_ENTRY.encode().replace(b"\n", b"\r\n")
                + b"\r\nKeep our public API."
            ),
            "custom legacy block": LEGACY_ENTRY.replace(
                "Before substantive work", "Only when asked",
            ).encode(),
            "initial reading block with project content": (
                INITIAL_READING_ENTRY.encode() + b"\nKeep our public API."
            ),
            "custom initial reading block": INITIAL_READING_ENTRY.replace(
                "Before your first response", "Only when asked",
            ).encode(),
            "complete reading block with project content": (
                COMPLETE_READING_ENTRY.encode() + b"\nKeep our public API."
            ),
            "custom complete reading block": COMPLETE_READING_ENTRY.replace(
                "Read each required file in full", "Read only the introduction",
            ).encode(),
            "blank line inside initial reading block": INITIAL_READING_ENTRY.replace(
                "<!-- tact:begin -->\n", "<!-- tact:begin -->\n\n", 1,
            ).encode(),
            "blank line inside current block": current.replace(
                b"<!-- tact:begin -->\n", b"<!-- tact:begin -->\n\n", 1,
            ),
            "incomplete markers": b"# Project instructions\n<!-- tact:begin -->\nCustom guide.\n",
            "duplicate blocks": current + current,
            "non-UTF-8 project content": b"# Project instructions\n\xff\n",
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                entry.write_bytes(current)
                self.prepare_older_kit()
                entry.write_bytes(content)
                entry.chmod(0o640)
                missing_topic = self.root / ".tact/core/tools.md"
                missing_topic.unlink()
                before = self.snapshot()

                preview = self.run_cli("refresh", "--dry-run")
                self.assertIn("WOULD UPDATE .tact/core/README.md", preview.stdout)
                self.assertIn("WOULD CREATE .tact/core/tools.md", preview.stdout)
                self.assertNotIn("WOULD UPDATE AGENTS.md", preview.stdout)
                self.assertNotIn("WOULD APPEND AGENTS.md", preview.stdout)
                self.assertEqual(before, self.snapshot())

                result = self.run_cli("refresh")
                self.assertIn("UPDATE .tact/core/README.md", result.stdout)
                self.assertEqual(self.snapshot()["AGENTS.md"], before["AGENTS.md"])
                self.assertEqual(entry.stat().st_mode & 0o777, 0o640)
                self.assertEqual((self.root / ".tact/core/README.md").read_bytes(),
                                 (SOURCE_ROOT / "core/README.md").read_bytes())
                self.assertEqual(missing_topic.read_bytes(), (SOURCE_ROOT / "core/tools.md").read_bytes())
                manifest = json.loads((self.root / ".tact/manifest.json").read_text())
                for relative, digest in manifest["files"].items():
                    self.assertEqual(sha256((self.root / relative).read_bytes()).hexdigest(), digest)
                after = self.snapshot()
                self.assertIn("Already up to date", self.run_cli("refresh").stdout)
                self.assertEqual(after, self.snapshot())

    def test_refresh_restores_a_missing_or_empty_root_entry(self):
        self.run_cli("init")
        entry = self.root / "AGENTS.md"
        current = entry.read_bytes()
        for content in (None, b"", b"\r\n"):
            with self.subTest(content=content):
                entry.write_bytes(current)
                self.prepare_older_kit()
                if content is None:
                    entry.unlink()
                else:
                    entry.write_bytes(content)
                before = self.snapshot()
                preview = self.run_cli("refresh", "--dry-run")
                action = "CREATE" if content is None else "APPEND"
                self.assertIn(f"WOULD {action} AGENTS.md", preview.stdout)
                self.assertEqual(before, self.snapshot())
                self.run_cli("refresh")
                self.assertIn(b"[communication guidance](.tact/core/communication.md)", entry.read_bytes())
                self.assertNotIn(b".tact/core/style.md", entry.read_bytes())
                self.assertEqual((self.root / ".tact/core/README.md").read_bytes(),
                                 (SOURCE_ROOT / "core/README.md").read_bytes())

    def test_refresh_removes_source_adoption_block_from_shared_entry(self):
        from tact.cli import ENTRY

        self.run_cli("init")
        shared_entry = self.root / ".tact/AGENTS.md"
        expected_rules = shared_entry.read_bytes()
        root_entry = (self.root / "AGENTS.md").read_bytes()
        shared_entry.write_bytes(expected_rules + b"\n" + ENTRY.encode())
        manifest_path = self.root / ".tact/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"][".tact/AGENTS.md"] = sha256(shared_entry.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))

        self.run_cli("refresh")

        self.assertEqual(shared_entry.read_bytes(), expected_rules)
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), root_entry)
        updated = json.loads(manifest_path.read_text())
        self.assertEqual(updated["files"][".tact/AGENTS.md"], sha256(expected_rules).hexdigest())
        self.assertIn("Already up to date", self.run_cli("refresh").stdout)

    def test_refresh_refuses_local_changes_before_any_writes(self):
        self.prepare_older_kit()
        path = self.root / ".tact/core/working.md"
        path.write_bytes(path.read_bytes() + b"\nOur local shared-file edit.\n")
        (self.root / ".tact/core/tools.md").unlink()
        before = self.snapshot()
        for flags in [(), ("--dry-run",)]:
            result = self.run_cli("refresh", *flags, expected=1)
            self.assertIn(".tact/core/working.md: differs from the recorded installation", result.stderr)
            self.assertIn("No files changed", result.stderr)
            self.assertEqual(before, self.snapshot())

    def test_refresh_requires_a_valid_manifest_without_following_its_paths(self):
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
                result = self.run_cli("refresh", expected=1)
                self.assertIn("No files changed", result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_refresh_does_not_overwrite_an_untracked_file_at_a_new_shared_path(self):
        self.prepare_older_kit()
        manifest_path = self.root / ".tact/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        del manifest["files"][".tact/core/tools.md"]
        manifest_path.write_text(json.dumps(manifest))
        (self.root / ".tact/core/tools.md").write_text("Existing content without a recorded baseline.\n")
        before = self.snapshot()
        self.assertIn("not tracked", self.run_cli("refresh", expected=1).stderr)
        self.assertEqual(before, self.snapshot())

    def test_refresh_restores_missing_files_and_accepts_already_updated_files(self):
        self.prepare_older_kit()
        (self.root / ".tact/core/README.md").write_bytes((SOURCE_ROOT / "core/README.md").read_bytes())
        (self.root / ".tact/core/tools.md").unlink()
        self.run_cli("refresh")
        self.assertEqual((self.root / ".tact/core/tools.md").read_bytes(), (SOURCE_ROOT / "core/tools.md").read_bytes())
        self.assertIn("Already initialized", self.run_cli("init").stdout)

    def install_previous_style(self):
        self.run_cli("init")
        old_style = self.root / ".tact/core/style.md"
        old_style.write_text("Earlier shared style guidance.\n")
        manifest_path = self.root / ".tact/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"][".tact/core/style.md"] = sha256(old_style.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        return old_style, manifest_path

    def test_refresh_removes_unmodified_retired_style_and_migrates_entry(self):
        old_style, manifest_path = self.install_previous_style()
        entry = self.root / "AGENTS.md"
        entry.write_text(POST_COMPACTION_STYLE_ENTRY)
        supplement = self.root / ".tact/project/style.md"
        supplement.write_text("Our own preferences.\n")
        before = self.snapshot()
        preview = self.run_cli("refresh", "--dry-run")
        self.assertIn("WOULD DELETE .tact/core/style.md", preview.stdout)
        self.assertEqual(self.snapshot(), before)
        self.run_cli("refresh")
        self.assertFalse(old_style.exists())
        self.assertNotIn(".tact/core/style.md", json.loads(manifest_path.read_text())["files"])
        self.assertNotIn(".tact/core/style.md", entry.read_text())
        self.assertIn(".tact/project/style.md", entry.read_text())
        self.assertEqual(supplement.read_text(), "Our own preferences.\n")
        self.assertIn("Already up to date", self.run_cli("refresh").stdout)

    def test_refresh_refuses_modified_retired_style_before_writing(self):
        old_style, _ = self.install_previous_style()
        old_style.write_text("Local changes to shared style.\n")
        before = self.snapshot()
        for args in [(), ("--dry-run",)]:
            result = self.run_cli("refresh", *args, expected=1)
            self.assertIn("review the local edits", result.stderr)
            self.assertEqual(self.snapshot(), before)

    def test_refresh_accepts_retired_style_already_missing(self):
        old_style, manifest_path = self.install_previous_style()
        old_style.unlink()
        self.run_cli("refresh")
        self.assertNotIn(".tact/core/style.md", json.loads(manifest_path.read_text())["files"])

    def test_refresh_refuses_custom_entry_that_still_references_retired_style(self):
        self.install_previous_style()
        entry = self.root / "AGENTS.md"
        entry.write_text("# Our instructions\nRead .tact/core/style.md.\n")
        before = self.snapshot()
        for args in [(), ("--dry-run",)]:
            result = self.run_cli("refresh", *args, expected=1)
            self.assertIn("Update the custom project entry", result.stderr)
            self.assertEqual(self.snapshot(), before)

    def test_interrupted_retired_style_removal_can_resume(self):
        from tact.cli import main

        old_style, manifest = self.install_previous_style()
        (self.root / "AGENTS.md").write_text(POST_COMPACTION_STYLE_ENTRY)
        old_manifest = manifest.read_bytes()
        replace = Path.replace

        def fail_manifest(path, destination):
            if destination.resolve() == manifest.resolve():
                raise OSError("simulated storage failure")
            return replace(path, destination)

        with mock.patch.object(Path, "replace", fail_manifest), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(["refresh", str(self.root)]), 1)
        self.assertFalse(old_style.exists())
        self.assertEqual(manifest.read_bytes(), old_manifest)
        self.run_cli("refresh")
        self.assertNotIn(".tact/core/style.md", json.loads(manifest.read_text())["files"])

    def test_skill_conflicts_stop_init_and_refresh_without_overwriting_other_skills(self):
        for relative in ("SKILL.md", "agents/openai.yaml"):
            with self.subTest(relative=relative):
                self.prepare_older_kit()
                skill = self.root / ".agents/skills/tact" / relative
                skill.write_text("Existing custom skill content.\n")
                other = self.root / ".agents/skills/another/SKILL.md"
                other.parent.mkdir(parents=True, exist_ok=True)
                other.write_text("Another project's skill.\n")
                before = self.snapshot()
                for command in ("init", "refresh"):
                    for flags in ((), ("--dry-run",)):
                        result = self.run_cli(command, *flags, expected=1)
                        self.assertIn(f".agents/skills/tact/{relative}", result.stderr)
                        self.assertEqual(before, self.snapshot())
                skill.unlink()
                self.run_cli("refresh")
                self.assertEqual(other.read_text(), "Another project's skill.\n")

    def test_refresh_protects_tracked_skill_edits_and_restores_missing_metadata(self):
        self.run_cli("init")
        skill = self.root / ".agents/skills/tact/SKILL.md"
        original = skill.read_bytes()
        skill.write_bytes(original + b"\nOur local edit.\n")
        ui = self.root / ".agents/skills/tact/agents/openai.yaml"
        ui.unlink()
        before = self.snapshot()
        self.assertIn("differs from the recorded installation", self.run_cli("refresh", expected=1).stderr)
        self.assertEqual(before, self.snapshot())
        skill.write_bytes(original)
        self.run_cli("refresh")
        self.assertTrue(ui.is_file())

    def test_skill_refresh_replaces_only_an_unchanged_recorded_version(self):
        self.run_cli("init")
        skill = self.root / ".agents/skills/tact/SKILL.md"
        skill.write_text("Earlier skill instructions.\n")
        manifest_path = self.root / ".tact/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"][".agents/skills/tact/SKILL.md"] = sha256(skill.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        self.run_cli("refresh")
        self.assertEqual(skill.read_bytes(), (SOURCE_ROOT / "skills/tact/SKILL.md").read_bytes())

    def test_skill_links_resolve_to_the_selected_project_from_a_nested_working_directory(self):
        nested = self.root / "src/nested"
        nested.mkdir(parents=True)
        self.run_cli("init", self.root, cwd=nested)
        skill = self.root / ".agents/skills/tact/SKILL.md"
        destinations = re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill.read_text())
        self.assertEqual(
            {(skill.parent / destination).resolve() for destination in destinations},
            {(self.root / relative).resolve() for relative in (
                ".tact/AGENTS.md", ".tact/project/notes.md", ".tact/core/communication.md",
            )},
        )

    def test_interrupted_refresh_preserves_the_old_manifest_and_can_resume(self):
        from tact.cli import main

        self.prepare_older_kit()
        entry = self.root / "AGENTS.md"
        expected_entry = entry.read_bytes()
        entry.write_text(COMPLETE_READING_ENTRY)
        manifest_path = self.root / ".tact/manifest.json"
        previous_manifest = manifest_path.read_bytes()
        real_replace = Path.replace

        def fail_manifest_replace(path, destination):
            if destination.resolve() == manifest_path.resolve():
                raise OSError("simulated storage failure")
            return real_replace(path, destination)

        errors = io.StringIO()
        with mock.patch.object(Path, "replace", fail_manifest_replace), redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(main(["refresh", str(self.root)]), 1)
        self.assertIn("some files may have been created or updated", errors.getvalue())
        self.assertEqual(manifest_path.read_bytes(), previous_manifest)
        self.assertEqual((self.root / ".tact/core/README.md").read_bytes(), (SOURCE_ROOT / "core/README.md").read_bytes())
        self.assertEqual(entry.read_bytes(), expected_entry)
        self.run_cli("refresh")
        self.assertIn("Already initialized", self.run_cli("init").stdout)


if __name__ == "__main__":
    unittest.main()
