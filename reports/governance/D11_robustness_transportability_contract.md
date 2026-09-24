# D11 — Robustness & Transportability Governance Contract

## Purpose
D11 evaluates the robustness, stability, and development-stage transportability of the frozen clinical AI candidate under pre-specified perturbations and observed validation-population conditions.

## Frozen lifecycle boundary
- Source preprocessing stage: D7
- Source model stage: D8
- Source threshold stage: D9
- Source fairness stage: D10
- Evaluation partition: validation
- Locked TEST evaluation stage: D14
- Selected model: xgboost
- Frozen model SHA-256: 2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085
- Frozen development threshold: 0.12
- Validation encounters: 15052
- Validation positives: 1692
- Validation negatives: 13360

## Governance prohibitions
D11 does not retrain or retune the model, refit preprocessing, retune the D9 threshold, create subgroup-specific thresholds, recalibrate the model, access the locked TEST set, apply automatic mitigation, authorize autonomous clinical decisions, or authorize deployment.

## Interpretation boundary
Synthetic perturbations may be compared directly with the immutable whole-validation baseline because they preserve the same evaluation population. Observed slices characterize population heterogeneity and support limitations; whole-cohort differences must not be labelled automatic model degradation, causal effects, or external transportability failure.

Absence of degradation under simulated stress does not establish external, temporal, geographic, institutional, prospective, or deployment validity.

## Lifecycle rule
D11 may authorize progression to D12 Explainability only when the validated governance disposition permits progression. Progression is not deployment authorization.
