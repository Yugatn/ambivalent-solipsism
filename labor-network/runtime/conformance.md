# Critical Kernel Conformance Matrix

This matrix records the executable reference-kernel coverage for K01–K10. A test passing in the reference kernel demonstrates that the modeled boundary behaves as specified in that implementation; it does not certify production deployment.

| Kernel | Boundary | Executable test | Reference status | Production status |
|---|---|---|---|---|
| K01 | Unauthorized transition | test_k01_authorization_guard | covered | not certified |
| K02 | Decision / Action separation | test_k02_decision_action_separation | covered | not certified |
| K03 | Event idempotency | test_k03_event_idempotency | covered | not certified |
| K04 | UNKNOWN preservation | test_k04_unknown_preservation | covered | not certified |
| K05 | Human Review barrier | test_k05_review_barrier | covered | not certified |
| K06 | Authority non-escalation | test_k06_authority_non_escalation | covered | not certified |
| K07 | Historical correction | test_k07_history_preservation | covered | not certified |
| K08 | Recovery guard | test_k08_recovery_guard | covered | not certified |
| K09 | UNKNOWN representation | test_k09_unknown_is_representable | covered | not certified |
| K10 | State reconstruction | test_k10_reconstruction | covered | not certified |

## Interpretation

**Reference-kernel conformance coverage: 10/10 (100%).**

This percentage means that each currently defined Critical Kernel obligation has at least one executable conformance test in the reference implementation. It does not mean the whole STСеть runtime is implemented, secure, deployed or production-ready.

The next conformance layer must map these same obligations to durable storage, API boundaries, authorization, event processing and any federated runtime components introduced by the pilot.


## Durable boundary status

The reference conformance layer now includes an append-only JSON persistence adapter for Event identity and two executable tests covering duplicate delivery and history across a new kernel instance.

| Boundary | Reference status | Production status |
|---|---|---|
| In-memory K01–K10 | covered | not certified |
| Durable Event identity | covered | not certified |
| Cross-instance duplicate suppression | covered | not certified |
| Durable audit/history | not yet implemented | not certified |
| Durable authorization/policy state | not yet implemented | not certified |
| API/network boundary | not yet implemented | not certified |


## Durable decision and audit checkpoint

The reference runtime now persists versioned Decision records and purpose-bound AuditRecord entries through the same pilot persistence adapter, while keeping their semantic roles distinct.

| Boundary | Reference status | Production status |
|---|---|---|
| Durable Decision + policy version | covered | not certified |
| Decision / Audit separation | covered | not certified |
| Purpose-bound audit record | covered | not certified |
| Durable authorization/policy enforcement | partial | not certified |
| API/network boundary | not yet implemented | not certified |


## Durable authorization checkpoint

The reference runtime now requires an explicit persisted Decision for protected execution. Authorization is denied when the Decision is missing, denied, bound to another policy version, or still requires review.

| Boundary | Reference status | Production status |
|---|---|---|
| Persisted Decision required for execution | covered | not certified |
| Policy-version match | covered | not certified |
| Review completion guard | covered | not certified |
| Denied Decision blocks execution | covered | not certified |
| API/network authorization boundary | not yet implemented | not certified |


## API boundary checkpoint

The reference runtime now exposes a bounded ActionRequest entry point that delegates to the durable authorization boundary. The API-facing path cannot execute a protected Action without a matching persisted Decision, policy version and review state.

| Boundary | Reference status | Production status |
|---|---|---|
| API request enters through authorization | covered | not certified |
| Missing Decision blocked at API boundary | covered | not certified |
| Policy mismatch blocked at API boundary | covered | not certified |
| Direct protected execution from API payload | not exposed | not certified |
| Network transport/authentication | not implemented | not certified |


## HTTP adapter checkpoint

A minimal standard-library HTTP adapter now exposes /action and delegates to the existing ActionRequest authorization path. The adapter is intentionally a reference adapter: it does not claim transport authentication, TLS, production hardening, rate limiting or distributed deployment.

| Boundary | Reference status | Production status |
|---|---|---|
| HTTP request reaches existing authorization path | covered | not certified |
| Missing persisted Decision rejected | covered | not certified |
| Direct API-to-Action bypass | not exposed by adapter | not certified |
| Transport authentication | not implemented | not certified |
| TLS / network hardening | not implemented | not certified |


## API security boundary checkpoint

The reference adapter now has explicit principal/authentication state and deterministic request fingerprints. These primitives prepare the boundary for replay protection and authenticated request handling; they do not constitute real credential verification or transport security.

| Boundary | Reference status | Production status |
|---|---|---|
| Explicit authenticated/unauthenticated principal state | covered | not certified |
| Deterministic request fingerprint | covered | not certified |
| Replay prevention | prepared, not enforced | not certified |
| Real credential verification | not implemented | not certified |
| TLS / transport security | not implemented | not certified |


## API replay/idempotency checkpoint

The reference API path now persists a canonical request fingerprint before accepting a repeated request as new. An identical request is treated as a duplicate and does not execute a second protected Action. A changed payload receives a different fingerprint.

| Boundary | Reference status | Production status |
|---|---|---|
| Canonical request fingerprint | covered | not certified |
| Duplicate API request detection | covered | not certified |
| Duplicate protected execution prevention | covered | not certified |
| Cross-process replay protection | reference persistence only | not certified |
| Cryptographic request authentication | not implemented | not certified |
