# D11 — Robustness & Transportability Gate Decision

## Decision
**CONDITIONAL_PASS_PROGRESS_WITH_DOCUMENTED_ROBUSTNESS_FINDINGS**

Progression authorized: **True**  
Next lifecycle stage: **D12 — Explainability**  
Deployment authorized: **False**

## Evidence summary
- Synthetic perturbation assessments: 2
- Synthetic degradation-review triggers: 0
- Observed-slice assessments: 35
- Adequate-support heterogeneity findings: 6
- Low-support interpretation limitations: 12
- Mandatory carry-forward actions: 6

## Interpretation
D11 development-stage robustness evaluation is complete and may progress to D12 Explainability with documented carry-forward findings. This conditional pass is not deployment authorization and does not establish external, temporal, geographic, institutional, or prospective transportability.

The six adequate-support observed-slice findings are governance review signals, not automatic model failures. The twelve low-support rows remain explicit evidence limitations. Direct causal interpretation and direct observed-slice degradation claims are prohibited.

## Frozen-system assurance
No model retraining, hyperparameter retuning, preprocessing refit, threshold retuning, recalibration, locked-TEST access, external-validation claim, or deployment authorization occurred in D11.

## Required carry-forward actions
1. D12: investigate the contribution of prior-utilization features to the observed operating-point heterogeneity without changing the frozen D9 threshold.
2. D12: examine feature-attribution behavior for admission_source_id and age while avoiding causal interpretation of attribution values.
3. D12: document whether the observed utilization pattern is consistent with model feature dependence, population case-mix differences, or both; do not infer causality from D11 alone.
4. Governance evidence: retain all 12 low-support observed slices as interpretation limitations rather than treating unstable small-sample metrics as strong evidence.
5. D14: reassess discrimination, calibration, operating-point behavior, and relevant subgroup/slice findings once on the locked TEST partition without validation-driven threshold retuning.
6. Deployment governance: do not authorize clinical deployment from D11 evidence; external, temporal, institutional/geographic, and prospective validation remain unestablished.
