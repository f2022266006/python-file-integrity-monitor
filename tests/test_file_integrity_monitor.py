import tempfile
import unittest
from pathlib import Path

from file_integrity_monitor import compare_snapshots, sha256_file


class FileIntegrityMonitorTests(unittest.TestCase):
    def test_hash_is_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "sample.txt"
            sample.write_text("hello", encoding="utf-8")
            self.assertEqual(sha256_file(sample), sha256_file(sample))

    def test_hash_changes_when_content_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "sample.txt"
            sample.write_text("before", encoding="utf-8")
            before = sha256_file(sample)
            sample.write_text("after", encoding="utf-8")
            self.assertNotEqual(before, sha256_file(sample))

    def test_compare_detects_all_change_types(self):
        old = {
            "modified.txt": {"sha256": "old"},
            "deleted.txt": {"sha256": "same"},
            "unchanged.txt": {"sha256": "same"},
        }
        new = {
            "modified.txt": {"sha256": "new"},
            "added.txt": {"sha256": "same"},
            "unchanged.txt": {"sha256": "same"},
        }
        changes = compare_snapshots(old, new)
        self.assertEqual(changes["modified"], ["modified.txt"])
        self.assertEqual(changes["deleted"], ["deleted.txt"])
        self.assertEqual(changes["added"], ["added.txt"])

    def test_compare_reports_no_changes(self):
        snapshot = {"file.txt": {"sha256": "abc"}}
        self.assertEqual(
            compare_snapshots(snapshot, snapshot),
            {"added": [], "deleted": [], "modified": []},
        )


if __name__ == "__main__":
    unittest.main()
