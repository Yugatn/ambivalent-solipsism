use anyhow::{Context, Result};
use base64::{engine::general_purpose::STANDARD as B64, Engine};
use chacha20poly1305::{aead::{Aead, KeyInit}, XChaCha20Poly1305, XNonce};
use ed25519_dalek::{Signature, Verifier, VerifyingKey};
use hkdf::Hkdf;
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::{env, fs};

#[derive(Deserialize)]
struct Envelope {
    version: u8,
    algorithm: String,
    sender_signing_pubkey: String,
    receiver_x25519_pubkey: String,
    nonce: String,
    ciphertext: String,
    signature: String,
}

fn derive_key(shared: &[u8; 32]) -> [u8; 32] {
    let hk = Hkdf::<Sha256>::new(Some(b"eugene-messenger-sim-v1"), shared);
    let mut key = [0u8; 32];
    hk.expand(b"message-key", &mut key).expect("HKDF length is valid");
    key
}

fn main() -> Result<()> {
    let mut args = env::args().skip(1);
    if args.next().as_deref() == Some("--derive-public") {
        let private_path = args.next().context("private key path")?;
        let public_path = args.next().context("public key path")?;
        let bytes: [u8; 32] = fs::read(private_path)?.try_into().map_err(|_| anyhow::anyhow!("invalid private key"))?;
        let secret = x25519_dalek::StaticSecret::from(bytes);
        fs::write(public_path, x25519_dalek::PublicKey::from(&secret).as_bytes())?;
        return Ok(());
    }

    let input = args.next().context("encrypted message path")?;
    let receiver_private = fs::read(args.next().context("receiver private key path")?)?;
    let expected = env::var("EXPECTED_PLAINTEXT").unwrap_or_else(|_| "hello from Eugene Messenger".into());

    let envelope: Envelope = serde_json::from_slice(&fs::read(input)?)?;
    anyhow::ensure!(envelope.version == 1, "unsupported envelope version");
    anyhow::ensure!(envelope.algorithm.contains("X25519"), "unexpected algorithm");

    let sender_pub = B64.decode(envelope.sender_signing_pubkey)?;
    let sender_pub: [u8; 32] = sender_pub.try_into().map_err(|_| anyhow::anyhow!("invalid sender signing key"))?;
    let sender_pub = VerifyingKey::from_bytes(&sender_pub)?;

    let signature = B64.decode(envelope.signature)?;
    let signature = Signature::from_slice(&signature)?;
    let ciphertext = B64.decode(&envelope.ciphertext)?;
    sender_pub.verify(&ciphertext, &signature).context("signature verification failed")?;

    let receiver_secret: [u8; 32] = receiver_private.try_into().map_err(|_| anyhow::anyhow!("invalid receiver private key"))?;
    let receiver_secret = x25519_dalek::StaticSecret::from(receiver_secret);
    let sender_x25519 = B64.decode(envelope.receiver_x25519_pubkey)?;
    let _ = sender_x25519;

    // The sender's ephemeral X25519 public key is carried separately by the simulation.
    let sender_public = x25519_dalek::PublicKey::from(
        fs::read("sender_x25519_public.key")?.try_into().map_err(|_| anyhow::anyhow!("invalid sender public key"))?
    );
    let receiver_public = x25519_dalek::PublicKey::from(&receiver_secret);
    anyhow::ensure!(B64.encode(receiver_public.as_bytes()) == envelope.receiver_x25519_pubkey, "receiver key binding mismatch");

    let shared = receiver_secret.diffie_hellman(&sender_public);
    let key = derive_key(shared.as_bytes());
    let cipher = XChaCha20Poly1305::new((&key).into());
    let nonce = B64.decode(envelope.nonce)?;
    let plaintext = cipher.decrypt(XNonce::from_slice(&nonce), ciphertext.as_ref())?;
    let plaintext = String::from_utf8(plaintext)?;

    anyhow::ensure!(plaintext == expected, "plaintext mismatch");

    let trace = serde_json::json!([
        {"event":"artifact_received"},
        {"event":"signature_verified"},
        {"event":"aead_decryption_verified"},
        {"event":"plaintext_verified"},
        {"event":"conformance_pass"}
    ]);
    let result = serde_json::json!({
        "status":"pass",
        "checks":[
            "SignatureVerifies",
            "AEADIntegrity",
            "PlaintextMatches"
        ],
        "ciphertext_sha256": format!("sha256:{:x}", Sha256::digest(B64.decode(envelope.ciphertext)?)),
        "residual_risk":[
            "runner_compromise",
            "traffic_analysis",
            "metadata_correlation",
            "cryptographic_strength_not_formally_proven"
        ],
        "trace": trace
    });
    fs::write("receiver_result.json", serde_json::to_vec_pretty(&result)?)?;
    Ok(())
}
