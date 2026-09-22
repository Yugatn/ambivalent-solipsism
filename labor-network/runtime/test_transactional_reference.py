import json
import tempfile
import unittest
from pathlib import Path
from threading import Thread

from transactional_reference import ReferenceTransaction


class TransactionalReferenceTests(unittest.TestCase):
    def test_claim_is_atomic_for_shared_process_callers(self):
        with tempfile.TemporaryDirectory() as d:
            tx = ReferenceTransaction(str(Path(d) / "state.json"))
            results = []

            def worker():
                with tx:
                    results.append(tx.claim("request:fingerprint-1", "accepted"))

            threads = [Thread(target=worker) for _ in range(8)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.assertEqual(sum(results), 1)
            self.assertEqual(len(tx.load()), 1)

    def test_atomic_replacement_preserves_complete_json(self):
        with tempfile.TemporaryDirectory() as d:
            tx = ReferenceTransaction(str(Path(d) / "state.json"))
            with tx:
                tx.append({"kind": "event", "event_id": "e1"})
            self.assertEqual(tx.load(), [{"event_id": "e1", "kind": "event"}])

    def test_recovery_completes_interrupted_commit_from_journal(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "state.json"
            journal = path.with_suffix(path.suffix + ".journal")
            records = [{"kind": "event", "event_id": "e-recover"}]
            journal.write_text(
                json.dumps({"target": str(path), "records": records}),
                encoding="utf-8",
            )

            tx = ReferenceTransaction(str(path))
            with tx:
                pass

            self.assertEqual(tx.load(), records)
            self.assertFalse(journal.exists())

    def test_invalid_journal_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "state.json"
            journal = path.with_suffix(path.suffix + ".journal")
            journal.write_text('{"records": "invalid"}', encoding="utf-8")

            tx = ReferenceTransaction(str(path))
            with self.assertRaises(ValueError):
                with tx:
                    pass


if __name__ == "__main__":
    unittest.main()
