# Yugatneo Canonical CBOR Profile

Version: 0.8-B+
Status: Normative for Level 1

## 1. Deterministic encoding

Yugatneo Level 1 uses the core deterministic CBOR requirements of RFC 8949:

- preferred serialization;
- definite-length arrays, maps and strings;
- deterministic map-key ordering;
- minimal integer and length encodings.

The implementation additionally forbids floating-point values and CBOR tags in the current Level 1 protocol profile.

## 2. Map ordering

Map keys are ordered by the bytewise lexicographic ordering of their deterministic CBOR encodings.

This is the ordering specified by RFC 8949 section 4.2.1.

## 3. Decoder policy

The decoder:

1. parses exactly one CBOR data item;
2. rejects trailing bytes;
3. rejects floats;
4. rejects tags;
5. canonicalizes the decoded value;
6. compares the canonical bytes with the supplied bytes;
7. rejects the input if the bytes differ.

This makes non-canonical input an explicit protocol error rather than an accepted alternative representation.

## 4. JSON boundary

JSON is an authoring and review representation.

JSON is not hashed directly.

A JSON trace is converted to the same deterministic CBOR representation before identifier hashing.

## 5. Identifier domains

The existing domain-separated SHA-256 identifier contract remains:

ID = SHA-256(domain || 0x00 || canonical_cbor(object_without_id))

Domains:

- YUGATNEO/EVENT/v1
- YUGATNEO/EVIDENCE/v1
- YUGATNEO/TRACE/v1
- YUGATNEO/WITNESS/v1

## 6. What this profile does not prove

Deterministic serialization proves reproducibility of representation. It does not prove semantic correctness, validity-rule completeness, T-star completeness, or protocol security.

## Reference

RFC 8949 section 4.2 defines deterministic CBOR requirements, including preferred serialization, prohibition of indefinite-length items, and bytewise lexicographic ordering of deterministically encoded map keys.
