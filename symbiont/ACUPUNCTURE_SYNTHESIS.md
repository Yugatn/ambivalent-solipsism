# Acupuncture Synthesis

## Scope
Акупунктура рассматривается как семейство needle-based interventions, а не как единое вмешательство. Традиционная теория, конкретная техника, физиологический механизм, клинический эффект и субъективный опыт разделяются.

## Epistemic separation
**Meridian ≠ Anatomical Nerve by Default.**
**Qi ≠ Measurable Physical Energy by Default.**
**Acupoint ≠ Proven Unique Biological Target by Default.**
**Traditional Explanation ≠ Established Mechanism.**
**Clinical Effect ≠ Proof of Traditional Ontology.**

## Evidence architecture
Для каждого утверждения нужно различать:
- TRADITIONAL: утверждение традиционной китайской медицины.
- SUBJECTIVE: опыт субъекта.
- PHYSIOLOGICAL: измеряемый биологический ответ.
- CLINICAL: изменение клинического исхода.
- CORRELATED: статистическая связь.
- CAUSAL-CANDIDATE: предложенный механизм, требующий проверки.
- CLINICALLY-VALIDATED: эффект с приемлемой доказательной базой для конкретного исхода и популяции.
- NOT_TESTED / CONFLICTED / RESIDUAL.

## Acupuncture is not one intervention
Manual acupuncture, electroacupuncture, auricular acupuncture and other needling protocols отличаются техникой, дозировкой, локализацией и контекстом.
Следовательно, результат исследования одного протокола нельзя автоматически переносить на всю акупунктуру.

## Clinical evidence
Наиболее полезно оценивать акупунктуру по конкретному состоянию и исходу, а не вопросом «работает ли акупунктура вообще».
WHO guideline for chronic primary low back pain рассматривает needling therapies отдельно и сообщает о небольших эффектах на некоторых краткосрочных исходах при низкой или очень низкой определенности доказательств; поэтому результат не следует интерпретировать как универсальное лечение боли. citeturn0search2turn0search37

## Pain model
Для АС особенно полезно различать pain intensity, pain unpleasantness, functional limitation, expectation, attention, context and behavior.
Даже при изменении субъективной боли нельзя автоматически заключать, что устранена исходная тканевая причина.

## Context and measurement
Акупунктура является хорошим примером того, что клинический эффект может зависеть от контекста процедуры, ожиданий, взаимодействия practitioner–subject, сенсорной стимуляции и естественной динамики симптома.
Это связывается с принципом SymbiontOS:
**Observation is not a direct readout of the Subject.**

## Sham is not simple
Контрольная процедура должна быть определена точно. «Sham» может содержать сенсорную стимуляцию или другие активные компоненты и поэтому не всегда представляет полностью инертный контроль.
Следовательно, разница между verum и sham не обязательно равна разнице между лечением и полным отсутствием эффекта.

## Mechanism discipline
Возможные физиологические механизмы акупунктуры могут включать периферическую сенсорную стимуляцию, нейронные и автономные ответы, нисходящую модуляцию боли и контекстуальные эффекты.
Каждый механизм должен проверяться отдельно. Нельзя использовать обнаружение физиологического ответа как доказательство существования традиционной концепции qi или meridians.

## Safety
Акупунктура не должна классифицироваться как «безопасная безусловно». Современные систематические обзоры показывают, что серьезные нежелательные явления редки, но возможны; описаны пневмоторакс, повреждения органов и нервов, инфекции, кровотечения, синкопе и другие осложнения. citeturn0search1turn0search10turn0search9

Evidence mapping 535 systematic reviews обнаружил 33 категории adverse effects, включая повреждения органов и тканей, системные реакции, инфекции и синкопе; большинство включенных обзоров имели низкое или критически низкое методологическое качество. citeturn0search0

## Safety engineering
Основные факторы риска связаны не только с самим воздействием, но и с техникой, глубиной введения иглы, стерильностью, выбором зоны и квалификацией практикующего.
Поэтому SymbiontOS должен рассматривать competence, sterile technique, exact body site, needle type, depth when documented, session context and adverse events как часть intervention record.

## Adverse event integration
Акупунктурные события подключаются к `ADVERSE_EVENT_SCHEMA.md`.
Нужно различать:
- expected local response;
- minor adverse event;
- event requiring treatment;
- serious adverse event;
- suspected causal reaction;
- unrelated concurrent event.

Temporal association не доказывает причинность.

## New acupuncture intervention schema
Рекомендуемые поля:
- technique;
- body sites;
- needle count;
- stimulation mode;
- session duration;
- practitioner qualification;
- sterile protocol;
- indication;
- baseline;
- concurrent treatment;
- subjective outcome;
- physiological outcome;
- clinical outcome;
- adverse events;
- evidence status;
- uncertainty.

## First-person / third-person integration
Первое лицо может сообщать pain, warmth, relaxation, anxiety, fatigue, dizziness, perceived energy and symptom change.
Третье лицо может фиксировать validated pain scales, function, vital signs, neurological findings and other validated outcomes.
Оба потока должны сохраняться отдельно.

**Subjective Improvement ≠ Physiological Cure.**
**Physiological Change ≠ Proof of Traditional Mechanism.**

## Individualization
Индивидуальный выбор точек и протокола может быть интересным объектом исследования, но персонализация не должна становиться свободной зоной для недоказуемых утверждений.
Если персонализированный протокол заявляет преимущество, преимущество должно быть проверяемым.

## Acupuncture and psychophysiology
Акупунктура полезна для исследовательской архитектуры АС как controlled perturbation: вводится стандартизируемая сенсорная стимуляция, после чего можно наблюдать subjective, autonomic, behavioral and clinical responses.
Это позволяет исследовать динамику состояния без утверждения, что традиционная теория является современной физиологической моделью.

## Acupuncture and Subject
Акупунктура не дает оснований отождествлять Subject с телом или нервной системой.
Одновременно она не дает научного доказательства психоэнергии или души.
Сохраняется AS distinction:
**Subject ≠ Body.**
**Subject ≠ CNS.**
**Model ≠ Subject.**

## Integration with existing SymbiontOS
Акупунктурный протокол должен проходить:
`MEDICAL_STATE_MACHINE.md` для состояния процесса;
`MEDICAL_SAFETY_GATE.md` для рисков;
`CLINICAL_EVIDENCE_MATRIX.md` для доказательности;
`ADVERSE_EVENT_SCHEMA.md` для безопасности;
`SHARED_DECISION_PROTOCOL.md` для выбора субъекта;
`PSYCHOPHYS_STATE_SCHEMA.md` для состояния;
`INTEROCEPTION_PROTOCOL.md` для телесного опыта.

## Decision rule
Если цель относится к хроническому симптому, необходимо определить:
1. клиническую цель;
2. альтернативные методы;
3. качество доказательств именно для этой цели;
4. индивидуальные противопоказания и риски;
5. критерий успеха;
6. критерий прекращения;
7. план повторной оценки.

## Anti-magical principle
Не следует считать, что процедура работает потому, что субъект ощущает поток энергии.
Не следует считать, что процедура не работает только потому, что традиционная модель не подтверждена.
Нужно отдельно оценивать experience, mechanism and outcome.

## New principle: Intervention Decomposition
Любое комплексное традиционное вмешательство должно быть разложено на физическую стимуляцию, контекст, ожидания, взаимодействие, поведенческие изменения и специфический компонент техники.
Это предотвращает ошибку attribution, когда весь эффект приписывается одному объяснительному компоненту.

## New principle: Specificity Claim
Чем сильнее утверждение о специфичности конкретной точки, меридиана или традиционного механизма, тем более специфическим должно быть экспериментальное подтверждение.

## New principle: Safety-by-Protocol
Безопасность является свойством конкретного протокола и его выполнения, а не абстрактным свойством названия «акупунктура».

## Final synthesis
Акупунктура может быть исследована как конкретная сенсорная и поведенческая интервенция с возможными клиническими эффектами для отдельных состояний. Ее традиционная система объяснения должна сохраняться как историко-культурная модель, пока отдельные соответствия не будут подтверждены независимо.

Ключевая формула:
**Preserve the practice. Separate the mechanism. Measure the outcome. Track the risk. Respect the Subject.**