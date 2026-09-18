# D8 — Governed Model Development & Selection Contract

## Purpose

D8 develops and selects a development-stage model for prediction
of 30-day hospital readmission in the governed diabetes cohort.

The stage consumes the frozen D7 preprocessing pathway and does
not modify the D1-D7 lifecycle decisions.

## Development Boundary

- Model fitting occurs on TRAIN only.
- Hyperparameter optimization occurs on TRAIN only.
- Cross-validation is patient-disjoint at the model-fitting level.
- VALIDATION is excluded from hyperparameter optimization.
- VALIDATION is used for development-stage model comparison.
- The locked TEST partition is inaccessible during D8.
- No clinical operating threshold is selected during D8.
- No deployment authorization is granted during D8.

## Candidate Architecture

The governed candidate architecture contains:

- DummyClassifier as the no-skill reference.
- Logistic Regression as the interpretable baseline.
- Random Forest as the nonlinear tree challenger.
- XGBoost as the boosted-tree challenger.

The dummy reference is not hyperparameter tuned.

## Primary Selection Metric

The pre-specified primary development-selection metric is
held-out VALIDATION PR-AUC.

VALIDATION ROC-AUC is retained as secondary discrimination
evidence.

Accuracy is not the primary selection criterion because the
30-day readmission outcome is imbalanced.

## Hyperparameter Optimization

Hyperparameter optimization uses five-fold patient-disjoint
StratifiedGroupKFold cross-validation within TRAIN.

The optimization scoring metric is average precision.

VALIDATION and locked TEST do not contribute to tuning.

## Internal CV Preprocessing Interpretation

D8 hyperparameter cross-validation operates on the frozen D7
transformed TRAIN representation.

The D7 preprocessing state was fitted once on the complete TRAIN
partition before D8 model-development cross-validation. The
preprocessing pipeline was not independently re-fitted within
each internal D8 cross-validation fold.

Accordingly, patient grouping prevents patient overlap between
the model-fitting and model-validation portions of each D8 CV
fold, but the internal CV scores are interpreted as
hyperparameter-tuning evidence conditional on the frozen D7
representation.

They are not represented as fully nested, unbiased estimates of
generalization performance.

This limitation does not introduce external VALIDATION or locked
TEST observations into D8 hyperparameter tuning. External
VALIDATION remains the held-out development-stage model
comparison partition, and locked TEST remains untouched.

## Selection Interpretation

Selection identifies a development candidate only.

It does not establish:

- clinical superiority;
- clinical utility;
- an approved clinical operating threshold;
- locked-test generalization;
- deployment readiness.

Those questions are addressed in later lifecycle stages.

## D8 Exit Requirement

D8 may close only when:

1. candidate-model evidence is complete;
2. TRAIN-only tuning evidence is complete;
3. patient-disjoint model-level CV controls pass;
4. the frozen-D7 preprocessing interpretation is explicitly documented;
5. VALIDATION discrimination evidence passes;
6. the development-model selection decision passes;
7. the selected model is persisted and checksum protected;
8. locked TEST remains untouched;
9. no clinical threshold has been selected;
10. deployment remains unauthorized.
