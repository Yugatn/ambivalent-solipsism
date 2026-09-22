import json
import tempfile
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from threading import Thread
from http.server import HTTPServer
from unittest.mock import patch

from api_adapter import make_handler
from pilot_kernel import DurableDecision, DurableKernelStore, PilotKernel, record_decision_durably


class ApiAdapterTests(unittest.TestCase):
    def _post(self, server, payload):
        body = json.dumps(payload).encode()
        req = Request(
            f"http://127.0.0.1:{server.server_port}/action",
            data=body,
            method="POST",
        )
        thread = Thread(target=server.handle_request)
        thread.start()
        with urlopen(req) as response:
            result = json.loads(response.read())
        thread.join()
        return result

    def test_http_request_uses_same_authorization_boundary_and_replay_guard(self):
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            record_decision_durably(store, DurableDecision("http-1", True, "policy-v1", "completed"))
            kernel = PilotKernel()
            kernel.resolve_evidence()
            kernel.decide(permitted=True)
            server = HTTPServer(("127.0.0.1", 0), make_handler(kernel, store))
            try:
                payload = {
                    "request_id": "http-req-1",
                    "decision_id": "http-1",
                    "policy_version": "policy-v1",
                    "review_state": "completed",
                    "permitted": True,
                    "action_type": "protected",
                }
                first = self._post(server, payload)
                second = self._post(server, payload)
                self.assertTrue(first["executed"])
                self.assertFalse(first["duplicate"])
                self.assertFalse(second["executed"])
                self.assertTrue(second["duplicate"])
            finally:
                server.server_close()

    def test_http_request_without_matching_decision_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            store = DurableKernelStore(str(Path(d) / "state.json"))
            kernel = PilotKernel()
            kernel.resolve_evidence()
            kernel.decide(permitted=True)
            server = HTTPServer(("127.0.0.1", 0), make_handler(kernel, store))
            try:
                payload = {
                    "request_id": "http-req-2",
                    "decision_id": "missing",
                    "policy_version": "policy-v1",
                    "review_state": "completed",
                    "permitted": True,
                    "action_type": "protected",
                }
                body = json.dumps(payload).encode()
                req = Request(
                    f"http://127.0.0.1:{server.server_port}/action",
                    data=body,
                    method="POST",
                )
                thread = Thread(target=server.handle_request)
                thread.start()
                with self.assertRaises(Exception):
                    urlopen(req)
                thread.join()
            finally:
                server.server_close()


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

    def _prepared(self):
        d = tempfile.TemporaryDirectory()
        store = DurableKernelStore(str(Path(d.name) / "state.json"))
        record_decision_durably(store, DurableDecision("replay-d1", True, "policy-v1", "completed"))
        kernel = PilotKernel()
        kernel.resolve_evidence()
        kernel.decide(permitted=True)
        return d, store, kernel

    def test_identical_request_is_idempotent(self):
        from api_adapter import process_idempotent_action_request
        d, store, kernel = self._prepared()
        try:
            first = process_idempotent_action_request(kernel, store, self._payload())
            second = process_idempotent_action_request(kernel, store, self._payload())
            self.assertFalse(first["duplicate"])
            self.assertTrue(second["duplicate"])
            self.assertTrue(first["executed"])
            self.assertFalse(second["executed"])
        finally:
            d.cleanup()

    def test_changed_payload_is_not_same_request(self):
        from api_adapter import process_idempotent_action_request
        d, store, kernel = self._prepared()
        try:
            first = process_idempotent_action_request(kernel, store, self._payload())
            changed = dict(self._payload())
            changed["request_id"] = "replay-2"
            second = process_idempotent_action_request(kernel, store, changed)
            self.assertFalse(first["duplicate"])
            self.assertFalse(second["duplicate"])
        finally:
            d.cleanup()

    def test_concurrent_identical_requests_have_one_non_duplicate(self):
        from api_adapter import process_idempotent_action_request
        d, store, kernel = self._prepared()
        try:
            results = []
            workers = [
                Thread(
                    target=lambda: results.append(
                        process_idempotent_action_request(kernel, store, self._payload())
                    )
                )
                for _ in range(8)
            ]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join()

            self.assertEqual(len(results), 8)
            self.assertEqual(sum(1 for result in results if not result["duplicate"]), 1)
            self.assertEqual(sum(1 for result in results if result["duplicate"]), 7)
            self.assertEqual(sum(1 for result in results if result["executed"]), 1)
            self.assertEqual(len([
                record for record in store.load()
                if "request_fingerprint" in record
            ]), 1)
        finally:
            d.cleanup()

    def test_interrupted_execution_blocks_replay(self):
        from api_adapter import process_idempotent_action_request
        d, store, kernel = self._prepared()
        payload = self._payload()
        try:
            def interrupted_action(kernel_arg, store_arg, payload_arg):
                kernel_arg.execute()
                raise RuntimeError("simulated process interruption")

            with patch("api_adapter.process_action_payload", side_effect=interrupted_action):
                with self.assertRaises(RuntimeError):
                    process_idempotent_action_request(kernel, store, payload)

            second = process_idempotent_action_request(kernel, store, payload)
            self.assertTrue(second["duplicate"])
            self.assertTrue(second["recovery_required"])
            self.assertEqual(second["reservation_status"], "executing")
            self.assertEqual(kernel.action.value, "executed")
        finally:
            d.cleanup()


if __name__ == "__main__":
    unittest.main()
