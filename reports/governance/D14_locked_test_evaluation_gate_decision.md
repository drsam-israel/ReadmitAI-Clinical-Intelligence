# D14 — Locked-Test Evaluation Gate Decision

## Executive Decision

**Gate integrity status:** PASS

**Final disposition:** CONDITIONAL_PASS_PROGRESS_TO_D15_WITH_DOCUMENTED_RESIDUAL_RISKS

**Next lifecycle stage:** D15_DEPLOYMENT_AND_MONITORING_DESIGN

**Deployment authorized:** False

---

## Internal Validation Decision

The registered candidate completed the pre-specified one-time internal locked-TEST evaluation without TEST-driven retraining, threshold retuning, preprocessing refit, recalibration, feature modification, candidate replacement, or redesign.

Internal held-out generalization is supported within the evaluated dataset context.

This decision does **not** establish external validation, clinical effectiveness, or deployment readiness.

---

## Residual Risks

- **D14-RISK-001 — MATERIAL — UTILIZATION_DEPENDENT_MODEL_BEHAVIOR**: Locked TEST robustness evidence confirmed substantial operating-point dependence on prior healthcare-utilization history.
- **D14-RISK-002 — MATERIAL — EXPLAINABILITY_UTILIZATION_DOMINANCE**: Prior-utilization source-feature families accounted for 77.274016% of locked TEST global source-family attribution.
- **D14-RISK-003 — DOCUMENTED — SUBGROUP_OPERATING_HETEROGENEITY**: Locked TEST subgroup analysis demonstrated heterogeneous operating characteristics across age, race, and gender strata, with age showing notable variation.
- **D14-RISK-004 — DOCUMENTED — ADMISSION_CONTEXT_HETEROGENEITY**: Performance varied across admission-source and admission-type strata, including reduced sensitivity in some adequately supported admission-source groups.
- **D14-RISK-005 — MATERIAL — LIMITED_MODEL_DISCRIMINATION**: Locked TEST discrimination remained modest.
- **D14-RISK-006 — UNRESOLVED — EXTERNAL_TRANSPORTABILITY**: D14 used an internal patient-disjoint locked TEST partition from the same underlying dataset.
- **D14-RISK-007 — UNRESOLVED — CLINICAL_EFFECTIVENESS**: D14 evaluated predictive and operating performance but did not test whether model-supported interventions improve patient outcomes.

---

## Governance Interpretation

The candidate may progress to D15 for deployment and monitoring **design** activities.

Progression does not constitute clinical deployment authorization.

The residual risks documented above remain open and must be explicitly represented in monitoring design, external-validation requirements, prospective evaluation planning, clinical workflow controls, and the final Clinical AI Validation Protocol & Evidence Report.
