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

Минимально: decision_id, subject_ref, context, evidence_refs, policy_version, impact_class, outcome, reason_code, review_status. Decision не содержит обязательного action; фактическое исполнение описывается отдельным Action.

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


## Phase 1 consistency findings

The schema review identified and resolved one architectural ambiguity:

- Decision previously referenced an action as a required field.
- The canonical architecture separates Decision from Action.
- Decision therefore records the permitted or denied consequence and its basis; Action records actual execution separately.
- A Decision may optionally reference a planned effect, but execution is never implied by the existence of a Decision.

The following entities remain part of the broader canonical entity model and require contracts in subsequent schema slices:

- Organization
- Dispute
- Support
- Resource
- Permission
- Relation

They are not removed by the nine-object Phase 1 core. Their contracts must preserve the same authority, provenance, privacy, lifecycle and audit invariants.

## Entity/Event consistency rule

The Entity × Event matrix is normative for protected lifecycle events. Every schema object participating in a stateful lifecycle must map its mutating events to:

1. source/actor;
2. guard;
3. resulting state;
4. invariant;
5. audit requirement;
6. recovery path.

State machines remain projections of event history and cannot silently introduce state changes without an event or explicitly defined system process.


## Phase 1 extended entity contracts

### Organization
Required: organization_id, schema_version, type, status, provenance_ref, created_at, updated_at.
Constraints:
- organizational role is contextual;
- ownership or technical administration does not create unrestricted authority over subjects;
- organization status is not a subject-value score.

### Permission
Required: permission_id, schema_version, subject_ref, actor_ref, purpose, scope, basis, granted_at, expires_at, status, provenance_ref.
Constraints:
- permission is purpose-bound and scope-bound;
- expiry/revocation are explicit;
- technical access is not equivalent to permission;
- permission cannot silently broaden through federation.

### Dispute
Required: dispute_id, schema_version, subject_ref, object_ref, opened_at, status, grounds, evidence_refs, resolution_ref, provenance_ref.
Constraints:
- opening a dispute does not establish the disputed claim as true or false;
- disputed evidence remains distinguishable from verified evidence;
- resolution is separately attributable and auditable.

### Support
Required: support_id, schema_version, subject_ref, program_ref, purpose, eligibility_basis, status, started_at, ended_at, provenance_ref.
Constraints:
- support eligibility is contextual;
- support status is not a reputation score;
- support systems cannot silently become disciplinary systems.

### Resource
Required: resource_id, schema_version, owner_ref, type, availability, access_policy_ref, provenance_ref, created_at, updated_at.
Constraints:
- resource ownership does not imply authority over unrelated subjects;
- access follows explicit policy;
- availability and access permission remain separate concepts.

### Relation
Required: relation_id, schema_version, source_ref, target_ref, relation_type, context, validity, provenance_ref, created_at, updated_at.
Constraints:
- a relation is contextual evidence of a connection, not a value judgment;
- relation validity may expire;
- derived relations must retain derivation provenance.

## Extended schema review gate

The same review requirements apply to these six entities. Changes affecting authority, purpose, scope, privacy, subject control, provenance, lifecycle or impact classification require architectural review.

The extended entities do not alter the nine-object core contract and must remain interoperable with Event, State, Decision, Action, Policy and Audit.
