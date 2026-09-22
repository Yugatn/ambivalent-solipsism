"""Reference transactional persistence primitives for the pilot.

This module deliberately uses a single-process lock plus atomic file replacement.
It is a reference boundary only: it is not a distributed database transaction,
does not reserve work across process crashes, and is not a production durability claim.
"""
from __future__ import annotations

import json
from pathlib import Path
from threading import RLock
from typing import Dict, Iterator


class ReferenceTransaction:
    def __init__(self, path: str):
        self.path = Path(path)
        self._lock = RLock()

    def __enter__(self) -> "ReferenceTransaction":
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._lock.release()

    def load(self) -> list[Dict[str, str]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def append(self, record: Dict[str, str]) -> None:
        records = self.load()
        records.append(dict(record))
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(records, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def claim(self, key: str, value: str) -> bool:
        """Atomically claim a logical key within this reference process."""
        for record in self.load():
            if record.get("claim_key") == key:
                return False
        self.append({"claim_key": key, "claim_value": value})
        return True
