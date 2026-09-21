# Протокол событий СТСети

## 1. Назначение

Событие фиксирует изменение, имеющее значение для состояния, полномочий, provenance или аудита.

Минимальное событие содержит:

- event_id;
- event_type;
- actor;
- subject;
- occurred_at;
- recorded_at;
- context;
- schema_version;
- causation_id, если событие вызвано другим событием;
- correlation_id для связывания одной операции;
- payload;
- provenance;
- integrity metadata.

## 2. Типы событий

Базовый набор:

- Created;
- Updated;
- Confirmed;
- Challenged;
- Revoked;
- Expired;
- Restricted;
- Restored;
- Completed.

## 3. Время

occurred_at описывает время события, а recorded_at — время его регистрации. Они не должны автоматически считаться одинаковыми.

## 4. Причинность

causation_id связывает событие с непосредственной причиной. correlation_id объединяет события одной операции.

## 5. Дубликаты

event_id уникален. Повторная доставка уже принятого события должна быть идемпотентной.

## 6. Конфликты

Конфликтующие события не должны разрешаться молчаливым выбором последнего значения. Для сущности определяется явная политика разрешения конфликта.

## 7. Существенные последствия

Событие, способное создать существенное необратимое последствие, проходит дополнительную policy-проверку до применения последствия.

## 8. Версия

Изменение схемы события не должно незаметно менять смысл старых событий.


## Phase 3 Event Engine contract

Phase 3 defines execution semantics for the append-only event log. Projections, state transitions and side effects consume events but never rewrite historical events.

### Canonical event envelope

Every accepted event MUST contain: `event_id`, `event_type`, `schema_version`, actor/source, affected subject or aggregate reference, `occurred_at`, `recorded_at`, context/purpose, `causation_id` when applicable, `correlation_id`, payload, provenance and integrity metadata. A partition or aggregate ordering key MAY be added. Timestamps alone MUST NOT define ordering.

### Immutability and idempotency

An accepted event is immutable. One `event_id` identifies one canonical payload and schema version. Re-delivery of equivalent content returns the existing processing result without repeating state changes or side effects. Reuse of an `event_id` with conflicting content is quarantined and audited; it MUST NOT overwrite history.

Idempotency applies both to event acceptance and effect application. Retry state MUST distinguish completed operations from operations that never completed and MUST be deterministic for the same event and processing version.

### Causality

`causation_id` identifies the immediate causal predecessor; `correlation_id` groups a wider workflow and does not itself establish causality. Causal chains remain auditable. Unknown or quarantined predecessors are explicit and are never silently replaced by temporal assumptions. Ordinary causal chains MUST be acyclic.

### Ordering

The system does not assume one global event order. Aggregates requiring sequential transitions MUST use an explicit per-aggregate mechanism such as sequence numbers or expected-version checks. Out-of-order events MUST be buffered, deferred, rejected or reconciled according to explicit policy; they MUST NOT be silently applied against incompatible state.

### Replay

Replay reconstructs projections from immutable history using a declared projection version. Replay MUST NOT repeat external side effects such as payments, notifications or permission grants. Historical event meaning remains recoverable when projection rules change.

### Reconciliation

Reconciliation handles missing, conflicting, late, duplicated or semantically incompatible events. It preserves original records, identifies the affected aggregate, records evidence and policy, produces an auditable reconciliation result/event, re-evaluates dependent projections or decisions when required, and provides recovery without deleting history. It MUST NOT silently use last-write-wins for rights, payments, permissions, protected statuses or decisions.

### Failure and recovery

Invalid events are rejected or quarantined with diagnostic/audit records. A failed transition MUST NOT appear successful merely because the event was appended. If persistence succeeds but projection/effect processing fails, the event remains durable and can be retried safely. Non-idempotent external effects require durable execution status and compensation/recovery rules.

### Security and data minimization

Event payloads contain only data necessary for the declared purpose. Sensitive data MUST NOT be copied merely for convenience. Event visibility, technical access and Permission remain separate; auditability MUST NOT become unrestricted surveillance.

### Phase 3 invariants

- E1: one `event_id` identifies one immutable canonical event.
- E2: duplicate delivery produces no duplicate logical effect.
- E3: conflicting reuse of an `event_id` cannot overwrite history.
- E4: causation and correlation remain distinguishable.
- E5: causal lineage remains auditable.
- E6: protected aggregate ordering is explicit and deterministic.
- E7: timestamps do not silently define causal/order semantics.
- E8: replay reconstructs state without repeating external side effects.
- E9: historical event meaning remains recoverable across projection versions.
- E10: reconciliation preserves source history and records its own outcome.
- E11: failed processing is retryable or recoverable without silent history loss.
- E12: event data remains purpose-bound and access-controlled.

Phase 3 runtime execution remains an implementation task. This contract is the canonical architectural basis for idempotency, causality, ordering, replay and reconciliation tests.
