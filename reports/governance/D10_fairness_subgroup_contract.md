# D10 — Fairness & Subgroup Evaluation Governance Contract

## Purpose
D10 evaluates development-validation subgroup performance, uncertainty, calibration, representation, error burden, and operational burden for the frozen D8 development model operating at the frozen D9 threshold.

## Governed boundary
- **Model:** xgboost
- **Model SHA256:** `2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085`
- **Evaluation partition:** VALIDATION
- **Frozen development threshold:** 0.12
- **Primary subgroup variables:** race, gender, age
- **Locked TEST evaluation:** reserved for D14

## Analytical support policy
A subgroup is classified as analytically adequate only when it has at least 100 encounters, 20 positive outcomes, and 20 negative outcomes. Low-support groups remain visible in evidence but are not used as the sole basis for primary disparity extrema or governance conclusions. These minima are analytical stability rules, not fairness, clinical, or regulatory thresholds.

## Fairness interpretation contract
D10 does **not** treat numerical subgroup differences as proof of unlawful discrimination, causal bias, or clinical inequity. Differences may reflect sample size, prevalence, data quality, measurement, clinical pathways, or model behavior. PR-AUC is interpreted with subgroup prevalence. Unknown/not-recorded race remains visible as a data-quality category and is not treated as an observed demographic group for primary disparity comparisons.

## Calibration contract
Subgroup calibration uses 5 within-subgroup equal-frequency quantile bins (`within_subgroup_equal_frequency_quantile_bins`). Calibration analysis is diagnostic only. D10 does not recalibrate the model and does not establish external probability calibration.

## Prohibited actions in D10
D10 does not permit model retraining, hyperparameter retuning, preprocessor refitting, threshold retuning, subgroup-specific thresholds, automatic fairness mitigation, autonomous clinical decision-making, locked TEST access, or deployment authorization.

## Sensitive-attribute disclosure
Race, gender, and age are both D10 subgroup evaluation variables and source features in the frozen primary model pathway. Their inclusion therefore requires explicit lifecycle governance, subgroup monitoring, data-quality review, and later locked-test assessment. D10 does not infer that inclusion is either acceptable or unacceptable solely from the present validation evidence.

## Required downstream handling
All D10 governance findings must be carried forward into D11 robustness/transportability analysis and subsequently into D14 locked-test evaluation and deployment-readiness governance. No D10 finding may be silently resolved by changing the global threshold for a subgroup.
