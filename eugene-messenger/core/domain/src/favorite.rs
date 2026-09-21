use std::collections::BTreeSet;

use crate::{
    errors::DomainError,
    ids::{MessageId, OperationId},
    operation::FavoriteOperation,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FavoriteState {
    None,
    Left,
    Right,
}

#[derive(Debug)]
pub struct FavoriteStateMachine {
    state: FavoriteState,
    applied_operations: BTreeSet<OperationId>,
    winning_operation: Option<FavoriteOperation>,
}

impl FavoriteStateMachine {
    pub fn new() -> Self {
        Self {
            state: FavoriteState::None,
            applied_operations: BTreeSet::new(),
            winning_operation: None,
        }
    }

    pub fn state(&self) -> FavoriteState {
        self.state
    }

    pub fn applied_operation_count(&self) -> usize {
        self.applied_operations.len()
    }

    pub fn apply(&mut self, op: FavoriteOperation) -> Result<bool, DomainError> {
        if self.applied_operations.contains(&op.operation_id) {
            return Ok(false);
        }

        self.applied_operations.insert(op.operation_id);

        match self.winning_operation {
            None => {
                self.state = op.target;
                self.winning_operation = Some(op);
                Ok(true)
            }
            Some(current) if op.ordering_key() > current.ordering_key() => {
                self.state = op.target;
                self.winning_operation = Some(op);
                Ok(true)
            }
            Some(_) => Ok(false),
        }
    }

    pub fn remove_for_message(
        &mut self,
        message_id: MessageId,
        op: FavoriteOperation,
    ) -> Result<bool, DomainError> {
        if op.message_id != message_id {
            return Err(DomainError::MessageMismatch);
        }
        self.apply(op)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        clock::HlcTimestamp,
        ids::{DeviceId, MessageId, OperationId},
    };

    fn op(id: u128, time: u64, target: FavoriteState) -> FavoriteOperation {
        let device = DeviceId(1);
        FavoriteOperation {
            operation_id: OperationId(id),
            message_id: MessageId(7),
            target,
            previous_state: FavoriteState::None,
            device_id: device,
            logical_time: HlcTimestamp {
                wall_time_ms: time,
                counter: 0,
                device_id: device,
            },
        }
    }

    #[test]
    fn duplicate_operation_is_idempotent() {
        let mut sm = FavoriteStateMachine::new();
        let first = op(1, 1, FavoriteState::Left);
        assert!(sm.apply(first).unwrap());
        assert!(!sm.apply(first).unwrap());
        assert_eq!(sm.state(), FavoriteState::Left);
        assert_eq!(sm.applied_operation_count(), 1);
    }

    #[test]
    fn newer_operation_wins_deterministically() {
        let mut sm = FavoriteStateMachine::new();
        assert!(sm.apply(op(1, 1, FavoriteState::Left)).unwrap());
        assert!(sm.apply(op(2, 2, FavoriteState::Right)).unwrap());
        assert_eq!(sm.state(), FavoriteState::Right);
    }

    #[test]
    fn older_operation_cannot_roll_back_newer_state() {
        let mut sm = FavoriteStateMachine::new();
        assert!(sm.apply(op(2, 2, FavoriteState::Right)).unwrap());
        assert!(!sm.apply(op(1, 1, FavoriteState::Left)).unwrap());
        assert_eq!(sm.state(), FavoriteState::Right);
    }
}
