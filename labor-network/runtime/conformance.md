# Critical Kernel Conformance Matrix

The reference implementation covers K01–K10 and the current pilot runtime boundaries. Passing reference tests does not certify production deployment.

## Critical Kernel

Reference-kernel conformance coverage: **10/10 (100%)**.

Production status: **not certified**.

## Runtime boundary status

| Boundary | Reference status | Production status |
|---|---|---|
| Critical Kernel K01–K10 | covered | not certified |
| Durable Event identity | covered | not certified |
| Durable Decision / Audit | covered | not certified |
| Durable execution authorization | covered | not certified |
| ActionRequest API boundary | covered | not certified |
| HTTP /action adapter | covered | not certified |
| Principal / fingerprint primitives | covered | not certified |
| Replay / idempotency | covered | not certified |
| Concurrent identical-request guard | covered in shared-process reference tests | not certified |
| Transactional reference claim | covered in shared-process reference tests | not certified |
| Journal-based recovery after interrupted reference commit | covered | not certified |
| Cross-process/distributed atomicity | not implemented | not certified |
| Production crash-safe transactional reservation | not implemented | not certified |
| Real credential verification | not implemented | not certified |
| TLS / transport hardening | not implemented | not certified |
| Production database transaction semantics | not implemented | not certified |

## Transactional reference checkpoint

The file transactional_reference.py provides a deliberately bounded persistence primitive. It combines a process-local transaction lock, atomic temporary-file replacement, a logical claim operation, and a small journal that can restore an interrupted reference commit when the next transaction begins.

The tests cover concurrent claiming, atomic replacement, successful journal recovery and rejection of malformed journal state.

This remains a **reference crash-recovery mechanism**, not a production transaction protocol. It does not solve multi-process coordination, database isolation, fencing, leases, distributed consensus, filesystem failure modes, or production durability guarantees.

## Pilot vertical slice

The reference vertical slice connects Event identity, Decision persistence, AuditRecord, execution authorization and replay protection. Its production deployment remains unimplemented.

Legacy STСеть files remain preserved as backup/baseline material and are not part of the runtime replacement path.
