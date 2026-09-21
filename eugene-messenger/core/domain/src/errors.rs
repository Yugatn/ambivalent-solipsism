#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DomainError {
    MessageMismatch,
    InvalidTransition,
}
