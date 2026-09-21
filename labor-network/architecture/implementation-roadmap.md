# Дорожная карта реализации СТСети

## Phase 0 — Canon

Зафиксировать принципы, термины и границы проекта.

## Phase 1 — Schema

Создать машинные схемы сущностей, событий, permissions, policy decisions и audit records.

## Phase 2 — State machines

Реализовать state transitions и guard conditions.

## Phase 3 — Policy Engine

Вынести ключевые правила в тестируемый policy layer.

## Phase 4 — Event Core

Реализовать idempotency, causation, correlation, versioning и replay protection.

## Phase 5 — Provenance graph

Реализовать зависимости Evidence, Claims, Decisions и Actions.

## Phase 6 — Reconciliation

Добавить поиск зависимых решений после исправления исходных данных.

## Phase 7 — Human Review

Реализовать review queue, reason codes, сроки и результаты пересмотра.

## Phase 8 — Audit

Добавить защищённый audit trail и observability без лишнего копирования пользовательских данных.

## Phase 9 — Federation

Реализовать API-контракты и минимальные проверяемые утверждения между независимыми узлами.

## Phase 10 — Formal verification

Формализовать критические state machines и invariants.

## Phase 11 — Pilot

Пилотировать на ограниченном сценарии с обратимыми последствиями.

## Phase 12 — Expansion

Расширять функциональность только после прохождения архитектурного review и регрессионных тестов.

## Gate principle

Каждая следующая фаза должна сохранять инварианты предыдущей.


## Current implementation checkpoint

Документная и архитектурная подготовка Phase 0 завершена.

Закрыты следующие контрольные ворота:

- Canon и терминологические границы зафиксированы.
- File migration: 66/66 canonical destinations.
- Semantic migration audit: закрыт для текущего набора legacy-источников.
- Core cross-module consistency: проверена для Event, State, Evidence, Decision, Policy, Privacy, Security, Human Review и Audit.
- Regression matrix: T01–T15 связана с инвариантами и regression groups.
- Release gate: структурные проверки G1–G8 зафиксированы.
- Runtime production validation: не заявляется как выполненная.

## Next execution phase

Следующей рабочей фазой является Phase 1 — Schema.

Минимальный первый срез реализации должен включать:

1. Subject
2. Opportunity
3. Engagement
4. Evidence
5. Decision
6. Action
7. Event
8. PolicyDecision
9. AuditRecord

Для каждого объекта должны быть определены:

- стабильный идентификатор;
- версия схемы;
- provenance;
- timestamp;
- context/purpose;
- access scope;
- lifecycle/state;
- связи с событиями и решениями;
- правила исправления и отзыва там, где они применимы.

### Implementation boundary

На Phase 1 запрещается молча добавлять новые нормативные полномочия. Схема должна сначала выражать уже утверждённую архитектуру.

Новые поля, которые способны изменить полномочия, субъектный контроль, privacy scope или impact classification, требуют отдельного architectural review.

### Next gate

Phase 1 считается завершённой только после:

- schema contract review;
- invariant mapping;
- positive and negative test cases;
- проверяемой обратной совместимости там, где она требуется;
- фиксации миграции версий схемы.

После этого можно переходить к Phase 2 — State Machines.


## Current phase alignment

The roadmap numbering above is a historical planning sequence and no longer matches the completed architectural work one-to-one. The current implementation track has advanced through the following documented gates:

- Phase 0: Canon and migration — **closed** for the current 66-file migration set.
- Phase 1: Schema — **architecturally closed**; 15 canonical entity contracts, lifecycle consistency and S01–S18 validation are documented.
- Phase 2: State Machines — **architecturally closed**; state classification, protected transitions and T16–T25 are documented.
- Phase 3: Event Engine — **architecturally closed at contract/regression level**; event envelope, idempotency, causality, ordering, replay, reconciliation and E01–E15 are documented and cross-checked against G1–G8.
- Runtime execution — **not claimed**; implementation and executable validation remain future work.

### Concept and project preservation

The migration did **not** replace the broader Ambivalent Solipsism concept or its independent projects. The Social Labor Network is being developed as one applied architectural branch of the existing ecosystem.

The canonical repository root continues to contain the wider concept and project layers, including the philosophy/concept documents and project areas for PROF-MAP, PSY-TOOLS-related work, Eugene Messenger, PICCS, Symbiont, Cinema Catharsis and infrastructure/transport projects. The labor-network migration concerns the STСеть branch and its 66 legacy files; it is not a migration of the entire repository into labor-network/.

The current queue is therefore **not a backlog of untransferred concept/project files**. The remaining queue concerns implementation and cross-project integration: executable schemas, state/event runtime, policy execution, provenance/reconciliation, review, audit, federation, formal verification and pilots.

Legacy STСеть files remain preserved as non-canonical comparison material. Broader AS/project documents remain in their existing canonical project locations unless a separate migration is explicitly initiated.


## Phase 4 completion checkpoint

Phase 4 Projection / Read Model is now architecturally closed at the documentation level. The contract, projection families, Entity × Event cross-check, P01–P12 scenarios and G1–G8 release-gate traceability are present.

The next architectural layer is Provenance / Dependency Graph: making explicit which Evidence, Events, Decisions, Policies and projections depend on one another, so correction and revocation can propagate without hidden dependencies.

Runtime materialization, executable tests and production certification remain implementation work.


## Phase 6 checkpoint

Phase 6, Policy Engine / Impact Evaluation, is architecturally closed on this branch. The policy contract, structured impact classification, Q01–Q12 scenarios and G1–G8 release-gate cross-check are documented. The gate explicitly preserves separation between policy evaluation, normative Decision and executed Action; treats uncertainty as unresolved rather than as a negative subject outcome; requires human review for high-impact operations; and preserves policy-versioned history.

This checkpoint does not claim runtime certification, executable conformance, deployment readiness or production safety. Those remain implementation and integration work.

Current architectural sequence: Phase 0 Migration → Phase 1 Schema → Phase 2 State Machines → Phase 3 Event Engine → Phase 4 Projection → Phase 5 Provenance → Phase 6 Policy Engine / Impact Evaluation.


## Phase 7 checkpoint

Phase 7, Human Review, is architecturally closed on this branch. The review contract, H01–H10 scenarios and G1–G8 release-gate cross-check are documented. The architecture keeps review bounded by purpose, evidence minimization, reviewer independence, deadlines, contestability and historical traceability. Human Review cannot become unrestricted subject profiling or direct Action execution.

Runtime review queue, assignment, SLA enforcement, notification, persistence and executable conformance remain implementation work.

Current architectural sequence: Phase 0 Migration → Phase 1 Schema → Phase 2 State Machines → Phase 3 Event Engine → Phase 4 Projection → Phase 5 Provenance → Phase 6 Policy Engine / Impact Evaluation → Phase 7 Human Review.
