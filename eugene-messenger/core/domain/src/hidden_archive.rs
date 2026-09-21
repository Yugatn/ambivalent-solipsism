use std::collections::VecDeque;
use std::time::{Duration, Instant};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum UnlockScope {
    HiddenArchive,
}

/// A successful unlock is intentionally process-local and non-serializable.
#[derive(Debug)]
pub struct UnlockSession {
    pub scope: UnlockScope,
    started_at: Instant,
    expires_at: Instant,
}

impl UnlockSession {
    pub fn new(scope: UnlockScope, now: Instant, lifetime: Duration) -> Self {
        Self {
            scope,
            started_at: now,
            expires_at: now + lifetime,
        }
    }

    pub fn is_active(&self, now: Instant) -> bool {
        now < self.expires_at
    }

    pub fn started_at(&self) -> Instant {
        self.started_at
    }
}

/// Crypto/KDF implementation belongs outside the domain crate.
/// The domain only consumes a boolean verification result.
pub trait UnlockVerifier {
    fn verify(&self, input: &str) -> bool;
}

#[derive(Debug)]
pub struct UnlockRateLimiter {
    attempts: VecDeque<Instant>,
    max_attempts: usize,
    window: Duration,
}

impl UnlockRateLimiter {
    pub fn new(max_attempts: usize, window: Duration) -> Self {
        Self {
            attempts: VecDeque::new(),
            max_attempts,
            window,
        }
    }

    pub fn allow(&mut self, now: Instant) -> bool {
        while self
            .attempts
            .front()
            .is_some_and(|t| now.duration_since(*t) >= self.window)
        {
            self.attempts.pop_front();
        }

        if self.attempts.len() >= self.max_attempts {
            return false;
        }

        self.attempts.push_back(now);
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn session_expires_without_persistence() {
        let now = Instant::now();
        let session = UnlockSession::new(UnlockScope::HiddenArchive, now, Duration::from_secs(5));
        assert!(session.is_active(now + Duration::from_secs(4)));
        assert!(!session.is_active(now + Duration::from_secs(5)));
    }

    #[test]
    fn rate_limiter_blocks_after_limit() {
        let now = Instant::now();
        let mut limiter = UnlockRateLimiter::new(2, Duration::from_secs(60));
        assert!(limiter.allow(now));
        assert!(limiter.allow(now + Duration::from_secs(1)));
        assert!(!limiter.allow(now + Duration::from_secs(2)));
    }
}
