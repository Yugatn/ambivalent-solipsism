---- MODULE Control_AlwaysTrue ----
EXTENDS Naturals
VARIABLE x

Init == x = 0
Next == x' = x + 1
AlwaysTrue == x = x
Spec == Init /\ [][Next]_x
====
