# Yugatneo Level 1 Reference

This is the first executable vertical slice of Yugatneo.

## Scope

The package establishes a closed-world Level 1 boundary around I-1 and attestation evidence.

It deliberately does not claim:

- distributed consensus;
- PoAS implementation;
- AAS correctness;
- economy or token implementation;
- production security;
- Mainnet readiness.

## Implementation order

1. stabilize TRACES.md;
2. canonical CBOR;
3. typed Trace/Event model;
4. ProvenanceGraph;
5. ValidityRule_ATT;
6. DependencyCertificate;
7. Witness Independence Level 2;
8. T★ evaluator;
9. I-1a and I-1b evaluator;
10. regression, property and fuzz tests;
11. CI.

The current CLI is a bootstrap executable contract checker. It must not be mistaken for the completed Level 1 implementation until the typed provenance and validity layers are implemented.
