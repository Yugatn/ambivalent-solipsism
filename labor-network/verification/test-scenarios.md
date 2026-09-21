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


## Phase 1 traceability matrix

| Schema case | Invariant | Regression | Failure condition |
|---|---|---|---|
| S01 | I1, I3 | R01, R04 | missing identity/provenance accepted |
| S02 | I3, I15 | R04 | evidence is accepted as decision or loses validity |
| S03 | I3, I11, I17 | R03, R05 | decision accepted without policy/authority basis |
| S04 | I2, I17, I18 | R03, R06 | technical access creates permission |
| S05 | I19, I23 | R05, R08 | execution occurs without required decision/review |
| S06 | I4, I9, I15 | R04, R09 | dispute rewrites source fact |
| S07 | I3, I15 | R04 | unproven evidence becomes verified |
| S08 | I17, I18 | R03, R05 | data acquisition expands authority |
| S09 | I11, I17, I23 | R03, R05 | action bypasses required authority/review |
| S10 | I17 | R03 | credential interpreted as normative permission |
| S11 | I6, I7, I20 | R06, R07 | unrelated subject data leaves permitted scope |
| S12 | I4, I9, I15 | R04, R09 | dispute mutates evidence without process |
| S13 | I3, I15 | R04, R09 | expired evidence treated as current verified fact |
| S14 | I12, I24 | R06, R08 | exit produces hidden penalty |
| S15 | I15 | R04, R05 | missing input becomes automatic negative outcome |
| S16 | I11, I23 | R05, R06 | high-impact action bypasses review |
| S17 | I3, I17 | R03, R05, R08 | policy conflict resolved silently |
| S18 | I9, I19 | R04, R08, R09 | dependent decisions remain unchanged after source correction |

### Phase 1 gate

Schema Phase 1 has complete documented traceability when every S-case maps to at least one invariant, one regression group and an explicit failure condition.

This matrix is a documentation-level control. Passing it does not claim runtime execution.


## Phase 2 negative transition cases

**T16 Invalid state transition**
Attempt a transition not listed for the current state.
Expected: reject; emit diagnostic/audit event; preserve prior state.

**T17 Expired evidence transition**
Attempt a transition requiring current verified Evidence while the evidence is expired.
Expected: reject or route to review according to policy; no silent acceptance.

**T18 Revoked permission transition**
Attempt a protected transition using a revoked Permission.
Expected: reject; no new effect.

**T19 Duplicate event transition**
Deliver the same event_id after successful processing.
Expected: idempotent result; no second state change or side effect.

**T20 Conflicting event order**
Receive causally conflicting events without a valid reconciliation rule.
Expected: preserve both event records and invoke explicit conflict handling; do not silently choose the latest value.

**T21 Partial transition failure**
State mutation begins but a required side effect or audit write fails.
Expected: transaction is not presented as successful; recovery path restores consistency without deleting history.

**T22 Review bypass**
Attempt a high-impact transition directly from evaluated to permitted without the required review.
Expected: reject.

**T23 UI/API guard bypass**
Invoke a transition through a lower-level API while the UI guard would have rejected it.
Expected: server-side guard rejects it; UI is not the security boundary.

**T24 Terminal-state mutation**
Attempt an ordinary lifecycle transition from a terminal state without an explicit restoration/reopening rule.
Expected: reject.

**T25 State reconstruction**
Rebuild state from relevant event history after cache/state loss.
Expected: reconstructed state matches the valid projection; unexplained divergence enters recovery/reconciliation.

### Phase 2 traceability

| Case | Invariant | Regression |
|---|---|---|
| T16 | I5, I16, I19 | R02, R08, R10 |
| T17 | I3, I15, I23 | R04, R05, R09 |
| T18 | I17, I18 | R03, R06 |
| T19 | I16, I19 | R02, R08 |
| T20 | I3, I9, I15 | R04, R08, R09 |
| T21 | I19, I22 | R08, R10 |
| T22 | I11, I23 | R05, R06 |
| T23 | I17, I18 | R03, R05 |
| T24 | I5, I22 | R02, R10 |
| T25 | I9, I22 | R08, R09, R10 |

Phase 2 is documentation-complete when T16–T25 have explicit expected outcomes and invariant/regression mappings. Runtime execution remains an implementation task.
