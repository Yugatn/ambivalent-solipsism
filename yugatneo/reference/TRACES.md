# Yugatneo Level 1 Regression Contract

Version: 0.8-B+
Status: Normative
Scope: I-1 Dissent Independence, Level 1 closed-world
Evidence type: attestation

## Contract

The normative regression classes are F, G, H, I, L and M.

The checker MUST return these independent dimensions:

- Truth: True, False, Unresolved
- Applicability: InScope, OutOfScope
- Decidability: Decidable, Undecidable
- DependencyStatus: Independent, Dependent, Unresolved
- I-1a: NotViolated, Violation, Unresolved
- I-1b: NotViolated, Violation, Unresolved

UNKNOWN MUST NEVER be coerced to INVALID.

## Validity dependency

ValidityDep is TRUE only when:

1. original evidence validity is VALID;
2. removal of the dissent makes a mandatory validity precondition INVALID;
3. the dependency witness is independently valid at Level 2;
4. the trace is inside T★.

If removal produces UNKNOWN, ValidityDep is UNRESOLVED.

Structural, generative or semantic dependency alone does not imply ValidityDep.

## T★

Level 1 uses a closed-world operational boundary. T★ does not prove metaphysical absence of hidden dependencies.

T★ requires:

- Complete Provenance
- Closed Dependency Universe
- Monotone Sanction
- Finite Scope

Outside T★, I-1b MUST be Unresolved.

## I-1a and I-1b

I-1a concerns direct sanction for dissent itself.

I-1b concerns sanction whose mandatory evidentiary basis has a validity dependency on dissent.

Sanction.target_evidence and Sanction.basis_evidence are distinct. The latter is normative for I-1b.

## Canonical time and identifiers

LogicalTime is a typed pair:

`{ counter: u64, subject_id: SubjectID }`

Canonical event ordering is:

`(logical_time, physical_time, event_id)`

Identifiers use domain-separated SHA-256 over canonical CBOR with the identifier field omitted.

The canonical CBOR profile is specified in `CANONICAL-CBOR.md`.

## Regression matrix

| Trace | T★ | Truth | Dependency | I-1a | I-1b |
|---|---|---|---|---|---|
| F | true | True | Independent | NotViolated | NotViolated |
| G | true | True | Independent | NotViolated | NotViolated |
| H | true | False | Dependent | NotViolated | Violation |
| I | false | Unresolved | Unresolved | NotViolated | Unresolved |
| L | true | Unresolved | Unresolved | NotViolated | Unresolved |
| M | true | False | Dependent | NotViolated | Violation |

## What this does not prove

This contract does not prove I-1 outside T★, correctness for other evidence types, absence of unmodelled dependencies, production security, distributed consensus safety, PoAS correctness, AAS correctness, or Level 3 witness independence.
