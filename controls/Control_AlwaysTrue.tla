---- MODULE Control_AlwaysTrue ----
EXTENDS TLC
VARIABLE x

Init == x = FALSE
Next == x' = ~x
AlwaysTrue == x = x
Spec == Init /\ [][Next]_x
====
