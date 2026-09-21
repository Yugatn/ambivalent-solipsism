use std::fs;
use yugatneo_checker::classify;
use yugatneo_checker::Trace;

#[test]
fn normative_regression_matrix() {
    let expected=[
        ("F","NotViolated"),("G","NotViolated"),("H","Violation"),
        ("I","Unresolved"),("L","Unresolved"),("M","Violation")
    ];
    for (name,want) in expected {
        let path=format!("fixtures/trace_{name}.json");
        let t:Trace=serde_json::from_str(&fs::read_to_string(path).unwrap()).unwrap();
        assert_eq!(classify(&t).i1b,want,"trace {name}");
    }
}
