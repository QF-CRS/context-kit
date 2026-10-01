import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from contextkit.cli import main


class CliTests(unittest.TestCase):
    def test_pack_json_and_inspect_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")

            json_output = StringIO()
            with redirect_stdout(json_output):
                self.assertEqual(
                    main(["pack", str(root), "--format", "json"]),
                    0,
                )
            self.assertEqual(json.loads(json_output.getvalue())["summary"]["included_files"], 1)

            inspect_output = StringIO()
            with redirect_stdout(inspect_output):
                self.assertEqual(main(["inspect", str(root)]), 0)
            self.assertIn("README.md", inspect_output.getvalue())


if __name__ == "__main__":
    unittest.main()
