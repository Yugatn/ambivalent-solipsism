use crate::{
    model::{Event, Trace, TriState, Validity},
    provenance::ProvenanceGraph,
};
use serde_json::Value;

pub fn evaluate(
    evidence: &Event,
    trace: &Trace,
    provenance: &ProvenanceGraph,
    removed: Option<&str>,
) -> Validity {
    let Some(payload) = evidence.payload.as_object() else {
        return Validity::Invalid;
    };

    let credential_ok = payload.get("credential").map(|v| !v.is_null()).unwrap_or(false);
    let key_ok = payload.get("key_id").map(|v| !v.is_null()).unwrap_or(false);

    if !credential_ok || !key_ok {
        return Validity::Invalid;
    }

    if let Some(removed_id) = removed {
        if let Some(claim) = payload.get("claim").and_then(Value::as_object) {
            let mandatory = string_array(claim.get("mandatory_validity_refs"));
            if mandatory.iter().any(|id| id == removed_id) {
                return Validity::Invalid;
            }

            let uncertain = string_array(claim.get("uncertain_refs"));
            if uncertain.iter().any(|id| id == removed_id) {
                return Validity::Unknown;
            }
        }

        if provenance.certificate_closure(trace, &evidence.id).contains(removed_id) {
            return Validity::Invalid;
        }
    }

    Validity::Valid
}

pub fn dependency_for(
    evidence: &Event,
    target: &str,
    trace: &Trace,
    provenance: &ProvenanceGraph,
) -> TriState {
    if evaluate(evidence, trace, provenance, None) != Validity::Valid {
        return TriState::Unresolved;
    }

    match evaluate(evidence, trace, provenance, Some(target)) {
        Validity::Invalid => TriState::True,
        Validity::Unknown => TriState::Unresolved,
        Validity::Valid => TriState::False,
    }
}

fn string_array(value: Option<&Value>) -> Vec<String> {
    value.and_then(Value::as_array)
        .map(|values| values.iter().filter_map(Value::as_str).map(ToOwned::to_owned).collect())
        .unwrap_or_default()
}
