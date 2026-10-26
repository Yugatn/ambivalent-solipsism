use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize)]
#[repr(u16)]
pub enum SchemaErrorCode {
    TraceVersionUnsupported = 1001,
    TraceEmpty = 1002,
    HorizonInvalid = 1003,
    EventOrderInvalid = 1004,
    EventIdInvalid = 2001,
    EventTypeUnknown = 2002,
    LogicalTimeInvalid = 2003,
    EventReferenceMissing = 2004,
    ProvenanceCycle = 4001,
    DanglingReference = 4002,
    ExternalReferenceUndeclared = 4003,
    CertificateClosureMissing = 4004,
    ScopeInvalid = 5001,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct SchemaError {
    pub code: SchemaErrorCode,
    pub message: String,
    pub location: String,
}

impl SchemaError {
    pub fn new(code: SchemaErrorCode, message: impl Into<String>, location: impl Into<String>) -> Self {
        Self { code, message: message.into(), location: location.into() }
    }
}
