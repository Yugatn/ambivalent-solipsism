//! Eugene Messenger conversation domain.
//! UI-independent state transitions for feed direction, favorites and archive.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum FeedDirection { Down, Up }
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum FavoriteState { None, Left, Right }
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ArchiveState { Active, Archived, Restored, Deleted }
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SwipeDirection { Left, Right }

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct MessageState {
    pub favorite: FavoriteState,
    pub archive: ArchiveState,
}
impl Default for MessageState {
    fn default() -> Self { Self { favorite: FavoriteState::None, archive: ArchiveState::Active } }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct FavoriteOperation {
    pub message_id: u64,
    pub target: FavoriteState,
    pub operation_id: u64,
    pub device_id: u64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum DomainError { DeletedMessage }

impl MessageState {
    pub fn commit_swipe(&mut self, direction: SwipeDirection) -> Result<(), DomainError> {
        if self.archive == ArchiveState::Deleted { return Err(DomainError::DeletedMessage); }
        self.favorite = match direction {
            SwipeDirection::Left => FavoriteState::Left,
            SwipeDirection::Right => FavoriteState::Right,
        };
        Ok(())
    }
    pub fn remove_favorite(&mut self) { self.favorite = FavoriteState::None; }
    pub fn archive(&mut self) { if self.archive != ArchiveState::Deleted { self.archive = ArchiveState::Archived; } }
    pub fn restore(&mut self) { if self.archive == ArchiveState::Archived { self.archive = ArchiveState::Restored; } }
    pub fn delete(&mut self) { self.archive = ArchiveState::Deleted; }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn left_and_right_are_mutually_exclusive() {
        let mut m = MessageState::default();
        m.commit_swipe(SwipeDirection::Left).unwrap();
        m.commit_swipe(SwipeDirection::Right).unwrap();
        assert_eq!(m.favorite, FavoriteState::Right);
    }
    #[test]
    fn archive_does_not_change_favorite() {
        let mut m = MessageState::default();
        m.commit_swipe(SwipeDirection::Left).unwrap();
        m.archive(); m.restore();
        assert_eq!(m.favorite, FavoriteState::Left);
    }
    #[test]
    fn deleted_message_cannot_be_favorited() {
        let mut m = MessageState::default();
        m.delete();
        assert_eq!(m.commit_swipe(SwipeDirection::Left), Err(DomainError::DeletedMessage));
    }
    #[test]
    fn favorite_is_idempotent() {
        let mut m = MessageState::default();
        m.commit_swipe(SwipeDirection::Left).unwrap();
        m.commit_swipe(SwipeDirection::Left).unwrap();
        assert_eq!(m.favorite, FavoriteState::Left);
    }
}
