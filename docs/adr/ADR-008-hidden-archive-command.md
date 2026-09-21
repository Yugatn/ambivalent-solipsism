# ADR-008: Hidden archive command in message search

## Decision

The archive unlock command is entered through the ordinary message-search surface. No dedicated password field is displayed.

The verifier is stored as a password-derived verifier, never plaintext. Search history, telemetry, synchronization payloads and application logs must not contain the secret or a reversible representation.

Unlock creates a temporary local session with explicit expiration. Failed attempts are rate-limited.

## Security boundary

This is UX access control, not a substitute for encryption at rest or endpoint security. Timing, memory-forensics and compromised-endpoint attacks require explicit threat-model treatment.

## Assurance

HiddenArchiveSecretNonDisclosure and ArchiveUnlockRateLimit remain specified until executable evidence exists.
