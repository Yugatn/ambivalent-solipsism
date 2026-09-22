# Audit и наблюдаемость

## 1. Цель

Audit позволяет восстановить существенные действия системы, не превращая наблюдаемость в постоянное наблюдение за людьми.

## 2. Аудируемые события

В первую очередь фиксируются:

- policy decisions;
- изменения полномочий;
- существенные доступы;
- изменения Evidence;
- Decisions;
- ручные пересмотры;
- исключения;
- системные ошибки.

## 3. Минимизация

Аудит хранит сведения, необходимые для доказательства действия, но не должен копировать весь контент данных без необходимости.

## 4. Неизменяемость

Критические audit events должны иметь защиту от незаметной модификации.

## 5. Доступ к аудиту

Сам аудит является защищённым ресурсом.

Доступ к нему должен быть ограничен целью и полномочиями.

## 6. Audit of automation

Автоматизированные действия должны быть различимы от человеческих.

## 7. Audit of policy

Необходимо сохранять версию policy, использованную для существенного решения.

## 8. Privacy-preserving observability

Метрики системы по возможности должны использовать агрегирование и минимизацию.

## 9. Alert ≠ violation

Алерт является сигналом для проверки, а не доказанным нарушением.

## 10. Principle

> Наблюдаемость должна делать систему проверяемой, а не человека постоянно наблюдаемым.


## Phase 8 Audit / Observability contract

Audit and observability provide evidence about significant system operations without becoming a general-purpose surveillance layer. AuditRecord is distinct from raw telemetry, application logs and subject profiling.

### 1. Purpose limitation

Every protected audit stream MUST have a declared purpose, retention basis, access scope and responsible owner. Observability data MUST NOT be retained merely because it might become useful later.

### 2. Event classes

The architecture distinguishes:

- **AuditRecord**: durable evidence of significant policy, permission, decision, review, state and protected execution events;
- **Operational telemetry**: service health, latency, capacity and reliability signals;
- **Security telemetry**: signals needed to detect compromise or unauthorized access;
- **Debug/application logs**: temporary diagnostic material subject to minimization and retention controls.

Operational and security telemetry MUST NOT silently acquire the authority or retention semantics of AuditRecord.

### 3. Minimum audit content

A protected AuditRecord SHOULD contain only what is necessary to reconstruct the relevant operation: audit id, event/action reference, actor or service identity, purpose, timestamp, policy/schema version where relevant, outcome, reason code where applicable, provenance reference and integrity metadata.

### 4. Subject boundary

Auditability does not require unrestricted reconstruction of a subject's complete history. Audit access MUST remain purpose-bound, permissioned and minimally disclosed.

### 5. Integrity

Protected audit records MUST be tamper-evident and linked to the originating Event/Decision/Action where applicable. Corrections are represented as new records or correction events; historical audit records are not silently overwritten.

### 6. Access

Audit access is itself auditable. Access to audit data does not imply permission to modify Decisions, execute Actions, expand profile scope or retrieve unrelated subject information.

### 7. Retention and deletion

Retention MUST be declared by data class and purpose. Where deletion or expiry is lawful and required, derived audit indexes MUST be handled consistently without falsifying retained historical records that have a separate lawful retention basis.

### 8. Aggregation

Aggregate observability MAY support reliability, capacity and systemic analysis, but aggregate metrics MUST NOT silently become individual ranking or hidden profiling. Individual-level drill-down requires a separate purpose and authorization.

### 9. High-impact observability

Monitoring associated with high-impact operations MUST preserve the same human-review, privacy and provenance boundaries as the operation itself. More monitoring does not create more normative authority.

### 10. Failure behavior

If the audit subsystem is unavailable, the system MUST distinguish between operations that may safely continue with deferred audit and protected operations that require durable audit before execution. Failure MUST NOT silently erase the fact that audit was unavailable.

### Phase 8 invariants

- A1: audit has explicit purpose and retention basis;
- A2: AuditRecord is distinct from unrestricted telemetry;
- A3: audit access is purpose-bound and auditable;
- A4: audit records are tamper-evident and historically traceable;
- A5: correction does not silently overwrite history;
- A6: observability cannot create authority;
- A7: aggregate analytics cannot silently become individual profiling;
- A8: high-impact monitoring preserves existing review/privacy boundaries;
- A9: audit failure has explicit safe/deferred behavior;
- A10: retention/deletion semantics are explicit and class-specific.

Runtime audit storage, integrity implementation, retention enforcement and executable conformance remain implementation work.
