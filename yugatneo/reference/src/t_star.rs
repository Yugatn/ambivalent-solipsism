use std::collections::BTreeSet;
use crate::{model::{Trace, TriState}, provenance::{EdgeKind, ProvenanceGraph}};

#[derive(Debug, Clone, Copy, PartialEq, Eq, serde::Serialize)]
pub struct TStarResult {
    pub complete_provenance: TriState,
    pub closed_dependency_universe: TriState,
    pub monotone_sanction: TriState,
    pub finite_scope: TriState,
}
impl TStarResult {
    pub fn overall(&self)->TriState {
        let all=[self.complete_provenance,self.closed_dependency_universe,self.monotone_sanction,self.finite_scope];
        if all.iter().any(|x|*x==TriState::False){TriState::False}
        else if all.iter().any(|x|*x==TriState::Unresolved){TriState::Unresolved}
        else{TriState::True}
    }
}
pub struct TStarChecker;
impl TStarChecker {
    pub fn check(trace:&Trace, prov:&ProvenanceGraph)->TStarResult {
        TStarResult{complete_provenance:Self::complete_provenance(trace,prov),closed_dependency_universe:Self::closed_dependency_universe(trace,prov),monotone_sanction:Self::monotone_sanction(trace),finite_scope:Self::finite_scope(trace)}
    }
    fn complete_provenance(trace:&Trace, prov:&ProvenanceGraph)->TriState {
        let declared:BTreeSet<&str>=trace.metadata.external_ids.iter().map(String::as_str).collect();
        for edge in &prov.edges {
            if !trace.events.iter().any(|e|e.id==edge.from)&&!declared.contains(edge.from.as_str()){return TriState::False;}
        }
        for ev in trace.events_of("Attestation") {
            let Some(p)=ev.payload.as_object() else{return TriState::False;};
            if p.get("credential").map(|v|v.is_null()).unwrap_or(true) || p.get("key_id").map(|v|v.is_null()).unwrap_or(true) {return TriState::False;}
        }
        if let Some(map)=&trace.certificate_closure {
            for ev in trace.events_of("Attestation") {
                if !map.contains_key(&ev.id){return TriState::Unresolved;}
            }
        }
        TriState::True
    }
    fn closed_dependency_universe(trace:&Trace, prov:&ProvenanceGraph)->TriState {
        let declared:BTreeSet<&str>=trace.metadata.external_ids.iter().map(String::as_str).collect();
        for edge in &prov.edges {
            if !trace.events.iter().any(|e|e.id==edge.from)&&!declared.contains(edge.from.as_str()){return TriState::False;}
        }
        for ev in trace.events_of("Attestation") {
            if let Some(claim)=ev.payload.get("claim").and_then(|v|v.as_object()) {
                for r in claim.get("source_refs").and_then(|v|v.as_array()).into_iter().flatten().filter_map(|v|v.as_str()) {
                    let explicit=prov.edges.iter().any(|e|e.to==ev.id&&e.from==r&&matches!(e.kind,EdgeKind::Input|EdgeKind::Context|EdgeKind::Certificate));
                    if !explicit{return TriState::False;}
                }
            }
        }
        TriState::True
    }
    fn monotone_sanction(trace:&Trace)->TriState {
        for s in trace.events_of("Sanction") {
            let Some(p)=s.payload.as_object() else{return TriState::False;};
            let Some(rule)=p.get("rule_id").and_then(|v|v.as_str()) else{return TriState::False;};
            if rule.is_empty(){return TriState::False;}
            if let Some(basis)=p.get("basis_evidence").and_then(|v|v.as_array()) {
                for id in basis.iter().filter_map(|v|v.as_str()) {
                    let Some(ev)=trace.event(id) else{return TriState::False;};
                    if ev.logical_time.counter>s.logical_time.counter{return TriState::False;}
                }
            }
        }
        TriState::True
    }
    fn finite_scope(trace:&Trace)->TriState {
        if trace.horizon.start>trace.horizon.end{return TriState::False;}
        if trace.events.iter().any(|e|e.logical_time.counter<trace.horizon.start||e.logical_time.counter>trace.horizon.end){return TriState::False;}
        TriState::True
    }
}
