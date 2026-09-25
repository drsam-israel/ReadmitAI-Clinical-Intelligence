# D13 Model Registry & Artifact Freeze — Governance Contract

## 1. Purpose

D13 creates the traceable, integrity-verifiable registry record for the exact
development-stage clinical-AI candidate that completed D12. D13 does not
evaluate model performance and does not authorize clinical deployment.

## 2. Registered Candidate

- Registry ID: `DIABETES_READMISSION_XGB_D13_V1`
- Model version: `1.0.0`
- Candidate status: `FROZEN_DEVELOPMENT_CANDIDATE_PENDING_D14_LOCKED_TEST`
- Source lifecycle stage: `D12`
- Source Git commit: `4e995f2`
- Model: `xgboost`
- Development operating threshold: `0.12`

## 3. Frozen Predictive-System Identity

- Candidate system SHA-256: `9349A52C715517666540C0D5B1EDB148D48709C0FC2CC77BE9B53F10FE373679`
- Model SHA-256: `2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085`
- Model metadata SHA-256: `5838A6C77F05BB183F90B9AA4B0ED9F0AE5B0FBF2E3E1B1326A79A3A67A1AC76`
- D7 preprocessor SHA-256: `076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC`
- Transformed schema SHA-256: `69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED`
- Source feature contract SHA-256: `277CCC7C847B2FE6882A4072EA991B1FEF701D0222471B8B1F583DE06924C0BC`
- Source feature count: `10`
- Transformed feature count: `49`

## 4. Reproducibility Provenance

- Software environment SHA-256: `D008029639FF03569910412173B84B557C3694A12B24ED8198E06F38616A6E7E`
- Freeze manifest SHA-256: `0F278573E2C4D139E6D0968DD624AB7C1304825D3B805B6FEF288162051B6119`

The software-environment fingerprint is maintained as reproducibility
provenance and is not used to redefine the frozen predictive-system
fingerprint.

## 5. Change-Control Rule

Any post-freeze change to the model, model metadata, preprocessing artifact,
transformed schema, ordered source-feature contract, or development operating
threshold invalidates the registered candidate identity and requires governed
change control and a new registry identity/version as appropriate.

## 6. D13 Safety Boundary

D13 performs registry and integrity work only. It does not retrain or retune
the model, refit preprocessing, re-engineer features, recalibrate
probabilities, create subgroup-specific thresholds, generate evaluation
predictions, access or evaluate the locked TEST partition, or authorize
deployment.

## 7. Progression Rule

A PASS at D13 authorizes progression only to D14 Locked-Test Evaluation.
It is not deployment authorization.

- Locked TEST accessed in D13: **False**
- Locked TEST evaluated in D13: **False**
- Deployment authorized: **False**
