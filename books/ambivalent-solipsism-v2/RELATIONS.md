# Граф новой версии книги

Этот файл является рабочей картой взаимосвязей. Он не заменяет тексты глав.

## Устойчивые узлы

- `subject.perception` — субъект восприятия
- `subject.other` — Другой как субъект
- `reality.model` — модель реальности
- `reality.residual` — остаток неизвестного
- `consciousness.interface` — сознание как интерфейс
- `consciousness.information` — синтез информации
- `consciousness.attention` — внимание и локальная представленность
- `society.superposition` — социальная суперпозиция
- `development.law` — Закон развития
- `ai.model` — ИИ как моделирующая система
- `ai.subjectivity` — субъектность искусственных систем
- `ai.perception` — ИИ в информационном контуре восприятия
- `ai.symbiotic_intelligence` — симбиотический интеллект
- `ethics.piccs` — PICCS
- `engineering.symbiontos` — SymbiontOS
- `engineering.eugene_messenger` — Eugene Messenger

## Типы связей

- `depends_on` — опирается на
- `extends` — развивает
- `related_to` — связан с
- `contrasts_with` — противопоставляется
- `applies_to` — применяется к
- `questions` — ставит под вопрос
- `critiques` — подвергает критике
- `implemented_by` — получает инженерное воплощение

## Первичная карта

- `consciousness.interface` depends_on `subject.perception`
- `consciousness.interface` related_to `consciousness.information`
- `consciousness.interface` related_to `consciousness.attention`
- `ai.perception` extends `consciousness.interface`
- `ai.perception` related_to `ai.model`
- `ai.symbiotic_intelligence` extends `ai.perception`
- `ai.symbiotic_intelligence` related_to `subject.other`
- `reality.model` related_to `reality.residual`
- `society.superposition` depends_on `subject.other`
- `development.law` applies_to `society.superposition`
- `ethics.piccs` applies_to `reality.residual`
- `engineering.symbiontos` implements philosophical and methodological implications only where formalization is justified
- `engineering.eugene_messenger` related_to `ai.symbiotic_intelligence`

## Ограничение

Связь в графе не является доказательством истинности связанного положения. Она фиксирует отношение внутри модели книги.
