use clap::Parser;
use std::{fs, path::PathBuf};
use yugatneo_checker::{classify, Trace};

#[derive(Parser)]
struct Cli {
    #[arg(short, long)]
    input: PathBuf,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    let trace: Trace = serde_json::from_str(&fs::read_to_string(cli.input)?)?;
    println!("{}", serde_json::to_string_pretty(&classify(&trace))?);
    Ok(())
}
