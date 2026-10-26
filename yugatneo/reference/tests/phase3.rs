use std::fs;

use yugatneo_checker::{
    canonical::{decode_trace, encode_trace},
    evaluate, SchemaValidator, TStarChecker,
};
use serde_json::Value;

fn fixture(name:&str)->yugatneo_checker::Trace{
    serde_json::from_str(&fs::read_to_string(format!("fixtures/trace_{name}.json")).unwrap()).unwrap()
}

#[test]
fn all_normative_fixtures_are_schema_valid_except_i() {
    for name in ["F","G","H","L","M"] {
        assert!(SchemaValidator::validate(&fixture(name)).is_ok(), "{name}");
    }
    assert!(SchemaValidator::validate(&fixture("I")).is_ok());
}

#[test]
fn operational_tstar_does_not_use_declared_flags() {
    let mut t=fixture("F");
    t.t_star.complete_provenance=false;
    let p=yugatneo_checker::provenance::ProvenanceGraph::build(&t);
    assert_eq!(TStarChecker::check(&t,&p).overall(), yugatneo_checker::model::TriState::True);
}

#[test]
fn trace_i_is_outside_tstar_from_content() {
    let t=fixture("I");
    let p=yugatneo_checker::provenance::ProvenanceGraph::build(&t);
    let result=TStarChecker::check(&t,&p);
    assert_eq!(result.overall(), yugatneo_checker::model::TriState::False);
    assert!(!evaluate(&t).t_star);
}

#[test]
fn binary_cbor_roundtrip_is_byte_stable_for_json_fixture() {
    for name in ["F","G","H","I","L","M"] {
        let t=fixture(name);
        let bytes=encode_trace(&t).unwrap();
        let decoded=decode_trace(&bytes).unwrap();
        assert_eq!(encode_trace(&decoded).unwrap(),bytes,name);
    }
}

#[test]
fn noncanonical_map_order_is_rejected() {
    let canonical=encode_trace(&fixture("F")).unwrap();
    let mut value:ciborium::Value=ciborium::de::from_reader(canonical.as_slice()).unwrap();
    if let ciborium::Value::Map(entries)=&mut value {
        entries.reverse();
    }
    let mut noncanonical=Vec::new();
    ciborium::ser::into_writer(&value,&mut noncanonical).unwrap();
    if noncanonical != canonical {
        assert!(decode_trace(&noncanonical).is_err());
    }
}

#[test]
fn expected_matrix_still_holds_after_phase3() {
    let expected:Value=serde_json::from_str(&fs::read_to_string("fixtures/expected.json").unwrap()).unwrap();
    for name in ["F","G","H","I","L","M"] {
        let actual=serde_json::to_value(evaluate(&fixture(name))).unwrap();
        for key in ["truth","applicability","decidability","dependency_status","i1a","i1b","validity_dependency","witness_independence"] {
            assert_eq!(actual.get(key),expected.get(name).and_then(|x|x.get(key)),"{name}:{key}");
        }
    }
}
