# D7 — Governed Preprocessing Contract

## Purpose

D7 converts the frozen D6 primary candidate feature set into a
reproducible model-ready representation while preserving leakage,
partition, feature-authorization, and locked-test controls.

## Prediction Point

Before discharge, at the point when model output would support discharge-planning decisions.

## Authorized Raw Model Inputs

Exactly 10 D6-CANDIDATE features are
authorized for the primary modeling pathway:

- race
- gender
- age
- admission_type_id
- admission_source_id
- prior_outpatient_use
- prior_emergency_use
- prior_inpatient_use
- prior_utilization_intensity
- prior_utilization_domain_count

## Categorical Pathway

Categorical features:

- race
- gender
- age
- admission_type_id
- admission_source_id

Controls:

- Explicit source-specific unknown markers are normalized to
  `__MISSING_OR_UNKNOWN__`.
- Unknown demographic membership is preserved rather than inferred.
- Native missing values are handled using the governed categorical
  imputation policy.
- Imputation state is learned from TRAIN only.
- One-hot vocabulary is learned from TRAIN only.
- Genuinely unseen later categories are handled without refitting.

## Numeric Pathway

Numeric features:

- prior_outpatient_use
- prior_emergency_use
- prior_inpatient_use
- prior_utilization_intensity
- prior_utilization_domain_count

Controls:

- Median imputation is fitted on TRAIN only.
- No D7 scaling is applied.
- Model-specific scaling, if justified, must be governed downstream.

## Development Boundary

- TRAIN: FIT + TRANSFORM
- VALIDATION: TRANSFORM ONLY
- LOCKED TEST: NOT ACCESSED

Validation must never contribute to fitted preprocessing state.

## Prohibited D7 Activities

D7 does not:

- redesign D6 feature authorization;
- promote D6-CONDITIONAL features;
- use identifiers or outcomes as model inputs;
- train predictive models;
- tune hyperparameters;
- select operating thresholds;
- access the locked test partition;
- authorize clinical deployment.

## Persistence & Reproducibility

The fitted preprocessing transformer and authoritative transformed
schema are persisted locally as runtime artifacts.

Their SHA-256 checksums and learned-state evidence are recorded in
the D7 manifest and evidence tables.

A persisted transformer must reproduce the original TRAIN and
VALIDATION transformations exactly before D7 may pass.

## Governance Principle

Unknown sensitive demographic values must remain explicitly unknown.
They must not be silently reassigned to an observed demographic
group through modal imputation.

