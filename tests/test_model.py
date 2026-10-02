import json
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest

from contextkit import PackOptions, build_pack


class PackTests(unittest.TestCase):
    def make_repo(self) -> Path:
        directory = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q"], cwd=directory, check=True)
        return directory

    def test_safe_discovery_respects_gitignore_and_sensitive_names(self) -> None:
        root = self.make_repo()
        (root / ".gitignore").write_text("ignored.log\n", encoding="utf-8")
        (root / "main.py").write_text("print('hello')\n", encoding="utf-8")
        (root / "ignored.log").write_text("a noisy log\n", encoding="utf-8")
        (root / ".env").write_text("TOKEN=secret-value\n", encoding="utf-8")
        (root / "image.bin").write_bytes(b"\x00\x01\x02")
        (root / "nested").mkdir()
        (root / "nested" / "notes.md").write_text("notes\n", encoding="utf-8")

        result = build_pack(PackOptions(root))
        included = {record.path for record in result.files}
        skipped = {item["path"]: item["reason"] for item in result.skipped}

        self.assertIn("main.py", included)
        self.assertIn("nested/notes.md", included)
        self.assertNotIn(".env", included)
        self.assertEqual(skipped[".env"], "sensitive filename")
        self.assertEqual(skipped["ignored.log"], "matched .gitignore")
        self.assertEqual(skipped["image.bin"], "binary file")
        self.assertNotIn(".git/config", included)

    def test_secret_values_are_redacted_but_hash_is_stable(self) -> None:
        root = self.make_repo()
        source = "api_key = 'super-secret-value'\nAuthorization: Bearer abcdefghijklmnopqrstuvwxyz\n"
        (root / "config.py").write_text(source, encoding="utf-8")

        result = build_pack(PackOptions(root))
        record = next(record for record in result.files if record.path == "config.py")

        self.assertNotIn("super-secret-value", record.content)
        self.assertNotIn("abcdefghijklmnopqrstuvwxyz", record.content)
        self.assertEqual(record.redactions, 2)
        self.assertEqual(
            record.sha256,
            hashlib.sha256((root / "config.py").read_bytes()).hexdigest(),
        )

    def test_quoted_assignments_with_spaces_are_redacted(self) -> None:
        root = self.make_repo()
        source = (
            'password = "secret value with # marker"\n'
            "token: 'another secret value'\n"
        )
        (root / "settings.ini").write_text(source, encoding="utf-8")

        result = build_pack(PackOptions(root))
        record = next(record for record in result.files if record.path == "settings.ini")

        self.assertEqual(record.redactions, 2)
        self.assertNotIn("secret value", record.content)
        self.assertNotIn("another secret value", record.content)
        self.assertIn('password = "[REDACTED]"', record.content)
        self.assertIn("token: '[REDACTED]'", record.content)

    def test_additional_credential_filenames_are_skipped(self) -> None:
        root = self.make_repo()
        for name in (".netrc", ".npmrc", ".pypirc", "auth.json", "token.json"):
            (root / name).write_text("credential=should not be included\n", encoding="utf-8")

        result = build_pack(PackOptions(root))
        self.assertFalse(result.files)
        self.assertEqual(
            {item["path"] for item in result.skipped},
            {".netrc", ".npmrc", ".pypirc", "auth.json", "token.json"},
        )

    def test_limits_are_reported_and_markdown_handles_backticks(self) -> None:
        root = self.make_repo()
        (root / "large.txt").write_text("x" * 40, encoding="utf-8")
        (root / "code.md").write_text("```python\nprint('x')\n```\n", encoding="utf-8")

        result = build_pack(PackOptions(root, max_file_bytes=30))
        self.assertTrue(any(item["path"] == "large.txt" for item in result.skipped))
        markdown = result.to_markdown()
        self.assertIn("````text", markdown)
        self.assertIn("```python", markdown)

    def test_json_is_deterministic_and_has_schema_version(self) -> None:
        root = self.make_repo()
        (root / ".gitignore").write_text("", encoding="utf-8")
        (root / "b.txt").write_text("b\n", encoding="utf-8")
        (root / "a.txt").write_text("a\n", encoding="utf-8")

        first = build_pack(PackOptions(root)).to_json()
        second = build_pack(PackOptions(root)).to_json()
        self.assertEqual(first, second)
        self.assertEqual(json.loads(first)["schema_version"], 1)
        self.assertEqual(
            [item["path"] for item in json.loads(first)["files"]],
            [".gitignore", "a.txt", "b.txt"],
        )


if __name__ == "__main__":
    unittest.main()
