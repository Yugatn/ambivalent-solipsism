# ADR-007: Down-first conversation feed

## Decision

FeedDirection::Down is the Eugene Messenger default. Newer conversation items are presented toward the top and primary navigation moves from top toward bottom.

FeedDirection::Up remains available as the conventional mode.

Feed direction is presentation state only. It cannot alter protocol sequence, timestamps, message identity, delivery/read state or cryptographic state.
