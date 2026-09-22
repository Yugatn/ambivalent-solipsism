"""Reference transactional persistence primitives for the pilot.

This module deliberately uses a single-process lock plus atomic file replacement.
It is a reference boundary only: it is not a distributed database transaction
and does not provide production durability or multi-process coordination.
"""
from __future__ import annotations

import json
from pathlib import Path
from threading import RLock
from typing import Dict


class ReferenceTransaction:
    def __init__(self, path: str):
        self.path = Path(path)
        self.journal_path = self.path.with_suffix(self.path.suffix + ".journal")
        self._lock = RLock()

    def __enter__(self) -> "ReferenceTransaction":
        self._lock.acquire()
        self.recover()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._lock.release()

    def load(self) -> list[Dict[str, str]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write_atomic(self, records: list[Dict[str, str]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(records, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def append(self, record: Dict[str, str]) -> None:
        records = self.load()
        records.append(dict(record))
        self.journal_path.write_text(
            json.dumps({"target": str(self.path), "records": records}, sort_keys=True),
            encoding="utf-8",
        )
        try:
            self._write_atomic(records)
        finally:
            if self.journal_path.exists():
                self.journal_path.unlink()

    def recover(self) -> None:
        if not self.journal_path.exists():
            return
        journal = json.loads(self.journal_path.read_text(encoding="utf-8"))
        records = journal.get("records")
        if not isinstance(records, list):
            raise ValueError("invalid transaction journal")
        self._write_atomic(records)
        self.journal_path.unlink()

    def claim(self, key: str, value: str) -> bool:
        """Atomically claim a logical key within this reference process."""
        for record in self.load():
            if record.get("claim_key") == key:
                return False
        self.append({"claim_key": key, "claim_value": value})
        return True


class RequestReservationLedger:
    """Durable request reservation state for reference idempotency.

    A reservation is persisted before protected execution. If execution reaches
    the terminal callback, the reservation becomes completed. If the process
    disappears after execution but before completion, the durable state remains
    executing, so a replay is blocked rather than silently executing twice.

    Recovery of an executing request is deliberately explicit. The reference
    layer does not guess whether an external side effect happened.
    """

    RESERVED = "reserved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

    def __init__(self, path: str):
        self.transaction = ReferenceTransaction(path)
        self._lock = RLock()

    def _record(self, fingerprint: str) -> Dict[str, str] | None:
        records = self.transaction.load()
        matches = [
            record for record in records
            if record.get("fingerprint") == fingerprint
        ]
        return matches[-1] if matches else None

    def reserve(self, fingerprint: str, request_id: str) -> str:
        with self._lock, self.transaction:
            record = self._record(fingerprint)
            if record is not None:
                return record["status"]
            self.transaction.append({
                "fingerprint": fingerprint,
                "request_id": request_id,
                "status": self.RESERVED,
            })
            return self.RESERVED

    def begin_execution(self, fingerprint: str) -> str:
        with self._lock, self.transaction:
            record = self._record(fingerprint)
            if record is None:
                raise ValueError("request is not reserved")
            if record["status"] != self.RESERVED:
                return record["status"]
            self.transaction.append({
                "fingerprint": fingerprint,
                "request_id": record["request_id"],
                "status": self.EXECUTING,
            })
            return self.EXECUTING

    def complete(self, fingerprint: str) -> str:
        with self._lock, self.transaction:
            record = self._record(fingerprint)
            if record is None:
                raise ValueError("request is not reserved")
            if record["status"] == self.COMPLETED:
                return self.COMPLETED
            if record["status"] != self.EXECUTING:
                raise ValueError("request is not executing")
            self.transaction.append({
                "fingerprint": fingerprint,
                "request_id": record["request_id"],
                "status": self.COMPLETED,
            })
            return self.COMPLETED

    def fail(self, fingerprint: str) -> str:
        with self._lock, self.transaction:
            record = self._record(fingerprint)
            if record is None:
                raise ValueError("request is not reserved")
            if record["status"] == self.FAILED:
                return self.FAILED
            if record["status"] == self.COMPLETED:
                return self.COMPLETED
            self.transaction.append({
                "fingerprint": fingerprint,
                "request_id": record["request_id"],
                "status": self.FAILED,
            })
            return self.FAILED

    def resolve_executing(self, fingerprint: str, outcome: str) -> str:
        """Resolve an interrupted request only from an explicit external outcome.

        The caller must establish whether the protected side effect completed.
        This method does not infer the outcome from local process state.
        """
        if outcome not in {self.COMPLETED, self.FAILED}:
            raise ValueError("outcome must be completed or failed")
        with self._lock, self.transaction:
            record = self._record(fingerprint)
            if record is None:
                raise ValueError("request is not reserved")
            if record["status"] != self.EXECUTING:
                raise ValueError("request is not executing")
            self.transaction.append({
                "fingerprint": fingerprint,
                "request_id": record["request_id"],
                "status": outcome,
            })
            return outcome

    def status(self, fingerprint: str) -> str | None:
        with self._lock, self.transaction:
            record = self._record(fingerprint)
            return None if record is None else record["status"]
