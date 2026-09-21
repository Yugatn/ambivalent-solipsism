# Eugene Messenger — Assurance Roadmap v3

## Статус

**Assurance Methodology / Meta-Assurance Specification / Research Roadmap**

Этот документ является аддитивным расширением формальной архитектуры Eugene Messenger. Он не заменяет существующую пятислойную архитектуру, PICCS-Core, PICCS-Hub, Federation, Plugin API, Eugene UI, Trust Model, Threat Model, EPS-001/001A, EPS-003 или ранее определённые assurance-положения.

Roadmap v3 сохраняет уровни assurance, введённые ранее, и добавляет формализацию доверия к самой инфраструктуре, которая производит evidence.

> **v2 закрывает разрыв между claim и evidence. v3 закрывает разрыв между evidence и доверием к evidence.**

Это исследовательская спецификация. Наличие раздела, модели или checklist не означает, что соответствующее доказательство уже механически выполнено.

---

## 1. Зачем нужен v3

Assurance pipeline сам является частью системы, которую необходимо рассматривать относительно threat model.

Registry, schema validation, CI runner, TLC, compiler/toolchain, configuration, evidence manifest, signatures и publication pipeline могут содержать ошибки или подвергаться атаке.

Поэтому Eugene Messenger вводит трёхуровневую модель:

1. **System Assurance** — claims о свойствах системы.
2. **Implementation Assurance** — соответствие реализации формальной модели и claims.
3. **Meta-Assurance** — проверяемость и целостность инфраструктуры, производящей evidence.

Цель v3 не в том, чтобы объявить pipeline безошибочным. Цель — сделать его ошибки, компрометацию и устаревание **наблюдаемыми, локализуемыми и проверяемыми**.

---

## 2. Сохраняемый канон

v3 не заменяет:

- существующую архитектуру Eugene Messenger;
- PICCS и его ограниченный принцип вмешательства;
- Certified Transition System;
- ValidState;
- Coq и Iris;
- Unified System Refinement;
- Detection, Decision и Action;
- UNKNOWN и Residual;
- threat-model-bounded security claims;
- различение specification, proof, extraction, runtime и testing;
- ранее определённые claim registry и evidence contract.

Все новые механизмы являются дополнительным assurance-слоем.

---

# 3. Трёхуровневая Assurance Architecture

```
Level 1 — System Assurance
    Claims
    AntiReplay
    IdentityContinuity
    EpochTransition
    ContextSovereignty
    ...

Level 2 — Implementation Assurance
    Conformance
    Trace validation
    Model checking
    Formal proofs
    Adversarial testing
    Extraction correspondence

Level 3 — Meta-Assurance
    Registry integrity
    Schema validity
    Toolchain integrity
    Runner provenance
    Evidence integrity
    Reproducibility
    Invalidation
    Composition
```

Ключевой принцип:

> Evidence не считается доверенным только потому, что оно существует.

---

# 4. Assurance State Machine

Каждый claim имеет жизненный цикл.

```
Claim
  |
  v
Specified
  |
  v
Modeled
  |
  v
Executed
  |
  v
ModelChecked
  |
  +------> Invalidated
  |             |
  |             v
  |         Reverified
  |             |
  +-------------+
```

Допустимые переходы должны быть формально ограничены.

Особенно важны:

- изменение specification;
- изменение scope;
- изменение assumption;
- изменение formal model;
- изменение toolchain;
- изменение verification configuration;
- обнаружение повреждения evidence;
- отзыв подписи;
- изменение provenance.

Историческое evidence не удаляется при invalidation. Оно получает статус `stale` и сохраняется для audit trail.

---

# 5. Evidence Integrity

Минимальный глобальный инвариант:

```
EvidenceIntegrity ==
    ∀ claim ∈ Registry :
        claim.status = model_checked
        ⇒ ∃ e ∈ Evidence :
            e.claim_hash = claim.hash
            ∧ e.source_revision = CurrentRevision
            ∧ e.toolchain_hash ∈ PinnedToolchains
            ∧ e.schema_version ∈ SupportedSchemas
            ∧ e.result ∈ {pass, expected_counterexample}
            ∧ VerifySignature(e)
            ∧ VerifyManifest(e)
            ∧ VerifyProvenance(e)
```

Следовательно, `model_checked` не означает просто «TLC завершился успешно».

Это составное состояние:

```
model_checked
=
correct claim
+
correct revision
+
correct scope
+
valid assumptions
+
correct model
+
pinned toolchain
+
valid schema
+
valid provenance
+
valid evidence
```

---

# 6. Evidence Bundle

Единицей доверия является canonical Evidence Bundle.

Минимальный состав:

```
claim
claim_hash
scope
assumptions
source_revision
model_revision
toolchain
toolchain_hash
configuration
schema_version
execution_metadata
result
traces
counterexamples
manifest
signature
provenance
```

Пример:

```yaml
evidence:
  id: ev-antireplay-001

  claim_id: AntiReplay
  claim_hash: sha256:...

  source_revision: git:...
  model_revision: git:...

  toolchain:
    tlc_version: ...
    java_version: ...
    runner_image: ...

  toolchain_hash: sha256:...
  configuration_hash: sha256:...

  result: pass

  manifest_hash: sha256:...

  signature:
    algorithm: ...
    value: ...

  provenance:
    runner: ...
    workflow: ...
```

---

# 7. Content-Addressed Claims

Имя claim недостаточно для идентификации его семантики.

Вводится:

```
claim_hash =
H(
    statement
    + scope
    + assumptions
    + falsification_criteria
    + formal_model
    + spec_revision
)
```

Evidence содержит этот hash.

Если specification изменяется:

```
Claim v1
   |
   | specification change
   v
Claim v2
```

то hash изменяется, а evidence v1 автоматически становится `stale` для v2.

Это закрывает класс ошибок **evidence drift**.

---

# 8. Scope как формальный объект

Scope не должен оставаться свободным текстом.

Пример:

```yaml
scope:
  environment:
    network: asynchronous
    adversary:
      network_control: true
      endpoint_compromise: false

  timing:
    model: unbounded

  subjects:
    federation: false
    identity_model: single_identity

  cryptography:
    model: symbolic
    perfect_cryptography: true
    side_channels: excluded

  out_of_scope:
    - traffic_analysis
    - endpoint_compromise
    - quantum_adversary
```

Вводится отношение:

```
ScopeCompatibility(A, B)
∈ {compatible, incompatible, unknown}
```

`unknown` является самостоятельным результатом и не должен автоматически трактоваться как compatibility.

---

# 9. Assumptions как first-class entities

Assumption получает собственный ID и lifecycle.

```yaml
assumptions:
  - id: AsyncNetwork
    statement: Network is asynchronous
    status: valid

  - id: NoEndpointCompromise
    statement: Adversary cannot compromise endpoint
    status: valid
```

Claim:

```yaml
claim:
  id: AntiReplay
  depends_on_assumptions:
    - AsyncNetwork
    - NoEndpointCompromise
```

Если assumption становится invalid:

```
AsyncNetwork
     |
     +---- AntiReplay
     |
     +---- EpochTransition
```

CI создаёт invalidation event и каскадно понижает зависимые claims.

Минимальное правило:

> Если обязательное assumption больше не имеет статуса `valid`, зависимый claim не может сохранять статус, требующий этого assumption.

---

# 10. Invalidation Events

Invalidation является first-class event.

```yaml
invalidation_event:
  id: inv-YYYY-MM-DD-NNN
  trigger: assumption_invalidated
  source: AsyncNetwork

  affected_claims:
    - AntiReplay
    - EpochTransition

  previous_status: model_checked
  new_status: specified

  reason: Assumption invalidation
  remediation: Re-verify with updated assumption

  evidence_preserved: true
```

Evidence не удаляется.

Оно сохраняется как историческое evidence со статусом `stale`.

---

# 11. Meta-Assurance State Machine

Сам assurance pipeline моделируется отдельно.

Минимальное состояние:

```
ClaimRegistered
  |
  v
ScopeValidated
  |
  v
AssumptionsValidated
  |
  v
ModelValidated
  |
  v
ToolchainValidated
  |
  v
VerificationExecuted
  |
  v
EvidenceCanonicalized
  |
  v
EvidenceVerified
  |
  v
Published
```

Любой failure должен вести в явно определённое состояние отказа, а не молча продолжать публикацию.

Целевая TLA+ модель должна проверять:

- корректность переходов;
- отсутствие публикации непроверенного evidence;
- каскадную invalidation;
- соответствие claim hash;
- соответствие source revision;
- соответствие pinned toolchain;
- корректность stale transition;
- невозможность получить `model_checked` из неподтверждённого evidence.

---

# 12. Negative Controls

Assurance pipeline должен проверять не только положительные случаи.

Минимальный набор:

| Контроль | Ожидаемый результат |
|---|---|
| Modified model | FAIL |
| Modified configuration | FAIL |
| Modified evidence | FAIL |
| Wrong claim hash | FAIL |
| Wrong toolchain hash | FAIL |
| Invalid signature | FAIL |
| Corrupted manifest | FAIL |
| Wrong source revision | FAIL |
| Wrong schema version | FAIL |
| Stale evidence presented as current | FAIL |

Negative controls являются частью assurance evidence самого pipeline.

---

# 13. Deterministic Evidence

Требуется различать два свойства.

### Semantic determinism

Одинаковые:

- source revision;
- model;
- configuration;
- toolchain;

должны давать одинаковый verification result.

### Canonical artifact determinism

Нормализованный manifest должен давать одинаковый hash:

```
Run A → canonical_manifest_hash = H
Run B → canonical_manifest_hash = H
```

Volatile metadata, например timestamp выполнения, не должна разрушать canonical hash.

Determinism не означает, что любой внешний runtime является полностью детерминированным. Требуется детерминированность **проверяемого результата и canonical evidence representation** при одинаковом входном контексте.

---

# 14. Assurance Threat Model

Threat model assurance pipeline разделяется на три класса.

## 14.1 Tool Integrity

- TLC substitution;
- compiler substitution;
- dependency poisoning;
- runner image substitution;
- compromised build environment.

## 14.2 Evidence Integrity

- manifest tampering;
- trace substitution;
- signature substitution;
- evidence replay;
- claim/evidence mismatch;
- stale evidence presented as current.

## 14.3 Process Integrity

- wrong branch;
- wrong commit;
- wrong configuration;
- wrong model revision;
- skipped verification stage;
- TOCTOU;
- publication of an unverified artifact.

Контрмеры должны быть проверяемыми, а не только заявленными.

---

# 15. TOCTOU Protection

Нельзя полагаться на последовательность:

```
generate evidence
    ↓
publish evidence
    ↓
hash evidence
```

Целевая последовательность:

```
Source
Model
Configuration
Toolchain
Evidence
    ↓
Canonical Evidence Bundle
    ↓
Bundle Hash
    ↓
Signature
    ↓
Publication
```

Все семантически значимые компоненты должны быть связаны криптографически до публикации.

---

# 16. Claim Composition

Claims становятся объектами формальной композиции.

Пример:

```yaml
composition:
  id: AntiReplay_AND_IdentityContinuity
  operator: conjunction

  operands:
    - AntiReplay
    - IdentityContinuity
```

Перед derived claim проверяются:

- scope compatibility;
- assumptions compatibility;
- invariant compatibility;
- dependency validity.

Для conjunction:

```
scope = compatible intersection
status = weakest valid operand
```

Если совместимость не доказана, результат не должен автоматически считаться valid.

---

# 17. Composition Operators

Минимальный набор:

### Conjunction

Оба claims должны быть валидны в совместимой области.

### Disjunction

Допустима одна из ветвей, но условия применимости каждой ветви должны быть формализованы.

### Refinement

Claim B уточняет Claim A, если область B является подмножеством области A и существует доказуемая implication relation.

Нельзя объявлять refinement только YAML-ссылкой.

### Independence

Claims могут быть помечены независимыми только при наличии явно определённых independence conditions.

---

# 18. Coverage

Coverage не должен автоматически сводиться к проценту.

Предпочтительное представление:

```yaml
coverage:
  covered:
    - asynchronous_network
    - symbolic_crypto
    - no_endpoint_compromise

  partially_covered:
    - federation

  uncovered:
    - traffic_analysis
    - endpoint_compromise

  unknown:
    - quantum_adversary
```

Числовой coverage допускается только при наличии явной нормализованной и обоснованной weighting model.

Таким образом, `73%` без модели веса не считается assurance metric.

---

# 19. Attack Pattern Library

Adversarial testing становится переиспользуемым.

Структура:

```
attack-patterns/
├── replay-within-epoch.json
├── replay-across-epoch.json
├── identity-resurrection.json
├── capability-scope-expansion.json
├── epoch-rollback.json
└── ...
```

Каждый pattern должен содержать:

- structured trace;
- trace-schema compatibility;
- formal-model fragment или reference;
- implementation test;
- falsification target;
- references на исследования или известные инциденты, если применимо.

Attack pattern может использоваться несколькими claims.

---

# 20. Verification Decision Framework

Не каждый claim требует одинакового метода.

Факторы:

- risk;
- impact;
- falsifiability;
- formalizability;
- cost;
- change frequency;
- attack surface;
- existing evidence.

Возможные стратегии:

| Условия | Стратегия |
|---|---|
| High risk + high formalizability | Formal verification |
| High risk + low formalizability | Adversarial testing + fuzzing |
| Medium risk + high verifiability | Property-based testing |
| Low risk | Unit tests + review |
| Unknown verifiability | Research spike |
| High change frequency | Prefer lower-cost continuously executable checks where adequate |

Выбор метода должен быть обоснован природой claim.

---

# 21. Standards Mapping

Roadmap v3 допускает conceptual mapping к:

- Common Criteria / ISO/IEC 15408;
- ISO 26262;
- DO-178C;
- IEC 62443.

Mapping не является сертификацией.

Цель mapping:

1. дать внешнему аудитору точку входа;
2. сопоставить terminology;
3. выявить отсутствующие assurance objectives;
4. избежать ложного заявления о compliance.

Формат:

```
Eugene Assurance Objective
        |
        +--- Common Criteria concept
        +--- DO-178C concept
        +--- ISO 26262 concept
        +--- IEC 62443 concept
```

---

# 22. Assurance Dashboard

Один Registry должен иметь три представления.

## Developer View

Показывает:

- claims без модели;
- stale evidence;
- invalidated assumptions;
- failing negative controls;
- missing evidence;
- ближайшие verification tasks.

## Auditor View

Показывает полную цепочку:

```
Claim
Scope
Assumptions
Model
Evidence
Toolchain
Provenance
Signature
Invalidation history
Composition
Residual risk
```

## User View

Показывает:

- что проверяется;
- что не проверяется;
- при каких assumptions;
- какие ограничения остаются;
- что пока неизвестно.

User View не должен создавать иллюзию абсолютной безопасности.

---

# 23. Rollback и Status Demotion

Статус claim должен быть понижаемым.

Пример:

```
model_checked
      |
      | assumption invalidated
      v
specified
```

или:

```
model_checked
      |
      | evidence integrity failure
      v
specified
```

или:

```
model_checked
      |
      | toolchain changed
      v
modeled
```

Точная целевая стадия зависит от того, какой именно объект потерял валидность.

Правило:

> Нельзя восстанавливать более высокий статус без повторной проверки необходимых prerequisites.

---

# 24. Assurance Maturity v3

Сохраняется шкала Level 0–8:

| Level | Значение |
|---:|---|
| 0 | Declared |
| 1 | Specified |
| 2 | Falsifiable |
| 3 | Modeled |
| 4 | Executed |
| 5 | Model Checked |
| 6 | Conformance |
| 7 | Adversarial |
| 8 | Reproducible |

Добавляются:

| Level | Значение |
|---:|---|
| -1 | Assumed |
| 9 | Meta-Assured |
| 10 | Composition-Closed |

### Level -1 — Assumed

Свойство существует только как неявное предположение.

### Level 9 — Meta-Assured

Assurance infrastructure имеет собственную модель, negative controls, provenance, deterministic canonical evidence и проверяемую invalidation logic.

### Level 10 — Composition-Closed

Claims имеют формальные composition rules, scope compatibility, assumption compatibility и вычислимые derived claims.

Уровни не являются процентом качества, рейтингом безопасности или гарантией отсутствия уязвимостей.

---

# 25. ASSURANCE-001 — Reproducible Evidence

Существующий milestone сохраняется.

Дополнения:

- [ ] claim hash;
- [ ] canonical evidence manifest;
- [ ] source revision;
- [ ] model revision;
- [ ] pinned toolchain;
- [ ] schema version;
- [ ] provenance;
- [ ] reproducible execution.

---

# 26. ASSURANCE-002 — Meta-Assurance

- [ ] TLA+ model of assurance state machine;
- [ ] invalidation transitions;
- [ ] dependency graph;
- [ ] evidence integrity invariant;
- [ ] negative controls;
- [ ] deterministic canonical manifest;
- [ ] toolchain pinning;
- [ ] provenance validation.

---

# 27. ASSURANCE-003 — Claim Integrity

- [ ] structured scope;
- [ ] structured assumptions;
- [ ] content-addressed claim hash;
- [ ] specification revision binding;
- [ ] evidence claim-hash binding;
- [ ] stale evidence detection.

---

# 28. ASSURANCE-004 — Invalidation

- [ ] assumption lifecycle;
- [ ] invalidation events;
- [ ] dependency traversal;
- [ ] automatic status demotion;
- [ ] historical evidence preservation;
- [ ] re-verification path.

---

# 29. ASSURANCE-005 — Composition

- [ ] conjunction;
- [ ] disjunction;
- [ ] refinement;
- [ ] scope compatibility;
- [ ] assumption compatibility;
- [ ] invariant conflict detection;
- [ ] derived claim status.

---

# 30. ASSURANCE-006 — Pipeline Negative Controls

- [ ] modified model → FAIL;
- [ ] modified configuration → FAIL;
- [ ] corrupted evidence → FAIL;
- [ ] wrong claim hash → FAIL;
- [ ] wrong toolchain hash → FAIL;
- [ ] invalid signature → FAIL;
- [ ] corrupted manifest → FAIL;
- [ ] wrong source revision → FAIL;
- [ ] stale evidence → FAIL.

---

# 31. ASSURANCE-007 — Determinism

- [ ] two identical runs;
- [ ] identical semantic result;
- [ ] canonical manifest normalization;
- [ ] identical canonical hash;
- [ ] documented volatile metadata;
- [ ] toolchain reproducibility.

---

# 32. ASSURANCE-008 — Attack Pattern Library

- [ ] replay patterns;
- [ ] resurrection patterns;
- [ ] rollback patterns;
- [ ] capability expansion;
- [ ] trace manipulation;
- [ ] implementation-level regression tests;
- [ ] formal counterexample mapping.

---

# 33. ASSURANCE-009 — Assurance Threat Model

- [ ] tool integrity;
- [ ] evidence integrity;
- [ ] process integrity;
- [ ] TOCTOU;
- [ ] CI runner compromise;
- [ ] dependency poisoning;
- [ ] evidence replay;
- [ ] publication tampering.

---

# 34. ASSURANCE-010 — Verification Economics

- [ ] risk classification;
- [ ] formalizability assessment;
- [ ] verification cost estimate;
- [ ] continuous verification cost;
- [ ] selection of verification method;
- [ ] research spike for unknown cases.

---

# 35. ASSURANCE-011 — External Standards Mapping

- [ ] Common Criteria conceptual mapping;
- [ ] DO-178C conceptual mapping;
- [ ] ISO 26262 conceptual mapping;
- [ ] IEC 62443 conceptual mapping;
- [ ] explicit non-certification statement.

---

# 36. ASSURANCE-012 — Assurance Dashboard

- [ ] Developer view;
- [ ] Auditor view;
- [ ] User view;
- [ ] one source of truth;
- [ ] explicit UNKNOWN;
- [ ] stale evidence visibility;
- [ ] invalidation history.

---

# 37. Definition of Done для v3

Roadmap v3 не считается выполненным по наличию файлов или YAML.

Минимальный критерий:

```
v3 complete
=
assurance state machine modeled
+
negative controls executed
+
canonical evidence reproducible
+
claim hash verified
+
assumption invalidation demonstrated
+
stale evidence detected
+
composition rules mechanically checked
```

При этом completion v3 не означает доказанную безопасность Eugene Messenger.

Он означает, что **сам assurance process достиг проверяемого уровня зрелости**.

---

# 38. Итоговая архитектура доверия

```
System
  |
  v
Claim
  |
  +--- Scope
  +--- Assumptions
  +--- Falsification Criteria
  +--- Formal Model
  |
  v
Verification
  |
  v
Evidence Bundle
  |
  +--- Claim Hash
  +--- Source Revision
  +--- Toolchain Hash
  +--- Schema
  +--- Provenance
  +--- Signature
  |
  v
Meta-Assurance
  |
  +--- Integrity
  +--- Reproducibility
  +--- Negative Controls
  +--- Invalidation
  |
  v
Composition
  |
  +--- Scope Compatibility
  +--- Assumption Compatibility
  +--- Invariant Compatibility
  |
  v
Current Assurance State
```

Главный принцип v3:

> **Не достаточно доказать claim. Необходимо также доказать, что evidence относится именно к этому claim, произведено допустимым процессом, относится к правильной версии системы, не стало устаревшим и может быть повторно проверено.**

И ещё более важное ограничение:

> **Meta-Assurance не доказывает истинность всей системы. Оно ограничивает пространство ошибок между действительностью, claim, verification и тем evidence, на основании которого делается assurance-утверждение.**

---

## Appendix A — минимальный Registry schema

```yaml
claim:
  id: AntiReplay
  hash:
    algorithm: SHA-256
    value: sha256:...

  statement: "..."

  scope:
    environment:
      network: asynchronous

  depends_on_assumptions:
    - AsyncNetwork
    - NoEndpointCompromise

  falsification_criteria:
    - replay-within-epoch
    - replay-across-epoch

  formal_model:
    type: tla+
    path: models/anti-replay.tla

  spec_revision: git:...

  status: model_checked

evidence:
  id: ev-antireplay-001
  claim_hash: sha256:...
  source_revision: git:...
  toolchain_hash: sha256:...
  configuration_hash: sha256:...
  schema_version: evidence/v1
  result: pass
  manifest_hash: sha256:...
  signature: ...

assumptions:
  - id: AsyncNetwork
    status: valid

  - id: NoEndpointCompromise
    status: valid
```

---

## Appendix B — Invalidation Rule

```
For every claim C:

if
    ∃ assumption A ∈ Dependencies(C)
    where A.status != valid
then
    C.status cannot remain in a state that requires A
    emit InvalidationEvent
    preserve historical evidence
    mark affected evidence stale
    require re-verification before restoration
```

---

## Appendix C — Non-Goals

Roadmap v3 не утверждает:

- что CI безошибочен;
- что formal verification доказывает отсутствие всех реальных атак;
- что reproducibility доказывает correctness;
- что signature доказывает semantic validity;
- что standards mapping является сертификацией;
- что Level 10 означает абсолютную безопасность;
- что coverage percentage может заменить содержательный scope analysis.

---

## Research Status

**Architecture:** defined  
**Meta-Assurance model:** proposed  
**TLA+ assurance state machine:** pending implementation  
**Negative controls:** pending implementation  
**Canonical evidence:** pending implementation  
**Claim hashing:** pending implementation  
**Assumption invalidation:** pending implementation  
**Composition engine:** pending implementation  
**Attack Pattern Library:** planned  
**Standards mapping:** planned  
**Dashboard:** planned

> **Сильная assurance-архитектура не скрывает остаток неизвестного. Она делает его частью самого механизма доверия.**
