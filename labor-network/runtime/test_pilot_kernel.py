"""Executable acceptance tests for the Phase 11 critical pilot kernel."""
import unittest

from pilot_kernel import Event, PilotKernel, ActionState, ReviewState, UnknownState


class PilotKernelTests(unittest.TestCase):
    def test_duplicate_event_has_no_second_effect(self):
        k = PilotKernel()
        e = Event("e1", "engagement.created")
        self.assertTrue(k.record_event(e))
        self.assertFalse(k.record_event(e))
        self.assertEqual(len(k.history), 1)

    def test_unknown_blocks_decision(self):
        k = PilotKernel()
        with self.assertRaises(ValueError):
            k.decide(permitted=True)
        self.assertEqual(k.unknown, UnknownState.UNKNOWN)

    def test_high_impact_review_blocks_decision_until_completed(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.require_review()
        with self.assertRaises(ValueError):
            k.decide(permitted=True)
        self.assertEqual(k.review, ReviewState.REQUIRED)
        k.complete_review()
        k.decide(permitted=True)
        self.assertTrue(k.decision_permitted)

    def test_decision_and_action_are_separate(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=True)
        self.assertEqual(k.action, ActionState.NOT_STARTED)
        self.assertTrue(k.execute())
        self.assertEqual(k.action, ActionState.EXECUTED)
        self.assertFalse(k.execute())

    def test_unauthorized_action_cannot_execute(self):
        k = PilotKernel()
        k.resolve_evidence()
        with self.assertRaises(ValueError):
            k.execute()

    def test_technical_data_does_not_create_action_authority(self):
        k = PilotKernel()
        self.assertFalse(k.has_authority("execute_protected_action"))

    def test_correction_preserves_original_history(self):
        k = PilotKernel()
        e = Event("e1", "engagement.created")
        k.record_event(e)
        k.correct("e1")
        self.assertEqual(len(k.history), 1)
        self.assertEqual(k.history[0].event_id, "e1")
        self.assertEqual(k.corrections, ["e1"])

    def test_recovery_blocks_duplicate_execution(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=True)
        k.begin_recovery()
        with self.assertRaises(ValueError):
            k.execute()
        k.complete_recovery()
        self.assertTrue(k.execute())

    def test_terminal_state_is_reconstructable(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=True)
        k.execute()
        reconstructed = k.reconstruct()
        self.assertEqual(reconstructed["action"], "executed")
        self.assertEqual(reconstructed["events"], "0")

    def test_denied_decision_cannot_execute(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=False)
        with self.assertRaises(ValueError):
            k.execute()


if __name__ == "__main__":
    unittest.main()


class ConformanceTraceTests(unittest.TestCase):
    """Map executable outcomes to Critical Kernel obligations K01-K10."""

    def test_k01_authorization_guard(self):
        k = PilotKernel()
        with self.assertRaises(ValueError):
            k.execute()

    def test_k02_decision_action_separation(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=True)
        self.assertEqual(k.action, ActionState.NOT_STARTED)

    def test_k03_event_idempotency(self):
        k = PilotKernel()
        e = Event("k03", "test")
        self.assertTrue(k.record_event(e))
        self.assertFalse(k.record_event(e))

    def test_k04_unknown_preservation(self):
        k = PilotKernel()
        self.assertEqual(k.unknown, UnknownState.UNKNOWN)
        with self.assertRaises(ValueError):
            k.decide(permitted=True)

    def test_k05_review_barrier(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.require_review()
        with self.assertRaises(ValueError):
            k.decide(permitted=True)

    def test_k06_authority_non_escalation(self):
        k = PilotKernel()
        self.assertFalse(k.has_authority("execute_protected_action"))

    def test_k07_history_preservation(self):
        k = PilotKernel()
        e = Event("k07", "historical")
        k.record_event(e)
        k.correct("k07")
        self.assertEqual(k.history[0], e)

    def test_k08_recovery_guard(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=True)
        k.begin_recovery()
        with self.assertRaises(ValueError):
            k.execute()

    def test_k09_unknown_is_representable(self):
        k = PilotKernel()
        self.assertIn(k.unknown, (UnknownState.UNKNOWN, UnknownState.RESOLVED))

    def test_k10_reconstruction(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=True)
        k.execute()
        self.assertEqual(k.reconstruct()["action"], "executed")


class DurableBoundaryTests(unittest.TestCase):
    def test_duplicate_event_is_blocked_by_durable_identity(self):
        import tempfile
        from pathlib import Path
        from pilot_kernel import DurableKernelStore, record_event_durably
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "events.json"))
            k = PilotKernel()
            e = Event("durable-1", "engagement.created")
            self.assertTrue(record_event_durably(k, store, e))
            self.assertFalse(record_event_durably(k, store, e))
            self.assertEqual(len(store.load()), 1)

    def test_durable_history_survives_new_kernel_instance(self):
        import tempfile
        from pathlib import Path
        from pilot_kernel import DurableKernelStore, record_event_durably
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "events.json")
            store = DurableKernelStore(path)
            first = PilotKernel()
            e = Event("durable-2", "engagement.created")
            self.assertTrue(record_event_durably(first, store, e))
            second = PilotKernel()
            self.assertFalse(record_event_durably(second, store, e))
            self.assertEqual(store.event_ids(), frozenset({"durable-2"}))


class DurableDecisionAuditTests(unittest.TestCase):
    def test_decision_is_versioned_and_durable(self):
        import tempfile
        from pathlib import Path
        from pilot_kernel import DurableDecision, DurableKernelStore, decision_records, record_decision_durably
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            record_decision_durably(store, DurableDecision("d1", True, "policy-v1", "completed"))
            records = decision_records(store)
            self.assertEqual(records[0]["decision_id"], "d1")
            self.assertEqual(records[0]["policy_version"], "policy-v1")

    def test_audit_is_separate_and_purpose_bound(self):
        import tempfile
        from pathlib import Path
        from pilot_kernel import DurableKernelStore, append_audit_record, decision_records
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            append_audit_record(store, audit_id="a1", event="decision.created", purpose="pilot-audit")
            self.assertEqual(decision_records(store), [])
            audit = [r for r in store.load() if r.get("audit_id") == "a1"]
            self.assertEqual(audit[0]["purpose"], "pilot-audit")


class DurableAuthorizationTests(unittest.TestCase):
    def _store_with_decision(self, permitted=True, policy_version="policy-v1", review_state="completed"):
        import tempfile
        from pathlib import Path
        from pilot_kernel import (
            DurableDecision,
            DurableKernelStore,
            record_decision_durably,
        )
        d = tempfile.TemporaryDirectory()
        store = DurableKernelStore(str(Path(d.name) / "state.json"))
        record_decision_durably(
            store,
            DurableDecision("d-auth", permitted, policy_version, review_state),
        )
        return d, store

    def test_matching_persisted_decision_authorizes_execution(self):
        from pilot_kernel import ExecutionAuthorization, PilotKernel, authorize_execution
        d, store = self._store_with_decision()
        try:
            self.assertTrue(authorize_execution(
                store,
                ExecutionAuthorization("d-auth", True, "policy-v1", "completed", "protected"),
            ))
        finally:
            d.cleanup()

    def test_missing_decision_denies_execution(self):
        import tempfile
        from pathlib import Path
        from pilot_kernel import DurableKernelStore, ExecutionAuthorization, authorize_execution
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            self.assertFalse(authorize_execution(
                store,
                ExecutionAuthorization("missing", True, "policy-v1", "completed", "protected"),
            ))

    def test_policy_version_mismatch_denies_execution(self):
        from pilot_kernel import ExecutionAuthorization, authorize_execution
        d, store = self._store_with_decision()
        try:
            self.assertFalse(authorize_execution(
                store,
                ExecutionAuthorization("d-auth", True, "policy-v2", "completed", "protected"),
            ))
        finally:
            d.cleanup()

    def test_incomplete_review_denies_execution(self):
        from pilot_kernel import ExecutionAuthorization, authorize_execution
        d, store = self._store_with_decision(review_state="required")
        try:
            self.assertFalse(authorize_execution(
                store,
                ExecutionAuthorization("d-auth", True, "policy-v1", "required", "protected"),
            ))
        finally:
            d.cleanup()

    def test_denied_decision_cannot_authorize_execution(self):
        from pilot_kernel import ExecutionAuthorization, authorize_execution
        d, store = self._store_with_decision(permitted=False)
        try:
            self.assertFalse(authorize_execution(
                store,
                ExecutionAuthorization("d-auth", True, "policy-v1", "completed", "protected"),
            ))
        finally:
            d.cleanup()
