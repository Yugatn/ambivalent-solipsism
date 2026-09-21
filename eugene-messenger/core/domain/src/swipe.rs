#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SwipeDirection {
    Left,
    Right,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct SwipePolicy {
    pub threshold_ratio_milli: u16,
    pub max_duration_ms: u64,
}

impl Default for SwipePolicy {
    fn default() -> Self {
        Self {
            threshold_ratio_milli: 300,
            max_duration_ms: 500,
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SwipeOutcome {
    None,
    Commit(SwipeDirection),
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct SwipeStateMachine {
    policy: SwipePolicy,
    direction: Option<SwipeDirection>,
    normalized_distance_milli: u16,
}

impl SwipeStateMachine {
    pub fn new(policy: SwipePolicy) -> Self {
        Self {
            policy,
            direction: None,
            normalized_distance_milli: 0,
        }
    }

    pub fn begin(&mut self, direction: SwipeDirection) {
        self.direction = Some(direction);
        self.normalized_distance_milli = 0;
    }

    pub fn drag(&mut self, normalized_distance: f32) {
        let clamped = normalized_distance.clamp(0.0, 1.0);
        self.normalized_distance_milli = (clamped * 1000.0).round() as u16;
    }

    pub fn release(&mut self, duration_ms: u64) -> SwipeOutcome {
        let outcome = match self.direction {
            Some(direction)
                if self.normalized_distance_milli
                    >= self.policy.threshold_ratio_milli
                    && duration_ms <= self.policy.max_duration_ms =>
            {
                SwipeOutcome::Commit(direction)
            }
            _ => SwipeOutcome::None,
        };
        self.cancel();
        outcome
    }

    pub fn cancel(&mut self) {
        self.direction = None;
        self.normalized_distance_milli = 0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn below_threshold_does_not_commit() {
        let mut sm = SwipeStateMachine::new(SwipePolicy::default());
        sm.begin(SwipeDirection::Left);
        sm.drag(0.299);
        assert_eq!(sm.release(100), SwipeOutcome::None);
    }

    #[test]
    fn threshold_commits() {
        let mut sm = SwipeStateMachine::new(SwipePolicy::default());
        sm.begin(SwipeDirection::Right);
        sm.drag(0.30);
        assert_eq!(sm.release(500), SwipeOutcome::Commit(SwipeDirection::Right));
    }

    #[test]
    fn slow_swipe_does_not_commit() {
        let mut sm = SwipeStateMachine::new(SwipePolicy::default());
        sm.begin(SwipeDirection::Left);
        sm.drag(0.9);
        assert_eq!(sm.release(501), SwipeOutcome::None);
    }
}
