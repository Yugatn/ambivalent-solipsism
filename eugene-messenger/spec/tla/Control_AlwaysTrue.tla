---- MODULE Control_AlwaysTrue ----
EXTENDS Naturals
VARIABLE x
Init == x = 0
Next == x' = x + 1
AlwaysTrue == [](x >= 0)
Spec == Init /\ [][Next]_<<x>>
====