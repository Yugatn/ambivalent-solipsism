---- MODULE Control_AlwaysFalse ----
EXTENDS Naturals
VARIABLE x
Init == x = 0
Next == x' = x + 1
AlwaysFalse == [](x < 0)
Spec == Init /\ [][Next]_<<x>>
====