# D6 Feature Engineering Gate Decision

## Decision

**PASS**

## Gate

D6 — Governed Feature Engineering

## Decision Basis

The D6 feature-engineering implementation was evaluated against
the approved D4 feature-governance contract and frozen D5
patient-level partition assignment.

The evidence confirms:

- 40 governed features are registered;
- 10 features are authorized as D6-CANDIDATE;
- 30 features remain D6-CONDITIONAL;
- candidate and conditional feature sets are disjoint;
- no prohibited raw variables enter the model feature set;
- no identifier or outcome variable enters the model feature set;
- no candidate feature depends on a D4-CONDITIONAL source;
- development data contains train and validation only;
- the locked test partition remains protected;
- the primary modeling matrix contains only the 10 authorized
  D6-CANDIDATE features.

## Downstream Authorization

If the gate decision is PASS, the 10-feature primary candidate
matrix may proceed to:

**D7 — Governed Preprocessing Pipeline**

D7 may fit preprocessing transformations using training data only.

The 30 D6-CONDITIONAL features remain excluded from the primary
modeling pathway unless a separate governance decision explicitly
changes their disposition.

The locked test partition remains unavailable for preprocessing
design, fitting, model selection, calibration, or threshold
selection.

## Final D6 Status

**PASS**
