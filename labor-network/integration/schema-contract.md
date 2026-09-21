# Машинные контракты СТСети

Этот документ фиксирует минимальный контракт данных до появления конкретной реализации.

## 1. Event

Обязательные поля: event_id, event_type, actor, subject, occurred_at, recorded_at, schema_version, correlation_id, payload, provenance.

Event должен быть идентифицируемым и идемпотентным.

## 2. Subject

Минимально: subject_id, status, identifiers и context references.

Идентификатор не является оценкой субъекта.

## 3. Evidence

Минимально: evidence_id, claim, source, provenance, status, validity_period.

Evidence должен позволять определить происхождение и актуальность утверждения.

## 4. Decision

Минимально: decision_id, subject, action, context, evidence_refs, policy_version, impact_class, outcome, reason_code, review_status.

## 5. Permission

Permission содержит subject, actor или principal, action, resource, purpose, scope, validity и policy basis.

Техническая возможность не является Permission.

## 6. Dispute

Dispute содержит dispute_id, subject, target_ref, claim, opened_at, status и resolution.

## 7. Audit Record

Audit Record содержит actor, action, target, purpose, policy_version, timestamp и integrity metadata.

## 8. Data minimization

Контракт не требует передачи всех полей между системами. Каждая интеграция определяет минимальный необходимый набор.

## 9. Versioning

Схемы версионируются. Изменение смысла поля требует новой версии контракта.


## Phase 1 canonical entity contract

The minimum schema set is now explicitly aligned with the implementation roadmap:

### Subject
Required: subject_id, schema_version, status, identifiers, context_refs, provenance_ref, created_at, updated_at.

Constraints:
- identifier is not a value judgment;
- status is contextual and cannot encode hidden reputation;
- sensitive attributes require separate purpose-bound handling.

### Opportunity
Required: opportunity_id, schema_version, owner_ref, type, conditions, status, validity, provenance_ref.

Constraints:
- publication does not create obligation;
- owner capability does not imply unrestricted authority over participants.

### Engagement
Required: engagement_id, schema_version, subject_ref, opportunity_ref, conditions, state, started_at, ended_at, provenance_ref.

Constraints:
- engagement scope is explicit;
- participation does not expand unrelated permissions.

### Evidence
Required: evidence_id, schema_version, claim_ref, source_ref, provenance, status, validity_period, recorded_at.

Constraints:
- evidence is not decision;
- challenge, expiry and revocation preserve history;
- uncertainty remains representable.

### Decision
Required: decision_id, schema_version, subject_ref, context, evidence_refs, policy_version, impact_class, outcome, reason_code, review_status, decided_at.

Constraints:
- decision requires applicable policy basis;
- high-impact outcomes require the declared review path;
- decision does not equal execution.

### Action
Required: action_id, schema_version, decision_ref, actor_ref, target_ref, purpose, scope, executed_at, outcome, audit_ref.

Constraints:
- action requires a valid decision or explicitly permitted non-decision action class;
- execution must remain separately auditable.

### Event
Required: event_id, schema_version, event_type, actor_ref, subject_ref, occurred_at, recorded_at, context, causation_id, correlation_id, payload, provenance, integrity_metadata.

Constraints:
- event_id is idempotency key;
- event history is append-oriented;
- event interpretation is versioned.

### PolicyDecision
Required: policy_decision_id, schema_version, policy_version, subject_ref, actor_ref, purpose, scope, input_refs, outcome, reason_code, decided_at.

Constraints:
- technical capability is not policy authority;
- outcome may be permit, deny, review_required or unknown;
- policy decision is not execution.

### AuditRecord
Required: audit_id, schema_version, actor_ref, action_type, target_ref, purpose, policy_version, timestamp, integrity_metadata.

Constraints:
- audit must be purpose-bound and minimized;
- audit is not unrestricted surveillance;
- integrity failure is itself observable.

## Schema review gate

A Phase 1 schema change requires review when it changes:
- authority semantics;
- permission scope;
- subject-control rights;
- privacy classification;
- impact classification;
- provenance meaning;
- lifecycle semantics.

A field addition is not automatically a harmless extension if it changes one of these semantics.
