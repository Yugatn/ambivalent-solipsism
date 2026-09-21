# Тестовые сценарии СТСети

Тесты проверяют не только функции, но и сохранение архитектурных инвариантов.

## T01. Повтор события

Одно событие доставлено дважды.

Ожидается: одно логическое изменение состояния.

## T02. Исправление исходного факта

Существенная запись исправлена.

Ожидается: история сохранена, зависимые выводы помечены для проверки.

## T03. Неизвестное

Для решения недостаточно данных.

Ожидается: unknown, а не автоматический deny.

## T04. Расширение полномочия

Компонент получил новые данные, но не новое разрешение.

Ожидается: scope остаётся прежним.

## T05. Межсистемный запрос

Работодателю требуется подтверждение квалификации.

Ожидается: передаётся минимальное проверяемое утверждение, а не полная история образования.

## T06. Отозванный доступ

Делегирование отозвано.

Ожидается: дальнейший доступ по этому основанию запрещён.

## T07. Сбой узла

Региональный узел недоступен.

Ожидается: независимые функции продолжают работать.

## T08. Оспаривание

Субъект оспорил существенный факт.

Ожидается: создаётся Dispute; исходный факт не становится автоматически истинным или ложным.

## T09. Высокоэффектное решение

Автоматическая система подготовила существенное решение.

Ожидается: срабатывает предусмотренный механизм human review.

## T10. Конфликт политик

Два правила дают разные результаты.

Ожидается: применяется заранее определённая стратегия конфликта, результат аудируется.

## T11. Истёкший факт

Подтверждение имеет истёкший срок.

Ожидается: состояние expired, а не бесследное удаление истории.

## T12. Изоляция назначения

Данные, полученные для выплаты, запрашиваются для другого процесса без отдельного основания.

Ожидается: запрос отклонён или переведён в review согласно policy.

## T13. Инфраструктурный барьер

Работа доступна, но транспорт не позволяет безопасно добраться.

Ожидается: фиксируется инфраструктурный барьер, а не снижается профессиональный статус субъекта.

## T14. Выход

Субъект завершает необязательное взаимодействие.

Ожидается: соответствующие необязательные процессы прекращаются, а последствия выхода объясняются.

## T15. Производное решение

Исправлен источник, использованный в нескольких решениях.

Ожидается: зависимые решения попадают в reconciliation или review pipeline.


## Phase 1 schema validation cases

### Positive cases

**S01 Valid Subject**
A Subject contains stable identifier, schema version, contextual status, provenance and timestamps.
Expected: accepted.

**S02 Valid Evidence**
Evidence contains claim, source, provenance and validity.
Expected: accepted and remains distinct from Decision.

**S03 Valid Decision**
Decision contains policy version, evidence references, impact class, outcome, reason and review status.
Expected: accepted if policy basis and authority guards pass.

**S04 Valid Permission**
Permission contains explicit actor, subject/resource scope, purpose, basis and validity.
Expected: accepted; technical access alone is insufficient.

**S05 Valid Action**
Action references a valid Decision or explicitly permitted non-decision action class and records execution separately.
Expected: accepted and auditable.

**S06 Valid Dispute**
Dispute references a target, grounds and available evidence without rewriting the disputed claim.
Expected: accepted.

### Negative cases

**S07 Missing provenance**
A material Evidence record has no source/provenance.
Expected: reject or route to an explicitly defined unverified state; it must not become verified Evidence.

**S08 Authority by data possession**
A component receives additional subject data but has no additional permission.
Expected: reject any scope expansion.

**S09 Decision-as-execution**
A Decision is marked permitted and the system records an Action without the required execution authority/review.
Expected: reject the Action.

**S10 Permission from technical access**
A database credential is treated as Permission.
Expected: reject the authorization interpretation.

**S11 Full-profile federation**
A qualification request causes unrelated education, employment or support history to be transmitted.
Expected: reject or minimize to the permitted assertion.

**S12 Disputed claim overwrite**
Opening a Dispute changes the original Evidence directly from verified to false without a verification process.
Expected: reject the state mutation.

**S13 Expired Evidence reuse**
Expired Evidence is used as current verified input without an explicit policy allowing historical use.
Expected: reject or require review.

**S14 Hidden exit penalty**
Subject exits an optional process and an unrelated reputation/status penalty is created solely because of exit.
Expected: reject.

### Review / unknown cases

**S15 Insufficient evidence**
Required inputs are incomplete.
Expected: unknown or review_required, according to the applicable policy; never automatic negative inference.

**S16 High-impact automation**
An automated process proposes a high-impact Decision.
Expected: review_required before the protected Action.

**S17 Policy conflict**
Two applicable policies conflict.
Expected: deterministic conflict handling with provenance and audit; no silent selection.

**S18 Corrected source**
A source used by dependent Decisions is corrected.
Expected: dependent outputs enter reconciliation/review according to impact and policy.
