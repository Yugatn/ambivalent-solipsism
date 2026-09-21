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
## Eugene Messenger

**Формальная архитектура защищённого коммуникационного контура.**

Eugene Messenger связывает принцип субъектности и когнитивной безопасности с формальной проверкой переходов, конкурентного исполнения и извлечённого runtime.

- [Формальная архитектура Eugene Messenger](PROJECTS/EUGENE_MESSENGER_FORMAL_ARCHITECTURE.md)
- [Assurance Roadmap v3 — Meta-Assurance](PROJECTS/EUGENE_MESSENGER_ASSURANCE_ROADMAP_V3.md)

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
