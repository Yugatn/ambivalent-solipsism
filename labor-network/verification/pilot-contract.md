# Phase 11 Pilot Contract

## Purpose

The pilot is the first bounded runtime validation of the STСеть architecture. It MUST exercise a reversible, low-scale scenario and MUST NOT be treated as evidence that the entire architecture is production-ready.

## Pilot boundary

The pilot MUST define:

- one concrete workflow;
- a limited set of entities and participants;
- explicit geographic/organizational scope;
- permitted data classes;
- retention period;
- measurable operational objectives;
- rollback/exit conditions;
- human review path for protected outcomes;
- incident and audit procedure.

## Minimum vertical slice

The first executable slice SHOULD cover:

1. Subject;
2. Opportunity;
3. Engagement;
4. Evidence;
5. Decision;
6. Action;
7. Event;
8. PolicyDecision;
9. AuditRecord.

The slice MUST preserve the previously established Decision/Action, Evidence/Decision, Permission/authority and Audit/surveillance boundaries.

## Pilot acceptance criteria

A pilot may proceed to expansion review only if executable tests demonstrate:

- event idempotency;
- protected transition guards;
- Unknown preservation;
- required Human Review;
- audit traceability;
- correction/revocation propagation;
- bounded federation behavior if federation is exercised;
- recovery without duplicate protected effects;
- no unexplained privacy-scope expansion.

## Reversibility

Pilot actions MUST be reversible where technically and legally possible. Irreversible effects require explicit prior approval, documented necessity and an independent recovery/contest path where applicable.

## Stop conditions

The pilot MUST pause or stop when a protected invariant is violated, an unexplained authority expansion occurs, auditability is lost for protected operations, privacy scope expands without authorization, or recovery cannot establish a consistent state.

## Evidence of pilot outcome

Pilot results MUST distinguish:

- test execution evidence;
- operational measurements;
- incidents and deviations;
- unresolved limitations;
- architectural invariant status.

A successful pilot does not automatically validate unrelated components or future expansion scenarios.

## Phase 11 invariants

- P11-1: pilot scope is explicit and bounded;
- P11-2: pilot consequences are reversible where possible;
- P11-3: protected architectural invariants remain enforced at runtime;
- P11-4: failures trigger explicit pause/stop conditions;
- P11-5: pilot evidence is distinguishable from production certification;
- P11-6: expansion requires a separate review gate.

Runtime pilot deployment is not claimed by this document.
