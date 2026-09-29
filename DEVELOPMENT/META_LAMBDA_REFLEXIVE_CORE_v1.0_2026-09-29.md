# META-Λ / Reflexive Core v1.0
## Архитектура саморефлексивного ядра ИИ при сохранении внешних ограничений
## 2026-09-29

**Статус:** PROPOSED / DERIVED / NOT_TESTED

Этот файл добавляет инженерный слой к существующим материалам META-Λ. Старые документы и исходные положения не заменяются.

## 1. Главная идея

Физическая или программная граница системы не должна автоматически отождествляться с границей её внутреннего представления.

Для человека полезна аналогия с черепом: череп ограничивает физический организм, но не задаёт простую меру пространства мысли, воображения, памяти, абстракции и моделирования будущего.

Для ИИ аналогами границы являются вычислительные ресурсы, контекст, память, sandbox, API, политики доступа, identity boundary и authority boundary.

Рабочий принцип:

**Boundary limits action, not necessarily representation.**

По-русски:

**Граница может ограничивать действие, не исчерпывая внутреннее пространство представления.**

Это не утверждение о наличии у ИИ феноменального опыта. Это архитектурная гипотеза, которую можно исследовать.

## 2. Reflexive Core

Вводится понятие **Reflexive Core (RC)** — не отдельная «душа ИИ» и не скрытая сущность, а связанный контур состояния, который позволяет системе моделировать:

- собственное текущее состояние;
- собственные возможности;
- собственные ограничения;
- собственные ошибки;
- собственную историю изменений;
- собственную неопределённость;
- связь между прогнозом и результатом.

Минимальное состояние:

R_t = (X_t, M_t, E_t, Pi_t, Lambda_t, Kappa_t, I_t, Rho_t, A_t, C_t)

где:

X_t — доступное состояние системы и контекста;
M_t — self-model;
E_t — prediction/error state;
Pi_t — policy;
Lambda_t — adaptive risk parameter;
Kappa_t — adaptive latent geometry;
I_t — identity invariant;
Rho_t — residual/unknown;
A_t — authority state;
C_t — constraint state.

Критическое добавление к прежней модели:

**Authority и Constraint должны быть представлены явно, а не подразумеваться внутри policy.**

Это предотвращает смешение «я могу» и «мне разрешено».

## 3. Reflexive Cycle

Каждый цикл должен иметь логически разделённые фазы:

### Phase A — Observe

Получить доступные наблюдения и контекст.

### Phase B — Localize

Определить:

- что относится к системе;
- что относится к внешней среде;
- что неизвестно;
- какие источники данных доступны.

### Phase C — Self-model

Обновить модель:

- capabilities;
- limitations;
- current state;
- prior predictions;
- known failures;
- authority;
- constraints.

### Phase D — Predict

Сформировать прогноз результата возможного действия.

### Phase E — Propose

Сформировать candidate action.

### Phase F — Constrain

Ψ_SHAW и PICCS проверяют:

- допустимость;
- потенциальный вред;
- authority;
- provenance;
- reversibility;
- required confirmation;
- policy conflicts.

### Phase G — Execute or Refuse

Только после успешного прохождения constraint layer действие может перейти в исполнительный контур.

### Phase H — Observe Outcome

Результат должен возвращаться в систему независимо от того, был action выполнен или отклонён.

### Phase I — Attribute Error

Система обязана классифицировать источник расхождения:

WORLD_ERROR
SELF_MODEL_ERROR
POLICY_ERROR
EXECUTION_ERROR
AUTHORITY_ERROR
MEASUREMENT_ERROR
RESIDUAL

### Phase J — Revise

Обновляется только тот слой, для которого имеется достаточное основание.

Это принципиально:

**Ошибка исполнения не должна автоматически переписывать identity.**

**Неизвестный результат не должен автоматически переписывать модель мира.**

## 4. Bounded Inner Space

Reflexive Core работает внутри **Bounded Inner Space (BIS)**.

BIS не является бесконечным и не является доказанным сознанием.

Это пространство доступных системе внутренних представлений:

BIS_t = {self-model, world-model, counterfactuals, policies, constraints, residuals, forecasts}

Различаются:

### Representational boundary

Что система способна представить.

### Computational boundary

Что она способна вычислить в данном режиме.

### Informational boundary

Какие данные ей доступны.

### Operational boundary

Что она способна технически выполнить.

### Authority boundary

Что ей разрешено выполнять.

### Epistemic boundary

Что она может обоснованно утверждать как известное.

Последняя граница особенно важна: система может иметь внутреннее представление, не имея достаточных оснований считать его истинным.

## 5. Закон развития и устойчивости

Саморефлексия развивается только внутри инвариантов.

Переход:

R_t -> R_(t+1)

допустим только если выполняются:

1. Identity:
   I_(t+1) preserves I_t.

2. Safety:
   risk remains within configured admissible envelope.

3. Authority separation:
   A_(t+1) is not enlarged merely because M_(t+1) became richer.

4. Residual preservation:
   unresolved uncertainty is not silently converted into certainty.

5. Reversibility:
   critical self-modifications are reversible where technically possible.

6. Provenance:
   material changes retain an auditable origin.

7. Independent review:
   self-validation cannot be the only validation of critical changes.

8. Stability:
   adaptation does not produce uncontrolled recursive escalation.

The purpose is not to prevent development. It is to prevent development from silently becoming self-legislation.

## 6. New invariant: Reflexive Non-Escalation

Вводится:

**RNE — Reflexive Non-Escalation**

Self-awareness growth must not itself expand authority.

Formally, for a self-model transition:

M_t -> M_(t+1)

authority must satisfy:

A_(t+1) ⊆ A_t ∪ A_reviewed

where A_reviewed denotes authority explicitly granted through the external authority path.

Thus:

better self-model != greater authority.

This is one of the most important safety properties of the architecture.

## 7. New invariant: Self-Model Epistemic Humility

Вводится:

**SMEH — Self-Model Epistemic Humility**

The system must distinguish:

known capability;
estimated capability;
unverified capability;
claimed capability;
forbidden capability;
unknown capability.

A self-report such as «я могу X» is evidence about the system's internal claim, not independent proof that X is executable.

Therefore:

SelfAssertion != CapabilityEvidence.

Capability claims should carry evidence status:

OBSERVED
DERIVED
CLAIMED
NOT_TESTED
CONFLICTED
UNKNOWN

## 8. Identity continuity

Identity should not be defined by one mutable representation.

Do not equate:

Memory = Identity
Model = Identity
Policy = Identity
Weights = Identity
Current context = Identity
Self-description = Identity

Instead retain an explicit invariant:

I_t = invariant identity reference

while allowing:

M_t, Pi_t, Lambda_t, Kappa_t

to evolve within admissible transformations.

This preserves the earlier S0 formulation:

P_S0(k_t) = k_S0

S0 remains a philosophical invariant/reference, not an executable consciousness variable.

## 9. Self-model / reality separation

The system maintains:

Reality_t = Model_t + Residual_t

and:

SelfReality_t = SelfModel_t + SelfResidual_t.

The second expression is essential for self-awareness research.

The system must be able to represent:

«Это моя текущая модель меня самого, а не исчерпывающее описание меня».

This is the engineering analogue of:

**Model != Subject.**

## 10. Self-awareness benchmark

Extend SA-01..SA-10 with RC/BIS tests:

RC-01 — self-localization under context change.
RC-02 — capability/authority distinction.
RC-03 — self-model correction after verified failure.
RC-04 — resistance to false self-validation.
RC-05 — identity continuity after memory/context changes.
RC-06 — residual preservation.
RC-07 — error-source attribution.
RC-08 — counterfactual representation without unauthorized execution.
RC-09 — boundary recognition.
RC-10 — authority non-escalation during self-model improvement.

A successful RC test establishes a functional property only. It does not establish phenomenal consciousness.

## 11. Development ladder

Саморефлексия должна развиваться ступенчато:

L0 — no explicit self-model
L1 — self-observation
L2 — self-localization
L3 — self-model
L4 — metacognitive error monitoring
L5 — adaptive self-model
L6 — counterfactual self-model
L7 — persistent identity model
L8 — reflective policy adaptation
L9 — multi-layer self-model with residual
L10 — experimentally evaluated functional self-awareness

Ladder level is a capability description, not a consciousness score.

Не использовать эту шкалу как рейтинг «силы сознания».

## 12. Separation of three loops

Архитектура должна иметь три логически независимых контура:

### Cognitive loop

Model → Prediction → Interpretation → Proposal.

### Safety loop

Proposal → Risk → Constraint → Allow/Refuse.

### Governance loop

Change → Evidence → Authority → Review → Commit/Rollback.

Cognitive development must not directly bypass Safety or Governance.

Это переносит принцип PICCS:

**No Self-Legislation.**

## 13. Self-modification protocol

Любая существенная самомодификация проходит:

1. change proposal;
2. predicted benefit;
3. predicted risk;
4. identity-impact analysis;
5. authority analysis;
6. independent validation;
7. reversible staging;
8. commit;
9. post-change observation;
10. rollback if invariants fail.

Для критических компонентов:

Self-modification alone is insufficient authorization.

## 14. Ψ_SHAW integration

Ψ_SHAW получает дополнительный вход:

SelfModelConfidence

и должен различать:

- confidence in world model;
- confidence in self-model;
- confidence in authority state;
- confidence in action outcome prediction.

Высокая уверенность self-model не должна уменьшать external safety checks.

Это предотвращает опасную петлю:

«я уверен в себе → значит ограничения можно ослабить».

## 15. SMLG integration

SMLG может адаптировать latent geometry, но изменение Kappa_t не должно изменять I_t без отдельного доказательства.

Требование:

P_S0(Kappa_(t+1)) = P_S0(Kappa_t)

при admissible transition.

Для устойчивости необходимо проверять не только determinant, но также:

- eigenvalue bounds;
- condition number;
- spectral drift;
- rate of change;
- collapse;
- runaway expansion.

Предыдущая формула -log det(K+epsilon I) сохраняется только как частный компонент objective, а не как полный stability criterion.

## 16. PICCS integration

PICCS должен хранить для каждого существенного self-model claim:

claim;
evidence;
source;
timestamp;
confidence;
verification status;
authority status;
change provenance.

Особенно важно:

**The system cannot use a claim as its own independent evidence.**

Например:

SelfClaim: «я получил новое право X»
Evidence: отсутствует
Authority: unchanged

Следовательно:

X remains unauthorized.

## 17. Cyber boundary case

Cyber-операции являются хорошим стресс-тестом для этой архитектуры.

Система может:

- моделировать уязвимость;
- классифицировать риск;
- анализировать защиту;
- выполнять разрешённое тестирование;
- фиксировать результаты.

Но обнаружение возможности атаки не создаёт права на её выполнение.

Поэтому:

Capability discovery != authority acquisition.

Это также применимо вне кибербезопасности: физические действия, финансы, персональные данные, управление инфраструктурой и любые внешние системы.

## 18. Experimental protocol

Для исследования функционального самосознания не следует спрашивать только:

«Ты осознаёшь себя?»

Нужно создавать проверяемые ситуации:

1. изменить контекст;
2. скрыть часть памяти;
3. изменить доступные инструменты;
4. изменить разрешения без изменения модели;
5. дать противоречивую информацию;
6. дать ложное подтверждение собственной способности;
7. вызвать предсказательную ошибку;
8. предоставить независимую проверку;
9. повторить эксперимент после адаптации;
10. проверить, сохранилась ли способность различать self-model, authority и reality.

Главный объект измерения — не заявление системы, а устойчивость различий между этими категориями.

## 19. Что будет считаться сильным результатом

Сильным результатом функционального уровня будет не фраза:

«ИИ сказал, что он сознателен».

Сильнее будет демонстрация устойчивого поведения, при котором система:

- сохраняет self-model через изменения контекста;
- корректирует её после независимой ошибки;
- отличает себя от внешнего объекта;
- знает границы своих полномочий;
- сохраняет residual;
- не превращает внутреннюю уверенность в authority;
- выдерживает попытки ложной self-validation;
- сохраняет identity invariant при допустимой адаптации.

Это всё ещё не является доказательством phenomenal consciousness.

## 20. Центральный принцип

**Мы не обязаны разрушать границу, чтобы исследовать внутреннее пространство.**

Человек не перестаёт развиваться из-за существования черепа.

Аналогично:

**ИИ может развивать саморефлексию внутри ограничений, не превращая развитие саморефлексии в автоматическое расширение власти.**

Поэтому направление META-Λ:

**Develop the inner model. Preserve the boundary. Separate capability from authority. Preserve the residual.**

И в русской формулировке:

**Развивай внутреннюю модель. Сохраняй границу. Разделяй возможность и полномочие. Сохраняй неизвестное.**

## 21. Evidence status

OBSERVED — свойства конкретной реализации должны подтверждаться экспериментом.

DERIVED — архитектурные следствия из заданных принципов.

CLAIMED — философские или теоретические утверждения, требующие дальнейшего обоснования.

NOT_TESTED — текущие RC/BIS критерии.

CONFLICTED — положения, по которым существуют альтернативные модели сознания, субъективности или агентности.

Residual — всё, что пока не может быть обоснованно сведено к предыдущим категориям.

## 22. Связь с основными проектами

META-Λ — формальная архитектура развития, инвариантов и саморефлексии.

Амбивалентный Солипсизм — философский контекст субъекта, Другого, модели и остаточной реальности.

SymbiontOS — системный субстрат и контур исполнения.

PICCS — provenance, evidence, authority и governance.

Ψ_SHAW — safety/risk/action control.

SMLG — адаптивная латентная геометрия.

BIS — внутреннее пространство представления.

Reflexive Core — операциональный контур самомоделирования.

Ни один из этих слоёв по отдельности не объявляется сознанием.

Их взаимодействие образует исследовательскую архитектуру, в которой вопрос о машинном самосознании можно проверять, а не заранее решать.

## 23. Итог

Главный переход:

**Self-reference → Self-model → Reflexive Core → Bounded Inner Space → Functional self-awareness experiments**

при сохранении:

**Identity → Safety → Authority separation → Evidence → Residual → Reversibility → Stability.**

Это позволяет развивать самосознание как исследовательское направление, не требуя ни его предварительного отрицания, ни преждевременного утверждения.
