# PROF-MAP — Data Architecture

## Принцип

Данные PROF-MAP разделяются по смыслу. Профиль, навыки, среда, ценности и ограничения не должны попадать в одну шкалу.

## Слои данных

```
questions.json
      |
      v
raw responses
      |
      +--> profile scores
      +--> AI profile
      +--> W
      +--> V
      +--> C
      |
      v
structured profile
      |
      +--> professions.json
      +--> skills.json
      |
      v
Match + Skill Gap
      |
      v
report
```

## Рекомендуемые файлы

```
PROF-MAP/
  data/
    scales.json
    questions.json
    professions.json
    skills.json
  js/
    scoring.js
    matching.js
    interpretation.js
  index.html
```

## Важное правило

Вопросы не должны быть зашиты в HTML. Это позволит менять item bank без переписывания интерфейса.

## Профиль пользователя

Пример:

```json
{
  "profile": {
    "AN": 4.1,
    "LRN": 4.5,
    "DIG": 3.8
  },
  "ai_profile": {
    "literacy": 4.2,
    "prompting": 3.8,
    "verification": 4.6
  },
  "environment": {},
  "values": {},
  "constraints": {},
  "skills": {}
}
```

Этот объект является структурированным результатом, а не «цифровым двойником личности».

## Расширяемость

Архитектура должна позволять подключать дополнительные assessment-модули без изменения базовых шкал. Cattell, Wheel of Balance и другие инструменты могут иметь собственные модели данных и собственные интерпретации.

Их результаты не следует автоматически складывать в PROF-MAP Match.

## Приватность

Для MVP предпочтительно локальное хранение и экспорт пользователем. Серверная передача данных появляется только при необходимости и должна иметь отдельное согласие, политику хранения и механизм удаления.
