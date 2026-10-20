from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_PATH = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_PATH))
import validate_repo  # noqa: E402


class ValidationTests(unittest.TestCase):
    def make_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        return temporary, root

    def git(self, root: Path, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()

    def initialize_git_repository(self, root: Path) -> None:
        self.git(root, "init", "--quiet")
        self.git(root, "config", "user.name", "Validation Tests")
        self.git(root, "config", "user.email", "validation@example.invalid")

    def write_skill(self, root: Path, name: str = "example-skill", body: str = "") -> Path:
        skill_dir = root / "skills" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            "description: Helps with a focused task when a concrete review is requested.\n"
            "---\n\n"
            "# Example Skill\n\n"
            f"{body}",
            encoding="utf-8",
        )
        return skill_dir

    def test_repository_without_published_skills_is_valid(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(validate_repo.validate_structure(root), [])

    def test_valid_standalone_package_passes(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        skill_dir = self.write_skill(root, body="Read [criteria](references/criteria.md).\n")
        references = skill_dir / "references"
        references.mkdir()
        (references / "criteria.md").write_text("# Criteria\n", encoding="utf-8")
        self.assertEqual(validate_repo.validate_structure(root), [])

    def test_name_must_match_directory(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        skill_dir = self.write_skill(root)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "name: example-skill", "name: different-name"
            ),
            encoding="utf-8",
        )
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("must match" in finding.message for finding in findings))

    def test_yaml_inline_comment_is_supported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        skill_dir = self.write_skill(root)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "name: example-skill", "name: example-skill # Package name"
            ),
            encoding="utf-8",
        )
        self.assertEqual(validate_repo.validate_structure(root), [])

    def test_null_description_is_rejected(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        skill_dir = self.write_skill(root)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "description: Helps with a focused task when a concrete review is requested.",
                "description: null",
            ),
            encoding="utf-8",
        )
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("description must be a string" in finding.message for finding in findings))

    def test_invalid_yaml_is_rejected(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        skill_dir = self.write_skill(root)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "description: Helps with a focused task when a concrete review is requested.",
                'description: "unterminated',
            ),
            encoding="utf-8",
        )
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("cannot parse frontmatter" in finding.message for finding in findings))

    def test_package_link_cannot_escape(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.write_skill(root, body="Read [outside](../../private.md).\n")
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("escapes" in finding.message for finding in findings))

    def test_missing_local_link_is_reported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.write_skill(root, body="Read [missing](references/missing.md).\n")
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("does not exist" in finding.message for finding in findings))

    def test_reference_style_link_cannot_escape(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.write_skill(
            root,
            body="Read [criteria][criteria].\n\n[criteria]: ../../outside.md\n",
        )
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("escapes" in finding.message for finding in findings))

    def test_missing_reference_definition_is_reported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.write_skill(root, body="Read [criteria][criteria].\n")
        findings = validate_repo.validate_structure(root)
        self.assertTrue(any("has no definition" in finding.message for finding in findings))

    def test_secret_like_value_is_reported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        (root / "notes.md").write_text(
            "token: " + "ghp_" + ("a" * 40) + "\n", encoding="utf-8"
        )
        findings = validate_repo.validate_public_safety(root)
        self.assertTrue(any("GitHub token" in finding.message for finding in findings))

    def test_local_user_path_is_reported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        (root / "notes.md").write_text(
            "Open /" + "Users/example/private/file.md\n", encoding="utf-8"
        )
        findings = validate_repo.validate_public_safety(root)
        self.assertTrue(any("macOS user path" in finding.message for finding in findings))

    def test_symlinked_directory_is_reported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        target = root / "target"
        target.mkdir()
        try:
            os.symlink(target, root / "linked-directory")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not available in this environment")
        findings = validate_repo.validate_public_safety(root)
        self.assertTrue(any("symlinks are not allowed" in finding.message for finding in findings))

    def test_forced_tracked_file_in_ignored_directory_is_reported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.initialize_git_repository(root)
        (root / ".gitignore").write_text(".venv/\n", encoding="utf-8")
        sensitive = root / ".venv" / ".env"
        sensitive.parent.mkdir()
        sensitive.write_text("placeholder=true\n", encoding="utf-8")
        self.git(root, "add", ".gitignore")
        self.git(root, "add", "--force", ".venv/.env")

        findings = validate_repo.validate_public_safety(root)
        self.assertTrue(any("sensitive filename" in finding.message for finding in findings))

    def test_history_reports_secret_added_then_deleted(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.initialize_git_repository(root)
        (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
        self.git(root, "add", "README.md")
        self.git(root, "commit", "--quiet", "-m", "Base")
        base = self.git(root, "rev-parse", "HEAD")

        transient = root / "transient.txt"
        transient.write_text("token=" + "ghp_" + ("a" * 40) + "\n", encoding="utf-8")
        self.git(root, "add", "transient.txt")
        self.git(root, "commit", "--quiet", "-m", "Add transient value")
        transient.unlink()
        self.git(root, "add", "--update")
        self.git(root, "commit", "--quiet", "-m", "Remove transient value")

        findings = validate_repo.validate_history(root, f"{base}..HEAD")
        self.assertTrue(any("GitHub token" in finding.message for finding in findings))


if __name__ == "__main__":
    unittest.main()
