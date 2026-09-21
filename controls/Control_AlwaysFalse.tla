---- MODULE Control_AlwaysFalse ----
EXTENDS Naturals
VARIABLE x

Init == x = 0
Next == x' = x
AlwaysFalse == FALSE
Spec == Init /\ [][Next]_x
====
