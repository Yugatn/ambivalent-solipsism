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


if __name__ == "__main__":
    unittest.main()
