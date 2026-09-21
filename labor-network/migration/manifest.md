# Migration Manifest

## Status

Перенос старой структуры labor-network/ в новую архитектуру завершён по файловому покрытию.

## File-level checkpoint

- Legacy migratable files: **66**
- Structured destinations: **66**
- Missing destinations: **0**
- Legacy deletion: **0**
- File-level coverage: **100%**
- Root README: intentionally retained as navigation index

Все исходные файлы верхнего уровня сохранены как legacy baseline. Ни один исходный файл не считается потерянным только из-за реорганизации структуры.

## Migration invariant

Если исходный файл был переработан, его предметная функция должна оставаться доступной в новой структуре.

Миграция не является механическим копированием текста. При переносе допускаются устранение дублирования, уточнение терминов, добавление связей, формализация ранее неформальных правил, сохранение исторического содержания и добавление тестируемых инвариантов.

При этом новые формальные слои не должны молча отменять исходный канон.

## Original migration baseline

На раннем checkpoint были сохранены исходные 15 файлов:

- README.md
- architecture.md
- education-and-prof-map.md
- employer-and-recruitment.md
- index.html
- principles.md
- privacy-and-state-integration.md
- professional-history.md
- professional-profile.md
- proof-of-development.md
- regional-development.md
- reputation.md
- self-employed.md
- subject-and-motivation.md
- work-conditions.md

Новая структура впоследствии расширена до 66 migratable legacy-файлов с отдельными canonical destinations.

## New formal layers

Новая структура дополняет исходные материалы следующими слоями:

1. domain modules;
2. data governance;
3. event protocol;
4. entity model;
5. state machines;
6. state transition specification;
7. policy engine;
8. safety kernel;
9. provenance;
10. reconciliation graph;
11. human review;
12. audit and observability;
13. machine contracts;
14. federation contract;
15. invariants;
16. decision lifecycle;
17. subject control;
18. consistency model;
19. formal verification;
20. implementation roadmap.

## Canonical architecture

The structured architecture separates:

1. Domain
2. Policy
3. Governance
4. Event
5. Evidence
6. State
7. Decision
8. Action
9. Audit
10. Privacy
11. Support
12. Regional
13. Security
14. Verification
15. Integration
16. Migration

The legacy files remain unchanged as a comparison and backup layer until content-level migration is verified.

## Semantic audit

The migration now operates at content level rather than filename level.

Control documents:

- [Legacy Crosswalk](legacy-crosswalk.md)
- [Content Audit](content-audit.md)
- [Semantic Checklist](semantic-checklist.md)
- [Traceability Matrix](traceability-matrix.md)
- [Semantic Audit](semantic-audit.md)

A semantic block may be distributed across several new modules. This is valid only when its meaning, constraints and relationships remain traceable.

### Audit classifications

A substantive legacy block may be classified as:

- preserved;
- refined;
- merged;
- decomposed;
- extended;
- intentionally indexed;
- pending.

No substantive block may be silently lost.

## Completion criterion

Migration reaches semantic completion only when:

- every legacy file has been reviewed;
- every substantive legacy section has a canonical destination;
- every non-trivial semantic block has traceability;
- every intentional refinement preserves the original constraint;
- no canonical principle is lost;
- regression tests cover migrated requirements;
- cross-module consistency has been checked;
- legacy can be made read-only without losing required project semantics.

Until these conditions are met, legacy files must remain preserved.

## Current audit checkpoint

File-level migration is **100% complete**.

Pairwise semantic verification is closed for the identified 66-file migration set. Verified pairs and intentional refinements are recorded in `migration/semantic-audit.md`.

The migration and semantic gates are closed. Runtime execution is intentionally not claimed by this documentation. Future work proceeds as versioned architecture development and must use the canonical modules and regression suite.
