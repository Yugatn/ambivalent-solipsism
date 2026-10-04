# Psychophysiological State Schema

## Purpose
Represent a time-indexed state without reducing the Subject to biomarkers.

## Fields
- subject_state_id
- timestamp
- subjective_state
- affect
- arousal
- stress_appraisal
- interoceptive_experience
- HR
- HRV
- respiration
- blood_pressure
- sleep_context
- activity_context
- endocrine_context
- immune_context
- metabolic_context
- social_context
- medication_context
- intervention_context
- baseline_reference
- data_quality
- missing_data
- uncertainty

## Rules
Every physiological field must retain measurement method, timestamp and quality where available.
Subjective and physiological observations remain separate namespaces.
One measurement must not be promoted to a global health score without validation.

## AS invariant
**State ≠ Identity.**
**Biomarker ≠ Subject.**