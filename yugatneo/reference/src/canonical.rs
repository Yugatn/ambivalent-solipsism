use serde_json::Value;
use sha2::{Digest, Sha256};
use std::fmt::Write;

#[derive(Debug, thiserror::Error)]
pub enum CanonicalError {
    #[error("floating point values are forbidden in the Yugatneo canonical profile")]
    FloatForbidden,
    #[error("CBOR tags are forbidden in the Yugatneo canonical profile")]
    TagForbidden,
    #[error("unsupported CBOR value")]
    Unsupported,
    #[error("CBOR decode failed: {0}")]
    Decode(String),
    #[error("input is not in Yugatneo deterministic CBOR form")]
    NonCanonical,
    #[error("trailing bytes after CBOR item")]
    TrailingBytes,
}

fn json_to_cbor(v: &Value) -> Result<ciborium::Value, CanonicalError> {
    use ciborium::Value as C;
    Ok(match v {
        Value::Null => C::Null,
        Value::Bool(b) => C::Bool(*b),
        Value::Number(n) => {
            if let Some(u) = n.as_u64() { C::Integer(u.into()) }
            else if let Some(i) = n.as_i64() { C::Integer(i.into()) }
            else { return Err(CanonicalError::FloatForbidden); }
        }
        Value::String(s) => C::Text(s.clone()),
        Value::Array(a) => C::Array(a.iter().map(json_to_cbor).collect::<Result<_,_>>()?),
        Value::Object(m) => {
            let mut entries = m.iter()
                .map(|(k,v)| Ok((C::Text(k.clone()), json_to_cbor(v)?)))
                .collect::<Result<Vec<_>, CanonicalError>>()?;
            entries.sort_by(|(ka,_),(kb,_)| {
                let mut a=Vec::new(); let mut b=Vec::new();
                ciborium::ser::into_writer(ka, &mut a).expect("in-memory CBOR");
                ciborium::ser::into_writer(kb, &mut b).expect("in-memory CBOR");
                a.cmp(&b)
            });
            C::Map(entries)
        }
    })
}

fn reject_unsupported(v: &ciborium::Value) -> Result<(), CanonicalError> {
    use ciborium::Value;
    match v {
        Value::Float(_) => Err(CanonicalError::FloatForbidden),
        Value::Tag(_, _) => Err(CanonicalError::TagForbidden),
        Value::Array(a) => a.iter().try_for_each(reject_unsupported),
        Value::Map(m) => m.iter().try_for_each(|(k,v)| {
            if !matches!(k, Value::Text(_)) { return Err(CanonicalError::Unsupported); }
            reject_unsupported(k)?; reject_unsupported(v)
        }),
        _ => Ok(()),
    }
}

fn canonical_cbor_value(v: &ciborium::Value) -> Result<Vec<u8>, CanonicalError> {
    reject_unsupported(v)?;
    let canonical = ciborium::value::CanonicalValue::from(v.clone());
    let mut out=Vec::new();
    ciborium::ser::into_writer(&canonical, &mut out)
        .map_err(|e| CanonicalError::Decode(e.to_string()))?;
    Ok(out)
}

pub fn encode(value: &Value) -> Result<Vec<u8>, CanonicalError> {
    let c = json_to_cbor(value)?;
    canonical_cbor_value(&c)
}

pub fn decode_value(bytes: &[u8]) -> Result<ciborium::Value, CanonicalError> {
    let mut cursor=std::io::Cursor::new(bytes);
    let value: ciborium::Value = ciborium::de::from_reader(&mut cursor)
        .map_err(|e| CanonicalError::Decode(e.to_string()))?;
    if cursor.position() as usize != bytes.len() {
        return Err(CanonicalError::TrailingBytes);
    }
    let canonical = canonical_cbor_value(&value)?;
    if canonical != bytes {
        return Err(CanonicalError::NonCanonical);
    }
    Ok(value)
}

pub fn decode_trace(bytes: &[u8]) -> Result<crate::model::Trace, CanonicalError> {
    let value=decode_value(bytes)?;
    reject_unsupported(&value)?;
    value.deserialized::<crate::model::Trace>()
        .map_err(|e| CanonicalError::Decode(e.to_string()))
}

pub fn encode_trace(trace: &crate::model::Trace) -> Result<Vec<u8>, CanonicalError> {
    let value = serde_json::to_value(trace).map_err(|_| CanonicalError::Unsupported)?;
    encode(&value)
}

pub fn sha256_domain(domain: &str, value: &Value) -> Result<String, CanonicalError> {
    let bytes=encode(value)?;
    let mut h=Sha256::new();
    h.update(domain.as_bytes());
    h.update([0]);
    h.update(bytes);
    let digest=h.finalize();
    let mut s=String::with_capacity(64);
    for b in digest { write!(&mut s, "{b:02x}").unwrap(); }
    Ok(s)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn map_order_is_deterministic() {
        let a=serde_json::json!({"b":1,"a":2});
        let b=serde_json::json!({"a":2,"b":1});
        assert_eq!(encode(&a).unwrap(),encode(&b).unwrap());
    }
    #[test]
    fn floats_are_rejected() {
        let v=serde_json::json!(1.5);
        assert!(matches!(encode(&v),Err(CanonicalError::FloatForbidden)));
    }
    #[test]
    fn cbor_roundtrip_is_byte_stable() {
        let v=serde_json::json!({"z": [1,2], "a": true});
        let bytes=encode(&v).unwrap();
        let decoded=decode_value(&bytes).unwrap();
        let mut out=Vec::new();
        ciborium::ser::into_writer(&ciborium::value::CanonicalValue::from(decoded), &mut out).unwrap();
        assert_eq!(bytes,out);
    }
}
