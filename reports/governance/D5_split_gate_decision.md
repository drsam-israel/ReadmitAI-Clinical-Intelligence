# D5 Governed Patient-Level Split Gate Decision

## Gate

**PASS**

## Source Cohort

- Encounters: 100,114
- Unique patients: 70,439

## Partition Results

- **train:** 70,024 encounters; 49,306 patients; 7,958 positive encounters; 11.3647% readmission rate
- **validation:** 15,052 encounters; 10,565 patients; 1,692 positive encounters; 11.2410% readmission rate
- **test:** 15,038 encounters; 10,568 patients; 1,707 positive encounters; 11.3512% readmission rate

## Patient Leakage Audit

- Multi-split patients: 0
- Train-validation overlap: 0
- Train-test overlap: 0
- Validation-test overlap: 0

## Reproducibility

Same governed cohort + same algorithm + seed `42`
reproduces the same patient assignment:

**True**

## Gate Basis

D5 may close only when:

- every source patient receives one split assignment;
- every source encounter is preserved;
- all three required partitions exist;
- patient overlap is zero;
- no split assignment is missing;
- patient assignments are unique;
- deterministic regeneration succeeds;
- the patient assignment is persisted as a governed artifact.

## Decision

D5 lifecycle gate: **PASS**

The train and validation partitions may proceed to downstream
development stages subject to existing D4 feature-governance
controls.

The test partition remains **LOCKED**.

## Clinical Deployment

**NOT APPROVED**

Successful data splitting does not establish model performance or
clinical deployment readiness.
