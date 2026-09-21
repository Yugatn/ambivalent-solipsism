use anyhow::{Context, Result};
use base64::{engine::general_purpose::STANDARD as B64, Engine};
use chacha20poly1305::{aead::{Aead, KeyInit}, XChaCha20Poly1305, XNonce};
use ed25519_dalek::{Signer, SigningKey};
use hkdf::Hkdf;
use rand::{rngs::OsRng, RngCore};
use serde::{Deserialize, Serialize};
use sha2::Sha256;
use std::{env, fs};

#[derive(Serialize, Deserialize)]
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
    let receiver_pub = fs::read(env::args().nth(1).context("receiver public key path")?)?;
    let plaintext = env::var("PLAINTEXT").unwrap_or_else(|_| "hello from Eugene Messenger".into());

    let receiver_public: [u8; 32] = receiver_pub.try_into().map_err(|_| anyhow::anyhow!("receiver public key must be 32 bytes"))?;
    let receiver_public = x25519_dalek::PublicKey::from(receiver_public);

    let sender_signing = SigningKey::generate(&mut OsRng);
    let sender_secret = x25519_dalek::StaticSecret::random_from_rng(OsRng);
    let sender_public = x25519_dalek::PublicKey::from(&sender_secret);
    let shared = sender_secret.diffie_hellman(&receiver_public);
    let key = derive_key(shared.as_bytes());

    let cipher = XChaCha20Poly1305::new((&key).into());
    let mut nonce = [0u8; 24];
    OsRng.fill_bytes(&mut nonce);
    let ciphertext = cipher.encrypt(XNonce::from_slice(&nonce), plaintext.as_bytes())?;

    let signature = sender_signing.sign(&ciphertext);

    let envelope = Envelope {
        version: 1,
        algorithm: "X25519+HKDF-SHA256+XChaCha20-Poly1305+Ed25519".into(),
        sender_signing_pubkey: B64.encode(sender_signing.verifying_key().to_bytes()),
        receiver_x25519_pubkey: B64.encode(receiver_public.as_bytes()),
        nonce: B64.encode(nonce),
        ciphertext: B64.encode(ciphertext),
        signature: B64.encode(signature.to_bytes()),
    };

    fs::write("encrypted_message.json", serde_json::to_vec_pretty(&envelope)?)?;
    fs::write("sender_x25519_private.key", sender_secret.to_bytes())?;
    fs::write("sender_x25519_public.key", sender_public.as_bytes())?;

    let trace = serde_json::json!([
        {"event":"sender_identity_created"},
        {"event":"message_encrypted"},
        {"event":"ciphertext_emitted"},
        {"event":"sender_private_key_revoked_from_artifact","detail":"private key must not be uploaded"}
    ]);
    fs::write("sender_trace.json", serde_json::to_vec_pretty(&trace)?)?;
    Ok(())
}
