# Migration Manifest СТСети

## Статус

Перенос старой структуры labor-network/ в новую архитектуру завершён по файловому покрытию.

На ветке main было 15 файлов в labor-network/.

На ветке feature/labor-network-v2 сохранены все 15 исходных файлов и добавлены 47 новых архитектурных и формальных модулей.

## Инвариант миграции

Ни один исходный файл не считается потерянным только из-за реорганизации структуры.

Если исходный файл был переработан, его предметная функция должна оставаться доступной в новой структуре.

## Сохранённые исходные модули

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

## Новые формальные слои

Новая структура дополняет исходные материалы:

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

## Правило улучшения

Миграция не является механическим копированием текста.

При переносе допускается:

- устранение дублирования;
- уточнение терминов;
- добавление связей;
- формализация ранее неформальных правил;
- сохранение исторического содержания;
- добавление тестируемых инвариантов.

При этом новые формальные слои не должны молча отменять исходный канон.

## Следующая проверка

Следующий этап — content-level audit: проверить, что каждый исходный смысловой блок представлен в новой структуре, а не только каждый исходный filename.


## Final migration architecture

The new structure now separates:

1. Domain
2. Policy
3. Event
4. Evidence
5. State
6. Decision
7. Action
8. Audit
9. Privacy
10. Support
11. Regional
12. Security
13. Verification
14. Integration

The legacy files remain unchanged as a backup layer until content-level migration is verified.

## Completion criterion

Migration reaches 100% only when:

- every legacy file has been reviewed;
- every substantive section has a destination;
- every destination has traceability;
- no canonical principle is lost;
- regression tests cover the migrated requirements;
- legacy bridge can be made read-only.

Until these conditions are met, legacy files must remain preserved.
