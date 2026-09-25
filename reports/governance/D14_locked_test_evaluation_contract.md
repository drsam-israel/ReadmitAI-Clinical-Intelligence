# D14 — Locked-Test Evaluation Governance Contract

## 1. Lifecycle Stage

**Stage:** D14 — Locked-Test Evaluation

**Registered Candidate:** DIABETES_READMISSION_XGB_D13_V1

**Candidate System SHA256:** `9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679`

**Source Git Commit:** `b4118f9`

---

## 2. Evaluation Purpose

D14 performs the one-time confirmatory evaluation of the frozen registered development candidate on the previously locked patient-level TEST partition.

The purpose is to determine whether development-stage evidence generalizes to the internal held-out TEST cohort without TEST-driven model modification.

---

## 3. Frozen Evaluation Boundary

- Evaluation partition: **LOCKED_TEST**
- Evaluation mode: **ONE_TIME_CONFIRMATORY_EVALUATION**
- Frozen operating threshold: **0.12**
- Expected TEST encounters: **15,038**
- Expected TEST patients: **10,568**
- Expected TEST positives: **1,707**
- Expected TEST negatives: **13,331**

The registered model, preprocessing state, feature contract, operating threshold, and candidate identity are frozen.

---

## 4. Confirmatory Evidence Domains

D14 evaluates:

1. Predictive discrimination and calibration.
2. Frozen-threshold operating performance.
3. Validation-to-TEST performance consistency.
4. Pre-specified subgroup operating characteristics.
5. Pre-specified robustness and internal transportability slices.
6. Confirmatory SHAP explainability and source-family attribution.
7. Residual clinical, operational, fairness, and transportability risk.

---

## 5. Prohibited TEST-Driven Activities

The locked TEST partition must not be used to:

- retrain the candidate;
- retune hyperparameters;
- refit preprocessing;
- recalibrate probabilities;
- alter the feature set;
- optimize the operating threshold;
- create subgroup-specific thresholds;
- select a replacement candidate;
- redesign the candidate based on TEST outcomes.

Unfavorable findings are retained as evidence rather than optimized away.

---

## 6. Interpretation Boundary

Successful D14 completion establishes internal locked-test validation evidence only.

It does not establish:

- external transportability;
- prospective clinical effectiveness;
- causal clinical relationships;
- autonomous clinical decision authority;
- production deployment authorization.

---

## 7. Governance Outcome

**Disposition:** CONDITIONAL_PASS_PROGRESS_TO_D15_WITH_DOCUMENTED_RESIDUAL_RISKS

**Next lifecycle stage:** D15_DEPLOYMENT_AND_MONITORING_DESIGN

**Deployment authorized:** False

Material and unresolved residual risks are carried forward to D15 and the final Clinical AI Validation Protocol & Evidence Report.
