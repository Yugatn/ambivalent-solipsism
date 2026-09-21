# Migration Map СТСети

## Исходные документы

Существующие доменные материалы сохраняются как канонические источники предметного содержания.

## Новая декомпозиция

Архитектурные темы распределяются между:

- domain;
- subject;
- opportunity;
- engagement;
- evidence;
- policy;
- event;
- state;
- decision;
- dispute;
- support;
- audit;
- federation;
- review;
- verification.

## Принцип декомпозиции

Один исходный документ может соответствовать нескольким новым модулям.

Это предпочтительнее искусственного сохранения крупного документа, если новая декомпозиция делает зависимости явными.

## Обратная трассировка

Каждый новый модуль должен иметь возможность указать:

- какие исходные концепции он продолжает;
- какие новые требования добавляет;
- какие соседние модули использует.

## Canon preservation

Новая структура расширяет канон, а не подменяет его.


## Domain migration mapping

| Legacy domain concept | New module |
|---|---|
| human / participant | domain/subject.md |
| work opportunity | domain/opportunity.md |
| actual cooperation | domain/engagement.md |
| proof / qualification | domain/evidence.md |
| learning / growth | domain/development.md |
| assistance | domain/support.md |
| employer | domain/employer.md |
| regional planning | domain/regional-development.md |
| professional reputation | domain/reputation.md |
| independent work | domain/self-employment.md |

These modules preserve the domain meaning while separating it from event, policy, audit and infrastructure concerns.
