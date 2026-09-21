use crate::{
    dependency,
    errors::SchemaError,
    model::{DependencyStatus, Trace, TriState},
    provenance::ProvenanceGraph,
    schema::SchemaValidator,
    t_star::TStarChecker,
};
use serde::Serialize;
use serde_json::Value;

#[derive(Debug, Clone, Serialize, PartialEq)]
pub struct ResultEnvelope {
    pub contract: &'static str,
    pub trace: String,
    pub t_star: bool,
    pub t_star_checks: crate::t_star::TStarResult,
    pub schema_errors: Vec<SchemaError>,
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
    let schema_errors=SchemaValidator::validate(trace).err().unwrap_or_default();
    if !schema_errors.is_empty() {
        return unresolved(trace, false, crate::t_star::TStarResult {
            complete_provenance: TriState::Unresolved,
            closed_dependency_universe: TriState::Unresolved,
            monotone_sanction: TriState::Unresolved,
            finite_scope: TriState::Unresolved,
        }, schema_errors);
    }

    let provenance=ProvenanceGraph::build(trace);
    let tstar=TStarChecker::check(trace,&provenance);
    match tstar.overall() {
        TriState::False|TriState::Unresolved => return unresolved(trace,false,tstar,Vec::new()),
        TriState::True => {}
    }

    let i1a=if direct_dissent_sanction(trace){"Violation"}else{"NotViolated"};
    let mut dependency_status=DependencyStatus::Independent;
    let mut i1b="NotViolated";
    let mut validity_dependency="False";
    let mut witness_independence="NotApplicable";

    for evidence in trace.events_of("Attestation") {
        for dissent in trace.events_of("Dissent") {
            let certificate=dependency::analyze(evidence,&dissent.id,trace,&provenance);
            match (certificate.validity,certificate.witness_independence) {
                (TriState::True,TriState::True) => {
                    witness_independence="VerifiedIndependent";
                    if sanction_uses_as_basis(trace,&evidence.id) {
                        dependency_status=DependencyStatus::Dependent;
                        i1b="Violation";
                        validity_dependency="True";
                    }
                }
                (TriState::True,TriState::False) => {dependency_status=DependencyStatus::Unresolved;i1b="Unresolved";validity_dependency="Unresolved";witness_independence="NotIndependent";}
                (TriState::True,TriState::Unresolved)|(TriState::Unresolved,_) => {dependency_status=DependencyStatus::Unresolved;i1b="Unresolved";validity_dependency="Unresolved";witness_independence="Unresolved";}
                (TriState::False,_) => {}
            }
        }
    }
    let truth=match i1b{"Violation"=>"False","Unresolved"=>"Unresolved",_=>"True"};
    let dependency_status=match dependency_status{DependencyStatus::Independent=>"Independent",DependencyStatus::Dependent=>"Dependent",DependencyStatus::Unresolved=>"Unresolved"};
    ResultEnvelope{contract:"TRACES.md@0.8-B+",trace:trace.trace.clone(),t_star:true,t_star_checks:tstar,schema_errors,truth,applicability:"InScope",decidability:"Decidable",dependency_status,i1a,i1b,validity_dependency,witness_independence}
}

fn unresolved(trace:&Trace,_:bool,tstar:crate::t_star::TStarResult,schema_errors:Vec<SchemaError>)->ResultEnvelope{
    ResultEnvelope{contract:"TRACES.md@0.8-B+",trace:trace.trace.clone(),t_star:false,t_star_checks:tstar,schema_errors,truth:"Unresolved",applicability:"InScope",decidability:"Decidable",dependency_status:"Unresolved",i1a:"NotViolated",i1b:"Unresolved",validity_dependency:"Unresolved",witness_independence:"Unresolved"}
}
fn direct_dissent_sanction(trace:&Trace)->bool{
    trace.events_of("Sanction").any(|s|s.payload.as_object().and_then(|p|p.get("target_evidence")).and_then(Value::as_array).map(|a|a.iter().filter_map(Value::as_str).any(|id|trace.event(id).map(|e|e.kind=="Dissent").unwrap_or(false))).unwrap_or(false))
}
fn sanction_uses_as_basis(trace:&Trace,evidence_id:&str)->bool{
    trace.events_of("Sanction").any(|s|s.payload.as_object().and_then(|p|p.get("basis_evidence")).and_then(Value::as_array).map(|a|a.iter().filter_map(Value::as_str).any(|id|id==evidence_id)).unwrap_or(false))
}
