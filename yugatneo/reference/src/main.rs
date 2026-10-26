use clap::Parser;
use std::{fs, path::PathBuf};
use yugatneo_checker::{canonical, evaluate, SchemaValidator, Trace};

#[derive(Parser)]
struct Cli {
    #[arg(short, long)]
    input: PathBuf,
    #[arg(short, long)]
    output: Option<PathBuf>,
    #[arg(long)]
    strict: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli=Cli::parse();
    let bytes=fs::read(&cli.input)?;
    let trace: Trace=if cli.input.extension().and_then(|x|x.to_str())==Some("cbor") {
        canonical::decode_trace(&bytes)?
    } else {
        serde_json::from_slice(&bytes)?
    };

    let schema=SchemaValidator::validate(&trace);
    if cli.strict && schema.is_err() {
        let errors=schema.err().unwrap();
        eprintln!("{}",serde_json::to_string_pretty(&errors)?);
        std::process::exit(2);
    }

    let result=evaluate(&trace);
    let rendered=serde_json::to_vec_pretty(&result)?;

    if let Some(path)=cli.output {
        if path.extension().and_then(|x|x.to_str())==Some("cbor") {
            fs::write(path,canonical::encode_trace(&trace)?)?;
        } else {
            fs::write(path,rendered)?;
        }
    } else {
        println!("{}",String::from_utf8(rendered)?);
    }
    Ok(())
}
