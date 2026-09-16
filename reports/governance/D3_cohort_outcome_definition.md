# D3 — Governed Cohort & Outcome Definition

## Lifecycle stage

D3 — Cohort & Outcome Engineering

## Purpose

Define the eligible modeling population and formal binary
30-day readmission outcome before patient-level splitting,
feature engineering, preprocessing, or model development.

## Source population

- Source encounters: 101,766
- Source unique patients: 71,518
- Source target: `readmitted`

## Governed eligibility rule

The primary modeling cohort excludes encounters whose discharge
disposition indicates death or expiration.

Expired disposition IDs:

[11, 19, 20, 21]

Hospice disposition IDs are retained in the primary cohort:

[13, 14]

Hospice is not treated as equivalent to death. Hospice-related
sensitivity analysis is reserved for the later robustness and
transportability stage.

## Cohort flow

- Source encounters: 101,766
- Excluded encounters: 1,652
- Excluded percentage: 1.6233%
- Governed encounters: 100,114
- Governed unique patients: 70,439
- Hospice encounters retained: 771
- Positive outcomes among excluded encounters: 0

## Formal outcome definition

Derived target:

`readmitted_30d`

Deterministic mapping:

- `<30` → 1
- `>30` → 0
- `NO` → 0

The original `readmitted` field is preserved for
auditability.

## Governed outcome distribution

- Negative encounters: 88,757
- Positive encounters: 11,357
- Positive prevalence: 11.3441%

## Governance controls

- Raw source dataset remains immutable.
- Cohort construction does not mutate the source dataframe.
- Death/expired exclusions are applied before model splitting.
- Hospice encounters remain in the primary cohort.
- Encounter identifiers remain unique.
- Patient identifiers remain complete.
- The formal target contains no missing values.
- The formal target is strictly binary.
- Source target semantics are preserved.
- Outcome mapping is deterministic and validated.
- Patient and encounter identifiers are retained only for
  governance and later split construction; they are not approved
  modeling features.
- Locked-test evaluation has not occurred.

## Persisted cohort artifact

Path:

`data/interim/D3_governed_modeling_cohort.parquet`

SHA-256:

`584861DC8CB2ABD0582D024C02335126D64D541A54C91B88CDA9E55336D983B1`

## D3 validation result

**PASS**

The governed cohort and formal outcome are approved to proceed
to downstream leakage and feature governance. This approval does
not constitute approval for clinical deployment.
