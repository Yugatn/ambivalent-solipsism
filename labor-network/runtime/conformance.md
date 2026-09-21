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
