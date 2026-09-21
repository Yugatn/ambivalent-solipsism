use crate::invariant::evaluate;
use crate::model::Trace;

pub fn classify(trace: &Trace) -> crate::ResultEnvelope {
    evaluate(trace)
}
