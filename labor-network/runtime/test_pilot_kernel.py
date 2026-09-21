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

    def test_denied_decision_cannot_execute(self):
        k = PilotKernel()
        k.resolve_evidence()
        k.decide(permitted=False)
        with self.assertRaises(ValueError):
            k.execute()


if __name__ == "__main__":
    unittest.main()
