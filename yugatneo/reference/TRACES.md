# Yugatneo Level 1 Regression Contract

Version: 0.8-B+
Status: Normative
Scope: I-1 Dissent Independence, Level 1 closed-world
Evidence type: attestation

## 1. Contract

The normative regression classes are F, G, H, I, L and M.

The checker MUST compute results from trace content. The trace label is metadata only and MUST NOT select the result.

Required independent dimensions:

- Truth: True, False, Unresolved
- Applicability: InScope, OutOfScope
- Decidability: Decidable, Undecidable
- DependencyStatus: Independent, Dependent, Unresolved
- I-1a: NotViolated, Violation, Unresolved
- I-1b: NotViolated, Violation, Unresolved
- ValidityDependency: True, False, Unresolved
- WitnessIndependence: VerifiedIndependent, NotIndependent, Unresolved, NotApplicable

UNKNOWN MUST NEVER be coerced to INVALID.

## 2. T★ closed-world boundary

Level 1 uses an explicit closed-world operational boundary. T★ does not prove metaphysical absence of hidden dependencies.

T★ requires:

- Complete Provenance
- Closed Dependency Universe
- Monotone Sanction
- Finite Scope

Outside T★, I-1b MUST be Unresolved.

## 3. Validity dependency

ValidityDep is TRUE only when:

1. original evidence validity is VALID;
2. removal of the dissent makes a mandatory validity precondition INVALID;
3. the witness is independently valid at Level 2;
4. the trace is inside T★.

If removal produces UNKNOWN, ValidityDep is UNRESOLVED.

Structural, generative or semantic dependency alone does not imply ValidityDep.

## 4. Explicit dependency declarations

The closed-world attestation claim schema supports:

- `mandatory_validity_refs`: removing the referenced node makes a mandatory validity precondition INVALID;
- `uncertain_refs`: removing the referenced node makes validity UNKNOWN;
- `source_refs`: semantic or provenance references that do not by themselves imply validity dependency.

This distinction is normative. A source reference is not automatically a validity dependency.

## 5. Witness Independence Level 2

A dependency witness is represented by:

`dependency_witness: { dependencies: [...] }`

For Level 2, the target dissent MUST NOT occur in the witness dependency closure.

Missing witness data does not count as independence. It yields WitnessIndependence = Unresolved.

## 6. I-1a and I-1b

I-1a concerns direct sanction for dissent itself.

I-1b concerns sanction whose mandatory evidentiary basis has a validity dependency on dissent.

`Sanction.target_evidence` and `Sanction.basis_evidence` are distinct. `basis_evidence` is normative for I-1b.

## 7. Certificate closure

Certificate closure is part of the mandatory dependency universe.

For an evidence item, the checker MUST consider both:

1. ordinary mandatory provenance;
2. declared ValidityCertificate closure.

Trace M is specifically designed to fail a checker that ignores certificate closure.

## 8. Canonical time and identifiers

LogicalTime is a typed pair:

`{ counter: u64, subject_id: SubjectID }`

Canonical event ordering is:

`(logical_time, physical_time, event_id)`

Identifiers use domain-separated SHA-256 over canonical deterministic CBOR with the identifier field omitted.

The serialization profile is specified in `CANONICAL-CBOR.md`.

## 9. Regression matrix

| Trace | T★ | Truth | Dependency | I-1a | I-1b | ValidityDep | Witness |
|---|---|---|---|---|---|---|---|
| F | true | True | Independent | NotViolated | NotViolated | False | NotApplicable |
| G | true | True | Independent | NotViolated | NotViolated | False | NotApplicable |
| H | true | False | Dependent | NotViolated | Violation | True | VerifiedIndependent |
| I | false | Unresolved | Unresolved | NotViolated | Unresolved | Unresolved | Unresolved |
| L | true | Unresolved | Unresolved | NotViolated | Unresolved | Unresolved | Unresolved |
| M | true | False | Dependent | NotViolated | Violation | True | VerifiedIndependent |

## 10. What this does not prove

This contract does not prove I-1 outside T★, correctness for other evidence types, completeness of SemanticDep, absence of unmodelled dependencies, production security, distributed consensus safety, PoAS correctness, AAS correctness, or Level 3 witness independence.
