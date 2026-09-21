use crate::{archive::ArchiveState, favorite::FavoriteState, ids::MessageId};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct MessageState {
    pub id: MessageId,
    pub favorite: FavoriteState,
    pub archive: ArchiveState,
}

impl MessageState {
    pub fn new(id: MessageId) -> Self {
        Self {
            id,
            favorite: FavoriteState::None,
            archive: ArchiveState::Active,
        }
    }
}
