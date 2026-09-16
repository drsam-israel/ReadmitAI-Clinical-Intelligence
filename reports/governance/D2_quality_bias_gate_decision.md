# D2 — Quality & Bias Gate Decision

## Project

**Diabetes Readmission Clinical AI**

## Gate

**D2 Data Quality & Bias Gate**

## Decision

# CONDITIONAL PASS

The admitted dataset may proceed to **D3 — Cohort & Outcome
Engineering** for controlled research and Clinical AI development.

This decision does not authorize clinical deployment.

## Mandatory Conditions

- Preserve raw-data immutability.
- Resolve or govern open data-quality issues.
- Preserve missingness semantics.
- Use patient-disjoint splitting.
- Perform prediction-time leakage governance.
- Evaluate subgroup model performance and fairness.
- Maintain locked-test controls.
- Require contemporary external validation before clinical deployment.

## Deployment Status

**NOT APPROVED FOR CLINICAL DEPLOYMENT**

## Governance Principle

Progression through the development lifecycle is permitted because
identified limitations can be controlled during subsequent governed
stages. Those limitations must not be silently removed from the risk
record.
