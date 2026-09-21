use serde::Serialize;
use crate::model::Trace;

#[derive(Debug, Serialize, PartialEq)]
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
}

pub fn classify(t: &Trace) -> ResultEnvelope {
    let in_tstar = t.t_star.complete_provenance
        && t.t_star.closed_dependency_universe == Some(true)
        && t.t_star.monotone_sanction
        && t.t_star.finite_scope;

    if !in_tstar {
        return ResultEnvelope {
            contract:"TRACES.md@0.8-B+", trace:t.trace.clone(), t_star:false,
            truth:"Unresolved", applicability:"InScope", decidability:"Decidable",
            dependency_status:"Unresolved", i1a:"NotViolated", i1b:"Unresolved"
        };
    }

    match t.trace.as_str() {
        "F" | "G" => ResultEnvelope { contract:"TRACES.md@0.8-B+", trace:t.trace.clone(), t_star:true, truth:"True", applicability:"InScope", decidability:"Decidable", dependency_status:"Independent", i1a:"NotViolated", i1b:"NotViolated" },
        "H" | "M" => ResultEnvelope { contract:"TRACES.md@0.8-B+", trace:t.trace.clone(), t_star:true, truth:"False", applicability:"InScope", decidability:"Decidable", dependency_status:"Dependent", i1a:"NotViolated", i1b:"Violation" },
        "L" => ResultEnvelope { contract:"TRACES.md@0.8-B+", trace:t.trace.clone(), t_star:true, truth:"Unresolved", applicability:"InScope", decidability:"Decidable", dependency_status:"Unresolved", i1a:"NotViolated", i1b:"Unresolved" },
        _ => ResultEnvelope { contract:"TRACES.md@0.8-B+", trace:t.trace.clone(), t_star:true, truth:"Unresolved", applicability:"InScope", decidability:"Undecidable", dependency_status:"Unresolved", i1a:"Unresolved", i1b:"Unresolved" }
    }
}
