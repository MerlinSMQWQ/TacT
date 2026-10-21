"""Install a versioned Kit snapshot without replacing project-owned guidance."""

import argparse
from dataclasses import dataclass
from difflib import unified_diff
from hashlib import sha256
from importlib import metadata, resources
import json
from pathlib import Path
import sys
import tempfile


PACKAGE = "tact-agent-kit"
SOURCE = "https://github.com/MerlinSMQWQ/TacT"
BEGIN = "<!-- tact:begin -->"
END = "<!-- tact:end -->"
ENTRY = f"""{BEGIN}
## TacT Agent Kit

Before substantive work, read the [TacT entry](.tact/AGENTS.md) and
[project notes](.tact/project/notes.md). Follow the entry's topic-reading triggers
and check matching project supplements.

The Kit root is `.tact/` in this repository. Resolve paths inside the Kit from
that directory, even when working in a subdirectory. Keep the existing repository
instructions in force. Resolve conflicts using the host's instruction hierarchy;
ask about consequential unresolved conflicts before taking dependent actions.
{END}
"""


class InitError(Exception):
    """A Kit operation cannot proceed safely."""


@dataclass
class Change:
    path: Path
    before: bytes | None
    after: bytes
    append: bool = False

    @property
    def action(self) -> str:
        if self.before is None:
            return "CREATE"
        return "APPEND" if self.append else "UPDATE"


def read_target(root: Path, relative: str) -> bytes | None:
    """Reject links and non-files before planning writes inside the target."""
    path = root
    parts = Path(relative).parts
    for index, part in enumerate(parts):
        path /= part
        if path.is_symlink():
            raise InitError(f"{relative}: symbolic links are not supported.")
        if path.exists():
            if index < len(parts) - 1 and not path.is_dir():
                raise InitError(f"{path}: expected a directory.")
            if index == len(parts) - 1:
                if not path.is_file():
                    raise InitError(f"{relative}: expected a regular file.")
                return path.read_bytes()
    return None


def show_diff(relative: str, before: bytes | None, after: bytes) -> str:
    lines = list(unified_diff(
        (before or b"").decode("utf-8", errors="replace").splitlines(),
        after.decode("utf-8", errors="replace").splitlines(),
        fromfile=f"{relative} (current)",
        tofile=f"{relative} (proposed)",
        lineterm="",
    ))
    if not lines and before != after:
        return f"{relative}: file bytes differ (such as line endings or the final newline)."
    if len(lines) > 60:
        lines = lines[:60] + ["... diff truncated after 60 lines"]
    return "\n".join(lines)


def entry_content(before: bytes | None) -> bytes:
    if before is None:
        return ENTRY.encode("utf-8")
    try:
        text = before.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InitError("AGENTS.md must be UTF-8.") from error
    normalized = text.replace("\r\n", "\n")
    if BEGIN in normalized or END in normalized:
        if normalized.count(BEGIN) != 1 or normalized.count(END) != 1:
            raise InitError("AGENTS.md has incomplete or duplicate TacT markers.")
        start, end = normalized.index(BEGIN), normalized.index(END) + len(END)
        if normalized[start:end] != ENTRY.rstrip("\n"):
            raise InitError(
                "The TacT block in AGENTS.md differs from this version. "
                "Review it before installing or updating.\n"
                + show_diff("AGENTS.md (TacT block)", normalized[start:end].encode(), ENTRY.encode())
            )
        return before
    newline = b"\r\n" if b"\r\n" in before else b"\n"
    separator = b""
    if before:
        separator = newline if before.endswith(newline) else newline * 2
        if before.endswith(newline * 2):
            separator = b""
    return before + separator + ENTRY.encode().replace(b"\n", newline)


def notes_content(version: str, *, introduction: bool = True) -> bytes:
    text = "# Project notes\n\n"
    if introduction:
        text += (
            "This file intentionally starts nearly empty so it does not inherit another project's constraints. "
            "The project maintainer and agents working within their authorization maintain it as useful "
            "guidance emerges: record confirmed constraints and working agreements, and label observations "
            "or proposals separately. Existing project instructions still apply; see "
            "[the project guide](README.md) for details.\n\n"
        )
    return (text +
        f"TacT source: [{SOURCE}]({SOURCE}), package `{PACKAGE}` version `{version}`. "
        "The installed shared-file hashes are recorded in `../manifest.json`.\n"
    ).encode()


def bundled_files() -> tuple[dict[str, bytes], dict[str, bytes]]:
    kit = resources.files("tact_resources")
    shared = {
        ".tact/AGENTS.md": kit.joinpath("AGENTS.md").read_bytes(),
        ".tact/LICENSE": kit.joinpath("LICENSE").read_bytes(),
        ".agents/skills/tact/SKILL.md": kit.joinpath("skills/tact/SKILL.md").read_bytes(),
        ".agents/skills/tact/agents/openai.yaml": kit.joinpath("skills/tact/agents/openai.yaml").read_bytes(),
    }
    for resource in sorted(kit.joinpath("core").iterdir(), key=lambda item: item.name):
        if resource.is_file() and resource.name.endswith(".md"):
            shared[f".tact/core/{resource.name}"] = resource.read_bytes()

    version = metadata.version(PACKAGE)
    manifest = {
        "schema_version": 1,
        "package": PACKAGE,
        "version": version,
        "source": SOURCE,
        "files": {name: sha256(content).hexdigest() for name, content in sorted(shared.items())},
    }
    shared[".tact/manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    project = {
        ".tact/project/README.md": kit.joinpath("project/README.md").read_bytes(),
        ".tact/project/notes.md": notes_content(version),
    }
    return shared, project


def installed_manifest(root: Path, shared: dict[str, bytes]) -> dict:
    raw = read_target(root, ".tact/manifest.json")
    if raw is None:
        raise InitError("No .tact/manifest.json found. Use 'tact init' for a new installation; restore the original manifest for an existing Kit.")
    try:
        manifest = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as error:
        raise InitError("Invalid .tact/manifest.json. Restore the installation record before updating.") from error
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_version") != 1
        or manifest.get("package") != PACKAGE
        or manifest.get("source") != SOURCE
        or not isinstance(manifest.get("version"), str)
        or not manifest["version"]
        or not isinstance(manifest.get("files"), dict)
        or ".tact/AGENTS.md" not in manifest["files"]
    ):
        raise InitError("Unsupported .tact/manifest.json. Restore a valid TacT installation record before updating.")
    for relative, digest in manifest["files"].items():
        if relative not in shared or relative == ".tact/manifest.json":
            raise InitError(f"The installed manifest lists a file absent from this package: {relative}. Automatic removal is not supported; review the installation record.")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise InitError(f"Invalid recorded hash for {relative}. Restore the original manifest before updating.")
    return manifest


def plan_changes(root: Path, *, update: bool = False) -> list[Change]:
    override = read_target(root, "AGENTS.override.md")
    if override and override.strip():
        raise InitError(
            "AGENTS.override.md would take precedence over AGENTS.md in Codex. "
            "Reconcile that entry before installing or updating."
        )

    shared, project = bundled_files()
    previous = installed_manifest(root, shared) if update else None

    changes = []
    conflicts = []
    for relative, content in shared.items():
        if relative == ".tact/manifest.json":
            continue
        before = read_target(root, relative)
        if before == content:
            continue
        if before is None or (
            previous is not None
            and sha256(before).hexdigest() == previous["files"].get(relative)
        ):
            changes.append(Change(root / relative, before, content))
        else:
            reason = ""
            if update:
                reason = f"{relative}: differs from the recorded installation or is not tracked.\n"
            conflicts.append(reason + show_diff(relative, before, content))
    for relative, content in project.items():
        before = read_target(root, relative)
        if before == content:
            continue
        # Migrate only known, byte-for-byte untouched notes templates. Any
        # project edits remain owned by the project, even its old source line.
        untouched_notes = (
            previous is not None
            and relative == ".tact/project/notes.md"
            and before in (
                notes_content(previous["version"]),
                notes_content(previous["version"], introduction=False),
            )
        )
        if before is None or untouched_notes:
            changes.append(Change(root / relative, before, content))

    before = read_target(root, "AGENTS.md")
    after = entry_content(before)
    if before != after:
        changes.append(Change(root / "AGENTS.md", before, after, append=True))

    relative = ".tact/manifest.json"
    before = read_target(root, relative)
    after = shared[relative]
    if before != after:
        if before is None or update:
            # Commit the new baseline last. An interrupted update can resume:
            # files already equal to the new package are also safe to retain.
            changes.append(Change(root / relative, before, after))
        else:
            conflicts.append(show_diff(relative, before, after))
    if conflicts:
        message = (
            "Some shared files have local changes or no recorded baseline. "
            "Keep those changes for review; refresh will not overwrite them."
            if update else
            "Existing TacT shared files or version metadata differ from this package. "
            "init does not upgrade or overwrite a Kit. From the target project, run "
            "'tact refresh --dry-run' to preview document changes from the installed package."
        )
        raise InitError(message + "\n\n" + "\n\n".join(conflicts))
    return changes


def apply_changes(root: Path, changes: list[Change]) -> None:
    for change in changes:
        relative = change.path.relative_to(root).as_posix()
        # Recheck before writing so a changed file is not knowingly overwritten.
        if read_target(root, relative) != change.before:
            raise InitError(f"{relative} changed during writing. Inspect the reported files before retrying.")
        change.path.parent.mkdir(parents=True, exist_ok=True)
        if change.before is None:
            with change.path.open("xb") as stream:
                stream.write(change.after)
        elif change.append:
            with change.path.open("ab") as stream:
                stream.write(change.after[len(change.before):])
        else:
            # Replace each shared file atomically, so a failed write cannot
            # truncate its previous contents. The manifest is replaced last.
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=change.path.parent, delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(change.after)
                temporary.chmod(change.path.stat().st_mode & 0o7777)
                temporary.replace(change.path)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
        print(f"{change.action} {relative}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tact", description="Initialize or refresh a project's TacT documents from the installed package.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {metadata.version(PACKAGE)}")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("init", "Add the bundled Kit and TacT skill without replacing project guidance."),
        ("refresh", "Refresh project documents from the installed TacT package, preserving custom project guidance."),
    ):
        command = commands.add_parser(name, help=help_text, description=help_text)
        command.add_argument("path", nargs="?", default=".", help="Existing project directory (default: current directory).")
        command.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    args = parser.parse_args(argv)
    writing = False
    try:
        root = Path(args.path).expanduser().resolve()
        if not root.is_dir():
            raise InitError(f"{root}: target must be an existing directory.")
        changes = plan_changes(root, update=args.command == "refresh")
        print(f"TacT documents from package {metadata.version(PACKAGE)} in {root}")
        if not changes:
            print("Already up to date; no files changed." if args.command == "refresh" else "Already initialized; no files changed.")
        elif args.dry_run:
            for change in changes:
                relative = change.path.relative_to(root).as_posix()
                print(f"WOULD {change.action} {relative}")
                if args.command == "refresh" or relative == "AGENTS.md":
                    print(show_diff(relative, change.before, change.after))
            print("Dry run complete; no files changed.")
        else:
            writing = True
            apply_changes(root, changes)
            action = "Refreshed" if args.command == "refresh" else "Initialized"
            print(f"{action}. Review AGENTS.md, .tact/, and .agents/skills/tact/ before committing them.")
        return 0
    except (InitError, OSError) as error:
        print(f"tact: {error}", file=sys.stderr)
        if writing:
            print("Stopped during writing; some files may have been created or updated. Inspect the target before retrying.", file=sys.stderr)
        else:
            print("No files changed.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
