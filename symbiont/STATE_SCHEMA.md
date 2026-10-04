# SymbiontOS State Schema

## Purpose

Каноническая схема состояния для наблюдательного контура SymbiontOS.

Она не является медицинским диагнозом и не должна использоваться как самостоятельная система клинического решения.

## State Domains

- metabolic_state
- nutrition_state
- hydration_state
- sleep_state
- activity_state
- autonomic_state
- neurophysiological_state
- subjective_state
- medication_context
- intervention_context
- confidence
- missing_data

## Observation Record

Каждое наблюдение должно содержать:

- observation_id
- timestamp
- source
- domain
- value
- unit
- quality
- confidence
- provenance
- evidence_status

## Rules

1. Raw measurement нельзя смешивать с derived feature.
2. Subjective report нельзя автоматически превращать в physiological fact.
3. Biomarker нельзя автоматически превращать в diagnosis.
4. Missing data должны быть явными.
5. Confidence относится к конкретному выводу, а не ко всему субъекту.
6. Состояние является временным: state(t), а не фиксированной сущностью.
7. Subject не равен State Vector.

## Evidence Status

- OBSERVED
- DERIVED
- MODELLED
- CORRELATED
- CAUSAL_CANDIDATE
- CLINICALLY_VALIDATED
- NOT_TESTED
- CONFLICTED
- RESIDUAL

## Core Principle

**State is a model of the current condition, not the Subject itself.**
