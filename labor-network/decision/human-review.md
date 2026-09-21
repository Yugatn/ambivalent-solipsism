# Human Review

## 1. Назначение

Human Review является процессом пересмотра заранее определённых высокоэффектных или спорных решений.

Это не декоративная кнопка «обратиться к человеку».

## 2. Когда требуется

Review может требоваться при:

- существенном ограничении доступа к труду;
- значительном финансовом последствии;
- конфликте данных;
- низкой уверенности при высоком воздействии;
- оспаривании существенного факта;
- обнаружении возможной системной ошибки.

## 3. Независимость

По возможности пересмотр не должен полностью совпадать с контуром, первоначально создавшим решение.

## 4. Материалы

Reviewer получает минимально необходимый набор:

- решение;
- основание;
- применённую policy version;
- релевантные Evidence;
- Dispute;
- историю существенных изменений.

## 5. Запрет расширения

Reviewer не должен получать автоматически всю историю субъекта.

## 6. Результаты

Минимальные результаты:

- confirm;
- modify;
- reverse;
- request_more_information;
- escalate.

## 7. Объяснение

Результат должен иметь структурированное основание.

## 8. Срок

Для существенных ограничений должен существовать целевой срок пересмотра.

## 9. Временная мера

Временное ограничение должно иметь срок и условия повторной проверки.

## 10. Принцип

> Human Review восстанавливает процессуальную субъектность, но не отменяет необходимость формальных правил.


## Phase 7 Human Review contract

Human Review is a bounded procedural control for high-impact, disputed or unresolved outcomes. It does not become a second unrestricted data-access layer and does not itself execute Actions.

### Review trigger

A review MUST be created when an applicable policy, impact classification, dispute rule or protected transition requires human oversight. The trigger MUST record the basis and policy version.

### Review packet

The review packet MUST be purpose-bound and contain only the minimum material required to evaluate the issue: affected Decision/PolicyDecision, reason code, relevant Evidence and provenance, applicable policy version, current relevant state, and dispute/history entries necessary for the question.

### Reviewer independence

Where feasible, the reviewer MUST be organizationally or procedurally separated from the original automated or human decision path. A conflict of interest or inability to perform independent review MUST be recorded rather than silently ignored.

### Outcomes

The review MUST produce a structured outcome such as confirm, modify, reverse, request_more_information or escalate. The outcome MUST identify reviewer role, timestamp, reason, evidence considered and resulting state transition where applicable.

### Deadline and temporary restrictions

High-impact review has a declared target deadline. Temporary restrictions MUST have an expiry or re-check condition and MUST NOT become indefinite merely because review is delayed.

### Contestability and recovery

A subject MAY contest a reviewable outcome according to the applicable dispute process. Review, reversal and recovery preserve the original history and do not silently rewrite the initial Decision or Action record.

### Data boundary

Human Review MUST NOT expand access to the complete subject history merely because review was triggered. Additional data requires a separate purpose and authority basis.

### Phase 7 invariants

- H1: review triggers are explicit and auditable;
- H2: review packets are purpose-bound and minimally disclosed;
- H3: reviewer independence/conflict is explicit;
- H4: review outcomes are structured and versioned;
- H5: high-impact review has a declared deadline or service target;
- H6: temporary restrictions have expiry/re-check conditions;
- H7: review cannot execute Action directly;
- H8: reversal/recovery preserves historical records;
- H9: contestability remains available where applicable;
- H10: review does not create unrestricted profile access.

Runtime review queue, assignment, SLA enforcement and executable conformance remain implementation work.
