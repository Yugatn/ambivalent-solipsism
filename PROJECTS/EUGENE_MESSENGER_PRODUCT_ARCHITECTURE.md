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
