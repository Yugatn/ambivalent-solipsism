# Adverse Event Schema

## Purpose
Фиксировать нежелательные события как данные для безопасности и обучения системы, не превращая одно событие автоматически в доказательство причинности.

## Event fields
- event_id
- timestamp
- subject_state_before
- intervention_or_exposure
- event_description
- onset
- severity
- duration
- outcome
- actions_taken
- escalation
- concomitant_factors
- concurrent_medications
- objective_measurements
- subjective_report
- suspected_relatedness
- certainty
- reporter
- follow_up
- preventability_assessment

## Causality discipline
Temporal sequence alone does not establish causality.
Следует различать event occurrence, temporal association, suspected relationship и established causality.

## Learning loop
WHO recommends patient-safety incident reporting as part of a learning system and emphasizes cautious interpretation of incident-report data. citeturn0search8turn0search27

**Adverse Event ≠ Proven Causal Effect.**
**No Report ≠ No Harm.**