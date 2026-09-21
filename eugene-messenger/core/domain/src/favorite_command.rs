use crate::favorite::FavoriteState;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FavoriteCommand {
    Set(FavoriteState),
    Remove,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FavoriteCommandResult {
    pub previous: FavoriteState,
    pub current: FavoriteState,
}

impl FavoriteCommand {
    pub fn target(self, previous: FavoriteState) -> FavoriteState {
        match self {
            Self::Set(state) => state,
            Self::Remove => FavoriteState::None,
        }
    }

    pub fn apply(self, previous: FavoriteState) -> FavoriteCommandResult {
        FavoriteCommandResult {
            previous,
            current: self.target(previous),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn remove_and_set_use_the_same_domain_path() {
        assert_eq!(
            FavoriteCommand::Set(FavoriteState::Left).apply(FavoriteState::None).current,
            FavoriteState::Left
        );
        assert_eq!(
            FavoriteCommand::Remove.apply(FavoriteState::Left).current,
            FavoriteState::None
        );
    }
}
