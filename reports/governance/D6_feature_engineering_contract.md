# D6 Feature Engineering Contract

## Project

Diabetes Readmission Clinical AI

## Lifecycle Stage

D6 — Governed Feature Engineering

## Prediction Point

Before discharge, at the point when model output would support
discharge-planning decisions.

## Outcome

`readmitted_30d` — 30-day hospital readmission.

## Development Boundary

Only the frozen D5 `train` and `validation`
partitions are permitted during D6.

The `test` partition remains locked.

Development encounters: **85,076**

## Frozen D5 Dependency

Authoritative patient split SHA-256:

`D575A296909467EB4CDE7529978D5306C38BFE26959A4EBEA907CE209472977E`

D6 does not generate a new patient split.

## Feature Engineering Boundary

D6 performs deterministic feature construction only.

D6 does not:

- fit imputers;
- fit encoders;
- perform scaling;
- train models;
- tune hyperparameters;
- calibrate models;
- select decision thresholds;
- evaluate the locked test partition.

## Primary Candidate Features

The primary downstream modeling pathway is authorized to consume
only the following 10
D6-CANDIDATE features:

- `race`
- `gender`
- `age`
- `admission_type_id`
- `admission_source_id`
- `prior_outpatient_use`
- `prior_emergency_use`
- `prior_inpatient_use`
- `prior_utilization_intensity`
- `prior_utilization_domain_count`

## Conditional Features

The following 30
features are retained for governed analysis but are not authorized
for primary model entry unless their D4 prediction-time uncertainty
is formally resolved:

- `diag_1_domain`
- `diag_2_domain`
- `diag_3_domain`
- `any_diabetes_diagnosis`
- `any_circulatory_diagnosis`
- `any_respiratory_diagnosis`
- `any_genitourinary_diagnosis`
- `any_injury_poisoning_diagnosis`
- `distinct_diagnosis_domain_count`
- `a1c_result_category`
- `max_glucose_result_category`
- `a1c_tested`
- `max_glucose_tested`
- `any_glycemic_test_recorded`
- `a1c_abnormal`
- `a1c_markedly_elevated`
- `max_glucose_abnormal`
- `max_glucose_markedly_elevated`
- `any_glycemic_abnormality`
- `any_marked_glycemic_abnormality`
- `glycemic_abnormality_count`
- `diabetes_medication_intensity`
- `any_diabetes_medication_exposure`
- `insulin_exposure`
- `metformin_exposure`
- `any_directional_medication_change`
- `directional_medication_change_count`
- `diabetes_medication_prescribed`
- `diabetes_medication_changed`
- `diabetes_treatment_structure`

## Leakage Controls

Identifiers are governance-only.

Outcome variables are target-only.

D4 hard-blocked retrospective encounter variables are prohibited
from model entry.

A D6-CANDIDATE feature cannot depend on a D4-CONDITIONAL source.

## Validation

Registered features: **40**

Candidate features: **10**

Conditional features: **30**

Candidate/conditional overlap:
**0**

Prohibited model features:
**0**

Candidate features with conditional lineage:
**0**

D6 validation status:

**PASS**
