# Federation Contract СТСети

Федерация соединяет независимые узлы без передачи им полного контроля над субъектом.

## 1. Минимальное утверждение

Предпочтительно передавать проверяемое утверждение вместо исходного массива данных.

Пример: «квалификация X подтверждена до даты Y».

## 2. Provenance

Удалённый узел должен иметь возможность проверить происхождение утверждения или его доверенный источник.

## 3. Scope

Получатель получает только полномочия и данные, предусмотренные контрактом.

## 4. Trust

Доверие к узлу не означает доверие ко всем его утверждениям безусловно.

## 5. Revocation

Должен существовать механизм отзыва ранее выданного разрешения или подтверждения.

## 6. Failure

Недоступность узла не должна автоматически становиться отрицательным фактом о субъекте.

## 7. Conflict

Конфликтующие утверждения сохраняются и направляются в определённый процесс reconciliation.

## 8. Privacy

Федеративный запрос должен иметь purpose и минимальный набор данных.

## 9. Audit

Межузловые существенные запросы и ответы должны быть трассируемы.

## 10. Boundary

Федерация не должна незаметно превращаться в единый централизованный профиль субъекта.


## Phase 9 Federation contract

Federation connects independently governed nodes through bounded, verifiable assertions. Federation is an interoperability mechanism, not a mechanism for constructing a centralized subject profile or transferring unrestricted authority.

### 1. Node identity and trust

Every federated node MUST have a stable node identity, declared governance scope, protocol/schema version and trust/provenance metadata. Connectivity MUST NOT itself imply trust, Permission or policy authority.

### 2. Assertion minimization

A federation message MUST carry the minimum assertion required for its declared purpose. A node SHOULD prefer verifiable claims such as status, validity, capability or authorization reference over copying the underlying subject record.

### 3. Assertion semantics

Each assertion MUST identify issuer, subject/reference scope, purpose, issued_at, validity interval where applicable, schema/protocol version, provenance/reference basis and integrity material. The receiving node MUST distinguish asserted facts from locally verified facts.

### 4. Authority boundary

An assertion received from another node MUST NOT create broader local authority than the receiving node's own governance and Permission rules allow. Federation cannot bypass local PolicyDecision, Human Review or Action controls.

### 5. Revocation and correction

Assertions MUST support expiry, revocation and supersession where applicable. A correction or revocation at the source MUST be propagable to affected dependent assertions without rewriting the historical fact that the earlier assertion was issued.

### 6. Failure and disagreement

Unavailable, stale, contradictory or unverifiable remote assertions MUST remain explicit. A remote failure MUST NOT silently become a negative subject status. Conflict resolution MUST be policy-defined and auditable.

### 7. Privacy boundary

Federated access MUST be purpose-bound, permissioned and minimized. A node MUST NOT infer permission to retrieve unrelated history merely because a federated relationship exists.

### 8. Profile-construction prohibition

Federation MUST NOT be used to silently aggregate cross-node activity into an unrestricted individual profile. Aggregate/system analysis MUST remain distinguishable from individual profiling.

### 9. Local sovereignty

Each node retains responsibility for local policy enforcement, subject rights, dispute handling and protected Action execution. A remote node may provide evidence or an assertion; it does not become the local decision maker by default.

### 10. Protocol evolution

Federation messages MUST declare compatible schema/protocol versions. Unknown versions or unsupported fields MUST follow an explicit compatibility path rather than being silently reinterpreted.

### Phase 9 invariants

- F1: node identity and governance scope are explicit;
- F2: connectivity does not create authority;
- F3: assertions are purpose-bound and minimized;
- F4: remote assertions remain distinguishable from locally verified facts;
- F5: revocation, expiry and correction are explicit;
- F6: remote failure/conflict remains UNKNOWN or follows declared resolution policy;
- F7: federation cannot bypass local Permission, Policy, Review or Action controls;
- F8: federation cannot silently create unrestricted individual profiles;
- F9: local node sovereignty remains explicit;
- F10: protocol/schema evolution is versioned and auditable.

Runtime federation transport, cryptographic verification, compatibility negotiation and executable conformance remain implementation work.
