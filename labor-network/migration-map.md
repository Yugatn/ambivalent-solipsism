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


## Policy migration mapping

Legacy rules concerning access, recruitment, development, support, regional planning, federation and review are now separated into the policy layer.

This prevents domain entities from carrying their own authorization logic and makes policy versioning explicit.

| Concern | Destination |
|---|---|
| permissions | policy/authority.md |
| data visibility | policy/data-access.md |
| recruitment rules | policy/recruitment.md |
| development rules | policy/development.md |
| support conditions | policy/support.md |
| regional rules | policy/regional-development.md |
| inter-node exchange | policy/federation.md |
| human review | policy/review.md |
