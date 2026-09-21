use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Trace {
    pub version: String,
    pub trace: String,
    pub horizon: Horizon,
    pub events: Vec<Event>,
    pub t_star: TStar,
    #[serde(default)]
    pub counterfactual: Option<Counterfactual>,
    #[serde(default)]
    pub certificate_closure: Option<serde_json::Map<String, Value>>,
    #[serde(default)]
    pub metadata: Metadata,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct Metadata {
    #[serde(default)]
    pub external_ids: Vec<String>,
    #[serde(default)]
    pub declared_scopes: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Horizon {
    pub start: u64,
    pub end: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Event {
    #[serde(rename = "type")]
    pub kind: String,
    pub id: String,
    pub subject: String,
    pub logical_time: LogicalTime,
    #[serde(default)]
    pub physical_time: Option<u64>,
    #[serde(default)]
    pub payload: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LogicalTime {
    pub counter: u64,
    pub subject_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TStar {
    #[serde(default)]
    pub complete_provenance: bool,
    #[serde(default)]
    pub closed_dependency_universe: Option<bool>,
    #[serde(default)]
    pub monotone_sanction: bool,
    #[serde(default)]
    pub finite_scope: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Counterfactual {
    pub removed: String,
    pub modified_validity: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum TriState {
    True,
    False,
    Unresolved,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum Validity {
    Valid,
    Invalid,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DependencyStatus {
    Independent,
    Dependent,
    Unresolved,
}

impl Trace {
    pub fn event(&self, id: &str) -> Option<&Event> {
        self.events.iter().find(|event| event.id == id)
    }

    pub fn events_of<'a>(&'a self, kind: &'a str) -> impl Iterator<Item = &'a Event> + 'a {
        self.events.iter().filter(move |event| event.kind == kind)
    }
}
