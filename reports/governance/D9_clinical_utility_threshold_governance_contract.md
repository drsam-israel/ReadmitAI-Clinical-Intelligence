# D9 — Clinical Utility & Threshold Governance Contract

## 1. Lifecycle Stage

**Stage:** D9  
**Stage Name:** Clinical Utility & Threshold Governance

D9 evaluates the clinical and operational consequences of the
frozen D8 development candidate using held-out VALIDATION data.

D9 does not perform final locked-test evaluation and does not
authorize clinical deployment.

## 2. Frozen Upstream Dependencies

**Selected D8 model:** xgboost  
**Frozen model SHA256:** `2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085`  
**Validation encounters:** 15,052  
**Transformed feature count:** 49

D9 consumes the frozen D7 preprocessing representation and
frozen D8 model without refitting either component.

## 3. Data Partition Governance

Threshold development and clinical-utility analysis are
performed on **VALIDATION only**.

The locked TEST partition remains inaccessible during D9.

TEST is reserved for the later authorized locked-test
evaluation stage.

## 4. Intended Clinical Use

The model is intended to support clinician-reviewed
identification of hospitalized patients with diabetes who may
benefit from intensified 30-day readmission-prevention planning
before discharge.

Primary intended users include:

- discharge planning teams;
- care-management teams;
- treating clinicians.

The model is a **risk-prioritization aid**.

It must not autonomously determine discharge, treatment,
admission, denial of care, or other clinical-management
decisions.

## 5. Development Threshold Governance

**Development operating threshold:** 0.12

**Decision classification:**  
`DEVELOPMENT_STAGE_OPERATING_THRESHOLD`

The threshold was derived using the following development-stage
analytical rule:

> Among VALIDATION thresholds satisfying sensitivity >= 0.40 and alerts_per_100_patients <= 35.0, select the threshold with highest sensitivity; break ties by higher precision, then lower alert burden, then higher threshold.

The analytical constraints were:

- minimum sensitivity: 40%;
- maximum alert burden:
  35.0 alerts per
  100 eligible patients.

These constraints are development assumptions. They do not
represent an approved institutional staffing policy or clinical
standard.

## 6. Validation Operating Characteristics

At threshold **0.12**:

- true positives: 785;
- false positives: 3,924;
- true negatives: 9,436;
- false negatives: 907;
- sensitivity: 0.4639;
- specificity: 0.7063;
- precision: 0.1667;
- negative predictive value:
  0.9123;
- F1 score: 0.2453;
- alerts per 100 patients:
  31.28;
- number needed to evaluate:
  6.00.

The model therefore misses
**907 of
1,692**
observed 30-day readmissions at this development operating
point.

This limitation must remain visible in downstream clinical and
governance review.

## 7. Probability Calibration Evidence

Observed VALIDATION prevalence:
**0.1124**

Mean predicted probability:
**0.1137**

Brier score:
**0.0974**

Calibration intercept:
**-0.0044**

Calibration slope:
**1.0045**

The validation calibration assessment shows close alignment
between predicted and observed probabilities within this
development validation cohort.

This does not establish calibration on the locked TEST
partition, external institutions, future populations, or
deployment data.

No recalibration was performed in D9.

## 8. Decision-Curve Evidence

Decision-curve analysis is treated as exploratory
development-stage evidence.

It compares the frozen model against treat-all and treat-none
strategies while preserving the limitations of development-only
validation evidence.

Decision-curve evidence does not independently authorize
clinical deployment.

## 9. Explicit Prohibitions

D9 does not permit:

- model retraining;
- hyperparameter retuning;
- preprocessing refitting;
- locked TEST access;
- autonomous clinical decision-making;
- final clinical-performance claims;
- external-validity claims;
- deployment authorization.

## 10. Downstream Requirements

Before clinical deployment can be considered, the system
requires additional lifecycle evidence including:

- subgroup and fairness evaluation;
- robustness and transportability assessment;
- explainability assessment;
- model and artifact freeze;
- locked-test evaluation;
- deployment and monitoring governance.

D9 therefore establishes a governed **development operating
point**, not a production clinical threshold.
