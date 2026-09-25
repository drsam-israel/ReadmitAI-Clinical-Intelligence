# D13 Model Registry & Artifact Freeze — Gate Decision

## Decision

**PASS_PROGRESS_TO_D14_LOCKED_TEST_EVALUATION**

## Evidence

- Validation status: `PASS`
- Registry ID: `DIABETES_READMISSION_XGB_D13_V1`
- Candidate system SHA-256: `9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679`
- Freeze manifest SHA-256: `0F278573E2C4D139E6D0968DD624AB7C1304825D3B805B6FEF288162051B6119`
- Progression to D14 authorized: `True`
- Locked TEST accessed: `False`
- Locked TEST evaluated: `False`
- Deployment authorized: `False`
- Failed checks: `[]`

## Governance Interpretation

The exact D12 development-stage candidate has been registered and frozen with
cryptographic identity, feature-contract binding, software provenance,
artifact inventory, lifecycle provenance, and explicit change control.

This decision authorizes one-way progression to D14 for locked TEST
evaluation under the frozen candidate identity. It does not authorize model
retraining, threshold retuning, validation-driven changes, or deployment.
