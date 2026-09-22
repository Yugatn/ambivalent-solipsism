import json
import tempfile
import unittest
from pathlib import Path
from threading import Thread

from transactional_reference import ReferenceTransaction, RequestReservationLedger


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

    def test_request_reservation_reaches_completed(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = RequestReservationLedger(str(Path(d) / "requests.json"))
            fingerprint = "fp-1"

            self.assertEqual(ledger.reserve(fingerprint, "req-1"), "reserved")
            self.assertEqual(ledger.begin_execution(fingerprint), "executing")
            self.assertEqual(ledger.complete(fingerprint), "completed")
            self.assertEqual(ledger.status(fingerprint), "completed")
            self.assertEqual(ledger.reserve(fingerprint, "req-1"), "completed")

    def test_executing_reservation_blocks_replay_after_restart(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "requests.json"
            first = RequestReservationLedger(str(path))
            self.assertEqual(first.reserve("fp-crash", "req-crash"), "reserved")
            self.assertEqual(first.begin_execution("fp-crash"), "executing")

            restarted = RequestReservationLedger(str(path))
            self.assertEqual(restarted.status("fp-crash"), "executing")
            self.assertEqual(restarted.reserve("fp-crash", "req-crash"), "executing")

    def test_concurrent_reservation_has_one_owner(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = RequestReservationLedger(str(Path(d) / "requests.json"))
            results = []

            def worker():
                results.append(ledger.reserve("fp-concurrent", "req"))

            threads = [Thread(target=worker) for _ in range(8)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.assertEqual(len(results), 8)
            self.assertEqual(results.count("reserved"), 1)
            self.assertEqual(results.count("reserved"), 1)

    def test_interrupted_request_requires_explicit_outcome(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = RequestReservationLedger(str(Path(d) / "requests.json"))
            fingerprint = "fp-recovery"
            ledger.reserve(fingerprint, "req-recovery")
            ledger.begin_execution(fingerprint)

            with self.assertRaises(ValueError):
                ledger.resolve_executing(fingerprint, "unknown")

            self.assertEqual(
                ledger.resolve_executing(fingerprint, RequestReservationLedger.COMPLETED),
                "completed",
            )
            self.assertEqual(ledger.status(fingerprint), "completed")

    def test_failed_recovery_is_terminal_and_not_reexecuted(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = RequestReservationLedger(str(Path(d) / "requests.json"))
            fingerprint = "fp-failed"
            ledger.reserve(fingerprint, "req-failed")
            ledger.begin_execution(fingerprint)

            self.assertEqual(
                ledger.resolve_executing(fingerprint, RequestReservationLedger.FAILED),
                "failed",
            )
            self.assertEqual(ledger.status(fingerprint), "failed")
            self.assertEqual(ledger.reserve(fingerprint, "req-failed"), "failed")


if __name__ == "__main__":
    unittest.main()
