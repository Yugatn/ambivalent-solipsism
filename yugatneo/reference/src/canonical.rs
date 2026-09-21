use serde_json::Value;
use sha2::{Digest, Sha256};
use std::fmt::Write;

#[derive(Debug, thiserror::Error)]
pub enum CanonicalError {
    #[error("floating point values are forbidden in canonical protocol data")]
    FloatForbidden,
    #[error("unsupported JSON value")]
    Unsupported,
}

fn uint_head(major: u8, n: u64, out: &mut Vec<u8>) {
    let base = major << 5;
    match n {
        0..=23 => out.push(base | n as u8),
        24..=255 => { out.push(base | 24); out.push(n as u8); }
        256..=65535 => { out.push(base | 25); out.extend_from_slice(&(n as u16).to_be_bytes()); }
        65536..=u32::MAX as u64 => { out.push(base | 26); out.extend_from_slice(&(n as u32).to_be_bytes()); }
        _ => { out.push(base | 27); out.extend_from_slice(&n.to_be_bytes()); }
    }
}

pub fn encode(value: &Value) -> Result<Vec<u8>, CanonicalError> {
    let mut out = Vec::new();
    encode_into(value, &mut out)?;
    Ok(out)
}

fn encode_into(v: &Value, out: &mut Vec<u8>) -> Result<(), CanonicalError> {
    match v {
        Value::Null => out.push(0xf6),
        Value::Bool(b) => out.push(if *b { 0xf5 } else { 0xf4 }),
        Value::Number(n) => {
            if let Some(u) = n.as_u64() {
                uint_head(0, u, out);
            } else if let Some(i) = n.as_i64() {
                let x = (-1i128 - i as i128) as u64;
                uint_head(1, x, out);
            } else {
                return Err(CanonicalError::FloatForbidden);
            }
        }
        Value::String(s) => {
            uint_head(3, s.len() as u64, out);
            out.extend_from_slice(s.as_bytes());
        }
        Value::Array(a) => {
            uint_head(4, a.len() as u64, out);
            for x in a { encode_into(x, out)?; }
        }
        Value::Object(m) => {
            let mut entries: Vec<(Vec<u8>, &Value)> = m.iter()
                .map(|(k,v)| {
                    let mut kb=Vec::new();
                    uint_head(3,k.len() as u64,&mut kb);
                    kb.extend_from_slice(k.as_bytes());
                    (kb,v)
                }).collect();
            entries.sort_by(|a,b| a.0.cmp(&b.0));
            uint_head(5, entries.len() as u64, out);
            for (kb,v) in entries {
                out.extend_from_slice(&kb);
                encode_into(v,out)?;
            }
        }
    }
    Ok(())
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
}
