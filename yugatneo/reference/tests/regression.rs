use std::fs;

use serde_json::json;
use yugatneo_checker::{evaluate, Trace};

#[test]
fn normative_regression_matrix() {
    let expected = [
        ("F", "NotViolated"),
        ("G", "NotViolated"),
        ("H", "Violation"),
        ("I", "Unresolved"),
        ("L", "Unresolved"),
        ("M", "Violation"),
    ];

    for (name, wanted) in expected {
        let path = format!("fixtures/trace_{name}.json");
        let trace: Trace =
            serde_json::from_str(&fs::read_to_string(path).expect("fixture must exist")).unwrap();
        assert_eq!(evaluate(&trace).i1b, wanted, "trace {name}");
    }
}

#[test]
fn trace_m_requires_certificate_closure() {
    let mut trace: Trace =
        serde_json::from_str(&fs::read_to_string("fixtures/trace_M.json").unwrap()).unwrap();

    assert_eq!(evaluate(&trace).i1b, "Violation");

    trace.certificate_closure = None;
    assert_eq!(evaluate(&trace).i1b, "NotViolated");
}

#[test]
fn unknown_is_not_invalid() {
    let trace: Trace =
        serde_json::from_str(&fs::read_to_string("fixtures/trace_L.json").unwrap()).unwrap();
    let result = evaluate(&trace);
    assert_eq!(result.i1b, "Unresolved");
    assert_eq!(result.validity_dependency, "Unresolved");
}

#[test]
fn outside_t_star_is_unresolved() {
    let trace: Trace =
        serde_json::from_str(&fs::read_to_string("fixtures/trace_I.json").unwrap()).unwrap();
    let result = evaluate(&trace);
    assert_eq!(result.i1b, "Unresolved");
    assert_eq!(result.dependency_status, "Unresolved");
}

#[test]
fn witness_that_depends_on_dissent_cannot_confirm_dependency() {
    let mut trace: Trace =
        serde_json::from_str(&fs::read_to_string("fixtures/trace_H.json").unwrap()).unwrap();

    let attestation = trace
        .events
        .iter_mut()
        .find(|event| event.id == "attestation-H")
        .expect("H attestation");

    attestation.payload["dependency_witness"] = json!({
        "dependencies": ["dissent-H"]
    });

    let result = evaluate(&trace);
    assert_eq!(result.i1b, "Unresolved");
    assert_eq!(result.witness_independence, "NotIndependent");
}
