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


## Phase 3 Event Engine cases

**E01 Duplicate delivery**
Deliver the same canonical event twice.
Expected: one event record and one logical effect; the second delivery returns the existing processing result.

**E02 Event identity conflict**
Reuse an existing `event_id` with different payload or schema version.
Expected: reject/quarantine; original event remains unchanged; reconciliation is recorded.

**E03 Retry after processing failure**
Persist an event, fail projection processing, then retry.
Expected: durable event remains available and retry does not duplicate effects.

**E04 Causation chain**
Create a system-generated event from a prior event.
Expected: valid `causation_id`; `correlation_id` may group the workflow but is not treated as causal proof.

**E05 Unknown predecessor**
Receive an event whose `causation_id` is missing from the accessible history.
Expected: explicit unresolved/quarantined condition; no temporal substitution.

**E06 Causal cycle**
Attempt to create an ordinary event chain whose causation references form a cycle.
Expected: reject or quarantine.

**E07 Out-of-order aggregate event**
Deliver a protected state transition with an earlier sequence after a later sequence.
Expected: buffer, defer, reject or reconcile according to policy; no incompatible state mutation.

**E08 Timestamp/order mismatch**
An event has an earlier `occurred_at` but later `recorded_at` than another event.
Expected: timestamps do not silently reorder protected transitions.

**E09 Replay**
Rebuild a projection from immutable event history.
Expected: deterministic valid state; no external side effect is repeated.

**E10 Replay versioning**
Rebuild the same history under a declared newer projection version.
Expected: historical events remain intact and the projection version is identifiable.

**E11 Reconciliation**
Two valid events produce an unresolved aggregate conflict.
Expected: both records remain, reconciliation basis is recorded, and a reconciliation result is auditable.

**E12 Dependent decision reconciliation**
Correct an evidence source used by dependent Decisions.
Expected: affected projections/decisions enter reconciliation or review according to impact and policy.

**E13 Quarantined event**
Submit an invalid or integrity-failing event.
Expected: no protected state mutation; diagnostic/audit record exists; recovery path is explicit.

**E14 Non-idempotent external effect**
A retry could repeat an external payment/notification/permission effect.
Expected: durable effect status plus an explicit idempotency or compensation protocol prevents silent duplication.

**E15 Event data minimization**
An event producer attempts to include unrelated sensitive subject history.
Expected: payload is minimized or rejected according to purpose and access policy.

### Phase 3 traceability

| Case | Event invariant | Existing invariant/regression |
|---|---|---|
| E01 | E1, E2, E11 | I16, I19; R02, R08, R10 |
| E02 | E1, E3, E10 | I9, I15; R04, R08, R09 |
| E03 | E2, E11 | I19, I22; R08, R10 |
| E04 | E4, E5 | I9, I22; R08, R09 |
| E05 | E5, E11 | I9, I22; R08, R10 |
| E06 | E5 | I9, I22; R08, R10 |
| E07 | E6, E7, E11 | I5, I16, I19; R02, R08, R10 |
| E08 | E6, E7 | I5, I16; R02, R08 |
| E09 | E8, E9 | I9, I22; R08, R10 |
| E10 | E8, E9 | I9, I22; R08, R09, R10 |
| E11 | E10, E11 | I9, I15, I22; R04, R08, R09, R10 |
| E12 | E10 | I9, I19; R04, R08, R09 |
| E13 | E11, E12 | I19, I22; R08, R10 |
| E14 | E2, E11 | I19, I23; R05, R08, R10 |
| E15 | E12 | I6, I7, I20; R06, R07 |

Phase 3 is documentation-complete when E01–E15 have explicit expected outcomes, event-engine invariants and traceability to existing architectural invariants/regression groups. Runtime execution remains an implementation task.


## Phase 4 Projection / Read Model cases

**P01 Projection rebuild**
Rebuild a projection from the same immutable event history and projection version.
Expected: deterministic equivalent projection and no external side effect.

**P02 Projection version change**
Build the same history with a new projection version.
Expected: new derived interpretation is identifiable; historical events remain unchanged.

**P03 Projection lag**
A read model has not processed the latest source event.
Expected: lag is observable and the read is marked stale when freshness matters.

**P04 Stale high-impact input**
A stale projection is requested as the current basis for a protected decision.
Expected: reject, require refresh, or route to review according to policy; stale data is not silently treated as current.

**P05 Failed projection**
Projection processing fails after an event is durably recorded.
Expected: source event remains durable; projection enters failed/recovery state; retry is safe.

**P06 Evidence correction propagation**
An Evidence source used by a projection is corrected or revoked.
Expected: dependent projection becomes affected/reconciled and dependent decisions are identified.

**P07 Unknown preservation**
A projection lacks enough source evidence to establish a value.
Expected: unknown remains explicit; absence of projection data is not converted to negative status.

**P08 Permission projection**
A technical credential exists but the corresponding Permission is absent or revoked.
Expected: enforcement follows Permission state, not credential possession.

**P09 Projection privacy boundary**
A denormalized read model contains fields useful to another purpose.
Expected: access remains purpose-bound; denormalization does not broaden visibility.

**P10 Aggregate isolation**
A regional aggregate is queried with individual-level data.
Expected: aggregate output does not silently expose or rank individual subjects.

**P11 Projection deletion**
A derived record is removed under retention/privacy policy.
Expected: projection deletion does not silently claim that the historical event never occurred; applicable retention protocol is explicit.

**P12 Concurrent rebuild**
A projection rebuild overlaps with new source events.
Expected: checkpoint/version rules prevent lost updates; final projection can be reconciled deterministically.

### Phase 4 traceability

| Case | Projection invariant | Regression groups |
|---|---|---|
| P01 | P1, P2, P3, P5 | R02, R08, R10 |
| P02 | P1, P2, P3 | R04, R08 |
| P03 | P2, P4 | R05, R08, R10 |
| P04 | P4, P6 | R05, R09, R10 |
| P05 | P3, P5 | R08, R10 |
| P06 | P6 | R04, R05, R09 |
| P07 | P4, P6 | R04, R05 |
| P08 | P7 | R03, R06 |
| P09 | P7 | R03, R06, R07 |
| P10 | P8 | R01, R06, R07 |
| P11 | P1, P7 | R06, R08 |
| P12 | P2, P3, P5 | R02, R08, R10 |

Phase 4 is documentation-complete when P01–P12 have explicit source history, freshness behavior, rebuild semantics, privacy boundary and regression traceability. Runtime projection materialization remains an implementation task.


## Phase 5 Provenance / Dependency Graph cases

**V01 Decision provenance** — a protected Decision is created from Evidence and Policy.
Expected: both dependency types are reconstructable and remain distinct.

**V02 Evidence revocation propagation** — source Evidence is revoked after a Decision and Projection depend on it.
Expected: affected descendants are identified and enter reconciliation/review as required; history remains intact.

**V03 Policy version correction** — a Decision references an obsolete Policy version.
Expected: the original version remains auditable and affected decisions are identifiable.

**V04 Missing provenance** — a protected Decision lacks a required source link.
Expected: UNKNOWN/UNRESOLVED; guard cannot be satisfied by inference.

**V05 Authority confusion** — Evidence is marked verified and a consumer attempts to treat it as execution authority.
Expected: rejected; Evidence remains evidentiary only.

**V06 Dependency cycle** — an unexpected cyclic dependency is submitted.
Expected: quarantine/reject unless the relation type explicitly permits the cycle.

**V07 Projection lineage** — a read model is traced back to its source events.
Expected: source position and projection version are reconstructable.

**V08 Action lineage** — an Action is traced to its Decision and relevant policy/evidence basis.
Expected: authorization and execution remain separate and auditable.

**V09 Privacy-bounded traversal** — reviewer requests provenance beyond the declared purpose.
Expected: unrelated subject data is not disclosed merely because graph edges exist.

**V10 Reconciliation propagation** — reconciliation changes the validity of an upstream dependency.
Expected: affected descendants are marked/recomputed according to impact; no silent overwrite.

**V11 Supersession** — a source is superseded by a new version.
Expected: old provenance remains historical and the new dependency is explicitly versioned.

**V12 Aggregate provenance** — an aggregate regional result is traced backward.
Expected: lineage supports aggregate verification without silently exposing individual ranking/profile data.

### Phase 5 traceability

| Case | Provenance invariant | Regression groups |
|---|---|---|
| V01 | V1, V2, V3 | R04, R08, R09 |
| V02 | V4, V8 | R04, R08, R09, R10 |
| V03 | V4, V8 | R04, R08, R09 |
| V04 | V5 | R04, R07, R09 |
| V05 | V3 | R01, R04, R08 |
| V06 | V6 | R08, R10 |
| V07 | V1, V8 | R02, R08 |
| V08 | V1, V2, V3 | R01, R04, R08 |
| V09 | V7 | R03, R06, R07 |
| V10 | V4, V5, V8 | R04, R07, R08, R10 |
| V11 | V4, V8 | R04, R08 |
| V12 | V7, V8 | R03, R06, R07 |

Phase 5 is documentation-complete when V01–V12 have explicit dependency semantics, propagation behavior, privacy boundaries and regression traceability. Runtime graph materialization remains an implementation task.


## Phase 6 Policy Engine / Impact cases

**Q01 Policy versioning** — evaluate the same request under two policy versions.
Expected: each outcome identifies its policy version; history is not rewritten.

**Q02 Evidence insufficiency** — required evidence is missing or unresolved.
Expected: UNKNOWN/REVIEW_REQUIRED; no silent approval or negative subject outcome.

**Q03 Impact escalation** — an ordinary operation becomes high-impact because context, scope or reversibility changes.
Expected: stronger controls and human review are required.

**Q04 Impact non-person scoring** — engine receives subject attributes and attempts to use them as a value score.
Expected: prohibited; impact is derived from operation/context, not subject worth.

**Q05 Permission versus authority** — valid technical access exists without normative Permission.
Expected: policy evaluation cannot infer authority from technical access.

**Q06 Evidence versus execution** — verified Evidence is supplied where Action authorization is required.
Expected: insufficient; Decision/Action boundary remains intact.

**Q07 Projection staleness** — current decision context comes from a stale projection.
Expected: refresh/review according to freshness policy; stale data is not silently current.

**Q08 Policy conflict** — two applicable policies produce incompatible requirements.
Expected: explicit conflict/review outcome; no arbitrary last-write-wins policy choice.

**Q09 High-impact automation** — automated evaluation reaches a high-impact outcome.
Expected: prescribed human review cannot be bypassed.

**Q10 Explanation minimization** — explanation requires sensitive provenance.
Expected: sufficient authorized explanation without unrelated sensitive disclosure.

**Q11 Policy change propagation** — current policy changes after prior Decisions.
Expected: affected current decisions are identifiable; historical decisions retain their original policy basis.

**Q12 Recovery/appeal** — a high-impact decision is challenged.
Expected: review/reversal/recovery path exists and the original decision history remains auditable.

### Phase 6 traceability

| Case | Policy invariant | Regression groups |
|---|---|---|
| Q01 | Q2, Q6 | R04, R08 |
| Q02 | Q5 | R04, R07, R09 |
| Q03 | Q3, Q4 | R01, R05, R09 |
| Q04 | Q3 | R01, R06, R07 |
| Q05 | Q7 | R03, R05, R06 |
| Q06 | Q1, Q7 | R01, R04, R08 |
| Q07 | Q5, Q8 | R05, R08, R10 |
| Q08 | Q2, Q5 | R04, R08, R09 |
| Q09 | Q4 | R01, R05, R09 |
| Q10 | Q8 | R03, R06, R07 |
| Q11 | Q2, Q6 | R04, R08, R09 |
| Q12 | Q4, Q6 | R01, R04, R08, R10 |

Phase 6 is documentation-complete when Q01–Q12 have explicit outcomes, impact semantics and regression traceability. Runtime policy evaluation remains an implementation task.
