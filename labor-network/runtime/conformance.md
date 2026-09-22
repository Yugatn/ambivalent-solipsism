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
| Cross-process/distributed atomicity | not implemented | not certified |
| Crash-safe transactional reservation | not implemented | not certified |
| Real credential verification | not implemented | not certified |
| TLS / transport hardening | not implemented | not certified |
| Production database transaction semantics | not implemented | not certified |

## Transactional reference checkpoint

The file transactional_reference.py adds a deliberately bounded persistence primitive for the next runtime layer. It combines a process-local transaction lock with atomic temporary-file replacement and a logical claim operation. The accompanying tests verify that concurrent callers sharing the same process produce exactly one successful claim and that persisted JSON remains complete after replacement.

This is **not** a distributed transaction protocol. It does not solve multi-process coordination, database isolation, crash-safe work reservation, fencing, leases, or production durability.

## Pilot vertical slice

The reference vertical slice connects Event identity, Decision persistence, AuditRecord, execution authorization and replay protection. Its production deployment remains unimplemented.

Legacy STСеть files remain preserved as backup/baseline material and are not part of the runtime replacement path.
