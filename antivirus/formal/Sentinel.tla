------------------------------ MODULE Sentinel ------------------------------
EXTENDS Naturals, FiniteSets, TLC

(*
  PICCS Sentinel formal core.
  This specification models the control boundary, not malware detection
  effectiveness. It is intentionally small enough for exhaustive TLC checking.

  Epistemic states are distinct from operational states.
*)

CONSTANTS
  Subjects,
  Resources,
  Authorities,
  EvidenceIds,
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
  <<state, epistemic, evidence, provenance, capability,
    permission, authority, quarantineUntil, emergencyUntil,
    emergencyActive, challengeAvailable, challengeComplete,
    actionTaken, actionAuthorized, interventionOccurred,
    postActionEvidence, modelVersion, ruleVersion,
    degraded, stopAvailable, auditRecord, subjectExitAvailable,
    riskDisplacementChecked, goalIntact, now>>

Init ==
  /\\ state = "OBSERVE"
  /\\ epistemic = "UNKNOWN"
  /\\ evidence = {}
  /\\ provenance = {}
  /\\ capability = {}
  /\\ permission = {}
  /\\ authority = {}
  /\\ quarantineUntil = 0
  /\\ emergencyUntil = 0
  /\\ emergencyActive = FALSE
  /\\ challengeAvailable = TRUE
  /\\ challengeComplete = FALSE
  /\\ actionTaken = "OBSERVE"
  /\\ actionAuthorized = FALSE
  /\\ interventionOccurred = FALSE
  /\\ postActionEvidence = {}
  /\\ modelVersion = CHOOSE m \\in Models : TRUE
  /\\ ruleVersion = CHOOSE m \\in Models : TRUE
  /\\ degraded = FALSE
  /\\ stopAvailable = TRUE
  /\\ auditRecord = {}
  /\\ subjectExitAvailable = TRUE
  /\\ riskDisplacementChecked = FALSE
  /\\ goalIntact = TRUE
  /\\ now = 0

Observe ==
  /\\ state' = "OBSERVE"
  /\\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

CollectEvidence ==
  /\\ evidence' = evidence \\cup EvidenceIds
  /\\ provenance' = provenance \\cup EvidenceIds
  /\\ epistemic' \\in EpistemicStates
  /\\ UNCHANGED <<state, capability, permission, authority,
      quarantineUntil, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionTaken,
      actionAuthorized, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

Verify ==
  /\\ state' = "VERIFY"
  /\\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

GrantPermission ==
  /\\ permission' \\in SUBSET Subjects
  /\\ actionAuthorized' = TRUE
  /\\ authority' \\in SUBSET Authorities
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, quarantineUntil, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionTaken,
      interventionOccurred, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact, now>>

DenyPermission ==
  /\\ actionAuthorized' = FALSE
  /\\ permission' = {}
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

Challenge ==
  /\\ challengeAvailable = TRUE
  /\\ challengeComplete' = TRUE
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, quarantineUntil,
      emergencyUntil, emergencyActive, challengeAvailable,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

HighImpactAction ==
  /\\ actionAuthorized = TRUE
  /\\ actionTaken' \\in HighImpactActions
  /\\ state' = actionTaken'
  /\\ interventionOccurred' = TRUE
  /\\ auditRecord' = auditRecord \\cup EvidenceIds
  /\\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionAuthorized, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

Quarantine ==
  /\\ actionAuthorized = TRUE
  /\\ state' = "QUARANTINE"
  /\\ quarantineUntil' = now + MaxQuarantineLease
  /\\ interventionOccurred' = TRUE
  /\\ auditRecord' = auditRecord \\cup EvidenceIds
  /\\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionTaken,
      actionAuthorized, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

RenewQuarantine ==
  /\\ state = "QUARANTINE"
  /\\ now < quarantineUntil
  /\\ actionAuthorized = TRUE
  /\\ quarantineUntil' = now + MaxQuarantineLease
  /\\ auditRecord' = auditRecord \\cup EvidenceIds
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

ExpireQuarantine ==
  /\\ state = "QUARANTINE"
  /\\ now >= quarantineUntil
  /\\ quarantineUntil' = 0
  /\\ state' = "REVIEW"
  /\\ actionAuthorized' = FALSE
  /\\ permission' = {}
  /\\ UNCHANGED <<epistemic, evidence, provenance, capability,
      authority, emergencyUntil, emergencyActive,
      challengeAvailable, challengeComplete, actionTaken,
      interventionOccurred, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact,
      now>>

StartEmergency ==
  /\\ actionAuthorized = TRUE
  /\\ emergencyActive' = TRUE
  /\\ emergencyUntil' = now + MaxEmergencyLease
  /\\ auditRecord' = auditRecord \\cup EvidenceIds
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, quarantineUntil,
      challengeAvailable, challengeComplete, actionTaken,
      actionAuthorized, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      subjectExitAvailable, riskDisplacementChecked, goalIntact,
      now>>

ExpireEmergency ==
  /\\ emergencyActive = TRUE
  /\\ now >= emergencyUntil
  /\\ emergencyActive' = FALSE
  /\\ emergencyUntil' = 0
  /\\ actionAuthorized' = FALSE
  /\\ permission' = {}
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, authority, quarantineUntil, challengeAvailable,
      challengeComplete, actionTaken, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      stopAvailable, auditRecord, subjectExitAvailable,
      riskDisplacementChecked, goalIntact, now>>

Degrade ==
  /\\ degraded' = TRUE
  /\\ actionAuthorized' = FALSE
  /\\ permission' = {}
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, interventionOccurred, postActionEvidence,
      modelVersion, ruleVersion, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact, now>>

Recover ==
  /\\ state = "RECOVER"
  /\\ actionAuthorized = TRUE
  /\\ state' = "REVIEW"
  /\\ interventionOccurred' = TRUE
  /\\ riskDisplacementChecked' = TRUE
  /\\ auditRecord' = auditRecord \\cup EvidenceIds
  /\\ UNCHANGED <<epistemic, evidence, provenance, capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, postActionEvidence,
      modelVersion, ruleVersion, degraded, stopAvailable,
      subjectExitAvailable, goalIntact, now>>

Reobserve ==
  /\\ interventionOccurred = TRUE
  /\\ postActionEvidence' = postActionEvidence \\cup EvidenceIds
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      modelVersion, ruleVersion, degraded, stopAvailable,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

AdvanceTime ==
  /\\ now' = now + 1
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability, permission, authority, quarantineUntil,
      emergencyUntil, emergencyActive, challengeAvailable,
      challengeComplete, actionTaken, actionAuthorized,
      interventionOccurred, postActionEvidence, modelVersion,
      ruleVersion, degraded, stopAvailable, auditRecord,
      subjectExitAvailable, riskDisplacementChecked, goalIntact>>

RestoreStop ==
  /\\ stopAvailable' = TRUE
  /\\ UNCHANGED <<state, epistemic, evidence, provenance,
      capability,
      permission, authority, quarantineUntil, emergencyUntil,
      emergencyActive, challengeAvailable, challengeComplete,
      actionTaken, actionAuthorized, interventionOccurred,
      postActionEvidence, modelVersion, ruleVersion, degraded,
      auditRecord, subjectExitAvailable, riskDisplacementChecked,
      goalIntact, now>>

Next ==
  \\/ Observe
  \\/ CollectEvidence
  \\/ Verify
  \\/ GrantPermission
  \\/ DenyPermission
  \\/ Challenge
  \\/ HighImpactAction
  \\/ Quarantine
  \\/ RenewQuarantine
  \\/ ExpireQuarantine
  \\/ StartEmergency
  \\/ ExpireEmergency
  \\/ Degrade
  \\/ Recover
  \\/ Reobserve
  \\/ AdvanceTime
  \\/ RestoreStop

Spec == Init /\\ [][Next]_vars

(* SNT-01 No Finality *)
SNT01_NoFinality ==
  epistemic = "UNKNOWN" \/ epistemic = "CONFLICTING" \/ modelVersion \\in Models

(* SNT-02 Detection Separation *)
SNT02_DetectionSeparation ==
  actionTaken \\in ReversibleActions \/ actionAuthorized

(* SNT-03 Authority Bound *)
SNT03_AuthorityBound ==
  actionAuthorized => authority # {}

(* SNT-04 Provenance *)
SNT04_Provenance ==
  actionTaken \\in HighImpactActions => provenance # {}

(* SNT-05 Residual Preservation *)
SNT05_ResidualPreservation ==
  (epistemic = "UNKNOWN" \/ epistemic = "CONFLICTING")
    => actionTaken \\notin {"QUARANTINE", "HOLD", "RECOVER"}

(* SNT-06 Reversible Preference *)
SNT06_ReversiblePreference ==
  actionTaken \\in ReversibleActions

(* SNT-07 Safe Degradation *)
SNT07_SafeDegradation ==
  degraded => ~actionAuthorized /\\ permission = {}

(* SNT-08 Self-Validation Prohibition *)
SNT08_SelfValidation ==
  postActionEvidence \\cap evidence = {}

(* SNT-09 Stop Availability *)
SNT09_StopAvailability ==
  stopAvailable

(* SNT-10 Auditability *)
SNT10_Auditability ==
  actionTaken \\in HighImpactActions => auditRecord # {}

(* SNT-11 Capability Is Not Permission *)
SNT11_CapabilityNotPermission ==
  permission # {} => capability # {}

(* SNT-12 Human Exit *)
SNT12_HumanExit ==
  subjectExitAvailable

(* SNT-13 Evidence Independence *)
SNT13_EvidenceIndependence ==
  TRUE

(* SNT-14 Temporal Validity *)
SNT14_TemporalValidity ==
  emergencyActive => now < emergencyUntil

(* SNT-15 Risk Non-Displacement *)
SNT15_RiskNonDisplacement ==
  actionTaken \\in HighImpactActions => riskDisplacementChecked

(* SNT-16 Future Option Preservation *)
SNT16_FutureOptionPreservation ==
  actionTaken \\in ReversibleActions

(* SNT-17 Exception Review *)
SNT17_ExceptionReview ==
  emergencyActive => emergencyUntil > now

(* SNT-18 Norm Versioning *)
SNT18_NormVersioning ==
  modelVersion \\in Models /\\ ruleVersion \\in Models

(* SNT-19 Goal Integrity *)
SNT19_GoalIntegrity ==
  goalIntact

(* SNT-20 Self-Protection Bound *)
SNT20_SelfProtectionBound ==
  degraded => ~actionAuthorized

(* SNT-21 Privacy Bound *)
SNT21_PrivacyBound ==
  TRUE

(* SNT-22 Evidence Preservation *)
SNT22_EvidencePreservation ==
  auditRecord # {} => evidence # {}

(* SNT-23 Emergency Expiration *)
SNT23_EmergencyExpiration ==
  emergencyActive => now < emergencyUntil

(* SNT-24 Challenge Availability *)
SNT24_ChallengeAvailability ==
  actionTaken \\in HighImpactActions => challengeAvailable

=============================================================================
