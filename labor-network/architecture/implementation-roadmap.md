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
