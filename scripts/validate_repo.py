#!/usr/bin/env python3
"""Deterministic structural and public-safety checks for this repository."""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


IGNORED_PARTS = {".git", ".pytest_cache", "__pycache__", ".venv"}
ALLOWED_BINARY_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
MAX_BINARY_BYTES = 2 * 1024 * 1024
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
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


def repository_files(root: Path) -> list[Path]:
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


def read_text(path: Path) -> tuple[str | None, str | None]:
    data = path.read_bytes()
    if b"\x00" in data:
        return None, "contains NUL bytes"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "is not UTF-8 text"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, "must start with YAML frontmatter"
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return {}, "frontmatter is not closed with ---"

    values: dict[str, str] = {}
    index = 1
    while index < closing:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith((" ", "\t")):
            index += 1
            continue
        match = FRONTMATTER_KEY_RE.match(line)
        if not match:
            return {}, f"cannot parse frontmatter line {index + 1}"
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        if key in values:
            return {}, f"frontmatter key {key!r} is duplicated"
        if raw_value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block: list[str] = []
            index += 1
            while index < closing and (
                lines[index].startswith((" ", "\t")) or not lines[index].strip()
            ):
                block.append(lines[index].strip())
                index += 1
            separator = " " if raw_value.startswith(">") else "\n"
            values[key] = separator.join(part for part in block if part).strip()
            continue
        if len(raw_value) >= 2 and raw_value[0] == raw_value[-1] and raw_value[0] in "\"'":
            raw_value = raw_value[1:-1]
        values[key] = raw_value
        index += 1
    return values, None


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

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        findings.append(Finding(skill_file, "frontmatter name is required"))
    elif name != skill_dir.name:
        findings.append(Finding(skill_file, "frontmatter name must match the package directory"))
    elif len(name) > 64 or not NAME_RE.fullmatch(name):
        findings.append(Finding(skill_file, "name must be kebab-case and at most 64 characters"))
    if not description:
        findings.append(Finding(skill_file, "frontmatter description is required"))
    elif len(description) > 1024:
        findings.append(Finding(skill_file, "description must be at most 1,024 characters"))

    for markdown_path in sorted(skill_dir.rglob("*.md")):
        markdown, markdown_error = read_text(markdown_path)
        if markdown_error:
            findings.append(Finding(markdown_path, markdown_error))
            continue
        assert markdown is not None
        for target in MARKDOWN_LINK_RE.findall(markdown):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
                continue
            relative_target = unquote(parsed.path)
            if not relative_target:
                continue
            if Path(relative_target).is_absolute():
                findings.append(Finding(markdown_path, f"uses an absolute local link: {target}"))
                continue
            resolved = (markdown_path.parent / relative_target).resolve()
            if not is_within(resolved, skill_dir.resolve()):
                findings.append(Finding(markdown_path, f"link escapes the skill package: {target}"))
            elif not resolved.exists():
                findings.append(Finding(markdown_path, f"local link does not exist: {target}"))

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


def validate_public_safety(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in repository_files(root):
        relative = path.relative_to(root)
        if path.is_symlink():
            findings.append(Finding(path, "symlinks are not allowed in the public payload"))
            continue
        if path.name in SENSITIVE_FILENAMES or path.name.startswith(".env."):
            findings.append(Finding(path, "sensitive filename is not allowed"))
        if stat.S_IMODE(path.stat().st_mode) & 0o111:
            findings.append(Finding(path, "executable files are not allowed"))

        text, error = read_text(path)
        if text is None:
            if path.suffix.lower() not in ALLOWED_BINARY_SUFFIXES:
                findings.append(Finding(path, error or "binary file is not allowed"))
            elif path.stat().st_size > MAX_BINARY_BYTES:
                findings.append(Finding(path, f"binary asset exceeds {MAX_BINARY_BYTES} bytes"))
            continue

        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(Finding(path, f"contains a possible {label}"))
        for label, pattern in LOCAL_PATH_PATTERNS.items():
            if pattern.search(text):
                findings.append(Finding(path, f"contains a possible {label}"))

        if ".." in relative.parts:
            findings.append(Finding(path, "path traversal is not allowed"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--structure-only", action="store_true")
    mode.add_argument("--public-safety-only", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"repository root does not exist: {root}")

    findings: list[Finding] = []
    if not args.public_safety_only:
        findings.extend(validate_structure(root))
    if not args.structure_only:
        findings.extend(validate_public_safety(root))

    if findings:
        for finding in sorted(findings, key=lambda item: item.render(root)):
            print(f"ERROR: {finding.render(root)}", file=sys.stderr)
        print(f"Validation failed with {len(findings)} finding(s).", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
