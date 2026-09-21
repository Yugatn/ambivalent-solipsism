use clap::Parser;
use serde::{Deserialize, Serialize};
use std::{fs, path::PathBuf};

#[derive(Parser)]
struct Cli {
    #[arg(short, long)]
    input: PathBuf,
}

#[derive(Debug, Deserialize)]
struct Trace {
    trace: String,
    t_star: TStar,
}

#[derive(Debug, Deserialize)]
struct TStar {
    complete_provenance: bool,
    closed_dependency_universe: Option<bool>,
    monotone_sanction: bool,
    finite_scope: bool,
}

#[derive(Debug, Serialize, PartialEq)]
struct ResultEnvelope {
    contract: &'static str,
    trace: String,
    t_star: bool,
    truth: &'static str,
    applicability: &'static str,
    decidability: &'static str,
    dependency_status: &'static str,
    i1a: &'static str,
    i1b: &'static str,
}

fn classify(t: &Trace) -> ResultEnvelope {
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

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    let trace: Trace = serde_json::from_str(&fs::read_to_string(cli.input)?)?;
    println!("{}", serde_json::to_string_pretty(&classify(&trace))?);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn f_is_independent() {
        let t = Trace { trace:"F".into(), t_star:TStar{complete_provenance:true,closed_dependency_universe:Some(true),monotone_sanction:true,finite_scope:true} };
        assert_eq!(classify(&t).i1b, "NotViolated");
    }
}
