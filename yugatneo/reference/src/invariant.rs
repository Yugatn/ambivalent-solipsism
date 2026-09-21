use crate::{
    dependency,
    model::{DependencyStatus, Trace, TriState},
    provenance::ProvenanceGraph,
};
use serde::Serialize;
use serde_json::Value;

#[derive(Debug, Clone, Serialize, PartialEq)]
pub struct ResultEnvelope {
    pub contract: &'static str,
    pub trace: String,
    pub t_star: bool,
    pub truth: &'static str,
    pub applicability: &'static str,
    pub decidability: &'static str,
    pub dependency_status: &'static str,
    pub i1a: &'static str,
    pub i1b: &'static str,
    pub validity_dependency: &'static str,
    pub witness_independence: &'static str,
}

pub fn evaluate(trace: &Trace) -> ResultEnvelope {
    if !trace.in_t_star() {
        return ResultEnvelope {
            contract: "TRACES.md@0.8-B+",
            trace: trace.trace.clone(),
            t_star: false,
            truth: "Unresolved",
            applicability: "InScope",
            decidability: "Decidable",
            dependency_status: "Unresolved",
            i1a: "NotViolated",
            i1b: "Unresolved",
            validity_dependency: "Unresolved",
            witness_independence: "Unresolved",
        };
    }

    let provenance = ProvenanceGraph::build(trace);
    let i1a = if direct_dissent_sanction(trace) { "Violation" } else { "NotViolated" };

    let mut dependency_status = DependencyStatus::Independent;
    let mut i1b = "NotViolated";
    let mut validity_dependency = "False";
    let mut witness_independence = "NotApplicable";

    for evidence in trace.events_of("Attestation") {
        for dissent in trace.events_of("Dissent") {
            let certificate = dependency::analyze(evidence, &dissent.id, trace, &provenance);

            match (certificate.validity, certificate.witness_independence) {
                (TriState::True, TriState::True) => {
                    witness_independence = "VerifiedIndependent";
                    if sanction_uses_as_basis(trace, &evidence.id) {
                        dependency_status = DependencyStatus::Dependent;
                        i1b = "Violation";
                        validity_dependency = "True";
                    }
                }
                (TriState::True, TriState::False) => {
                    dependency_status = DependencyStatus::Unresolved;
                    i1b = "Unresolved";
                    validity_dependency = "Unresolved";
                    witness_independence = "NotIndependent";
                }
                (TriState::True, TriState::Unresolved) => {
                    dependency_status = DependencyStatus::Unresolved;
                    i1b = "Unresolved";
                    validity_dependency = "Unresolved";
                    witness_independence = "Unresolved";
                }
                (TriState::Unresolved, _) => {
                    dependency_status = DependencyStatus::Unresolved;
                    i1b = "Unresolved";
                    validity_dependency = "Unresolved";
                    witness_independence = "Unresolved";
                }
                (TriState::False, _) => {}
            }
        }
    }

    let truth = match i1b {
        "Violation" => "False",
        "Unresolved" => "Unresolved",
        _ => "True",
    };

    let dependency_status = match dependency_status {
        DependencyStatus::Independent => "Independent",
        DependencyStatus::Dependent => "Dependent",
        DependencyStatus::Unresolved => "Unresolved",
    };

    ResultEnvelope {
        contract: "TRACES.md@0.8-B+",
        trace: trace.trace.clone(),
        t_star: true,
        truth,
        applicability: "InScope",
        decidability: "Decidable",
        dependency_status,
        i1a,
        i1b,
        validity_dependency,
        witness_independence,
    }
}

fn direct_dissent_sanction(trace: &Trace) -> bool {
    trace.events_of("Sanction").any(|sanction| {
        sanction.payload.as_object()
            .and_then(|payload| payload.get("target_evidence"))
            .and_then(Value::as_array)
            .map(|targets| targets.iter().filter_map(Value::as_str).any(|id| {
                trace.event(id).map(|event| event.kind == "Dissent").unwrap_or(false)
            }))
            .unwrap_or(false)
    })
}

fn sanction_uses_as_basis(trace: &Trace, evidence_id: &str) -> bool {
    trace.events_of("Sanction").any(|sanction| {
        sanction.payload.as_object()
            .and_then(|payload| payload.get("basis_evidence"))
            .and_then(Value::as_array)
            .map(|basis| basis.iter().filter_map(Value::as_str).any(|id| id == evidence_id))
            .unwrap_or(false)
    })
}
