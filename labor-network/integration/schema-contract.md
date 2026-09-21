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
