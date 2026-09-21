# SymbiontOS Deployment Stages

Stage A, Stage B and Stage C are sequential deployment stages of one architecture, not mutually exclusive alternatives.

## Stage A — Service Layer
Linux host, userspace runtime, process isolation, HCT transport, local audit and federation services. Primary purpose: prototype and research.

## Stage B — Distribution
Hardened Linux base, SymbiontOS init/update layer, signed packages, provenance-aware updates, stronger isolation and boot-time compliance.

## Stage C — Native OS
Future native execution substrate with capability-based isolation, first-class IPC and kernel-enforced security properties.

## Compatibility rule
A protocol should be designed once and implemented at progressively stronger enforcement layers. Migration preserves identity, provenance, policy semantics, audit history and valid compliance records.

## Mixed-stage federation
Nodes at different stages may participate in one federation if protocol compatibility, identity, capability model, provenance and security requirements are satisfied.

## Verification boundary
Stage A does not imply kernel-level isolation. Stage B does not imply formal verification. Stage C is a target architecture; verification must be demonstrated property by property.

## Migration gate
A transition requires protocol compatibility tests, threat-model review, provenance preservation, rollback planning, security testing, compliance testing and explicit documentation of newly enforced and still-unenforced properties.
