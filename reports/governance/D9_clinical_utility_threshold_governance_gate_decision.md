# D9 — Clinical Utility & Threshold Governance Gate Decision

## Gate Status

# PASS — AUTHORIZED TO PROCEED TO D10

D9 has produced sufficient development-stage evidence to
proceed to **D10 — Fairness & Subgroup Evaluation**.

This PASS is a lifecycle progression decision only.

It is **not** authorization for clinical deployment.

## Evidence Supporting the Gate

The frozen D8 `xgboost` development
candidate was evaluated on held-out VALIDATION without model
retraining, hyperparameter retuning, or preprocessing refitting.

The governed development operating threshold is:

**0.12**

At this operating point:

- sensitivity:
  **46.39%**
- specificity:
  **70.63%**
- precision:
  **16.67%**
- negative predictive value:
  **91.23%**
- alerts per 100 patients:
  **31.28**
- true positives:
  **785**
- false positives:
  **3,924**
- false negatives:
  **907**

## Clinical Utility Evidence

At the selected development operating point:

- model net benefit:
  **0.016603**
- treat-all net benefit:
  **-0.008625**
- treat-none net benefit:
  **0.000000**
- incremental net benefit versus best default:
  **0.016603**

Within this VALIDATION analysis, the model exceeded both
default strategies under the decision-curve assumptions.

This remains exploratory development evidence.

## Calibration Evidence

- observed prevalence:
  **0.1124**
- mean predicted probability:
  **0.1137**
- Brier score:
  **0.0974**
- calibration intercept:
  **-0.0044**
- calibration slope:
  **1.0045**

Calibration is closely aligned on this held-out development
VALIDATION cohort.

No claim is made regarding calibration on TEST, external
institutions, or future populations.

## Material Clinical Limitation

At threshold **0.12**, the model
misses **907** observed 30-day
readmissions.

Sensitivity is therefore only
**46.39%**.

The model must be framed as a **risk-prioritization aid**, not a
high-sensitivity screening system.

This limitation must remain explicit in D10-D15 evidence and in
any future portfolio or deployment documentation.

## Governance Conditions Carried Forward

The following remain prohibited:

- locked TEST access before the authorized lifecycle stage;
- autonomous clinical decision-making;
- deployment;
- institutional clinical-use claims;
- external-validity claims;
- threshold representation as an approved hospital policy.

## Gate Decision

**D9 PASS**

Authorized next lifecycle stage:

**D10 — Fairness & Subgroup Evaluation**

Clinical deployment authorization:

**NO**
