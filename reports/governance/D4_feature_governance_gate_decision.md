# D4 Feature Governance Gate Decision

## Gate

**PASS**

## Basis

The D4 leakage and feature-governance process has:

- established the clinical decision point;
- established the prediction-time contract;
- inventoried all 51 fields;
- classified every field under a formal governance disposition;
- prohibited identifiers from model input;
- prohibited source and engineered outcomes from model input;
- blocked retrospective/end-of-encounter fields that are not
  proven prediction-time safe;
- prevented conditional variables from direct model entry;
- preserved locked-test independence.

## Disposition Summary

- APPROVED: 8
- CONDITIONAL: 33
- BLOCKED: 6
- IDENTIFIER/GOVERNANCE-ONLY: 2
- TARGET/OUTCOME: 2
- UNASSESSED: 0

## Decision

D4 may close with a **PASS** provided the generated evidence
package and automated tests remain valid.

Progression to D5 is authorized only under the D4 feature-governance
contract.

## Mandatory Downstream Controls

1. Patient-level disjoint splitting must be enforced.
2. Identifiers must not enter model predictors.
3. Source or engineered outcomes must not enter model predictors.
4. CONDITIONAL features must not enter the primary model without
   explicit governed transformation or approval.
5. BLOCKED features must remain excluded unless timestamp-safe
   reconstruction is separately governed.
6. Locked-test data must remain isolated from feature engineering,
   preprocessing, model selection, threshold selection, and
   calibration decisions.
7. Feature lineage must remain traceable through subsequent
   lifecycle stages.

## Clinical Deployment

**NOT APPROVED**

A D4 PASS is a feature-governance lifecycle decision, not evidence
of clinical deployment readiness.
