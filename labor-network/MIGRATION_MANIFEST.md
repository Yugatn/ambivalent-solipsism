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
