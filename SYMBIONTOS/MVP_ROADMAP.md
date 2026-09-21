# SymbiontOS MVP Roadmap

## Stage A first

### Milestone 0 — Contracts
Define identity, capability, context, ComplianceRecord, EventRecord, HCT message format and DLCM decision interface.

### Milestone 1 — Runtime
Implement symbiontd, agent registration, lifecycle management and append-only audit.

### Milestone 2 — Compliance
Implement fabric-service and dlcm-service with PASS, REVIEW, VIOLATION and UNKNOWN outcomes.

### Milestone 3 — Federation
Implement Router, capability-based selection, HCT transport and result aggregation.

### Milestone 4 — Feedback
Add auditable trust state, feedback signals and reversible routing updates.

### Milestone 5 — Adversarial validation
Test prompt injection, identity confusion, context substitution, capability escalation, malicious agents, collusion, replay, provenance corruption and rollback.

### Milestone 6 — Stage B preparation
Package the runtime reproducibly, define hardened host policies, signed update flow and migration tests.

### Milestone 7 — Stage C research
Separate long-term kernel research from the Stage A/B path. Candidate properties include capability isolation, IPC guarantees and kernel-level enforcement.

## Completion condition
The MVP is complete only when the system demonstrates controlled execution, refusal, provenance, compliance decisions, auditability, rollback and a reproducible federation cycle.
