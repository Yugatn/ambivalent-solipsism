"""Tamper-evident append-only evidence ledger."""
import json, os, threading
from .schemas import Evidence, hash_payload

GENESIS_HASH = "0" * 64

class LedgerError(Exception):
    pass

class EvidenceLedger:
    def __init__(self, path):
        self.path = path
        self._lock = threading.Lock()
        self._last_hash = GENESIS_HASH
        self._last_clock = 0
        self._seen_ids = set()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if os.path.exists(path):
            self._load_and_verify()
        else:
            open(path, "a", encoding="utf-8").close()

    def _load_and_verify(self):
        previous_hash, previous_clock, seen = GENESIS_HASH, 0, set()
        with open(self.path, encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    raise LedgerError(f"blank record at line {line_no}")
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise LedgerError(f"invalid JSON at line {line_no}") from exc
                evidence_id = record.get("evidence_id")
                if not evidence_id or evidence_id in seen:
                    raise LedgerError(f"duplicate/empty evidence_id at line {line_no}")
                if record.get("prev_hash") != previous_hash:
                    raise LedgerError(f"prev_hash mismatch at line {line_no}")
                clock = record.get("lamport_clock")
                if not isinstance(clock, int) or clock <= previous_clock:
                    raise LedgerError(f"lamport regression at line {line_no}")
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    raise LedgerError(f"invalid payload at line {line_no}")
                if record.get("payload_hash") != hash_payload(payload):
                    raise LedgerError(f"payload_hash mismatch at line {line_no}")
                previous_hash = hash_payload(record)
                previous_clock = clock
                seen.add(evidence_id)
        self._last_hash, self._last_clock, self._seen_ids = previous_hash, previous_clock, seen

    def append(self, evidence: Evidence):
        with self._lock:
            if evidence.evidence_id in self._seen_ids:
                raise LedgerError(f"duplicate evidence_id: {evidence.evidence_id}")
            if evidence.lamport_clock <= self._last_clock:
                raise LedgerError("lamport regression")
            if evidence.prev_hash != self._last_hash:
                raise LedgerError("prev_hash does not point to current ledger head")
            if evidence.payload_hash != hash_payload(evidence.payload):
                raise LedgerError("payload_hash mismatch")
            record = evidence.to_dict()
            encoded = (json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()
            with open(self.path, "ab") as f:
                f.write(encoded)
                f.flush()
                os.fsync(f.fileno())
            self._last_hash = hash_payload(record)
            self._last_clock = evidence.lamport_clock
            self._seen_ids.add(evidence.evidence_id)
            return evidence

    def verify(self):
        self._load_and_verify()

    @property
    def head_hash(self): return self._last_hash

    @property
    def last_clock(self): return self._last_clock

    def all(self):
        with open(self.path, encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]
