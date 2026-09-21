use std::collections::{BTreeMap, BTreeSet};

use crate::{
    errors::DomainError,
    ids::{MessageId, OperationId},
    message::MessageState,
    operation::FavoriteOperation,
};

#[derive(Debug, Default)]
pub struct ConversationState {
    pub messages: BTreeMap<MessageId, MessageState>,
    applied_operations: BTreeSet<OperationId>,
}

impl ConversationState {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn insert_message(&mut self, message: MessageState) {
        self.messages.insert(message.id, message);
    }

    pub fn applied_operation_count(&self) -> usize {
        self.applied_operations.len()
    }

    /// Apply-once semantics is keyed by operation_id. A duplicate delivery is a no-op.
    /// Retention/GC is deliberately deferred to the storage/sync layer because
    /// premature GC could re-open replay acceptance.
    pub fn apply_favorite(&mut self, op: FavoriteOperation) -> Result<bool, DomainError> {
        if self.applied_operations.contains(&op.operation_id) {
            return Ok(false);
        }

        let message = self
            .messages
            .get(&op.message_id)
            .ok_or(DomainError::MessageNotFound)?;

        let current = message.favorite;
        let should_apply = match self
            .messages
            .get(&op.message_id)
            .and_then(|_| Some(current))
        {
            Some(_) => true,
            None => false,
        };

        if !should_apply {
            return Ok(false);
        }

        self.applied_operations.insert(op.operation_id);

        let message = self.messages.get_mut(&op.message_id).expect("message checked above");
        message.favorite = op.target;
        Ok(true)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{clock::HlcTimestamp, favorite::FavoriteState, ids::DeviceId};

    fn op(id: u128, msg: u128, target: FavoriteState) -> FavoriteOperation {
        let device = DeviceId(1);
        FavoriteOperation {
            operation_id: OperationId(id),
            message_id: MessageId(msg),
            target,
            device_id: device,
            logical_time: HlcTimestamp { wall_time_ms: id as u64, counter: 0, device_id: device },
        }
    }

    #[test]
    fn duplicate_delivery_has_no_second_effect() {
        let mut state = ConversationState::new();
        state.insert_message(MessageState::new(MessageId(9)));
        let operation = op(1, 9, FavoriteState::Left);

        assert!(state.apply_favorite(operation).unwrap());
        assert!(!state.apply_favorite(operation).unwrap());
        assert_eq!(state.messages[&MessageId(9)].favorite, FavoriteState::Left);
        assert_eq!(state.applied_operation_count(), 1);
    }

    #[test]
    fn unknown_message_does_not_mark_operation_applied() {
        let mut state = ConversationState::new();
        let operation = op(1, 404, FavoriteState::Left);

        assert_eq!(
            state.apply_favorite(operation).unwrap_err(),
            DomainError::MessageNotFound
        );
        assert_eq!(state.applied_operation_count(), 0);
    }
}
