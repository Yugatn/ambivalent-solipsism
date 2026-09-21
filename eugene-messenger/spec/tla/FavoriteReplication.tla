---- MODULE FavoriteReplication ----
EXTENDS Naturals

CONSTANTS None, Left, Right, DeviceA, DeviceB, Op1, Op2

VARIABLES state, winner

vars == <<state, winner>>

Init ==
    /\ state = None
    /\ winner = 0

Apply(opTime, device, operationId, target) ==
    IF <<opTime, device, operationId>> > winner
    THEN /\ state' = target
         /\ winner' = <<opTime, device, operationId>>
    ELSE /\ UNCHANGED <<state, winner>>

DeterministicResolution ==
    winner = 0 \/ state \in {None, Left, Right}

====
