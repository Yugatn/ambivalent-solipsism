"""Minimal standard-library HTTP adapter for the Phase 11 reference API boundary.

This adapter deliberately has no network authentication or production security claims.
Its purpose is to prove that an external request enters the same authorization path.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable

from pilot_kernel import ActionRequest, DurableKernelStore, PilotKernel, handle_action_request


def process_action_payload(
    kernel: PilotKernel,
    store: DurableKernelStore,
    payload: dict,
) -> dict:
    request = ActionRequest(
        request_id=str(payload["request_id"]),
        decision_id=str(payload["decision_id"]),
        policy_version=str(payload["policy_version"]),
        review_state=str(payload["review_state"]),
        permitted=bool(payload["permitted"]),
        action_type=str(payload["action_type"]),
    )
    executed = handle_action_request(kernel, store, request)
    return {"executed": executed, "request_id": request.request_id}


def make_handler(kernel: PilotKernel, store: DurableKernelStore) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/action":
                self.send_error(404)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                result = process_action_payload(kernel, store, payload)
                body = json.dumps(result).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                self.send_error(403, str(exc))

        def log_message(self, format: str, *args) -> None:  # noqa: A002
            return

    return Handler


def serve(kernel: PilotKernel, store: DurableKernelStore, host: str = "127.0.0.1", port: int = 8080) -> None:
    HTTPServer((host, port), make_handler(kernel, store)).serve_forever()
