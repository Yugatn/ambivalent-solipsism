import tempfile
import unittest
from pathlib import Path

from api_adapter import process_idempotent_action_request
from pilot_kernel import (
    DurableDecision,
    DurableKernelStore,
    Event,
    PilotKernel,
    append_audit_record,
    record_decision_durably,
    record_event_durably,
)


class PilotVerticalSliceTests(unittest.TestCase):
    def test_event_decision_authorization_audit_and_replay(self):
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            kernel = PilotKernel()

            event = Event("pilot-event-1", "evidence.received")
            self.assertTrue(record_event_durably(kernel, store, event))
            self.assertFalse(record_event_durably(kernel, store, event))

            record_decision_durably(
                store,
                DurableDecision(
                    "pilot-decision-1",
                    True,
                    "policy-v1",
                    "completed",
                ),
            )
            append_audit_record(
                store,
                audit_id="pilot-audit-1",
                event="decision:pilot-decision-1",
                purpose="pilot-conformance",
            )

            kernel.resolve_evidence()
            kernel.decide(permitted=True)

            payload = {
                "request_id": "pilot-request-1",
                "decision_id": "pilot-decision-1",
                "policy_version": "policy-v1",
                "review_state": "completed",
                "permitted": True,
                "action_type": "protected",
            }
            first = process_idempotent_action_request(kernel, store, payload)
            second = process_idempotent_action_request(kernel, store, payload)

            self.assertTrue(first["executed"])
            self.assertFalse(first["duplicate"])
            self.assertFalse(second["executed"])
            self.assertTrue(second["duplicate"])

            records = store.load()
            self.assertEqual(
                len([r for r in records if r.get("event_id") == "pilot-event-1"]),
                1,
            )
            self.assertEqual(
                len([r for r in records if r.get("decision_id") == "pilot-decision-1"]),
                1,
            )
            self.assertEqual(
                len([r for r in records if r.get("audit_id") == "pilot-audit-1"]),
                1,
            )
            self.assertEqual(
                len([r for r in records if r.get("request_fingerprint")]),
                1,
            )
            self.assertEqual(kernel.action.value, "executed")


if __name__ == "__main__":
    unittest.main()
