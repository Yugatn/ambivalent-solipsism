# Yugatneo Level 1 Reference

This is the executable reference slice for Yugatneo I-1 Dissent Independence.

## Current engine

The CLI computes the result from trace content through these stages:

`Trace`
`ProvenanceGraph`
`Validity evaluation`
`counterfactual dependency`
`witness gate`
`I-1 evaluation`

The trace name F/G/H/I/L/M is metadata and is not used to select the result.

## Scope

Level 1 currently covers:

- attestation evidence;
- I-1a;
- I-1b;
- T★ closed-world evaluation;
- provenance and certificate closure;
- VALID, INVALID and UNKNOWN validity states;
- Level 2 witness-independence gate;
- deterministic regression fixtures;
- explicit DependencyCertificate computation.

It deliberately does not claim:

- distributed consensus;
- PoAS implementation;
- AAS correctness;
- economy or token implementation;
- production security;
- Mainnet readiness.

## Run

`cargo test`

`cargo run -- --input fixtures/trace_H.json`

## Implementation gates

1. ProvenanceGraph
2. ValidityRule_ATT
3. counterfactual dependency
4. DependencyCertificate
5. witness independence
6. I-1 evaluator
7. binary CBOR
8. mutation and property tests
9. security review

The current result is a stronger bootstrap reference, but it is not yet Level 1 Complete.
