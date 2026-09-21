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
