# Policy Engine СТСети

Policy Engine отвечает за проверку того, разрешено ли действие в конкретном контексте.

## 1. Разделение

Policy Engine не должен одновременно собирать произвольные данные, расширять собственный scope, скрывать основание решения и быть единственным каналом апелляции.

## 2. Вход

Проверка может использовать actor, subject, resource, action, purpose, context, applicable rules, consent или другое правовое основание, а также data classification.

## 3. Результат

Минимальный результат:

- permit;
- deny;
- review;
- unknown.

unknown является полноценным результатом и не преобразуется автоматически в deny.

## 4. Reason code

Каждый deny, review или ограниченный permit получает машинно читаемый reason code.

Человеческое объяснение строится поверх него.

## 5. Policy version

Результат связан с версией применённых правил.

## 6. Conflict

При конфликте политик применяется заранее определённая стратегия разрешения конфликта.

## 7. No authority by inference

Policy Engine не выводит новое полномочие только из того, что действие технически возможно.

## 8. Separation from enforcement

Проверка разрешённости и фактическое исполнение действия разделяются там, где этого требует уровень риска.


## Phase 6 Policy Engine / Impact Evaluation contract

The Policy Engine evaluates whether a proposed transition or action is permitted under explicit policy. It does not itself execute the Action and does not infer human value from policy outcomes.

### 1. Policy evaluation input

A policy evaluation MUST identify subject/context, requested operation, applicable policy version, relevant Decision/Action type, evidence references, provenance, current state, permissions and impact classification.

### 2. Decision separation

Policy evaluation produces a PolicyDecision or review requirement. It MUST NOT directly execute an Action. A permitted PolicyDecision remains subject to the Decision and Action boundaries already defined in the architecture.

### 3. Impact classification

Impact is a contextual property of the proposed operation, not a score of subject worth. At minimum, the engine distinguishes ordinary, sensitive and high-impact operations according to declared policy criteria. High-impact operations retain required human review.

### 4. Unknown and insufficiency

Insufficient evidence, missing provenance or policy conflict MUST produce an explicit UNKNOWN, REVIEW_REQUIRED or equivalent unresolved outcome. The engine MUST NOT silently convert uncertainty into denial, approval or a negative subject status.

### 5. Policy versioning

Every policy outcome records the policy identifier and version used. Policy changes do not rewrite historical decisions. A changed policy can trigger re-evaluation of affected current decisions according to impact rules.

### 6. Explanation and audit

The engine MUST expose the applicable rule basis, relevant evidence/provenance references, policy version, outcome, uncertainty and review path sufficient for authorized review. Explanation MUST NOT disclose unrelated sensitive data.

### 7. No hidden authority

Technical access, data possession, projection membership or provenance visibility MUST NOT create policy authority. Policy authority comes from explicitly defined governance and Permission rules.

### 8. Phase 6 invariants

- Q1: policy evaluation is separate from Action execution.
- Q2: every policy outcome is versioned and auditable.
- Q3: impact classification is contextual, not a subject-value score.
- Q4: high-impact operations retain prescribed human review.
- Q5: uncertainty remains explicit and cannot silently become a negative outcome.
- Q6: policy changes preserve historical decision provenance.
- Q7: technical access cannot become normative authority.
- Q8: explanations remain purpose-bound and privacy-minimized.

Runtime policy evaluation remains an implementation task.


## Phase 6 Impact Evaluation Matrix

Impact classification describes the consequences and reversibility of an operation. It is not a ranking of subjects.

| Impact class | Typical characteristics | Required controls |
|---|---|---|
| ordinary | reversible, low external consequence | policy evaluation, audit |
| sensitive | affects privacy, access, reputation or support conditions | explicit purpose, provenance, stronger audit, correction path |
| high-impact | materially affects rights, livelihood, access, safety, durable status or irreversible consequences | explicit evidence basis, policy version, human review, explanation, recovery/appeal path |

### Impact modifiers

Classification MUST consider operation, affected domain, reversibility, duration, scope, uncertainty and potential external effects. The same operation MAY have different impact classes in different contexts.

### Protected evaluation flow

1. establish applicable policy and version;
2. establish current state and Permission;
3. resolve relevant Evidence and provenance;
4. classify impact;
5. evaluate policy constraints;
6. produce PolicyDecision or REVIEW_REQUIRED;
7. apply human review where required;
8. create separate Decision when a normative consequence is authorized;
9. only then permit an Action pathway.

A failed or unresolved step MUST NOT be silently skipped.

### Phase 6 dependency matrix

| Input | Used for | Must not imply |
|---|---|---|
| Evidence | factual/evidentiary basis | authority to act |
| Provenance | source lineage | truth by graph completeness |
| Policy | constraint | execution |
| Permission | access authorization | normative decision |
| Projection | current read context | historical truth |
| Impact class | required safeguards | subject value |
| Human review | required oversight | automatic approval |
| PolicyDecision | policy evaluation result | executed Action |

