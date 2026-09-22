# Доверие и provenance

Доверие в СТСети относится прежде всего к данным и процессам, а не к «хорошести» человека.

## 1. Уровни подтверждения

Сведения могут иметь разные уровни:

- заявлено;
- получено из источника;
- подтверждено документом;
- подтверждено практикой;
- подтверждено несколькими независимыми источниками;
- оспаривается.

## 2. Trust context

Доверие должно быть контекстным.

Источник может быть надёжным для одного типа сведений и неподходящим для другого.

## 3. Репутация источника

Репутация организации или подтверждающего механизма не должна автоматически превращаться в репутацию субъекта.

## 4. Цепочка происхождения

Для существенного вывода желательно сохранять цепочку:

источник → утверждение → проверка → вывод → решение.

Если звено неизвестно, это должно быть явно обозначено.

## 5. Исправления

Исправление исходной записи должно по возможности инициировать пересмотр зависимых выводов.

## 6. Неизвестное

Если происхождение не установлено, система должна хранить это как неопределённость, а не подменять её уверенностью.

## 7. Принцип

> Доверие должно быть локальным, контекстным и проверяемым.


## Phase 5 Provenance / Dependency Graph contract

The provenance layer makes explicit how Evidence, Events, Decisions, Policies, Actions and Projections depend on one another. It is a dependency model, not a value score for subjects.

### 1. Provenance node

A provenance node identifies an immutable or versioned source, including its type, identifier, version, origin, assertion time, validity interval, verification status and access/purpose constraints.

### 2. Dependency edge

A dependency edge MUST identify source node, target node, relation type, creation event and validity. Canonical relation types include `supports`, `derived_from`, `triggered_by`, `constrained_by`, `reviewed_by`, `projected_from`, `supersedes` and `reconciles`.

An edge MUST NOT imply stronger authority than the source actually has. In particular, Evidence supports a Decision but does not itself constitute permission to execute an Action.

### 3. Lineage

A Decision, PolicyDecision or protected Projection MUST be able to expose the relevant provenance chain sufficient for explanation and review. Provenance MAY be summarized for privacy, but protected dependencies MUST remain reconstructable to authorized reviewers.

### 4. Correction and revocation propagation

When a source Evidence, Event or Policy version is corrected, revoked or superseded, the graph identifies affected descendants. Descendants enter an affected/reconciliation state according to impact policy; history is preserved and no descendant is silently rewritten as though the original basis never existed.

### 5. Dependency semantics

The graph distinguishes:

- causal dependency: one event/process produced another;
- evidentiary dependency: a claim supports an evaluation;
- policy dependency: a rule constrained an evaluation;
- projection dependency: a read model was derived from source history;
- execution dependency: an Action was authorized or triggered by a Decision.

These relations MUST NOT be collapsed into one generic dependency type.

### 6. Cycles and missing provenance

Unexpected dependency cycles are invalid for acyclic provenance chains and must be quarantined or explicitly modeled when a domain requires a cycle. Missing provenance is an explicit UNKNOWN/UNRESOLVED condition, not permission to infer a source.

### 7. Privacy and minimization

Provenance exposes only the minimum chain needed for the declared purpose. A reviewer may receive sufficient lineage to verify a high-impact Decision without receiving unrelated subject history.

### 8. Phase 5 invariants

- V1: every protected Decision and Projection has reconstructable relevant provenance.
- V2: dependency relation types are semantically distinct.
- V3: provenance never creates authority that the source lacks.
- V4: correction/revocation identifies affected descendants without rewriting history.
- V5: missing provenance remains explicit UNKNOWN/UNRESOLVED.
- V6: unexpected dependency cycles cannot silently enter the canonical graph.
- V7: provenance access is purpose-bound and minimized.
- V8: provenance versions remain auditable across policy and projection changes.

Runtime graph materialization remains an implementation task.
