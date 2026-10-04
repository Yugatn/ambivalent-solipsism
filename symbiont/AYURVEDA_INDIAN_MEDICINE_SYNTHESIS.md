# Ayurveda and Traditional Indian Medicine Synthesis

## Scope
Этот документ рассматривает Ayurveda и связанные традиционные индийские медицинские системы через epistemic separation: традиционная теория, наблюдаемые практики, физиологические корреляты, клинические исходы и риски не смешиваются.

## Core separation
**Traditional Category ≠ Anatomical Structure.**
**Dosha ≠ Biomarker by Default.**
**Prakriti ≠ Genetic Profile by Default.**
**Agni ≠ Metabolic Rate by Default.**
**Ama ≠ Specific Toxin by Default.**
**Ojas ≠ Measurable Molecule by Default.**
**Herbal Tradition ≠ Proven Pharmacology.**
**Natural ≠ Safe.**

## Traditional model
Ayurveda представляет целостную систему, в которой питание, образ жизни, физические практики, растительные препараты и другие вмешательства рассматриваются как части индивидуализированного подхода.
Классические категории dosha, dhatu, mala, agni, prakriti и другие должны храниться как элементы традиционной модели, пока для их научного соответствия не существует отдельного доказательства.

## Epistemic layers
- TRADITIONAL: утверждение внутри аюрведической системы.
- OBSERVED: непосредственно наблюдаемый результат.
- PHYSIOLOGICAL: измеряемый физиологический процесс.
- CLINICAL: клинический исход.
- CORRELATED: статистическая связь.
- CAUSAL-CANDIDATE: правдоподобный, но еще проверяемый механизм.
- CLINICALLY-VALIDATED: подтвержденный конкретным клиническим массивом данных.
- METAPHORICAL: философская аналогия.
- NOT_TESTED: недостаточно данных.
- CONFLICTED: противоречивые данные.
- RESIDUAL: неизвестное.

## Individualization
Интересная часть Ayurveda для SymbiontOS — идея индивидуализированной стратегии. Ее нельзя автоматически принимать как доказательство dosha, но ее можно перевести в современный дизайн персонализированной медицины: baseline, phenotype, preferences, environment, adherence, response и adverse events.

**Traditional personalization can inspire a protocol without proving the traditional ontology.**

## Diet and lifestyle
Диетические рекомендации и режим могут иметь эффекты через обычные физиологические и поведенческие механизмы: energy intake, nutrient composition, sleep, activity, stress, habit formation и adherence.
Поэтому полезный компонент следует проверять независимо от традиционного объяснения.

## Yoga and mind-body practices
Аюрведическая практика исторически пересекается с йогой и другими mind-body approaches. Для SymbiontOS такие компоненты следует анализировать теми же методами, что и отдельный слой йоги и цигуна: dose, adherence, subjective response, physiological response, functional outcome и safety.

## Herbal medicines
Растительный препарат следует рассматривать как фармакологически активную экспозицию, а не как автоматически безопасный natural product.
NCCIH отмечает, что для некоторых аюрведических подходов имеются предварительные данные по отдельным исходам, но многие исследования малы или имеют методологические ограничения. citeturn0search0

## Clinical evidence
Доказательность Ayurveda нельзя выражать одной фразой «работает» или «не работает». Она должна оцениваться по конкретному вмешательству и исходу.
Например, NCCIH отмечает отдельные исследования по остеоартриту, диабету и некоторым другим состояниям, но подчеркивает ограниченность общей доказательной базы. citeturn0search0

## Safety gate
Для аюрведических препаратов Safety Gate должен быть строже, чем для обычной поведенческой практики.
Особое внимание требуется продуктам, содержащим минералы или металлы, а также поликомпонентным препаратам.
NCCIH предупреждает о возможном содержании свинца, ртути и мышьяка в некоторых аюрведических препаратах. citeturn0search0

## Heavy metals
Систематический scoping review Ayurveda и Siddha выявил 220 опубликованных случаев токсичности тяжелыми металлами; среди них преобладали lead, mercury и arsenic. В анализированных образцах значительная доля содержала уровни выше допустимых ориентиров. Авторы связывают риск в том числе с загрязнением, неправильным производством и назначением. citeturn0search1turn0search4

Это не означает, что любой аюрведический продукт содержит токсичные металлы. Риск зависит от конкретного продукта, производства, состава и контроля качества.

## Quality before efficacy
Для SymbiontOS вводится принцип:
**Product Identity → Composition → Contamination → Dose → Interaction → Efficacy → Outcome.**
Нельзя оценивать клиническую пользу продукта, если его состав неизвестен или нестабилен.

## Herb–drug interactions
Поликомпонентные растительные препараты требуют учета возможных взаимодействий с лекарствами. До рекомендации необходимо выяснять concurrent medications, supplements, allergies, pregnancy status when relevant, renal/hepatic context and known contraindications.

## Pharmacovigilance
Аюрведический слой должен быть связан с ADVERSE_EVENT_SCHEMA.md.
Каждый препарат должен иметь traceable identity, batch information when available, dose, duration, co-medications, indication, outcome и adverse events.

## Panchakarma
Панчакарма и другие интенсивные очищающие процедуры нельзя считать безопасными только потому, что они традиционны.
Для каждой процедуры нужны отдельные risk-benefit data, protocol specification, contraindications, hydration/nutrition considerations, adverse-event monitoring и escalation criteria.

**Traditional Purification ≠ Proven Detoxification.**

## Detoxification
Термин «детоксикация» должен использоваться только при четко определенном биологическом механизме или клиническом исходе.
Субъективное ощущение легкости после процедуры не доказывает удаление токсина.

## Prakriti and precision medicine
Prakriti можно исследовать как гипотезу о фенотипической типологии, но нельзя автоматически отождествлять ее с генотипом, метаболомом или стабильным биологическим типом.
Современные исследования пытаются искать связи традиционной типологии с биомаркерами, но такие связи требуют независимой валидации.

**Phenotype hypothesis ≠ validated biomarker classifier.**

## Agni
Agni можно использовать как исторический термин для описания традиционного представления о пищеварении и метаболическом состоянии.
Для современной модели его следует декомпозировать на appetite, gastric function, digestion, absorption, metabolic regulation и subjective gastrointestinal state.

Это позволяет сохранить традиционный термин без ложного утверждения о существовании единого физиологического объекта «agni».

## Dosha
Dosha следует хранить как традиционную explanatory category.
Если исследователь пытается связать dosha с физиологическими или психологическими признаками, каждая такая связь должна становиться отдельной тестируемой гипотезой.

**Dosha classification must not become an unvalidated diagnostic shortcut.**

## Mind and consciousness
Аюрведа содержит представления о теле, уме и сознании, которые могут быть философски сопоставлены с АС.
Но традиционная метафизика не становится научным доказательством природы субъекта.

Для АС сохраняется:
**Subject ≠ Body.**
Однако Ayurveda не должна использоваться как эмпирическое доказательство того, что субъект является психоэнергетической субстанцией.

## Psychophysiological integration
Полезный общий контур:
**Practice + Context + Subjective State + Behavior + Physiology + Clinical Outcome.**
Этот контур объединяет Ayurveda с ранее разработанными слоями психофизиологии, йоги и цигуна.

## First-person / third-person
Первое лицо может сообщать hunger, satiety, energy, digestion, calmness, pain, sleep quality и perceived balance.
Третье лицо может измерять body mass, blood pressure, glucose, laboratory markers, sleep measures, physical function и другие показатели.
Расхождение между ними является информацией, а не основанием автоматически объявлять одну сторону неправильной.

## Ayurveda and fasting
Традиционные практики ограничения питания нельзя автоматически переносить в современную концепцию лечебного голодания.
Любое fasting intervention должно проходить через Medical State Machine, Safety Gate и Clinical Evidence Matrix.

## Ayurveda and cellular health
Традиционные утверждения о «очищении клеток» или восстановлении тканей не должны считаться доказанными механизмами без соответствующих биомаркеров и клинических данных.

## SymbiontOS representation
Для каждого Ayurvedic intervention рекомендуется хранить:
- traditional_name;
- traditional_claim;
- exact_product_or_practice;
- ingredients;
- batch_or_source;
- dose;
- duration;
- population;
- indication;
- comparator;
- subjective_outcomes;
- physiological_outcomes;
- clinical_outcomes;
- adverse_events;
- interactions;
- evidence_status;
- uncertainty.

## Shared Decision
Выбор аюрведической практики должен использовать SHARED_DECISION_PROTOCOL.md.
Субъекту необходимо сообщать, что относится к традиционному знанию, что имеет клинические данные, где доказательства слабые и какие существуют риски.

## Safety integration
Аюрведические препараты и процедуры подключаются к MEDICAL_SAFETY_GATE.md и ADVERSE_EVENT_SCHEMA.md.
При потенциальной токсичности, лекарственном взаимодействии или серьезном ухудшении система должна переходить в ESCALATION, а не продолжать оптимизацию.

## Anti-Authority Principle
Традиционный авторитет, древность текста или статус практикующего не являются заменой клиническим доказательствам.

**Ancient ≠ Proven.**
**Traditional ≠ False.**
**Traditional ≠ Automatically True.**

## Useful synthesis for AS
Аюрведа дает АС несколько потенциально полезных контекстов:
1. Ценность индивидуального контекста.
2. Необходимость рассматривать образ жизни вместе с телесным состоянием.
3. Различие субъективного опыта и объективного измерения.
4. Важность профилактики и долгосрочного поведения.
5. Идею целостной модели организма.

Но эти элементы должны проходить современную проверку, а не приниматься вместе с традиционной метафизикой.

## New principle: Epistemic Translation
Перевод традиционной категории в современную модель должен проходить четыре стадии:
традиционное утверждение; наблюдаемая практика; измеряемый феномен; проверяемая гипотеза.
Если соответствие не установлено, оно остается OPEN или METAPHORICAL.

## New principle: Safety-Weighted Integration
Чем выше потенциальный риск вмешательства, тем выше требуемый уровень доказательности и контроля качества.
Безопасность должна иметь приоритет над сохранением традиционной процедуры в исходном виде.

## Final synthesis
Аюрведа может быть ценным источником исторических наблюдений, поведенческих практик и гипотез о персонализации здоровья. Но современный SymbiontOS должен разделять традиционную карту, наблюдаемую практику, физиологический механизм и клинический эффект.

Ключевая формула:
**Preserve the tradition. Separate the claims. Measure the effects. Track the risks. Respect the Subject.**

Итог для АС:
**Традиция может содержать полезное наблюдение, не являясь современной научной теорией.**
**Научное подтверждение отдельного эффекта не подтверждает всю традиционную систему.**
**Отсутствие доказательства конкретного механизма не делает субъективный опыт несуществующим.**
**Но субъективный опыт не освобождает вмешательство от требований безопасности и доказательности.**