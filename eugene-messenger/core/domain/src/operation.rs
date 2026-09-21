use crate::{
    clock::HlcTimestamp,
    favorite::FavoriteState,
    ids::{DeviceId, MessageId, OperationId},
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FavoriteOperation {
    pub operation_id: OperationId,
    pub message_id: MessageId,
    pub target: FavoriteState,
    pub device_id: DeviceId,
    pub logical_time: HlcTimestamp,
}

impl FavoriteOperation {
    pub fn ordering_key(&self) -> (HlcTimestamp, DeviceId, OperationId) {
        (self.logical_time, self.device_id, self.operation_id)
    }
}
