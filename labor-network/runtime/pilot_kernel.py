"""Minimal executable kernel for the STСеть Phase 11 pilot.

This is deliberately small: it validates critical boundaries from the
architectural contract without claiming production readiness.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, FrozenSet


class UnknownState(Enum):
    RESOLVED = "resolved"
    UNKNOWN = "unknown"


class ReviewState(Enum):
    NOT_REQUIRED = "not_required"
    REQUIRED = "required"
    COMPLETED = "completed"


class ActionState(Enum):
    NOT_STARTED = "not_started"
    EXECUTED = "executed"


@dataclass(frozen=True)
class Event:
    event_id: str
    kind: str
    payload: tuple[tuple[str, str], ...] = ()


@dataclass
class PilotKernel:
    """Bounded in-memory reference implementation of the critical kernel."""

    processed_events: FrozenSet[str] = frozenset()
    unknown: UnknownState = UnknownState.UNKNOWN
    review: ReviewState = ReviewState.NOT_REQUIRED
    decision_permitted: bool = False
    action: ActionState = ActionState.NOT_STARTED
    audit: list[str] = field(default_factory=list)
    history: list[Event] = field(default_factory=list)
    authority: FrozenSet[str] = frozenset()
    corrections: list[str] = field(default_factory=list)
    recovery_pending: bool = False
    terminal_snapshot: Optional[Dict[str, str]] = None

    def record_event(self, event: Event) -> bool:
        """Accept an event once; duplicate delivery has no protected effect."""
        if event.event_id in self.processed_events:
            return False
        self.processed_events = self.processed_events | {event.event_id}
        self.history.append(event)
        self.audit.append(f"event:{event.event_id}")
        return True

    def resolve_evidence(self) -> None:
        self.unknown = UnknownState.RESOLVED

    def require_review(self) -> None:
        self.review = ReviewState.REQUIRED

    def complete_review(self) -> None:
        if self.review is ReviewState.REQUIRED:
            self.review = ReviewState.COMPLETED
        else:
            raise ValueError("review is not required")

    def grant_authority(self, capability: str) -> None:
        self.authority = self.authority | {capability}

    def has_authority(self, capability: str) -> bool:
        return capability in self.authority

    def decide(self, *, permitted: bool) -> None:
        if self.unknown is UnknownState.UNKNOWN:
            raise ValueError("cannot decide from unresolved evidence")
        if self.review is ReviewState.REQUIRED:
            raise ValueError("human review is incomplete")
        self.decision_permitted = permitted
        self.audit.append(f"decision:{'permit' if permitted else 'deny'}")

    def correct(self, reference_event_id: str) -> None:
        if reference_event_id not in self.processed_events:
            raise ValueError("cannot correct unknown historical event")
        self.corrections.append(reference_event_id)
        self.audit.append(f"correction:{reference_event_id}")

    def begin_recovery(self) -> None:
        self.recovery_pending = True
        self.audit.append("recovery:started")

    def complete_recovery(self) -> None:
        self.recovery_pending = False
        self.audit.append("recovery:completed")

    def execute(self) -> bool:
        """Execute only after a permitted Decision; never directly from review."""
        if not self.decision_permitted:
            raise ValueError("no permitted decision")
        if self.recovery_pending:
            raise ValueError("recovery is incomplete")
        if self.action is ActionState.EXECUTED:
            return False
        self.action = ActionState.EXECUTED
        self.audit.append("action:executed")
        return True

    def reconstruct(self) -> Dict[str, str]:
        return self.snapshot()

    def snapshot(self) -> Dict[str, str]:
        return {
            "unknown": self.unknown.value,
            "review": self.review.value,
            "decision": "permitted" if self.decision_permitted else "not_permitted",
            "action": self.action.value,
            "events": str(len(self.history)),
        }
