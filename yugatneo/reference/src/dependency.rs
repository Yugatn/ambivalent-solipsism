use serde::Serialize;

use crate::{
    model::{Event, Trace, TriState, Validity},
    provenance::ProvenanceGraph,
    validity,
};

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct DependencyCertificate {
    pub evidence_id: String,
    pub target_id: String,
    pub structural: TriState,
    pub validity: TriState,
    pub witness_independence: TriState,
    pub original_validity: ValidityStatus,
    pub modified_validity: ValidityStatus,
}

#[derive(Debug, Clone, Copy, Serialize, PartialEq, Eq)]
pub enum ValidityStatus {
    Valid,
    Invalid,
    Unknown,
}

impl From<Validity> for ValidityStatus {
    fn from(value: Validity) -> Self {
        match value {
            Validity::Valid => Self::Valid,
            Validity::Invalid => Self::Invalid,
            Validity::Unknown => Self::Unknown,
        }
    }
}

pub fn analyze(
    evidence: &Event,
    target: &str,
    trace: &Trace,
    provenance: &ProvenanceGraph,
) -> DependencyCertificate {
    let original = validity::evaluate(evidence, trace, provenance, None);
    let modified = validity::evaluate(evidence, trace, provenance, Some(target));

    let structural = if provenance.ancestors(&evidence.id).contains(target)
        || provenance.certificate_closure(trace, &evidence.id).contains(target)
    {
        TriState::True
    } else {
        TriState::False
    };

    let validity = match (original, modified) {
        (Validity::Valid, Validity::Invalid) => TriState::True,
        (Validity::Valid, Validity::Unknown) => TriState::Unresolved,
        (Validity::Valid, Validity::Valid) => TriState::False,
        _ => TriState::Unresolved,
    };

    let witness_independence = match evidence
        .payload
        .as_object()
        .and_then(|payload| payload.get("dependency_witness"))
        .and_then(|value| value.as_object())
        .and_then(|witness| witness.get("dependencies"))
        .and_then(|value| value.as_array())
    {
        Some(dependencies) => {
            if dependencies
                .iter()
                .filter_map(|value| value.as_str())
                .any(|id| id == target)
            {
                TriState::False
            } else {
                TriState::True
            }
        }
        None => TriState::Unresolved,
    };

    DependencyCertificate {
        evidence_id: evidence.id.clone(),
        target_id: target.to_string(),
        structural,
        validity,
        witness_independence,
        original_validity: original.into(),
        modified_validity: modified.into(),
    }
}
