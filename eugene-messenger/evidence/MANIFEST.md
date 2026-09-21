# Evidence Manifest

Evidence is immutable research output, not a decorative build artifact.

For every recorded verification run, retain:
- claim identifier;
- exact specification and configuration;
- toolchain identity;
- input hashes;
- model-check result;
- counterexample, when expected;
- reproduction command;
- timestamp.

A later toolchain update creates a new evidence record. It does not silently rewrite historical evidence.

Evidence must distinguish:
- model checking of an abstract specification;
- conformance of an implementation;
- adversarial testing;
- external audit.

None of these alone proves the entire Eugene Messenger system.