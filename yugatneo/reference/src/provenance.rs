use std::collections::BTreeSet;

use crate::model::{Event, Trace};
use serde_json::Value;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EdgeKind {
    Input,
    Context,
    Certificate,
}

#[derive(Debug, Clone)]
pub struct Edge {
    pub from: String,
    pub to: String,
    pub kind: EdgeKind,
}

#[derive(Debug, Clone)]
pub struct ProvenanceGraph {
    pub nodes: BTreeSet<String>,
    pub edges: Vec<Edge>,
}

impl ProvenanceGraph {
    pub fn build(trace: &Trace) -> Self {
        let mut nodes = BTreeSet::new();
        let mut edges = Vec::new();

        for event in &trace.events {
            nodes.insert(event.id.clone());

            if let Some(payload) = event.payload.as_object() {
                for key in ["inputs", "basis_evidence", "target_evidence"] {
                    if let Some(values) = payload.get(key).and_then(Value::as_array) {
                        for value in values.iter().filter_map(Value::as_str) {
                            nodes.insert(value.to_string());
                            edges.push(Edge { from: value.to_string(), to: event.id.clone(), kind: EdgeKind::Input });
                        }
                    }
                }

                if let Some(values) = payload.get("context_refs").and_then(Value::as_array) {
                    for value in values.iter().filter_map(Value::as_str) {
                        nodes.insert(value.to_string());
                        edges.push(Edge { from: value.to_string(), to: event.id.clone(), kind: EdgeKind::Context });
                    }
                }

                if event.kind == "CertificateContext" {
                    if let Some(values) = payload.get("inputs").and_then(Value::as_array) {
                        for value in values.iter().filter_map(Value::as_str) {
                            nodes.insert(value.to_string());
                            edges.push(Edge { from: value.to_string(), to: event.id.clone(), kind: EdgeKind::Certificate });
                        }
                    }
                }
            }
        }

        Self { nodes, edges }
    }

    pub fn parents(&self, id: &str, kinds: &[EdgeKind]) -> BTreeSet<String> {
        self.edges.iter()
            .filter(|edge| edge.to == id && kinds.contains(&edge.kind))
            .map(|edge| edge.from.clone())
            .collect()
    }

    pub fn closure(&self, id: &str, kinds: &[EdgeKind]) -> BTreeSet<String> {
        let mut seen = BTreeSet::new();
        let mut stack: Vec<String> = self.parents(id, kinds).into_iter().collect();

        while let Some(current) = stack.pop() {
            if seen.insert(current.clone()) {
                for parent in self.parents(&current, kinds) {
                    stack.push(parent);
                }
            }
        }
        seen
    }

    pub fn ancestors(&self, id: &str) -> BTreeSet<String> {
        self.closure(id, &[EdgeKind::Input, EdgeKind::Context, EdgeKind::Certificate])
    }

    pub fn certificate_closure(&self, trace: &Trace, evidence_id: &str) -> BTreeSet<String> {
        let mut result = self.closure(evidence_id, &[EdgeKind::Certificate]);

        if let Some(map) = &trace.certificate_closure {
            if let Some(values) = map.get(evidence_id).and_then(Value::as_array) {
                for value in values.iter().filter_map(Value::as_str) {
                    result.insert(value.to_string());
                }
            }
        }
        result
    }
}
