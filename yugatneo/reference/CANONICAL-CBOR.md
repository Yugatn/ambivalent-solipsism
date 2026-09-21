# Yugatneo Canonical Serialization Profile

This document removes the ambiguity between generic CBOR and the Yugatneo identifier contract.

## 1. Encoding

The Level 1 implementation uses deterministic CBOR compatible with RFC 8949 deterministic encoding.

Rules:

- no floating point values;
- no indefinite-length strings, arrays or maps;
- unsigned integers use the shortest permitted representation;
- negative integers use the shortest permitted representation;
- text strings are UTF-8;
- map keys are text strings only;
- map keys are ordered by deterministic CBOR key encoding;
- arrays preserve semantic order unless the schema explicitly declares canonical sorting.

## 2. Event ordering

Events are canonically ordered by:

1. LogicalTime.counter;
2. LogicalTime.subject_id;
3. physical_time;
4. EventID.

Physical time is never used as primary semantic time.

## 3. Identifier domains

Identifiers are domain separated:

- EventID: `YUGATNEO/EVENT/v1`
- EvidenceID: `YUGATNEO/EVIDENCE/v1`
- TraceID: `YUGATNEO/TRACE/v1`
- WitnessID: `YUGATNEO/WITNESS/v1`

The identifier field itself is omitted from the hashed object.

Conceptually:

`ID = SHA-256(domain || canonical_cbor(object_without_id))`

## 4. JSON

JSON is a review and fixture-authoring representation. It is not hashed.

JSON key order is not semantically significant.

A conforming implementation MUST produce identical canonical bytes when the same semantic object is parsed repeatedly.

## 5. Determinism test

A valid Level 1 implementation MUST satisfy:

`canonicalize(parse(canonicalize(x))) == canonicalize(x)`

byte-for-byte.

## 6. Boundary

Canonical serialization does not prove protocol correctness. It only makes the represented state reproducible.
