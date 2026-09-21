# Identity Continuity

This is the second formalization track after Anti-Replay.

The first version is deliberately small. It models:
- an active identity;
- a current key;
- revocation;
- a rejected operation after revocation.

The model does not yet claim cryptographic key continuity, recovery security, forward secrecy, or production conformance.

The broken model introduces an explicit resurrection transition so TLC can falsify the no-resurrection property once the invariant is made precise.

This model will be refined before implementation.