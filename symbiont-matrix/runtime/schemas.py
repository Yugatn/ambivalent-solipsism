"""Typed records and canonical hashing."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib, json

EPISTEMIC = {"OBSERVED", "DERIVED", "CLAIMED"}

@dataclass(frozen=True)
class Event:
    event_id: str
    node_id: str
    session_id: str
    event_type: str
    observed_at: int
    clock: int
    payload: Dict[str, Any]
    epistemic: str = "CLAIMED"

    @classmethod
    def from_json(cls, data):
        event = cls(
            event_id=data["event_id"], node_id=data["node_id"],
            session_id=data.get("session_id", "unknown"),
            event_type=data["event_type"], observed_at=data["observed_at"],
            clock=data["clock"], payload=data["payload"],
            epistemic=data.get("epistemic", "CLAIMED"))
        event.validate()
        return event

    def validate(self):
        if not self.event_id or not self.node_id or not self.event_type:
            raise ValueError("event_id, node_id and event_type are required")
        if self.observed_at < 0 or self.clock < 0:
            raise ValueError("observed_at and clock must be non-negative")
        if self.epistemic not in EPISTEMIC:
            raise ValueError(f"invalid epistemic value: {self.epistemic}")
        if not isinstance(self.payload, dict):
            raise ValueError("payload must be an object")

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    node_id: str
    issued_at: int
    lamport_clock: int
    prev_hash: str
    payload_hash: str
    payload: Dict[str, Any]
    signature: str = "UNSIGNED"
    supersedes: Optional[str] = None

    def to_dict(self):
        return {
            "evidence_id": self.evidence_id, "node_id": self.node_id,
            "issued_at": self.issued_at, "lamport_clock": self.lamport_clock,
            "prev_hash": self.prev_hash, "payload_hash": self.payload_hash,
            "payload": self.payload, "signature": self.signature,
            "supersedes": self.supersedes}

@dataclass(frozen=True)
class Verdict:
    rule_id: str
    verdict: str
    severity: str
    epistemic: str
    evidence: List[str] = field(default_factory=list)

def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def hash_payload(data):
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()
