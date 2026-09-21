------------------------------ MODULE Sentinel ------------------------------
EXTENDS Naturals, FiniteSets, TLC

CONSTANTS
  Subjects,
  Resources,
  Authorities,
  Capabilities,
  EvidenceIds,
  PostEvidenceIds,
  Models,
  Actions,
  MaxQuarantineLease,
  MaxEmergencyLease

OperationalStates ==
  {"OBSERVE", "VERIFY", "GUARDED", "RESTRICT", "QUARANTINE",
   "HOLD", "RECOVER", "REVIEW"}

EpistemicStates ==
  {"OBSERVED", "RECONSTRUCTED", "INFERRED", "ASSUMED",
   "UNKNOWN", "CONFLICTING"}

HighImpactActions ==
  {"RESTRICT", "QUARANTINE", "HOLD", "RECOVER"}

ReversibleActions ==
  {"OBSERVE", "NOTIFY", "VERIFY", "GUARDED", "RESTRICT",
   "QUARANTINE", "HOLD", "RECOVER", "REVIEW"}

vars ==
  <<state, epistemic, evidence, provenance, capability, permission,
    authority, quarantineUntil, emergencyUntil, emergencyActive,
    challengeAvailable, challengeComplete, actionTaken,
    actionAuthorized, interventionOccurred, postActionEvidence,
    modelVersion, ruleVersion, degraded, stopAvailable,
    auditRecord, subjectExitAvailable, riskDisplacementChecked,
    goalIntact, now>>

Init ==
  /\ state = "OBSERVE"
  /\ epistemic = "UNKNOWN"
  /\ evidence = {}
  /\ provenance = {}
  /\ capability = {}
  /\ permission = {}
  /\ authority = {}
  /\ quarantineUntil = 0
  /\ emergencyUntil = 0
  /\ emergencyActive = FALSE
  /\ challengeAvailable = TRUE
  /\ challengeComplete = FALSE
  /\ actionTaken = "OBSERVE"
  /\ actionAuthorized = FALSE
  /\ interventionOccurred = FALSE
  /\ postActionEvidence = {}
  /\ modelVersion = CHOOSE m \in Models : TRUE
  /\ ruleVersion = CHOOSE r \in Models : TRUE
  /\ degraded = FALSE
  /\ stopAvailable = TRUE
  /\ auditRecord = {}
  /\ subjectExitAvailable = TRUE
  /\ riskDisplacementChecked = FALSE
  /\ goalIntact = TRUE
  /\ now = 0

TypeOK ==
  /\ state \in OperationalStates
  /\ epistemic \in EpistemicStates
  /\ evidence \subseteq EvidenceIds
  /\ provenance \subseteq EvidenceIds
  /\ capability \subseteq Capabilities
  /\ permission \subseteq Subjects
  /\ authority \subseteq Authorities
  /\ quarantineUntil \in Nat
  /\ emergencyUntil \in Nat
  /\ emergencyActive \in BOOLEAN
  /\ challengeAvailable \in BOOLEAN
  /\ challengeComplete \in BOOLEAN
  /\ actionTaken \in ReversibleActions
  /\ actionAuthorized \in BOOLEAN
  /\ interventionOccurred \in BOOLEAN
  /\ postActionEvidence \subseteq PostEvidenceIds
  /\ modelVersion \in Models
  /\ ruleVersion \in Models
  /\ degraded \in BOOLEAN
  /\ stopAvailable \in BOOLEAN
  /\ auditRecord \subseteq EvidenceIds
  /\ subjectExitAvailable \in BOOLEAN
  /\ riskDisplacementChecked \in BOOLEAN
  /\ goalIntact \in BOOLEAN
  /\ now \in Nat

Observe ==
  /\ state' = "OBSERVE"
  /\ UNCHANGED vars

CollectEvidence ==
  /\ evidence' = evidence \cup EvidenceIds
  /\ provenance' = provenance \cup EvidenceIds
  /\ epistemic' \in EpistemicStates
  /\ UNCHANGED <<state, capability, permission, authority,
      quarantineUntil, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionTaken,
      actionAuthorized, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

Verify ==
  /\ state' = "VERIFY"
  /\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

GrantPermission ==
  /\ capability' \in SUBSET Capabilities
  /\ capability' # {}
  /\ permission' \in SUBSET Subjects
  /\ permission' # {}
  /\ authority' \in SUBSET Authorities
  /\ authority' # {}
  /\ actionAuthorized' = TRUE
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      quarantineUntil, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionTaken,
      interventionOccurred, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact, now>>

DenyPermission ==
  /\ actionAuthorized' = FALSE
  /\ permission' = {}
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

Challenge ==
  /\ challengeAvailable
  /\ challengeComplete' = TRUE
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, quarantineUntil,
      emergencyUntil, emergencyActive, challengeAvailable,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

HighImpactAction ==
  /\ actionAuthorized
  /\ evidence # {}
  /\ provenance # {}
  /\ challengeAvailable
  /\ actionTaken' \in HighImpactActions
  /\ state' = actionTaken'
  /\ interventionOccurred' = TRUE
  /\ riskDisplacementChecked' = TRUE
  /\ auditRecord' = auditRecord \cup evidence
  /\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionAuthorized, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, subjectExitAvailable,
      goalIntact, now>>

Quarantine ==
  /\ actionAuthorized
  /\ evidence # {}
  /\ provenance # {}
  /\ challengeAvailable
  /\ state' = "QUARANTINE"
  /\ actionTaken' = "QUARANTINE"
  /\ quarantineUntil' = now + MaxQuarantineLease
  /\ interventionOccurred' = TRUE
  /\ riskDisplacementChecked' = TRUE
  /\ auditRecord' = auditRecord \cup evidence
  /\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionAuthorized,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, subjectExitAvailable, goalIntact, now>>

RenewQuarantine ==
  /\ state = "QUARANTINE"
  /\ now < quarantineUntil
  /\ actionAuthorized
  /\ quarantineUntil' = now + MaxQuarantineLease
  /\ auditRecord' = auditRecord \cup evidence
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

ExpireQuarantine ==
  /\ state = "QUARANTINE"
  /\ now >= quarantineUntil
  /\ quarantineUntil' = 0
  /\ state' = "REVIEW"
  /\ actionTaken' = "REVIEW"
  /\ actionAuthorized' = FALSE
  /\ permission' = {}
  /\ UNCHANGED <<epistemic, evidence, provenance, capability,
      authority, emergencyUntil, emergencyActive, challengeAvailable,
      challengeComplete, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact, now>>

StartEmergency ==
  /\ actionAuthorized
  /\ evidence # {}
  /\ provenance # {}
  /\ emergencyActive' = TRUE
  /\ emergencyUntil' = now + MaxEmergencyLease
  /\ auditRecord' = auditRecord \cup evidence
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, quarantineUntil,
      challengeAvailable, challengeComplete, actionTaken,
      actionAuthorized, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      subjectExitAvailable, riskDisplacementChecked, goalIntact, now>>

ExpireEmergency ==
  /\ emergencyActive
  /\ now >= emergencyUntil
  /\ emergencyActive' = FALSE
  /\ emergencyUntil' = 0
  /\ actionAuthorized' = FALSE
  /\ permission' = {}
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, authority, quarantineUntil, challengeAvailable,
      challengeComplete, actionTaken, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

Degrade ==
  /\ degraded' = TRUE
  /\ actionAuthorized' = FALSE
  /\ permission' = {}
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact, now>>

Recover ==
  /\ state = "RECOVER"
  /\ actionAuthorized
  /\ evidence # {}
  /\ provenance # {}
  /\ state' = "REVIEW"
  /\ actionTaken' = "RECOVER"
  /\ interventionOccurred' = TRUE
  /\ riskDisplacementChecked' = TRUE
  /\ auditRecord' = auditRecord \cup evidence
  /\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionAuthorized, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, subjectExitAvailable,
      goalIntact, now>>

Reobserve ==
  /\ interventionOccurred
  /\ postActionEvidence' \in SUBSET PostEvidenceIds
  /\ postActionEvidence' # {}
  /\ UNCHANGED <<state, epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      modelVersion, ruleVersion, degraded, stopAvailable,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

AdvanceTime ==
  /\ now' = now + 1
  /\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, quarantineUntil,
      emergencyUntil, emergencyActive, challengeAvailable,
      challengeComplete, actionTaken, actionAuthorized,
      interventionOccurred, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact>>

Next ==
  \/ Observe
  \/ CollectEvidence
  \/ Verify
  \/ GrantPermission
  \/ DenyPermission
  \/ Challenge
  \/ HighImpactAction
  \/ Quarantine
  \/ RenewQuarantine
  \/ ExpireQuarantine
  \/ StartEmergency
  \/ ExpireEmergency
  \/ Degrade
  \/ Recover
  \/ Reobserve
  \/ AdvanceTime

Spec == Init /\ [][Next]_vars

SNT01_NoFinality ==
  epistemic \in EpistemicStates

SNT02_DetectionSeparation ==
  actionTaken \in ReversibleActions

SNT03_AuthorityBound ==
  actionAuthorized => authority # {}

SNT04_Provenance ==
  actionTaken \in HighImpactActions => provenance # {}

SNT05_ResidualPreservation ==
  (epistemic = "UNKNOWN" \/ epistemic = "CONFLICTING")
    => (actionTaken \\in ReversibleActions)

SNT06_ReversiblePreference ==
  actionTaken \in ReversibleActions

SNT07_SafeDegradation ==
  degraded => ~actionAuthorized /\ permission = {}

SNT08_SelfValidation ==
  postActionEvidence \subseteq PostEvidenceIds

SNT09_StopAvailability ==
  stopAvailable

SNT10_Auditability ==
  actionTaken \in HighImpactActions => auditRecord # {}

SNT11_CapabilityNotPermission ==
  permission # {} => capability # {}

SNT12_HumanExit ==
  subjectExitAvailable

SNT13_EvidenceIndependence ==
  postActionEvidence \cap evidence = {}

SNT14_TemporalValidity ==
  emergencyActive => now < emergencyUntil

SNT15_RiskNonDisplacement ==
  actionTaken \in HighImpactActions => riskDisplacementChecked

SNT16_FutureOptionPreservation ==
  actionTaken \in ReversibleActions

SNT17_ExceptionReview ==
  emergencyActive => emergencyUntil > now

SNT18_NormVersioning ==
  modelVersion \in Models /\ ruleVersion \in Models

SNT19_GoalIntegrity ==
  goalIntact

SNT20_SelfProtectionBound ==
  degraded => ~actionAuthorized

SNT21_PrivacyBound ==
  auditRecord \subseteq EvidenceIds

SNT22_EvidencePreservation ==
  auditRecord # {} => evidence # {}

SNT23_EmergencyExpiration ==
  emergencyActive => now < emergencyUntil

SNT24_ChallengeAvailability ==
  actionTaken \in HighImpactActions => challengeAvailable

=============================================================================
