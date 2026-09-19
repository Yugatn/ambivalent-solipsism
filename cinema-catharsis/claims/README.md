# Claim Specification v0.3.0

Claim — версионируемое эпистемическое утверждение проекта.

## Статусы

- definition
- observation
- measurement
- assumption
- hypothesis
- literature
- interpretation
- philosophical

confidence не является status и не означает вероятность истинности.

## Минимальная структура

```yaml
claim_id: CK-CLAIM-0001
claim: "screen_time_share вычисляется как T_omega / T"
status: definition
scope:
  object: program_manifestation
  level: L3
source:
  type: internal
  document: "CONTENT_PASSPORT_3.0.md"
  version: "0.3.0"
method:
  type: formula
validation:
  required: false
uncertainty:
  applicable: false
versions:
  ontology: "0.3.0"
  measurement: "0.3.0"
  validation: "0.1.0"
sensitivity_analysis:
  required: false
correction_history: []
publishable: true
```

Для scientific claim по возможности фиксируются population, design, comparator, outcome, effect, uncertainty и limitations.

literature — provenance/source type, а не сила доказательства.

Для assumption обязательны value/range, validation plan и sensitivity analysis.

Интерпретации могут быть множественными:

```yaml
interpretations:
  - label: romanticization
    confidence: 0.42
    basis:
      - repeated_positive_social_reaction
  - label: irony
    confidence: 0.31
    basis:
      - contradictory_dialogue
```

Это не означает вероятность истинности интерпретации.

Исправления сохраняются как original → correction → corrected; старый claim получает superseded.
Полная JSON Schema находится в schema/claim.schema.json.
