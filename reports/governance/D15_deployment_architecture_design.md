
# D15 — Controlled Deployment Architecture Design

## 1. Architecture Purpose

The architecture defines a controlled clinical-AI inference pathway for the
frozen D13 candidate without authorizing production deployment.

## 2. Controlled Architecture Layers

1. {'layer_id': 'D15-ARCH-01', 'layer_name': 'INPUT_CAPTURE', 'purpose': 'Capture the governed source variables required for candidate inference.', 'mutation_of_frozen_candidate': False}
2. {'layer_id': 'D15-ARCH-02', 'layer_name': 'INPUT_VALIDATION', 'purpose': 'Validate schema, required fields, permitted values, missingness, type integrity, and inference eligibility before preprocessing.', 'mutation_of_frozen_candidate': False}
3. {'layer_id': 'D15-ARCH-03', 'layer_name': 'GOVERNED_FEATURE_ENGINEERING', 'purpose': 'Apply the authoritative deterministic D6 feature engineering logic required by the frozen system.', 'mutation_of_frozen_candidate': False}
4. {'layer_id': 'D15-ARCH-04', 'layer_name': 'FROZEN_PREPROCESSING', 'purpose': 'Transform governed source features using the persisted frozen D7 preprocessing artifact and transformed feature schema.', 'mutation_of_frozen_candidate': False}
5. {'layer_id': 'D15-ARCH-05', 'layer_name': 'FROZEN_MODEL_INFERENCE', 'purpose': 'Generate readmission probability using the registered frozen D8 XGBoost model.', 'mutation_of_frozen_candidate': False}
6. {'layer_id': 'D15-ARCH-06', 'layer_name': 'FROZEN_OPERATING_POINT', 'purpose': 'Apply the frozen 0.12 operating threshold without runtime optimization or subgroup-specific threshold adjustment.', 'mutation_of_frozen_candidate': False}
7. {'layer_id': 'D15-ARCH-07', 'layer_name': 'ADVISORY_OUTPUT', 'purpose': 'Present probability and advisory prioritization status to an authorized human reviewer.', 'mutation_of_frozen_candidate': False}
8. {'layer_id': 'D15-ARCH-08', 'layer_name': 'EXPLANATION', 'purpose': 'Provide model interpretation evidence without representing attribution as clinical causality.', 'mutation_of_frozen_candidate': False}
9. {'layer_id': 'D15-ARCH-09', 'layer_name': 'AUDIT_LOGGING', 'purpose': 'Record inference provenance, model identity, threshold identity, validation status, and human-review events.', 'mutation_of_frozen_candidate': False}
10. {'layer_id': 'D15-ARCH-10', 'layer_name': 'MONITORING_TELEMETRY', 'purpose': 'Emit governed telemetry for data quality, model behavior, subgroup behavior, residual risks, workflow adoption, and incidents.', 'mutation_of_frozen_candidate': False}
11. {'layer_id': 'D15-ARCH-11', 'layer_name': 'HUMAN_OVERSIGHT', 'purpose': 'Require qualified human interpretation, override capability, and accountability for downstream clinical action.', 'mutation_of_frozen_candidate': False}
12. {'layer_id': 'D15-ARCH-12', 'layer_name': 'GOVERNANCE_CONTROL', 'purpose': 'Provide escalation, incident management, change control, rollback, and deployment-governance decision mechanisms.', 'mutation_of_frozen_candidate': False}

## 3. Governed Raw Input Contract

The controlled inference boundary accepts exactly eight governed source
features:

- race
- gender
- age
- admission_type_id
- admission_source_id
- number_outpatient
- number_emergency
- number_inpatient

## 4. Feature Transformation Contract

- Raw governed inputs: 8
- Engineered primary features: 10
- Frozen transformed features: 49
- Frozen preprocessing: D7
- Frozen model: D8
- Frozen operating threshold: 0.12

## 5. Output Contract

Output classification:

**CLINICAL_DECISION_SUPPORT_ADVISORY**

Allowed advisory states:

- PRIORITIZE_FOR_HUMAN_REVIEW
- NO_MODEL_PRIORITY_FLAG

The output is advisory and requires human clinical interpretation.

## 6. Safety Boundary

The architecture does not permit autonomous discharge, treatment,
eligibility, or care decisions.

## 7. Deployment Status

Production deployment authorized: **FALSE**
