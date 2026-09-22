import json
import tempfile
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from threading import Thread
from http.server import HTTPServer

from api_adapter import make_handler
from pilot_kernel import DurableDecision, DurableKernelStore, PilotKernel, record_decision_durably


class ApiAdapterTests(unittest.TestCase):
    def test_http_request_uses_same_authorization_boundary(self):
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            record_decision_durably(store, DurableDecision("http-1", True, "policy-v1", "completed"))
            kernel = PilotKernel()
            kernel.resolve_evidence()
            kernel.decide(permitted=True)
            server = HTTPServer(("127.0.0.1", 0), make_handler(kernel, store))
            thread = Thread(target=server.handle_request)
            thread.start()
            payload = json.dumps({
                "request_id": "http-req-1",
                "decision_id": "http-1",
                "policy_version": "policy-v1",
                "review_state": "completed",
                "permitted": True,
                "action_type": "protected",
            }).encode()
            req = Request(f"http://127.0.0.1:{server.server_port}/action", data=payload, method="POST")
            with urlopen(req) as response:
                body = json.loads(response.read())
            thread.join()
            server.server_close()
            self.assertTrue(body["executed"])

    def test_http_request_without_matching_decision_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            kernel = PilotKernel()
            kernel.resolve_evidence()
            kernel.decide(permitted=True)
            server = HTTPServer(("127.0.0.1", 0), make_handler(kernel, store))
            thread = Thread(target=server.handle_request)
            thread.start()
            payload = json.dumps({
                "request_id": "http-req-2",
                "decision_id": "missing",
                "policy_version": "policy-v1",
                "review_state": "completed",
                "permitted": True,
                "action_type": "protected",
            }).encode()
            req = Request(f"http://127.0.0.1:{server.server_port}/action", data=payload, method="POST")
            with self.assertRaises(Exception):
                urlopen(req)
            thread.join()
            server.server_close()


if __name__ == "__main__":
    unittest.main()


class ApiSecurityBoundaryTests(unittest.TestCase):
    def test_missing_identity_is_not_authenticated(self):
        from api_adapter import authenticate_principal
        principal = authenticate_principal({})
        self.assertFalse(principal.authenticated)

    def test_reference_identity_is_explicit(self):
        from api_adapter import authenticate_principal
        principal = authenticate_principal({"X-Principal-Token": "reference-user"})
        self.assertTrue(principal.authenticated)
        self.assertEqual(principal.principal_id, "reference-user")

    def test_request_fingerprint_is_deterministic(self):
        from api_adapter import request_fingerprint
        a = {"decision_id": "d1", "permitted": True}
        b = {"permitted": True, "decision_id": "d1"}
        self.assertEqual(request_fingerprint(a), request_fingerprint(b))

    def test_request_fingerprint_changes_when_payload_changes(self):
        from api_adapter import request_fingerprint
        a = {"decision_id": "d1", "permitted": True}
        b = {"decision_id": "d1", "permitted": False}
        self.assertNotEqual(request_fingerprint(a), request_fingerprint(b))


class ReplayProtectionTests(unittest.TestCase):
    def _payload(self):
        return {
            "request_id": "replay-1",
            "decision_id": "replay-d1",
            "policy_version": "policy-v1",
            "review_state": "completed",
            "permitted": True,
            "action_type": "protected",
        }

    def test_identical_request_is_idempotent(self):
        import tempfile
        from pathlib import Path
        from api_adapter import process_idempotent_action_request
        from pilot_kernel import DurableDecision, DurableKernelStore, PilotKernel, record_decision_durably
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            record_decision_durably(store, DurableDecision("replay-d1", True, "policy-v1", "completed"))
            kernel = PilotKernel()
            kernel.resolve_evidence()
            kernel.decide(permitted=True)
            first = process_idempotent_action_request(kernel, store, self._payload())
            second = process_idempotent_action_request(kernel, store, self._payload())
            self.assertFalse(first["duplicate"])
            self.assertTrue(second["duplicate"])
            self.assertTrue(first["executed"])
            self.assertFalse(second["executed"])

    def test_changed_payload_is_not_same_request(self):
        import tempfile
        from pathlib import Path
        from api_adapter import process_idempotent_action_request
        from pilot_kernel import DurableDecision, DurableKernelStore, PilotKernel, record_decision_durably
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            record_decision_durably(store, DurableDecision("replay-d1", True, "policy-v1", "completed"))
            kernel = PilotKernel()
            kernel.resolve_evidence()
            kernel.decide(permitted=True)
            first = process_idempotent_action_request(kernel, store, self._payload())
            changed = dict(self._payload())
            changed["request_id"] = "replay-2"
            second = process_idempotent_action_request(kernel, store, changed)
            self.assertFalse(first["duplicate"])
            self.assertFalse(second["duplicate"])
