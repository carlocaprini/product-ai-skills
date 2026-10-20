#!/usr/bin/env python3
"""Deterministic structural and public-safety checks for this repository."""

from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml
from yaml.constructor import ConstructorError


IGNORED_PARTS = {".git", ".pytest_cache", "__pycache__", ".venv"}
ALLOWED_BINARY_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
MAX_BINARY_BYTES = 2 * 1024 * 1024
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
MARKDOWN_REFERENCE_DEFINITION_RE = re.compile(
    r"^[ ]{0,3}\[([^\]\n]+)\]:[ \t]*(?:<([^>\n]+)>|(\S+))", re.MULTILINE
)
MARKDOWN_REFERENCE_LINK_RE = re.compile(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]")
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
STRING_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "allowed-tools",
}

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,255}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
LOCAL_PATH_PATTERNS = {
    "macOS user path": re.compile(r"(?<![A-Za-z0-9_])/Users/[A-Za-z0-9._-]+/"),
    "Linux user path": re.compile(r"(?<![A-Za-z0-9_])/home/[A-Za-z0-9._-]+/"),
    "Windows user path": re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+\\"),
}
SENSITIVE_FILENAMES = {
    ".env",
    ".env.local",
    "credentials.json",
    "id_dsa",
    "id_ed25519",
    "id_rsa",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str

    def render(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root)
        except ValueError:
            display = self.path
        return f"{display}: {self.message}"


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def run_git(root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_repository_files(root: Path) -> list[Path] | None:
    try:
        top_level = run_git(root, "rev-parse", "--show-toplevel").stdout.decode().strip()
        if Path(top_level).resolve() != root.resolve():
            return None
        output = run_git(
            root, "ls-files", "--cached", "--others", "--exclude-standard", "-z"
        ).stdout
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        return None

    paths: list[Path] = []
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        try:
            relative = Path(raw_path.decode("utf-8"))
        except UnicodeDecodeError:
            continue
        path = root / relative
        if path.exists() or path.is_symlink():
            paths.append(path)
    return sorted(set(paths))


def repository_files(root: Path) -> list[Path]:
    tracked_and_untracked = git_repository_files(root)
    if tracked_and_untracked is not None:
        return tracked_and_untracked

    files: list[Path] = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        visible_directories: list[str] = []
        for name in sorted(directories):
            if name in IGNORED_PARTS:
                continue
            path = current_path / name
            if path.is_symlink():
                files.append(path)
            else:
                visible_directories.append(name)
        directories[:] = visible_directories
        for name in sorted(filenames):
            path = current_path / name
            if not any(part in IGNORED_PARTS for part in path.relative_to(root).parts):
                files.append(path)
    return files


def decode_text(data: bytes) -> tuple[str | None, str | None]:
    if b"\x00" in data:
        return None, "contains NUL bytes"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "is not UTF-8 text"


def read_text(path: Path) -> tuple[str | None, str | None]:
    return decode_text(path.read_bytes())


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str | None]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, "must start with YAML frontmatter"
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return {}, "frontmatter is not closed with ---"

    source = "\n".join(lines[1:closing])
    try:
        values = yaml.load(source, Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        problem = getattr(error, "problem", None) or "invalid YAML"
        return {}, f"cannot parse frontmatter: {problem}"
    if values is None:
        values = {}
    if not isinstance(values, dict):
        return {}, "frontmatter must be a YAML mapping"
    if any(not isinstance(key, str) for key in values):
        return {}, "frontmatter keys must be strings"
    return values, None


def normalize_reference_label(label: str) -> str:
    return " ".join(label.split()).casefold()


def validate_local_link(markdown_path: Path, skill_dir: Path, target: str) -> Finding | None:
    target = target.strip().split(maxsplit=1)[0].strip("<>")
    parsed = urlsplit(target)
    if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
        return None
    relative_target = unquote(parsed.path)
    if not relative_target:
        return None
    if Path(relative_target).is_absolute():
        return Finding(markdown_path, f"uses an absolute local link: {target}")
    resolved = (markdown_path.parent / relative_target).resolve()
    if not is_within(resolved, skill_dir.resolve()):
        return Finding(markdown_path, f"link escapes the skill package: {target}")
    if not resolved.exists():
        return Finding(markdown_path, f"local link does not exist: {target}")
    return None


def validate_markdown_links(markdown_path: Path, skill_dir: Path, markdown: str) -> list[Finding]:
    findings: list[Finding] = []
    for target in MARKDOWN_LINK_RE.findall(markdown):
        finding = validate_local_link(markdown_path, skill_dir, target)
        if finding:
            findings.append(finding)

    definitions: dict[str, str] = {}
    for match in MARKDOWN_REFERENCE_DEFINITION_RE.finditer(markdown):
        label = normalize_reference_label(match.group(1))
        target = match.group(2) or match.group(3)
        definitions[label] = target
        finding = validate_local_link(markdown_path, skill_dir, target)
        if finding:
            findings.append(finding)

    for match in MARKDOWN_REFERENCE_LINK_RE.finditer(markdown):
        label = normalize_reference_label(match.group(2) or match.group(1))
        if label not in definitions:
            findings.append(
                Finding(markdown_path, f"reference-style link has no definition: {label}")
            )
    return findings


def validate_skill_package(skill_dir: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [Finding(skill_dir, "skill package is missing SKILL.md")]

    text, error = read_text(skill_file)
    if error:
        return [Finding(skill_file, error)]
    assert text is not None
    frontmatter, error = parse_frontmatter(text)
    if error:
        findings.append(Finding(skill_file, error))
        return findings

    unknown = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
    if unknown:
        findings.append(
            Finding(skill_file, f"uses unsupported top-level frontmatter keys: {', '.join(unknown)}")
        )

    for key in sorted(STRING_FRONTMATTER_KEYS):
        if key in frontmatter and not isinstance(frontmatter[key], str):
            findings.append(Finding(skill_file, f"frontmatter {key} must be a string"))
    if "metadata" in frontmatter:
        metadata = frontmatter["metadata"]
        if not isinstance(metadata, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        ):
            findings.append(
                Finding(skill_file, "frontmatter metadata must map strings to strings")
            )

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if name is None:
        findings.append(Finding(skill_file, "frontmatter name is required"))
    elif isinstance(name, str):
        if not name.strip():
            findings.append(Finding(skill_file, "frontmatter name is required"))
        elif name != skill_dir.name:
            findings.append(Finding(skill_file, "frontmatter name must match the package directory"))
        elif len(name) > 64 or not NAME_RE.fullmatch(name):
            findings.append(Finding(skill_file, "name must be kebab-case and at most 64 characters"))
    if description is None:
        findings.append(Finding(skill_file, "frontmatter description is required"))
    elif isinstance(description, str):
        if not description.strip():
            findings.append(Finding(skill_file, "frontmatter description is required"))
        elif len(description) > 1024:
            findings.append(Finding(skill_file, "description must be at most 1,024 characters"))

    for markdown_path in sorted(skill_dir.rglob("*.md")):
        markdown, markdown_error = read_text(markdown_path)
        if markdown_error:
            findings.append(Finding(markdown_path, markdown_error))
            continue
        assert markdown is not None
        findings.extend(validate_markdown_links(markdown_path, skill_dir, markdown))

    return findings


def validate_structure(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skills_dir = root / "skills"
    if not skills_dir.exists():
        return findings
    if not skills_dir.is_dir():
        return [Finding(skills_dir, "skills must be a directory")]

    for child in sorted(skills_dir.iterdir()):
        if child.is_symlink():
            findings.append(Finding(child, "skill packages cannot be symlinks"))
        elif not child.is_dir():
            findings.append(Finding(child, "only skill package directories are allowed under skills"))
        else:
            findings.extend(validate_skill_package(child, root))
    return findings


def validate_payload(
    display_path: Path,
    relative: Path,
    data: bytes,
    *,
    executable: bool = False,
    symlink: bool = False,
) -> list[Finding]:
    findings: list[Finding] = []
    if symlink:
        return [Finding(display_path, "symlinks are not allowed in the public payload")]
    if relative.name in SENSITIVE_FILENAMES or relative.name.startswith(".env."):
        findings.append(Finding(display_path, "sensitive filename is not allowed"))
    if executable:
        findings.append(Finding(display_path, "executable files are not allowed"))

    text, error = decode_text(data)
    if text is None:
        if relative.suffix.lower() not in ALLOWED_BINARY_SUFFIXES:
            findings.append(Finding(display_path, error or "binary file is not allowed"))
        elif len(data) > MAX_BINARY_BYTES:
            findings.append(Finding(display_path, f"binary asset exceeds {MAX_BINARY_BYTES} bytes"))
        return findings

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding(display_path, f"contains a possible {label}"))
    for label, pattern in LOCAL_PATH_PATTERNS.items():
        if pattern.search(text):
            findings.append(Finding(display_path, f"contains a possible {label}"))
    return findings


def validate_public_safety(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in repository_files(root):
        relative = path.relative_to(root)
        if ".." in relative.parts:
            findings.append(Finding(path, "path traversal is not allowed"))
            continue
        if path.is_symlink():
            findings.extend(validate_payload(path, relative, b"", symlink=True))
            continue
        findings.extend(
            validate_payload(
                path,
                relative,
                path.read_bytes(),
                executable=bool(stat.S_IMODE(path.stat().st_mode) & 0o111),
            )
        )
    return findings


def validate_history(root: Path, revision_range: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        commits = run_git(root, "rev-list", "--reverse", revision_range).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        return [Finding(root, f"cannot read Git revision range: {revision_range}")]

    for raw_commit in commits:
        commit = raw_commit.decode("ascii")
        short_commit = commit[:12]
        try:
            changed_paths = {
                path
                for path in run_git(
                    root,
                    "diff-tree",
                    "--root",
                    "--no-commit-id",
                    "--name-only",
                    "--diff-filter=ACMRTUXB",
                    "-r",
                    "-m",
                    "-z",
                    commit,
                ).stdout.split(b"\0")
                if path
            }
            entries = run_git(root, "ls-tree", "-r", "-z", commit).stdout.split(b"\0")
        except (OSError, subprocess.CalledProcessError):
            findings.append(Finding(root, f"cannot inspect Git commit: {short_commit}"))
            continue
        for entry in entries:
            if not entry:
                continue
            metadata, raw_path = entry.split(b"\t", 1)
            if raw_path not in changed_paths:
                continue
            mode, object_type, object_id = metadata.split(b" ", 2)
            if object_type != b"blob":
                continue
            try:
                relative = Path(raw_path.decode("utf-8"))
                data = run_git(root, "cat-file", "blob", object_id.decode("ascii")).stdout
            except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
                findings.append(
                    Finding(root / ".history" / short_commit, "cannot inspect a Git object")
                )
                continue
            display_path = root / ".history" / short_commit / relative
            findings.extend(
                validate_payload(
                    display_path,
                    relative,
                    data,
                    executable=mode == b"100755",
                    symlink=mode == b"120000",
                )
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--structure-only", action="store_true")
    mode.add_argument("--public-safety-only", action="store_true")
    parser.add_argument(
        "--history-range",
        help="also scan every commit tree in this Git revision range for public-safety issues",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"repository root does not exist: {root}")

    findings: list[Finding] = []
    if not args.public_safety_only:
        findings.extend(validate_structure(root))
    if not args.structure_only:
        findings.extend(validate_public_safety(root))
        if args.history_range:
            findings.extend(validate_history(root, args.history_range))

    if findings:
        for finding in sorted(findings, key=lambda item: item.render(root)):
            print(f"ERROR: {finding.render(root)}", file=sys.stderr)
        print(f"Validation failed with {len(findings)} finding(s).", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
