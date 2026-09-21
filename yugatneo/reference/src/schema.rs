use std::collections::BTreeSet;
use crate::{errors::{SchemaError, SchemaErrorCode}, model::Trace, provenance::{EdgeKind, ProvenanceGraph}};

pub struct SchemaValidator;

impl SchemaValidator {
    pub fn validate(trace: &Trace) -> Result<(), Vec<SchemaError>> {
        let mut errors=Vec::new();
        if trace.version != "0.8-B+" && trace.version != "0.8-B" {
            errors.push(SchemaError::new(SchemaErrorCode::TraceVersionUnsupported, "unsupported trace version", "version"));
        }
        if trace.events.is_empty() {
            errors.push(SchemaError::new(SchemaErrorCode::TraceEmpty, "trace has no events", "events"));
        }
        if trace.horizon.start > trace.horizon.end {
            errors.push(SchemaError::new(SchemaErrorCode::HorizonInvalid, "horizon start exceeds end", "horizon"));
        }

        let mut ids=BTreeSet::new();
        for (i,e) in trace.events.iter().enumerate() {
            if e.id.is_empty() || !ids.insert(e.id.clone()) {
                errors.push(SchemaError::new(SchemaErrorCode::EventIdInvalid, "event id is empty or duplicated", format!("events[{i}].id")));
            }
            if e.kind.is_empty() {
                errors.push(SchemaError::new(SchemaErrorCode::EventTypeUnknown, "event type is empty", format!("events[{i}].type")));
            }
            if e.logical_time.subject_id.is_empty() {
                errors.push(SchemaError::new(SchemaErrorCode::LogicalTimeInvalid, "logical time subject is empty", format!("events[{i}].logical_time")));
            }
            if e.logical_time.counter < trace.horizon.start || e.logical_time.counter > trace.horizon.end {
                errors.push(SchemaError::new(SchemaErrorCode::LogicalTimeInvalid, "logical time outside horizon", format!("events[{i}].logical_time")));
            }
        }

        for pair in trace.events.windows(2) {
            let a=(&pair[0].logical_time.counter, &pair[0].logical_time.subject_id, &pair[0].physical_time, &pair[0].id);
            let b=(&pair[1].logical_time.counter, &pair[1].logical_time.subject_id, &pair[1].physical_time, &pair[1].id);
            if a >= b {
                errors.push(SchemaError::new(SchemaErrorCode::EventOrderInvalid, "events are not in canonical order", "events"));
                break;
            }
        }

        let declared: BTreeSet<&str>=trace.metadata.external_ids.iter().map(String::as_str).collect();
        for event in &trace.events {
            for reference in references(event) {
                if trace.event(&reference).is_none() && !declared.contains(reference.as_str()) {
                    errors.push(SchemaError::new(SchemaErrorCode::ExternalReferenceUndeclared, format!("reference {reference} is not an event or declared external id"), format!("event[{}]", event.id)));
                }
            }
        }

        let prov=ProvenanceGraph::build(trace);
        if has_cycle(&prov) {
            errors.push(SchemaError::new(SchemaErrorCode::ProvenanceCycle, "provenance graph contains a cycle", "provenance"));
        }

        if let Some(map)=&trace.certificate_closure {
            for (e, deps) in map {
                if trace.event(e).is_none() {
                    errors.push(SchemaError::new(SchemaErrorCode::CertificateClosureMissing, "certificate closure names unknown evidence", e));
                }
                if let Some(values)=deps.as_array() {
                    for value in values.iter().filter_map(|v| v.as_str()) {
                        if trace.event(value).is_none() && !declared.contains(value) {
                            errors.push(SchemaError::new(SchemaErrorCode::ExternalReferenceUndeclared, format!("certificate dependency {value} is not declared"), e));
                        }
                    }
                }
            }
        }

        if errors.is_empty() { Ok(()) } else { Err(errors) }
    }
}

fn references(event: &crate::model::Event) -> Vec<String> {
    let mut out=Vec::new();
    if let Some(p)=event.payload.as_object() {
        for key in ["inputs","context_refs","target_evidence","basis_evidence"] {
            if let Some(a)=p.get(key).and_then(|v| v.as_array()) {
                out.extend(a.iter().filter_map(|v| v.as_str()).map(ToOwned::to_owned));
            }
        }
        if let Some(c)=p.get("claim").and_then(|v| v.as_object()) {
            for key in ["source_refs","mandatory_validity_refs","uncertain_refs"] {
                if let Some(a)=c.get(key).and_then(|v| v.as_array()) {
                    out.extend(a.iter().filter_map(|v| v.as_str()).map(ToOwned::to_owned));
                }
            }
        }
    }
    out
}

fn has_cycle(prov: &ProvenanceGraph) -> bool {
    fn visit(node:&str, prov:&ProvenanceGraph, visiting:&mut BTreeSet<String>, visited:&mut BTreeSet<String>) -> bool {
        if visiting.contains(node) { return true; }
        if !visited.insert(node.to_string()) { return false; }
        visiting.insert(node.to_string());
        for edge in prov.edges.iter().filter(|e| e.to == node && matches!(e.kind, EdgeKind::Input|EdgeKind::Certificate|EdgeKind::Context)) {
            if visit(&edge.from, prov, visiting, visited) { return true; }
        }
        visiting.remove(node);
        false
    }
    let mut visiting=BTreeSet::new(); let mut visited=BTreeSet::new();
    prov.nodes.iter().any(|n| visit(n, prov, &mut visiting, &mut visited))
}
