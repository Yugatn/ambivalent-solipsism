#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ArchiveState {
    Active,
    Archived,
    Deleted,
}

impl ArchiveState {
    pub fn archive(self) -> Self {
        match self {
            Self::Active => Self::Archived,
            Self::Archived => Self::Archived,
            Self::Deleted => Self::Deleted,
        }
    }

    pub fn restore(self) -> Self {
        match self {
            Self::Archived => Self::Active,
            other => other,
        }
    }
}
