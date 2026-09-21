# ADR-006: Two symmetric Favorite folders

## Decision

Eugene Messenger exposes two symmetric personal message collections:

- Left edge: **Important**
- Right edge: **Interesting**

Dragging a message beyond the corresponding edge commits the classification. A partial drag is cancelled and produces no domain mutation.

The two collections are mutually exclusive for one message. Moving from one to the other is a replacement operation, not an accumulation of labels.

## Boundaries

The gesture belongs to Presentation. The resulting FavoriteState belongs to Conversation State. Synchronization persists the domain operation. Protocol message ordering is unaffected.

Archive state is orthogonal to favorite state.

## Consequences

The implementation must test atomicity, idempotence, multi-device convergence and archive/favorite independence.
