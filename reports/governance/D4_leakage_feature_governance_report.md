# D4 Leakage & Feature Governance Report

## Project

Diabetes Readmission Clinical AI

## D4 Objective

D4 determines which source variables may legitimately participate
in model development at the defined clinical prediction time.

The purpose is to prevent target leakage, temporal leakage,
post-prediction leakage, aggregation leakage, identifier leakage,
proxy leakage, and unsupported assumptions about retrospective
variable availability.

## Prediction Context

**Prediction timestamp:** Before discharge, at the point when the model output would be used to support discharge-planning decisions.

**Prediction horizon:** Readmission occurring within 30 days after discharge.

**Decision:** Identify patients who may warrant enhanced readmission-prevention planning before discharge.

## Leakage Taxonomy

- **TARGET_LEAKAGE:** Variable directly contains, derives from, or reveals the prediction outcome.
- **POST_PREDICTION_LEAKAGE:** Variable is generated or finalized after the defined prediction timestamp.
- **TEMPORAL_LEAKAGE:** Variable uses information from the future relative to the prediction timestamp.
- **AGGREGATION_LEAKAGE:** Variable summarizes information across a period that extends beyond the prediction timestamp.
- **IDENTIFIER_LEAKAGE:** Identifier may enable memorization, linkage, or patient/encounter-specific shortcut learning.
- **PROXY_LEAKAGE:** Variable may indirectly encode the target or a post-prediction event strongly enough to create an invalid predictive shortcut.
- **SEMANTIC_AMBIGUITY:** The dataset does not establish with sufficient certainty when or how the variable became available.

## Governance Results

- Total governed fields: 51
- APPROVED: 8
- CONDITIONAL: 33
- BLOCKED: 6
- IDENTIFIER/GOVERNANCE-ONLY: 2
- TARGET/OUTCOME: 2
- UNASSESSED: 0
- Validation status: PASS

## Approved Source Features

These fields are eligible for governed preprocessing and feature
engineering. Approval does not require that the raw representation
be used directly.

- `race`
- `gender`
- `age`
- `admission_type_id`
- `admission_source_id`
- `number_outpatient`
- `number_emergency`
- `number_inpatient`

## Conditional Source Features

These variables are not authorized for direct model entry.
They require governed transformation, reconstruction, or explicit
prediction-time justification.

- `weight`
- `payer_code`
- `medical_specialty`
- `diag_1`
- `diag_2`
- `diag_3`
- `max_glu_serum`
- `A1Cresult`
- `metformin`
- `repaglinide`
- `nateglinide`
- `chlorpropamide`
- `glimepiride`
- `acetohexamide`
- `glipizide`
- `glyburide`
- `tolbutamide`
- `pioglitazone`
- `rosiglitazone`
- `acarbose`
- `miglitol`
- `troglitazone`
- `tolazamide`
- `examide`
- `citoglipton`
- `insulin`
- `glyburide-metformin`
- `glipizide-metformin`
- `glimepiride-pioglitazone`
- `metformin-rosiglitazone`
- `metformin-pioglitazone`
- `change`
- `diabetesMed`

## Blocked Source Features

These fields are excluded from the primary model because their
final retrospective values are not proven safe at the defined
prediction time.

- `discharge_disposition_id`
- `time_in_hospital`
- `num_lab_procedures`
- `num_procedures`
- `num_medications`
- `number_diagnoses`

## Identifier Governance

`encounter_id` and `patient_nbr` are prohibited as predictive
features.

They remain available only for integrity checking, traceability,
audit, and patient-level data splitting.

## Outcome Governance

`readmitted` is the raw source outcome and `readmitted_30d` is the
formal binary prediction target.

Neither may enter the predictor matrix.

## Primary Safety Decision

No CONDITIONAL or BLOCKED field is authorized for direct primary
model entry at this stage.

Conditional fields may become eligible only after explicit
governed transformation or prediction-time justification.

Blocked fields may become eligible only if a timestamp-safe version
is reconstructed and independently governed.

## Locked-Test Protection

No feature-governance decision has been informed by locked-test
performance.

## D4 Validation

All source/governance fields received exactly one formal
disposition.

No unassessed fields remain.

D4 validation status: **PASS**

## Deployment Status

Clinical deployment is not approved by D4.

D4 authorizes progression to subsequent governed lifecycle stages;
it does not establish clinical effectiveness, calibration,
fairness, robustness, transportability, or deployment readiness.
