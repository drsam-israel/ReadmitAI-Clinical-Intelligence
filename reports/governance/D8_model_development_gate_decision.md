# D8 — Model Development & Selection Gate Decision

## Gate Status

**PASS**

D8 has satisfied the governed requirements for development-stage
model selection.

## Selected Development Candidate

**Model:** xgboost

**Held-out VALIDATION PR-AUC:** 0.184874

**Held-out VALIDATION ROC-AUC:** 0.620365

**Runner-up:** logistic_regression

**PR-AUC margin versus runner-up:** 0.002610

The model was selected under the pre-specified primary criterion
of held-out VALIDATION PR-AUC.

The observed margin is retained as quantitative evidence and is
not interpreted as proof of clinical superiority.

## Internal CV Preprocessing Limitation

D8 hyperparameter cross-validation was performed on the frozen
D7 transformed TRAIN representation.

D7 preprocessing was fitted once on the complete TRAIN partition
before D8 cross-validation and was not independently re-fitted
within each internal CV fold.

Patient-level separation was maintained between model-training
and model-validation portions of each D8 CV fold. However,
because preprocessing was not re-estimated independently within
each fold, the internal CV scores are interpreted as
hyperparameter-tuning evidence conditional on the frozen D7
representation rather than as fully nested estimates of
generalization performance.

External VALIDATION was not used for hyperparameter tuning and
the locked TEST partition remained untouched.

Held-out VALIDATION therefore remains the development-stage
comparison evidence, while final locked-test generalization is
reserved for the authorized later lifecycle stage.

## Artifact Integrity

**Selected-model SHA256:**

`2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085`

The selected estimator is persisted as a development artifact
with checksum-based integrity verification.

## Governance Boundary

At D8 exit:

- development-model selection is complete;
- internal CV preprocessing limitations are explicitly documented;
- clinical superiority is not claimed;
- clinical utility has not yet been established;
- no clinical operating threshold has been selected;
- the locked TEST partition remains untouched;
- deployment is not authorized.

## Authorization

D8 authorizes progression to:

**D9 — Clinical Utility & Threshold Governance**

D8 does not authorize locked-test evaluation or clinical
deployment.
