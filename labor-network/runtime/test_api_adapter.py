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
