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
