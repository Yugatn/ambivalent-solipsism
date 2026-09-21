# Согласованность и конкурирующие изменения

СТСеть должна определять, как обрабатываются одновременные изменения одного объекта.

## 1. Optimistic concurrency

Для защищённых сущностей используется версия состояния.

Изменение старой версии не должно молча перезаписывать более новое изменение.

## 2. Conflict

Конфликт фиксируется явно и передаётся в определённую стратегию разрешения.

## 3. Last-write-wins

Последняя запись не является универсальным механизмом разрешения конфликтов.

Для прав, выплат, статусов и решений требуется контекстная политика.

## 4. Ordering

Порядок событий определяется только там, где он имеет смысл для конкретной сущности.

## 5. Causality

Causation и temporal order различаются.

Позднее зарегистрированное событие может относиться к более раннему моменту фактического события.

## 6. Duplicate and replay

Повторное событие и повторная доставка старого события должны быть безопасны.

## 7. Reconciliation

После разрешения конфликта система проверяет зависимые решения, если конфликт мог изменить их основание.

## Principle

> Согласованность данных не должна достигаться ценой незаметной потери истории.


## Phase 4 Projection / Read Model contract

Projection is a derived read representation built from immutable Event History. It is an optimization and query boundary, not a replacement source of truth.

### 1. Source of truth

- Event History is authoritative for recorded historical occurrences.
- State is a current projection of applicable events.
- Projection data MUST be rebuildable from the relevant event history and declared projection version.
- A projection MUST NOT invent historical events or silently modify their meaning.

### 2. Projection identity

Every projection MUST identify:

- aggregate/subject scope;
- projection name and version;
- source event position or checkpoint;
- last successfully applied event identity;
- rebuild/reconciliation status;
- materialization timestamp.

### 3. Read consistency

The system MUST declare the consistency expected by each read model: strong/transactional where required, otherwise explicitly eventual.

A stale projection MUST NOT be presented as current for decisions where freshness is a protected condition. If freshness cannot be established, the result is stale/unknown or routed to review according to policy.

### 4. Projection lag

Projection lag is observable metadata, not a hidden failure. A consumer MUST be able to distinguish:

- current projection;
- stale projection;
- rebuilding;
- failed/quarantined projection;
- reconciled projection.

### 5. Rebuild and replay

Rebuild starts from immutable history and a declared projection version. It MUST be deterministic for the same history, version and configuration. Rebuild MUST NOT execute external Actions.

A new projection version creates a new derived interpretation; it does not rewrite historical events.

### 6. Corrections and reconciliation

When an upstream Evidence or event is corrected, dependent projections are marked affected and rebuilt or reconciled according to impact. Last-write-wins is not sufficient for protected decisions, permissions, payments or rights.

### 7. Query isolation

A read model may denormalize data for performance, but denormalization MUST NOT silently broaden privacy scope. Projection access remains subject to Permission, purpose limitation and minimization.

### 8. Aggregate analytics

Aggregated regional/system views MUST remain distinguishable from individual subject profiles. A projection designed for aggregate analysis MUST NOT silently become an individual ranking surface.

### 9. Phase 4 invariants

- P1: Event History remains the historical source of truth.
- P2: every projection is versioned and traceable to its source position.
- P3: projection state is rebuildable from event history.
- P4: stale data is explicitly distinguishable from current data.
- P5: replay/rebuild does not execute external side effects.
- P6: corrected upstream facts propagate to affected projections and dependent decisions.
- P7: projection denormalization does not create new authority or privacy scope.
- P8: aggregate analytics does not silently become individual profiling.

Phase 4 runtime materialization remains an implementation task.
