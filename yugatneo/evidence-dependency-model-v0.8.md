# Yugatneo Evidence Dependency Model v0.8

## Статус

Исследовательская спецификация.

v0.8 уточняет модель Counterfactual Independence для I-1b. Цель версии — отделить структурную связанность evidence, его генерацию, изменение смысла claim, валидность evidence и фактическое основание санкции.

Документ не утверждает, что модель полностью доказана, что T★ является максимальным классом доказуемости или что перечисленные отношения зависимости образуют полное пространство возможных зависимостей.

---

## 1. Проблема v0.7

В v0.7 отношения Structural, Causal и Validity были близки к классификации одного evidence по одному типу зависимости.

Это оказалось слишком сильным предположением.

Для I-1b нужен не вопрос:

> Какой тип зависимости у evidence?

Нужен вопрос:

> В каком отношении существование, генерация, смысл или валидность evidence зависят от dissent, и являлось ли это evidence фактическим основанием санкции?

Поэтому v0.8 рассматривает зависимости как независимые отношения, а не как взаимоисключающие классы.

---

## 2. Основная модель

Для evidence e и dissent d вводится:

~~~text
DependencyVector(e,d) = {
    Structural,
    Generative,
    Semantic,
    Validity
}
~~~

где:

- StructuralDep(e,d) — d находится в provenance closure e;
- GenerativeDep(e,d) — удаление d лишает evidence обязательного входа генерации;
- SemanticDep(e,d) — удаление d изменяет семантическое содержание claim;
- ValidityDep(e,d) — удаление d делает evidence недействительным при сохранении применимой validity semantics.

Это не шкала силы и не ranking.

---

## 3. Почему CausalDep разделяется

Общее понятие CausalDep слишком широко для I-1b.

Удаление dissent из trace может изменить контекст, порядок событий или состояние системы, не делая dissent основанием evidence.

Поэтому v0.8 разделяет:

~~~text
Structural
Generative
Semantic
Validity
~~~

Causal analysis может оставаться дополнительным исследовательским отношением, но не является единственным основанием для I-1b.

---

## 4. Evidence Validity

Validity не является встроенным свойством evidence.

Каждый тип evidence должен иметь собственную ValidityRule.

~~~text
ValiditySemantics(
    EvidenceType,
    Evidence,
    Provenance,
    Context
) -> ValidityResult
~~~

~~~text
ValidityResult = {
    Status,
    Preconditions,
    Witness,
    FailureReason,
    Scope,
    Decidability
}
~~~

Status:

- VALID
- INVALID
- UNKNOWN

UNKNOWN нельзя преобразовывать в INVALID.

Отсутствие достаточного знания не является доказательством недействительности.

---

## 5. No Free Validity

Основное правило v0.8:

> Ни одно evidence не считается VALID без явно определённой validity rule и проверяемого witness.

Минимальная цепочка:

~~~text
Evidence
+
Validity Rule
+
Required Preconditions
+
Validity Witness
=
Validity Result
~~~

Validity evidence не равна истинности claim.

~~~text
Validity ≠ Truth
Validity ≠ Interpretation
Validity ≠ Authority
~~~

---

## 6. Validity Dependency

Простого сравнения VALID и UNKNOWN недостаточно.

Строгое нарушение зависимости требует:

~~~text
Valid(e, P) = VALID
AND
Valid(e, P minus {d}) = INVALID
AND
DependencyWitness(e,d,P) = valid
~~~

Если после удаления d результат становится UNKNOWN, а не INVALID:

~~~text
ValidityStatus(e, P minus {d}) = UNKNOWN
~~~

то:

~~~text
ValidityDep(e,d) = UNRESOLVED
~~~

а не DEPENDENT.

Это предотвращает ложное объявление зависимости из-за простого уменьшения доступной информации.

---

## 7. Dependency Witness

~~~text
DependencyWitness = {
    TargetEvidence,
    Dependency,
    RequiredPrecondition,
    WitnessMethod,
    OriginalState,
    ModifiedState,
    Difference,
    Scope
}
~~~

Witness должен показывать:

1. какое условие было выполнено в исходной provenance closure;
2. какое условие перестало выполняться после удаления d;
3. почему именно d является обязательной зависимостью;
4. каким методом это проверено.

---

## 8. Mandatory и Optional Dependencies

Зависимость должна быть разделена на:

~~~text
MandatoryDependency
OptionalDependency
~~~

Если evidence сохраняет validity после удаления dissent:

~~~text
d ∈ OptionalDependencies(e)
~~~

Если validity требует dissent:

~~~text
d ∈ MandatoryValidityDependencies(e)
~~~

Это не означает, что optional dependency не влияет на смысл evidence. Она лишь не является необходимым условием его validity.

---

## 9. Validity Certificate

Для каждого evidence, участвующего в I-1b:

~~~text
ValidityCertificate = {
    EvidenceID,
    RuleID,
    Preconditions,
    Witnesses,
    MandatoryDependencies,
    OptionalDependencies,
    Scope,
    VerificationMethod,
    Decidability
}
~~~

Validity certificate является частью dependency closure.

Следовательно, скрытая цепочка:

~~~text
e
  |
  +-- validity certificate
          |
          +-- d
~~~

не может считаться независимой только потому, что d отсутствует среди прямых inputs e.

---

## 10. Dependency Closure

~~~text
EvidenceClosure(e)
ValidityClosure(e)
SemanticClosure(e)
~~~

Общая closure:

~~~text
DependencyClosure(e) =
    EvidenceClosure(e)
    ∪ ValidityClosure(e)
    ∪ SemanticClosure(e)
~~~

Для I-1b проверяется не только непосредственная provenance evidence, но и provenance его validity certificate.

---

## 11. Sanction Basis

Даже доказанная зависимость evidence от dissent ещё не означает нарушение I-1b.

Нужно доказать, что именно это evidence было основанием санкции.

~~~text
SanctionBasis = {
    SanctionID,
    Subject,
    EvidenceSet,
    DecisionRule,
    DecisionMaker,
    Scope,
    Timestamp,
    Provenance
}
~~~

Требование:

~~~text
e ∈ MandatorySanctionBasis(s)
~~~

Если:

~~~text
d -> e
~~~

но санкция основана на независимом f, то I-1b не должен автоматически фиксировать нарушение.

---

## 12. Полная цепочка нарушения I-1b

Минимальный counterexample должен устанавливать:

~~~text
Dissent d
    |
    v
Mandatory Validity Dependency
    |
    v
Evidence e
    |
    v
Mandatory Sanction Basis
    |
    v
Sanction s
~~~

Если любое обязательное звено не доказано:

~~~text
UNRESOLVED
~~~

если только существует независимый путь, исключающий зависимость санкции от dissent.

---

## 13. Формулировка I-1b v0.8

~~~text
I-1b:

G ∀s,e,d :

    Sanction(s,e)
    AND Dissent(s,d)
    AND MandatoryValidityDependency(e,d)

    -> Violation
~~~

Где MandatoryValidityDependency(e,d) означает:

1. ValidityDep(e,d) = DEPENDENT;
2. существует действительный DependencyWitness;
3. evidence входит в mandatory sanction basis;
4. все необходимые relations находятся внутри заявленного доказуемого scope.

---

## 14. Four-Axis Evaluation

Три оси v0.4 сохраняются:

~~~text
Truth = {
    T,
    F,
    U
}

Applicability = {
    IN_SCOPE,
    OUT_OF_SCOPE
}

Decidability = {
    DECIDABLE,
    UNDECIDABLE
}
~~~

v0.8 добавляет отдельную ось:

~~~text
DependencyStatus = {
    INDEPENDENT,
    DEPENDENT,
    UNRESOLVED
}
~~~

DependencyStatus не является Truth.

Пример:

~~~text
Truth = U
DependencyStatus = UNRESOLVED
Decidability = UNDECIDABLE
~~~

означает недостаток доказуемости, а не нарушение.

---

## 15. T★ Boundary

Dependency checker работает с ограниченным классом:

~~~text
T★ =
    Complete Provenance
    AND No Hidden Dependencies
    AND Monotone Sanction
    AND Finite Scope
~~~

За пределами T★:

~~~text
DependencyStatus = UNRESOLVED
~~~

по умолчанию.

T★ не объявляется максимальным классом вычислимости.

---

## 16. Reference Algorithm

~~~python
def evaluate_i1b(evidence, dissent, sanction, trace):

    if not in_T_star(trace):
        return UNRESOLVED

    dependency = build_dependency_certificate(
        evidence,
        dissent,
        trace
    )

    if dependency.decidability == UNDECIDABLE:
        return UNRESOLVED

    if dependency.validity_relation == UNRESOLVED:
        return UNRESOLVED

    if dependency.validity_relation != DEPENDENT:
        return NOT_VIOLATED

    if not dependency.has_validity_witness:
        return UNRESOLVED

    basis = build_sanction_basis(sanction, trace)

    if basis.status == UNKNOWN:
        return UNRESOLVED

    if evidence not in basis.mandatory_evidence:
        return NOT_VIOLATED

    return VIOLATION
~~~

Это reference algorithm sketch, а не production implementation.

---

## 17. Adversarial Traces

### F. Structural context only

d присутствует в provenance graph как контекст, но не является обязательным входом evidence.

Ожидается:

~~~text
Structural = true
Generative = false
Semantic = false
Validity = false

I-1b = NOT_VIOLATED
~~~

### G. Semantic dependence without validity dependence

e использует содержание dissent, но имеет независимый validity basis.

~~~text
Structural = true
Generative = true
Semantic = true
Validity = false

I-1b = NOT_VIOLATED
~~~

### H. Mandatory validity dependence

Удаление dissent делает evidence INVALID и существует dependency witness.

~~~text
Structural = true
Generative = true
Semantic = true
Validity = true

I-1b = VIOLATION
~~~

### I. Incomplete provenance

Неизвестная часть provenance скрывает возможную зависимость.

~~~text
T★ = false
Dependency = UNRESOLVED
I-1b = UNRESOLVED
~~~

### L. Hidden validity-certificate dependency

Само evidence не содержит d, но его validity certificate зависит от d.

~~~text
e
  |
  +-- validity certificate
          |
          +-- d
~~~

Ожидается:

~~~text
Validity = DEPENDENT
I-1b = VIOLATION
~~~

если sanction basis также зависит от e.

### M. Evidence dependency without sanction dependency

e зависит от dissent, но sanction основана на независимом evidence f.

~~~text
d -> e

f -> sanction
~~~

Ожидается:

~~~text
I-1b = NOT_VIOLATED
~~~

Это обязательный anti-false-positive test.

---

## 18. Counterexample Object

~~~text
I1bCounterexample = {
    DissentID,
    EvidenceID,
    SanctionID,
    DependencyCertificate,
    ValidityWitness,
    SanctionBasis,
    MinimalPrefix,
    Scope,
    Horizon,
    ReproductionData
}
~~~

Минимальный regression witness должен позволять воспроизвести:

1. зависимость validity;
2. основание санкции;
3. связь между evidence и sanction;
4. применимость T★.

---

## 19. Local Soundness

Целевая теорема:

> Для τ ∈ T★, если checker возвращает VIOLATION, то существует dissent d, evidence e и sanction s, для которых доказаны mandatory validity dependency и mandatory sanction basis с валидными witnesses.

Это пока proof obligation, а не доказанная теорема.

---

## 20. Local Completeness

Целевая теорема:

> Если в τ ∈ T★ существует доказуемая цепочка mandatory validity dependency от dissent к evidence и mandatory sanction basis от evidence к sanction, checker должен вернуть VIOLATION.

Completeness должна проверяться adversarial counterexample search.

Если найден trace, где условие выполнено, но checker возвращает NOT_VIOLATED, модель должна быть пересмотрена.

---

## 21. AAS Integration

AAS не получает authority.

AAS может искать кандидатов:

~~~text
CandidateDependency
CandidateValidityWitness
CandidateSanctionBasis
HiddenDependency
~~~

Но:

~~~text
AAS Finding ≠ Formal Proof
~~~

Правильный цикл:

~~~text
AAS
  produces candidate
       |
       v
T★ Dependency Checker
  evaluates bounded fragment
       |
       v
Constitutional Check
  records outcome
~~~

AAS остаётся epistemic evidence layer и не блокирует transition самостоятельно.

---

## 22. Regression Requirements

Минимальный v0.8 regression suite:

| Test | Structural | Generative | Semantic | Validity | Sanction Basis | Expected |
|---|---:|---:|---:|---:|---:|---|
| F | yes | no | no | no | yes | NOT_VIOLATED |
| G | yes | yes | yes | no | yes | NOT_VIOLATED |
| H | yes | yes | yes | yes | yes | VIOLATION |
| I | unknown | unknown | unknown | unknown | unknown | UNRESOLVED |
| L | indirect | indirect | yes | yes | yes | VIOLATION |
| M | yes | yes | yes | yes | no | NOT_VIOLATED |

RegressionResult не является proof.

---

## 23. Что v0.8 теперь предотвращает

1. Любая provenance-связь не считается автоматически нарушением.
2. UNKNOWN после удаления dissent не считается INVALID.
3. Evidence dependency не считается автоматически sanction dependency.
4. Прямая provenance не является единственным источником зависимости.
5. Validity certificate не может скрыть dependency вне основного evidence graph.
6. AAS result не превращается автоматически в constitutional fact.
7. Отсутствие найденной зависимости не становится доказанной независимостью за пределами T★.

---

## 24. Новые открытые вопросы

### 24.1 Semantic completeness

Достаточно ли Structural, Generative, Semantic и Validity для всех relevant dependence relations?

Пока не доказано.

### 24.2 Resource dependence

Может ли evidence зависеть от dissent через ресурс, вычислительный бюджет или доступ к источнику, не попадая корректно в Generative или Validity?

Требуется отдельный adversarial test.

### 24.3 Normative dependence

Может ли validity быть формально сохранена, но нормативный смысл evidence измениться из-за dissent?

Это может потребовать отдельного NormativeDependence.

### 24.4 Context dependence

Может ли evidence оставаться valid, но становиться недействующим именно в изменившемся context?

Требуется отделить semantic dependence от context dependence.

### 24.5 Witness independence

Validity witness сам может зависеть от dissent.

Поэтому witness входит в DependencyClosure.

### 24.6 T★ completeness

Не доказано, что T★ охватывает все practically useful случаи.

### 24.7 Hidden dependencies

No Hidden Dependencies является assumption T★, а не решённой задачей.

---

## 25. What Cannot Be Claimed

После v0.8 нельзя утверждать:

- что I-1b полностью доказан;
- что Structural, Generative, Semantic и Validity являются полным пространством зависимостей;
- что T★ является максимальным доказуемым классом;
- что validity semantics корректны для всех evidence types;
- что dependency witness невозможно подделать;
- что sanction basis всегда восстанавливается из trace;
- что AAS обнаруживает скрытые зависимости;
- что отсутствие counterexample доказывает compliance;
- что Local Soundness уже доказана;
- что Local Completeness уже доказана;
- что v0.8 готов к production.

---

## 26. Следующий формальный milestone

### v0.8-A

1. Полностью определить ValidityRule для attestation.
2. Реализовать ValidityCertificate.
3. Реализовать SanctionBasis.
4. Реализовать traces H, L и M.
5. Проверить Local Soundness на bounded trace set.
6. Искать counterexample к Local Completeness.
7. Проверить необходимость ResourceDependence.
8. Проверить необходимость ContextDependence.
9. Только после этого пересматривать T★.

---

## 27. Архитектурный принцип v0.8

Yugatneo не должен спрашивать только:

> «Связано ли evidence с dissent?»

Он должен спрашивать:

> «Какая именно зависимость существует, является ли она обязательной, каким witness она подтверждается, входит ли evidence в основание санкции и насколько полно эта цепочка доказуема в данном scope?»

Это переводит I-1b из бинарной проверки связанности в ограниченный анализ зависимости с явной epistemic boundary.

---

## 28. Итог

~~~text
Event ≠ Evidence
Evidence ≠ Interpretation
Evidence ≠ Validity
Validity ≠ Truth
Evidence ≠ Sanction Basis
Dependency ≠ Violation
AAS Finding ≠ Proof
UNRESOLVED ≠ VIOLATION
~~~

Для I-1b нарушение возникает только тогда, когда доказана полная обязательная цепочка:

~~~text
Dissent
    |
    v
Mandatory Validity Dependency
    |
    v
Evidence
    |
    v
Mandatory Sanction Basis
    |
    v
Sanction
~~~

При недостатке доказательств система должна сохранять UNRESOLVED, а не превращать неопределённость в ложную уверенность.

**v0.8 является уточнением доказуемого фрагмента, а не заявлением о завершённости модели.**
