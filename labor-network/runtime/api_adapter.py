"""Minimal standard-library HTTP adapter for the Phase 11 reference API boundary.

This adapter deliberately has no network authentication or production security claims.
Its purpose is to prove that an external request enters the same authorization path.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import RLock

from pilot_kernel import ActionRequest, DurableKernelStore, PilotKernel, handle_action_request
from transactional_reference import RequestReservationLedger


# Reference-only process lock. It prevents a check-then-execute race between
# callers sharing this Python process. It is not distributed transactionality.
_REQUEST_LOCK = RLock()
_LEDGER_LOCK = RLock()
_REQUEST_LEDGERS: dict[str, RequestReservationLedger] = {}


def _request_ledger(store: DurableKernelStore) -> RequestReservationLedger:
    path = str(store.path) + ".requests"
    with _LEDGER_LOCK:
        ledger = _REQUEST_LEDGERS.get(path)
        if ledger is None:
            ledger = RequestReservationLedger(path)
            _REQUEST_LEDGERS[path] = ledger
        return ledger


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
                result = process_idempotent_action_request(kernel, store, payload)
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


@dataclass(frozen=True)
class ApiPrincipal:
    principal_id: str
    authenticated: bool


def authenticate_principal(headers) -> ApiPrincipal:
    token = headers.get("X-Principal-Token")
    if not token:
        return ApiPrincipal("", False)
    # Reference-only identity mapping. Real credential verification is out of scope.
    return ApiPrincipal(token, True)


def request_fingerprint(payload: dict) -> str:
    import hashlib
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def process_idempotent_action_request(
    kernel: PilotKernel,
    store: DurableKernelStore,
    payload: dict,
) -> dict:
    """Reserve before execution so a crash cannot silently permit replay."""
    fingerprint = request_fingerprint(payload)
    ledger = _request_ledger(store)

    with _REQUEST_LOCK:
        status = ledger.reserve(fingerprint, str(payload.get("request_id", "")))

        if status == RequestReservationLedger.COMPLETED:
            return {
                "executed": False,
                "request_id": str(payload.get("request_id", "")),
                "duplicate": True,
            }

        if status != RequestReservationLedger.RESERVED:
            return {
                "executed": False,
                "request_id": str(payload.get("request_id", "")),
                "duplicate": True,
                "recovery_required": status == RequestReservationLedger.EXECUTING,
                "reservation_status": status,
            }

        ledger.begin_execution(fingerprint)
        try:
            result = process_action_payload(kernel, store, payload)
        except Exception:
            ledger.fail(fingerprint)
            raise

        ledger.complete(fingerprint)
        # Preserve the existing request-fingerprint record for compatibility
        # with the reference conformance tests and audit inspection.
        store.append({
            "request_fingerprint": fingerprint,
            "request_id": str(payload["request_id"]),
            "result": str(result["executed"]).lower(),
        })
        return {**result, "duplicate": False}
