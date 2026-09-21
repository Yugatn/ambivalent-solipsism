# Eugene Messenger — ADR set 0001–007

Status: **accepted for the domain prototype**

These decisions are additive. They do not replace the existing five-layer Eugene Messenger architecture, PICCS-Core, PICCS-Hub, Federation, Plugin API, Eugene UI, Trust Model, Threat Model, EPS-001/001A or EPS-003.

## ADR-0001 — LogicalTime semantics

Use a Hybrid Logical Clock (HLC) for replicated FavoriteOperation ordering. An HLC contains wall-clock milliseconds, a logical counter, and device identity. It gives deterministic ordering but is not a causal proof and is not a CRDT by itself.

## ADR-0002 — Operation idempotence

FavoriteOperation is identified by unique operation_id. Re-delivery of the same operation_id has no second state effect. The prototype keeps applied operation identifiers in an in-memory set; garbage collection is deferred to storage/sync design.

## ADR-0003 — Hidden archive verification boundary

Search interpretation, secret verification and UnlockSession creation are separate concerns. The domain crate stores no plaintext secret and performs no password KDF. A crypto adapter will provide Argon2id or an equivalent platform-secure verifier and constant-time comparison of derived values.

Unlock attempts are excluded from ordinary search history, telemetry, logs, crash reports and sync. The exact implementation boundary is itself a testable claim.

## ADR-0004 — Favorite, Archive and Delete

FavoriteState and ArchiveState are orthogonal. Archive does not clear favorite state. Delete is a separate transition and must use a tombstone or equivalent authenticated historical record so concurrent Favorite and Delete operations converge deterministically.

## ADR-0005 — UnlockSession lifecycle

UnlockSession is process-local and non-serializable. A full application restart requires a new unlock or a separately specified device-authentication flow.

## ADR-0006 — Derived messages

Reply and forward create new message identities and start with FavoriteState::None. Quote does not mutate the source message. Edit preserves the source message's favorite state.

## ADR-0007 — Rate-limit state

The domain prototype uses a local in-memory limiter. Persistent encrypted rate-limit state is deferred until the storage threat model is defined. Rate-limit state is not synchronized as ordinary conversation state.
