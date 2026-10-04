# SymbiontOS Safety Invariants

## Mandatory Invariants

1. Biomarker ≠ diagnosis.
2. Subjective improvement ≠ cellular healing proof.
3. EEG frequency ≠ universal health frequency.
4. THC ≠ therapeutic control layer.
5. Fasting duration must not be autonomously extended because of subjective improvement.
6. Algorithmic inference must not independently initiate brain stimulation.
7. The Subject can stop observation and intervention.
8. Intervention events are logged.
9. Uncertainty is visible.
10. Safety escalation has priority over optimization.

## Medical Boundary

SymbiontOS may observe and organize data. It must not present an unvalidated algorithmic interpretation as medical fact.

Any future medical-device interface belongs to a separate clinical interface with its own validation, authorization and safety controls.

## Cognitive Safety

The system must avoid statements such as:

«Твой мозг работает неправильно, поэтому система должна исправить его частоту».

Preferred formulation:

«Обнаружен паттерн с указанной степенью неопределенности; доступны несколько объяснений».

## Autonomy

Required controls:

- Pause
- Stop
- Disconnect Device
- Export Data
- Review Evidence

## Fail-Safe

When confidence is low, data quality is poor, or a safety condition is triggered, the system moves toward observation-only or escalation rather than stronger intervention.

## Core Principle

**Safety takes precedence over optimization.**
