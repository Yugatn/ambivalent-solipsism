# Eugene Messenger — Product Architecture

## 1. Product direction

Eugene Messenger is a privacy-oriented communication environment with a familiar Telegram-class interaction model, extended with explicit cognitive-control features. This document defines product behavior and does not replace the formal assurance architecture.

## 2. Feed navigation

### Primary direction: top-to-bottom

The primary conversation feed direction is **top-to-bottom**. Downward navigation is a first-class interaction mode rather than merely an alternative gesture.

### Switchable modes

The user can switch between:

- **Down mode**: primary Eugene mode, downward feed navigation.
- **Up mode**: conventional messenger navigation, upward feed navigation.

The mode is only a UI preference. It never changes message timestamps, sequence numbers, protocol ordering, unread/read state, or cryptographic state.

Accessibility controls must provide an equivalent non-gesture mechanism.

## 3. Message archive

Archive is a first-class message state:

- active;
- archived;
- restored;
- permanently deleted according to retention policy.

Archived content is excluded from the normal feed until the user explicitly opens the archive.

## 4. Hidden archive access

The archive may optionally be protected by a **hidden search command**. No separate PIN/password field is displayed.

The intended flow is:

1. Open message search.
2. Enter the configured secret command into the normal search interface.
3. Recognize the command locally.
4. Do not display the secret as ordinary search text.
5. On successful verification, unlock the archive for the authorized session.
6. On failure, behave like an ordinary unsuccessful search.

Security requirements:

- never store the secret in plaintext;
- use a memory-hard password KDF such as Argon2id or a platform-equivalent secure mechanism;
- never put the command in search history, analytics, logs, crash reports, telemetry, or sync payloads;
- do not reveal whether a failed string was close to the secret;
- apply rate limiting and local lockout;
- define an explicit archive-unlock session timeout;
- do not expose the secret through accessibility APIs or clipboard handling.

The hidden command is a UI access mechanism, not a claim that archived data is cryptographically invisible.

## 5. Telegram-inspired interaction architecture

Eugene Messenger should borrow useful interaction patterns rather than proprietary implementation or branding:

- chat list;
- pinned conversations;
- folders/categories;
- message search;
- replies and quotes;
- forwarding;
- reactions;
- media and documents;
- saved messages;
- mute and notification controls;
- archive;
- per-chat settings;
- message context actions;
- multi-device synchronization;
- local drafts;
- unread counters;
- delivery and read states.

These patterns are redesigned around Eugene's own protocol, threat model, cognitive-safety principles, and assurance requirements.

## 6. Layer separation

- **Presentation Layer**: feed direction, gestures, archive UX, search UX.
- **Conversation State Layer**: ordering, unread/read state, archive state, drafts.
- **Protocol Layer**: identity, epochs, message sequencing, delivery.
- **Crypto Core**: encryption, authentication, key management.
- **Assurance Layer**: claims, TLA+ models, traces, evidence and invalidation.
- **Storage Layer**: encrypted local persistence and retention.
- **Sync Layer**: authenticated synchronization between devices.

A UI preference such as `feed_direction = down` must never alter protocol semantics.

## 7. Product-level data model

    conversation:
      id: conversation-id
      feed_direction: down
      archive:
        enabled: true
        unlock:
          mode: hidden_search_command
          verifier: argon2id-or-platform-equivalent
          session_timeout_seconds: 300
      messages:
        ordering: protocol_sequence
        archive_state:
          - active
          - archived
          - deleted

This is a product-level model; the production schema must be versioned separately.

## 8. Threat boundary

HiddenArchiveUX protects against casual discovery through the normal interface. It is not by itself a cryptographic security boundary. If an attacker controls decrypted application storage, process memory, an unlocked endpoint, or the endpoint itself, archived content may be recoverable.

Therefore `HiddenArchiveUX` must never be used as evidence for `ConfidentialityAtRest` or `EndpointSecurity`.

## 9. Future assurance claims

The product layer introduces future claims without declaring them proven:

- `FeedDirectionInvariant`
- `ArchiveStateIntegrity`
- `HiddenArchiveSecretNonDisclosure`
- `ArchiveUnlockRateLimit`
- `ArchiveSecretNotLogged`
- `ProtocolOrderingIndependentOfUI`
- `ArchivedMessageCryptographicContinuity`

Each claim must enter the Registry with explicit scope, assumptions, falsification criteria, and evidence requirements before receiving an assurance status.

## 10. Implementation sequence

1. Conversation domain model.
2. Bidirectional feed controller.
3. Down-mode UI as the default.
4. Conventional up-mode switch.
5. Archive state and encrypted local persistence.
6. Hidden-search unlock state machine.
7. Secret handling and logging exclusion.
8. Threat-model tests.
9. Formal claim definitions.
10. Reference implementation and conformance evidence.


## Conversation Domain Model

The product layer now has an explicit domain boundary between presentation gestures and persistent conversation state.

### Feed direction

`FeedDirection = Down | Up` is a presentation preference. Down is the primary Eugene Messenger mode: newer messages enter from the top and the user navigates the conversation by swiping from top toward bottom. Up preserves the conventional messenger behavior. Switching direction never changes protocol ordering, sequence numbers, timestamps, delivery/read state, cryptographic state, or message identity.

### Two Favorite folders

A message may belong to one of two symmetric personal collections:

- **Left, Important** — messages the user considers important.
- **Right, Interesting** — messages the user wants to keep as interesting.

A message is placed by physically dragging it beyond the corresponding screen edge. A partial gesture is cancelled; only a committed threshold crossing changes domain state.

`FavoriteState = None | Left | Right`.

The two collections are mutually exclusive for a single message. Moving a message from one side to the other is an explicit state transition. Removing a favorite is an explicit domain command, not an accidental consequence of scrolling.

The folders are orthogonal to Archive: archiving a message does not remove its favorite state, and restoring a message does not change its favorite state. This permits an archived message to remain in Important or Interesting.

### Gesture protocol

The UI emits domain-level events rather than directly mutating message state:

`SwipeBegin(direction)`, `SwipeDrag(distance)`, `SwipeCommit(direction)`, `SwipeCancel`, `FavoriteRemove`.

Only `SwipeCommit` can mutate `FavoriteState`. The threshold, atomicity, idempotence and conflict-resolution rules belong to Conversation State, not to the renderer.

### Multi-device semantics

Favorite changes are user-owned conversation-state mutations. They must carry a monotonic operation identifier and device/session identity. The initial implementation uses deterministic last-operation ordering for convergence; the protocol must not infer semantic importance from wall-clock time alone. A later CRDT implementation may replace this mechanism without changing the UI contract.

### Archive

`ArchiveState = Active | Archived | Restored | Deleted`. Archive is independent of feed direction and favorites. Deleted is terminal at the domain layer unless an explicit recovery policy is introduced.

### Hidden archive command

The archive can expose a local unlock session through the normal message-search surface. The command is deliberately not represented as a visible password field. The secret is not persisted in search history, telemetry, sync payloads, logs, or accessibility labels. Unlock state is temporary and scoped to the local device/session. This is an access-control UX layer, not a replacement for encryption at rest.

### Core invariants

- **Favorite exclusivity:** one message cannot simultaneously be in Left and Right.
- **Favorite atomicity:** no externally observable intermediate favorite state exists during a committed gesture.
- **Archive/Favorite orthogonality:** archive transitions do not mutate favorite state.
- **UI/protocol independence:** changing feed direction cannot mutate protocol ordering or cryptographic state.
- **Secret non-disclosure:** the hidden archive command is absent from ordinary search results, history, telemetry and synchronization.

These invariants are registered as assurance targets but remain unproven until executable tests and formal models produce evidence.

## Reference Domain Types

A future Rust core should expose equivalent domain types without coupling them to UI widgets:

```rust
pub enum FeedDirection { Down, Up }
pub enum FavoriteState { None, Left, Right }
pub enum ArchiveState { Active, Archived, Restored, Deleted }

pub struct FavoriteOperation {
    pub message_id: MessageId,
    pub target: FavoriteState,
    pub operation_id: OperationId,
    pub device_id: DeviceId,
}
```

The renderer translates a physical gesture into these commands; storage and synchronization persist the resulting domain event. The protocol remains the source of truth for message ordering.

## Telegram-inspired product patterns and layer boundaries

The architecture may borrow mature interaction patterns from Telegram without copying its implementation or protocol. Patterns are classified before implementation:

| Pattern | Layer | Protocol impact |
|---|---|---|
| Chat list, pinned chats, folders, mute | Presentation | None or local preference |
| Replies, forwarding, reactions | Conversation State | Message references / mutations |
| Drafts | Conversation State | Optional synchronization |
| Delivery and read states | Protocol | Acknowledgement events |
| Multi-device synchronization | Protocol | Replicated conversation state |
| Media and documents | Protocol + Storage | Content addressing, transfer and integrity |
| Archive and two Favorite folders | Conversation State | Replicated user-owned state |

This keeps Telegram-inspired usability separate from Eugene Messenger's protocol and assurance claims.

## Assurance targets introduced by this domain model

The following targets are intentionally not promoted to `model_checked`:

`FeedDirectionInvariant`, `FavoriteStateAtomicity`, `FavoriteFolderSymmetry`, `ArchiveFavoriteOrthogonality`, `ArchiveUnlockRateLimit`, `HiddenArchiveSecretNonDisclosure`, and `ProtocolOrderingIndependentOfUI`.

Each requires executable tests and, where appropriate, a TLA+ model before a stronger assurance status is allowed.


## 11. Executable domain baseline

The product model is now backed by an independent Rust domain prototype under `eugene-messenger/core/domain`.

The baseline defines:

- `FavoriteState = None | Left | Right`;
- `FavoriteOperation` with `operation_id`, `device_id` and HLC timestamp;
- deterministic operation ordering;
- duplicate-operation idempotence;
- normalized swipe distance with a 30% default threshold and 500 ms maximum duration;
- independent `ArchiveState`;
- process-local, non-serializable `UnlockSession`;
- local hidden-archive rate limiting.

These are implementation artifacts, not claims of completed formal verification. The Claim Registry remains at `status: specified`, `level: 2` until executable evidence and formal models are actually checked.
