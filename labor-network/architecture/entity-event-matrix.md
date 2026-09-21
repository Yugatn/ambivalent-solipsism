# Матрица Entity × Event × Guard × Invariant

| Entity | Event | Основные Guard | Ключевой инвариант |
|---|---|---|---|
| Opportunity | publish | authority, completeness | возможность не становится обязательством |
| Engagement | activate | acceptance, policy | участие не расширяет полномочия автоматически |
| Evidence | verify | provenance, verification | подтверждение имеет источник |
| Evidence | revoke | authority, reason | отзыв не стирает историю |
| Decision | permit | policy, impact | существенное решение проходит guards |
| Decision | deny | policy, reason | отказ имеет основание |
| Decision | review | impact, uncertainty | неопределённость не маскируется под факт |
| Dispute | open | subject access | оспаривание не переписывает источник |
| Dispute | resolve | review, evidence | результат имеет основание |
| Support | approve | eligibility, authority | поддержка не создаёт скрытого обязательства |
| Permission | revoke | authority | отозванное полномочие не используется |
| Audit | record | integrity | существенное действие трассируемо |

## Правило матрицы

Каждый новый Event для защищённой Entity должен иметь:

1. допустимый источник;
2. guard conditions;
3. ожидаемый результат;
4. инвариант;
5. audit requirement;
6. recovery path.


## Phase 2 complete lifecycle coverage

The matrix is extended to cover all 15 canonical Phase 1 entities:

| Entity | Lifecycle events | Guards | Invariants |
|---|---|---|---|
| Subject | create, update, consent, restrict, exit | subject control, purpose, authority | I1, I2, I12, I24 |
| Organization | register, update, suspend | governance authority, provenance | I3, I17 |
| Opportunity | publish, pause, fill, expire, withdraw | authority, completeness, validity | I5, I17 |
| Engagement | propose, accept, activate, pause, complete, terminate, dispute | participant authority, policy, evidence | I4, I17, I18 |
| Evidence | assert, verify, challenge, expire, revoke, supersede | provenance, verification, validity, authority | I3, I4, I9, I15 |
| Decision | propose, evaluate, permit, deny, review, reverse, supersede | policy, impact, authority, review | I3, I4, I11, I17, I23 |
| Action | execute, fail, compensate | decision/permission, scope, audit | I17, I18, I19, I23 |
| Event | append, acknowledge, reconcile | schema, idempotency, causality, integrity | I3, I16, I22 |
| PolicyDecision | evaluate, review, supersede | policy version, authority, purpose | I2, I3, I17 |
| AuditRecord | record, integrity-check, retain, restrict | integrity, purpose, access | I2, I19, I22 |
| Permission | grant, modify, expire, revoke | granting authority, purpose, scope | I2, I17, I18 |
| Dispute | open, acknowledge, investigate, resolve, escalate, withdraw | access, evidence, review | I4, I9, I15 |
| Support | offer, request, approve, activate, suspend, complete, revoke | eligibility, authority, purpose | I2, I12, I17 |
| Resource | register, update, allocate, release | ownership, access policy, availability | I2, I17, I18 |
| Relation | assert, confirm, expire, revoke | provenance, context, validity | I3, I7, I15 |

### Matrix closure rules

No protected lifecycle event is canonical unless its matrix row identifies:
- source/actor;
- guard;
- resulting state or validity;
- invariant;
- audit requirement;
- recovery path.

A new event must be added to this matrix before it can be treated as part of the canonical architecture.
