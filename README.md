# Амбивалентный Солипсизм

Авторский проект Югатна: философская, научно-методологическая и техническая система исследования восприятия, информации и взаимодействия Субъектов.

## Проекты

### Инфраструктура и развитие

- [СТСеть — связанная транспортная сеть](PROJECTS/STSET_NETWORK.md)
- [Единая система общественного транспорта с электробусами и цифровыми двойниками](PROJECTS/UNIFIED_PUBLIC_TRANSPORT.md)
- [Техническая архитектура цифрового двойника транспорта](PROJECTS/TRANSPORT_DIGITAL_TWIN.md)
- [Система субсидирования курьеров и таксистов за подтверждённое рабочее время](PROJECTS/COURIER_TAXI_SUBSIDY.md)

### Синема Катарсис

**Контентометрия как карта информационной среды Субъекта.**

> Не запрет. Не рекомендация. Не рейтинг. Видимость содержания.

- [Проект «Синема Катарсис»](cinema-catharsis/README.md)
- [Content Passport 3.0](cinema-catharsis/CONTENT_PASSPORT_3.0.md)
- [Scientific Contentometry Protocol v0.2](cinema-catharsis/methodology/CONTENTOMETRY_PROTOCOL.md)

### Принцип

```
WORLD → MEDIA → PERCEPTION → SUBJECT STATE
```

Синема Катарсис не решает за Субъекта, что ему думать о произведении. Она стремится сделать наблюдаемыми структуру медиаконтента, экспозицию, неопределённость и границы знания.

## Статус

Research Concept / Methodological Prototype.

Проект развивается итеративно: ontology → annotation schema → validation corpus → reference contentometer → Content Passport → experimental response studies.

## Лицензии и данные

Публичность исходного кода и методологии не означает автоматического права распространять сторонние изображения, видео, аудио или базы данных. Для внешних источников должны отдельно учитываться provenance, лицензия и условия перераспределения.


## PICCS Sentinel — антивирус

Новый прикладной контур PICCS: исследовательская архитектура антивируса, защищающего не только код и процессы, но также provenance, полномочия, AI-инструменты, обратную связь и корректируемость системы.

- [PICCS Sentinel](antivirus/)
- [Архитектура PICCS Sentinel](antivirus/ARCHITECTURE.md)

Ключевые принципы:

- Detection не равен Decision, а Decision не равен Action;
- UNKNOWN и CONFLICTING являются допустимыми эпистемическими состояниями;
- Capability не создаёт автоматически Permission;
- собственное вмешательство не считается независимым подтверждением;
- при сопоставимой эффективности предпочтение получает более обратимый ответ;
- отказ защитного контура не должен автоматически расширять его автономию;
- антивирус сам является частью Threat Model.

## Формальная архитектура Symbiont

Новый архитектурный слой проекта формализует принцип ограниченного вмешательства при неполной наблюдаемости.

- [Symbiont Formal Core](ARCHITECTURE/SYMBIONT_FORMAL_CORE.md)

Ключевые положения:

- **Reality = Model + Residual** — реконструкция всегда сохраняет остаток неизвестного;
- **Epistemic Type System** — факт, реконструкция, вывод, предположение и неизвестное различаются;
- **Authority Separation** — классификация или оценка не создают автоматически полномочия;
- **Subject Non-Reduction** — профиль, prediction, R и StateVector не являются самим субъектом;
- **Context Sovereignty** — данные не переходят между контекстами без отдельного основания;
- **Decision Traceability** — значимые решения имеют реконструируемое основание;
- **Minimal Necessary Intervention** — при сопоставимой эффективности рассматривается меньшее вмешательство;
- **Anti-Self-Validation** — собственное вмешательство не считается независимым подтверждением собственной гипотезы;
- **Graceful Epistemic Failure** — UNKNOWN является допустимым состоянием;
- **Auditability by Construction** — значимые действия и решения оставляют проверяемый след.

Архитектура связывает PICCS, DEFT, CTO, Event Fabric, Cell Principle, Symbiont Protocol и SymbiontOS в единую формальную линию, не заменяя существующие положения проекта.
## PROF-MAP 2.0

**Прикладная система профессиональной навигации:** профиль, AI-профиль, рабочая среда, ценности, навыки и модели деятельности.

- [PROF-MAP](PROF-MAP/)
- [Методология v0.2.1](PROF-MAP/METHODOLOGY_v0.2.1.md)
- [Архитектура данных](PROF-MAP/DATA_ARCHITECTURE.md)
- [Интеграция с существующими инструментами](PROF-MAP/INTEGRATION.md)
- [План разработки](PROF-MAP/ROADMAP.md)

PROF-MAP не заменяет существующие assessment-инструменты проекта. Он предназначен для профессиональной навигации и может связывать их через отдельные структурированные результаты без смешивания психометрических шкал.

## Eugene Messenger

**Формальная архитектура защищённого коммуникационного контура.**

Eugene Messenger связывает принцип субъектности и когнитивной безопасности с формальной проверкой переходов, конкурентного исполнения и извлечённого runtime.

- [Формальная архитектура Eugene Messenger](PROJECTS/EUGENE_MESSENGER_FORMAL_ARCHITECTURE.md)
- [Assurance Roadmap v3 — Meta-Assurance](PROJECTS/EUGENE_MESSENGER_ASSURANCE_ROADMAP_V3.md)

- [Продуктовая архитектура Eugene Messenger: лента, режимы свайпа и архив](PROJECTS/EUGENE_MESSENGER_PRODUCT_ARCHITECTURE.md)
- [Исполняемый Domain Prototype](eugene-messenger/)
- [ADR 0001–007: Domain Decisions](eugene-messenger/ADR/0001-007-domain-decisions.md)
- [Claim Registry](eugene-messenger/claims/REGISTRY.yaml)


Ключевые расширения:

- Certified Transition System и ValidState;
- Coq как основной proof assistant и Iris для concurrent reasoning;
- Unified System Refinement для связи concrete и abstract execution;
- trace integrity, authenticity, non-interference и linearizability;
- adversarial scheduler с явно заданными safety и liveness assumptions;
- semantic bridge между Coq, OCaml extraction и WASM;
- сохранение UNKNOWN и Residual как валидных эпистемических состояний;
- строгое разделение Detection, Decision и Action;
- сохранение AI Security Agent в пределах ограниченных capabilities;
- явное различение specification, proof, extraction, runtime и testing.

Этот слой является аддитивным: он не заменяет существующую архитектуру проекта и не является заявлением о завершённой механической верификации.


## Yugatneo: текущий конституционный research boundary

Текущий этап Yugatneo не объявляет конституционные инварианты доказанными только потому, что для них существуют формальные записи или симуляционные результаты.

### I-1b: Counterfactual Independence

Для санкции, основанной на evidence e, I-1b требует проверки независимости evidence от dissent d:

Sanction(s,e) ∧ ¬Independent(e,d) → Violation

На ограниченном классе трасс T★ независимость исследуется через provenance graph.

StructuralDep(e,d) означает достижимость d в ancestry evidence.

CausalDep(e,d) означает, что удаление d из наблюдаемого provenance graph изменяет релевантное значение e.

ValidityDep(e,d) означает, что после удаления d evidence теряет требуемую валидность.

Только ValidityDep является основанием для I-1b violation. Простая ссылка на dissent не считается зависимостью.

### T★

T★ требует полного provenance, наблюдаемых или доказуемо отсутствующих зависимостей, конечного scope и явно ограниченной модели санкции. За пределами T★ результат обязан быть UNRESOLVED.

### Provable fragment

I-1 остаётся Opposable в общем случае. Однако корректность алгоритма Independent может быть доказана для явно определённого фрагмента T★. Это не превращает весь I-1 в Provable invariant.

Необходимо отдельно доказать:

1. soundness: DEPENDENT не возвращается без ValidityDep;
2. completeness on T★: всякая наблюдаемая ValidityDep обнаруживается;
3. boundary correctness: вне T★ результатом является UNRESOLVED;
4. structural and causal dependence не являются достаточными условиями violation.

### Evidence boundary

AAS counterfactual simulation может давать evidence для случаев вне T★, но её результат не становится автоматически конституционным вердиктом. SUPPORTED, REFUTED и UNRESOLVED остаются результатами эксперимента.

### Что пока нельзя утверждать

- что I-1b доказан для всех трасс;
- что T★ охватывает реальные системы;
- что provenance graph всегда полон;
- что validity всех типов evidence имеет единственную процедуру;
- что AAS counterfactual simulation корректно решает случаи вне T★;
- что отсутствие найденного counterexample означает соблюдение I-1b.
