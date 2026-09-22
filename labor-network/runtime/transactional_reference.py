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
