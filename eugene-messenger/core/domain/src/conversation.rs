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
    winning_favorite_operations: BTreeMap<MessageId, FavoriteOperation>,
    #[test]
    fn undo_is_a_new_append_only_operation() {
        let mut state = ConversationState::new();
        state.insert_message(MessageState::new(MessageId(9)));
        assert!(state.apply_favorite(op(1, 9, 1, FavoriteState::Left)).unwrap());

        let undo = state.undo_favorite(
            MessageId(9),
            OperationId(2),
            DeviceId(1),
            HlcTimestamp { wall_time_ms: 2, counter: 0, device_id: DeviceId(1) },
        ).unwrap();

        assert_eq!(undo.previous_state, FavoriteState::Left);
        assert_eq!(undo.target, FavoriteState::None);
        assert_eq!(state.messages[&MessageId(9)].favorite, FavoriteState::None);
        assert_eq!(state.applied_operation_count(), 2);
    }

}

impl ConversationState {
    pub fn new() -> Self { Self::default() }

    pub fn insert_message(&mut self, message: MessageState) {
        self.messages.insert(message.id, message);
    }

    pub fn applied_operation_count(&self) -> usize {
        self.applied_operations.len()
    }

    pub fn undo_favorite(
        &mut self,
        message_id: MessageId,
        operation_id: OperationId,
        device_id: crate::ids::DeviceId,
        logical_time: crate::clock::HlcTimestamp,
    ) -> Result<FavoriteOperation, DomainError> {
        let current = self.messages.get(&message_id).ok_or(DomainError::MessageNotFound)?.favorite;
        let op = FavoriteOperation {
            operation_id,
            message_id,
            target: crate::favorite::FavoriteState::None,
            previous_state: current,
            device_id,
            logical_time,
        };
        self.apply_favorite(op)?;
        Ok(op)
    }

    pub fn apply_favorite(&mut self, op: FavoriteOperation) -> Result<bool, DomainError> {
        if self.applied_operations.contains(&op.operation_id) {
            return Ok(false);
        }
        if !self.messages.contains_key(&op.message_id) {
            return Err(DomainError::MessageNotFound);
        }

        self.applied_operations.insert(op.operation_id);

        let should_apply = self.winning_favorite_operations
            .get(&op.message_id)
            .map(|current| op.wins_over(current))
            .unwrap_or(true);

        if should_apply {
            self.winning_favorite_operations.insert(op.message_id, op);
            self.messages.get_mut(&op.message_id).expect("message checked above").favorite = op.target;
            Ok(true)
        } else {
            Ok(false)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{clock::HlcTimestamp, favorite::FavoriteState, ids::DeviceId};

    fn op(id: u128, msg: u128, time: u64, target: FavoriteState) -> FavoriteOperation {
        let device = DeviceId(1);
        FavoriteOperation {
            operation_id: OperationId(id),
            message_id: MessageId(msg),
            target,
            device_id: device,
            logical_time: HlcTimestamp { wall_time_ms: time, counter: 0, device_id: device },
        }
    }

    #[test]
    fn duplicate_delivery_has_no_second_effect() {
        let mut state = ConversationState::new();
        state.insert_message(MessageState::new(MessageId(9)));
        let operation = op(1, 9, 1, FavoriteState::Left);
        assert!(state.apply_favorite(operation).unwrap());
        assert!(!state.apply_favorite(operation).unwrap());
        assert_eq!(state.messages[&MessageId(9)].favorite, FavoriteState::Left);
    }

    #[test]
    fn newer_operation_wins_even_when_delivered_first() {
        let mut state = ConversationState::new();
        state.insert_message(MessageState::new(MessageId(9)));
        assert!(state.apply_favorite(op(2, 9, 20, FavoriteState::Right)).unwrap());
        assert!(!state.apply_favorite(op(1, 9, 10, FavoriteState::Left)).unwrap());
        assert_eq!(state.messages[&MessageId(9)].favorite, FavoriteState::Right);
    }

    #[test]
    fn older_then_newer_converges() {
        let mut state = ConversationState::new();
        state.insert_message(MessageState::new(MessageId(9)));
        assert!(state.apply_favorite(op(1, 9, 10, FavoriteState::Left)).unwrap());
        assert!(state.apply_favorite(op(2, 9, 20, FavoriteState::Right)).unwrap());
        assert_eq!(state.messages[&MessageId(9)].favorite, FavoriteState::Right);
    }

    #[test]
    fn unknown_message_does_not_mark_operation_applied() {
        let mut state = ConversationState::new();
        let operation = op(1, 404, 1, FavoriteState::Left);
        assert_eq!(state.apply_favorite(operation).unwrap_err(), DomainError::MessageNotFound);
        assert_eq!(state.applied_operation_count(), 0);
    }
    #[test]
    fn undo_is_a_new_append_only_operation() {
        let mut state = ConversationState::new();
        state.insert_message(MessageState::new(MessageId(9)));
        assert!(state.apply_favorite(op(1, 9, 1, FavoriteState::Left)).unwrap());

        let undo = state.undo_favorite(
            MessageId(9),
            OperationId(2),
            DeviceId(1),
            HlcTimestamp { wall_time_ms: 2, counter: 0, device_id: DeviceId(1) },
        ).unwrap();

        assert_eq!(undo.previous_state, FavoriteState::Left);
        assert_eq!(undo.target, FavoriteState::None);
        assert_eq!(state.messages[&MessageId(9)].favorite, FavoriteState::None);
        assert_eq!(state.applied_operation_count(), 2);
    }

}
