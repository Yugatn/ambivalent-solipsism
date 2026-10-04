# Concept Audit 2026-10-04

## Purpose
Проверить, какие инженерные предложения, сформулированные в текущем цикле развития АС и SymbiontOS, уже реализованы в GitHub, а какие оставались только предложениями.

## Implemented
- `PSYCHOPHYSIOLOGY_SYNTHESIS.md` — создан.
- `QIGONG_SYNTHESIS.md` — создан.
- `AYURVEDA_INDIAN_MEDICINE_SYNTHESIS.md` — создан.
- `MEDICAL_STATE_MACHINE.md` — создан.
- `MEDICAL_SAFETY_GATE.md` — создан.
- `CLINICAL_EVIDENCE_MATRIX.md` — создан.
- `ADVERSE_EVENT_SCHEMA.md` — создан.
- `SHARED_DECISION_PROTOCOL.md` — создан.
- Ранее созданные `MEDICINE_SYNTHESIS.md`, `N_OF_1_PROTOCOL.md`, `INTERVENTION_LADDER.md`, `EVIDENCE_LEDGER.md`, `STATE_SCHEMA.md`, `SAFETY_INVARIANTS.md` также присутствуют в репозитории.

## Missing after the chat proposals
Следующие файлы были предложены, но на момент аудита отсутствовали:
- `QUANTUM_PHYSICS_PSYCHOLOGY_SYNTHESIS.md`.
- `PSYCHOPHYS_STATE_SCHEMA.md`.
- `INTEROCEPTION_PROTOCOL.md`.
- `AUTONOMIC_RECOVERY_MODEL.md`.
- `PSYCHOPHYS_CAUSAL_GRAPH.md`.
- `SUBJECTIVE_PHYSIOLOGICAL_DISCORDANCE.md`.
- `QIGONG_PRACTICE_SCHEMA.md`.
- `QIGONG_SESSION_PROTOCOL.md`.
- `QIGONG_EVIDENCE_MATRIX.md`.
- `QIGONG_SAFETY_GATE.md`.
- `QIGONG_FIRST_THIRD_PERSON.md`.

## Scientific synthesis gap
Квантово-физический слой был подробно подготовлен в разговоре, но не был зафиксирован после неудачного коммита. Это является главным пропуском текущего цикла.

## Architecture gap
Исследовательские синтезы и медицинские протоколы существуют, но им не хватало явных schema/protocol файлов, которые связывают first-person data, physiological data, evidence status, safety and intervention state.

## Audit conclusion
Ничего из уже существующих материалов удалять не требуется. Основная задача — довести ранее обещанные спецификации до GitHub и связать их через общий Evidence/Safety/State слой.

## New integration rule
Каждая новая традиционная практика или научная область должна проходить один и тот же pipeline:
**Claim → Evidence type → Measurement → Alternative explanation → Safety → Applicability → Subject decision → Outcome → Review.**

## Priority
1. Restore quantum synthesis.
2. Formalize psychophysiology schemas.
3. Formalize qigong schemas and safety.
4. Connect all of them to medical state, evidence and shared decision layers.

## Invariant
**No scientific metaphor may silently become a physical mechanism.**
**No population evidence may silently become an individual diagnosis.**
**No intervention may silently bypass the Safety Gate.**
**No model may silently replace the Subject.**