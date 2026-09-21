---- MODULE AntiReplay_Protocol_Broken ----
EXTENDS Naturals, Sequences, FiniteSets

CONSTANT Messages
VARIABLES sender, receiver, channel, adversary

Vars == <<sender, receiver, channel, adversary>>

Init ==
    /\ sender = [sent |-> {}, nextSeq |-> 0]
    /\ receiver = [accepted |-> <<>>, seen |-> {}]
    /\ channel = <<>>
    /\ adversary = [seen |-> {}]

Send(m) ==
    /\ m \in Messages
    /\ m = sender.nextSeq
    /\ sender' = [sent |-> sender.sent \cup {m}, nextSeq |-> sender.nextSeq + 1]
    /\ channel' = Append(channel, m)
    /\ UNCHANGED <<receiver, adversary>>

Receive(m) ==
    /\ Len(channel) > 0
    /\ Head(channel) = m
    /\ channel' = Tail(channel)
    /\ receiver' = [
        accepted |-> Append(receiver.accepted, m),
        seen |-> receiver.seen \cup {m}
    ]
    /\ adversary' = [seen |-> adversary.seen \cup {m}]
    /\ UNCHANGED sender

AdversaryReplay(m) ==
    /\ m \in adversary.seen
    /\ channel' = Append(channel, m)
    /\ UNCHANGED <<sender, receiver, adversary>>

Next ==
    \/ \E m \in Messages : Send(m)
    \/ \E m \in Messages : Receive(m)
    \/ \E m \in Messages : AdversaryReplay(m)

NoReplayAccepted ==
    \A seq \in Messages :
        Cardinality({ i \in 1..Len(receiver.accepted) :
            receiver.accepted[i] = seq }) <= 1

Spec == Init /\ [][Next]_Vars
====