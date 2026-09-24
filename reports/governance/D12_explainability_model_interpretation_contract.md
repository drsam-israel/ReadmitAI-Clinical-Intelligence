# D12 — Explainability & Model Interpretation Governance Contract

## Purpose
D12 evaluates whether the frozen development-stage clinical AI candidate can be explained at global, feature, patient, and subgroup or slice levels in a clinically interpretable and governance-defensible manner, and whether those explanations help investigate D11 robustness findings without changing the frozen system.

## Frozen lifecycle boundary
- Source lifecycle stage: D11
- Source Git commit: 9fb775c
- Selected model: xgboost
- Frozen model SHA-256: 2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085
- Frozen D7 preprocessor SHA-256: 076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC
- Frozen D7 schema SHA-256: 69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED
- Frozen development threshold: 0.12
- Validation encounters: 15052
- Validation positives: 1692
- Validation negatives: 13360
- Transformed feature count: 49
- Explainability partition: validation
- Locked TEST evaluation stage: D14

## Governed explainability methods
D12 uses SHAP TreeExplainer for the frozen XGBoost candidate. SHAP values are interpreted in raw XGBoost margin/log-odds space and are linked back to model probability through the logistic expit function. SHAP values are not interpreted as direct probability-point changes.

Evidence is generated at:
1. transformed-feature global attribution level;
2. source-feature-family global attribution level;
3. observed feature-value directionality/dependence level;
4. representative local patient prediction level; and
5. observed validation-slice attribution-stability level.

## Governance prohibitions
D12 does not retrain or retune the model, refit preprocessing, reengineer or reselect features, retune the D9 threshold, recalibrate probabilities, create subgroup-specific thresholds, access the locked TEST set, automatically mitigate the model, authorize autonomous clinical decisions, or authorize deployment.

## Interpretation safeguards
Feature attribution is not causal inference. High importance does not establish clinical appropriateness, and low importance does not establish clinical irrelevance. SHAP describes model behavior rather than biological mechanism. Local explanations are not generalized to the whole population. Global explanations do not replace patient-level clinical review. Subgroup attribution differences may reflect case mix, representation, documentation, or data-generation processes.

Explainability does not establish external transportability, prospective effectiveness, fairness, safety, or deployment readiness.

## Lifecycle rule
D12 may authorize progression to D13 Model Registry & Artifact Freeze only when the validated D12 governance disposition permits progression. D12 progression is not deployment authorization.
