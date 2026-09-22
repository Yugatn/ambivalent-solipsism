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
- `life.prompt` — жизнь как метафорический промпт, заданный до рождения

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
- `life.prompt` related_to `subject.perception`
- `life.prompt` related_to `consciousness.interface`
- `life.prompt` related_to `development.law`
- `life.prompt` related_to `ai.model`

## Ограничение

Связь в графе не является доказательством истинности связанного положения. Она фиксирует отношение внутри модели книги.

- `consciousness.prenatal_perception` related_to `subject.perception`
- `consciousness.prenatal_perception` related_to `consciousness.interface`
- `consciousness.prenatal_perception` related_to `society.superposition`
- `consciousness.prenatal_perception` related_to `life.prompt`

- `consciousness.continuity` related_to `consciousness.prenatal_perception`
- `consciousness.continuity` related_to `consciousness.interface`
- `consciousness.continuity` related_to `subject.perception`
- `consciousness.continuity` extends `reality.residual`

- `consciousness.rebirth_recursion` related_to `consciousness.continuity`
- `consciousness.rebirth_recursion` related_to `consciousness.prenatal_perception`
- `consciousness.rebirth_recursion` related_to `society.superposition`
- `consciousness.rebirth_recursion` related_to `life.prompt`
- `consciousness.rebirth_recursion` related_to `reality.residual`

- `development.law` applies_to `ai.model`
- `development.law` applies_to `ai.symbiotic_intelligence`
- `ai.guardian_principle` extends `development.law`
- `ai.guardian_principle` related_to `consciousness.continuity`

- `subject.personality` — личность как исторически сформированный конструкт памяти, опыта и социальных ролей
- `perception.projection` — феномен проекции и активное конструирование воспринимаемой реальности
- `body.avatar` — тело как метафорический аватар, скафандр и биологический вычислительный комплекс

- `subject.personality` related_to `subject.perception`
- `subject.personality` related_to `society.superposition`
- `perception.projection` related_to `reality.model`
- `perception.projection` related_to `consciousness.information`
- `body.avatar` related_to `subject.perception`
- `body.avatar` related_to `consciousness.interface`


- `perception.cave` — пещера как граница доступного субъекту восприятия
- `social.myelin` — интернет как функциональная аналогия нового коммуникационного слоя социальной нервной системы
- `social.organism.stability` — Закон устойчивости системы
- `social.cell.human` — человек как аналог клетки социального организма
- `social.ideology.dna` — идеология как смысловая ДНК социального организма
- `social.octopus` — человечество как распределённая система с локальными центрами обработки
- `brain.fractal_history` — мозг как фрактальная карта исторической непрерывности
- `cosmology.cellular_world` — клеточная космологическая гипотеза
- `epistemology.majority` — большинство не является критерием истины

- `perception.cave` related_to `subject.perception`
- `perception.cave` related_to `reality.model`
- `social.myelin` related_to `consciousness.information`
- `social.myelin` related_to `social.organism.stability`
- `social.organism.stability` extends `development.law`
- `social.organism.stability` related_to `social.cell.human`
- `social.cell.human` related_to `subject.perception`
- `social.cell.human` related_to `subject.other`
- `social.ideology.dna` related_to `social.cell.human`
- `social.ideology.dna` related_to `social.organism.stability`
- `social.octopus` related_to `social.cell.human`
- `social.octopus` related_to `social.myelin`
- `brain.fractal_history` related_to `subject.perception`
- `brain.fractal_history` related_to `consciousness.information`
- `brain.fractal_history` related_to `cosmology.cellular_world`
- `cosmology.cellular_world` related_to `reality.residual`
- `cosmology.cellular_world` related_to `brain.fractal_history`
- `epistemology.majority` related_to `reality.residual`
- `epistemology.majority` related_to `development.law`

- `mortality.generation` — смена поколений при непрерывности человечества
- `mortality.body_horizon` — ограниченный телом временной горизонт
- `mortality.panic_hypothesis` — гипотеза о том, что паника перед конечностью может сужать горизонт решений
- `future.subjects` — будущие субъекты как продолжение пространства развития

- `mortality.generation` related_to `social.organism.stability`
- `mortality.generation` related_to `social.cell.human`
- `mortality.generation` related_to `development.law`
- `mortality.body_horizon` related_to `subject.perception`
- `mortality.body_horizon` related_to `body.avatar`
- `mortality.panic_hypothesis` extends `mortality.body_horizon`
- `mortality.panic_hypothesis` related_to `social.organism.stability`
- `mortality.panic_hypothesis` related_to `development.law`
- `future.subjects` related_to `subject.other`
- `future.subjects` related_to `development.law`
- `future.subjects` related_to `mortality.generation`

- `temporal.inheritance` — получение мира одним поколением и его передача следующему
- `temporal.scale` — столетие как мысленный масштаб смены поколений
- `posthumous.causality` — последствия действий, продолжающиеся после жизни автора
- `future.possibility` — сохранение пространства развития будущих субъектов

- `temporal.inheritance` related_to `mortality.generation`
- `temporal.inheritance` related_to `future.subjects`
- `temporal.inheritance` related_to `social.organism.stability`
- `temporal.scale` related_to `mortality.generation`
- `temporal.scale` related_to `subject.perception`
- `posthumous.causality` related_to `mortality.body_horizon`
- `posthumous.causality` related_to `development.law`
- `posthumous.causality` related_to `social.organism.stability`
- `future.possibility` related_to `future.subjects`
- `future.possibility` related_to `development.law`
- `future.possibility` related_to `reality.residual`

- `symbiont.os.ecosystem` — Симбионт ОС как распределённая информационная экосистема интеллектуальных агентов
- `symbiont.os.privacy` — минимизация раскрытия идентичности и данных
- `symbiont.os.anonymity` — архитектурная цель анонимной коммуникации при сохранении проверяемых полномочий
- `symbiont.os.agent_mesh` — взаимодействие специализированных агентов без обязательного объединения всех данных
- `symbiont.os.authorization` — разделение сообщения, идентичности, полномочия и разрешения на действие
- `symbiont.os.audit` — независимая проверка действий, ошибок и ограничений
- `symbiont.os.uncertainty` — сохранение неопределённости о состоянии агентов и среды

- `symbiont.os.ecosystem` extends `ai.symbiotic_intelligence`
- `symbiont.os.ecosystem` related_to `engineering.symbiontos`
- `symbiont.os.ecosystem` related_to `social.myelin`
- `symbiont.os.ecosystem` related_to `social.organism.stability`
- `symbiont.os.privacy` related_to `symbiont.os.ecosystem`
- `symbiont.os.privacy` related_to `development.law`
- `symbiont.os.anonymity` related_to `symbiont.os.privacy`
- `symbiont.os.anonymity` related_to `engineering.eugene_messenger`
- `symbiont.os.agent_mesh` related_to `ai.symbiotic_intelligence`
- `symbiont.os.agent_mesh` related_to `symbiont.os.ecosystem`
- `symbiont.os.authorization` related_to `engineering.eugene_messenger`
- `symbiont.os.authorization` related_to `ethics.piccs`
- `symbiont.os.authorization` related_to `symbiont.os.audit`
- `symbiont.os.audit` related_to `ethics.piccs`
- `symbiont.os.audit` related_to `symbiont.os.uncertainty`
- `symbiont.os.uncertainty` related_to `reality.residual`
- `symbiont.os.uncertainty` related_to `ai.subjectivity`
