# Phase 11 Runtime Pilot Kernel

This directory contains the deliberately minimal executable reference slice for Phase 11.

## Scope

The kernel currently exercises five protected boundaries:

1. Event idempotency;
2. UNKNOWN evidence preservation;
3. Human Review barrier;
4. Decision versus Action separation;
5. denial preventing Action execution.

It is an in-memory reference implementation, not a production service, persistence layer, authorization service or security boundary.

## Execution

From this directory:

    python -m unittest -v test_pilot_kernel.py

The tests correspond to P11-02, P11-03 and core parts of the Critical Formal Kernel K02–K05.

## Explicit non-goals

The kernel does not yet implement federation transport, cryptographic verification, durable storage, real identity, network authorization, retention enforcement or production audit infrastructure.


## Current kernel coverage

The executable slice now exercises K01–K05 and K06–K10 through in-memory tests: unauthorized execution, non-escalation of authority, historical correction, recovery blocking and terminal reconstruction are covered alongside event idempotency, UNKNOWN preservation, Human Review and Decision/Action separation.

This is test coverage of the reference kernel, not a production certification or proof that every external implementation path conforms to it.
