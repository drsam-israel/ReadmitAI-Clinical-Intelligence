# ============================================================
# D8 — GOVERNED MODEL DEVELOPMENT & SELECTION REPORTING
# ============================================================
#
# Purpose:
#   Generate reproducible governance evidence for the D8
#   Model Development & Selection lifecycle stage.
#
# Evidence generated here documents:
#   - candidate model architecture;
#   - TRAIN-only hyperparameter optimization;
#   - patient-disjoint cross-validation;
#   - held-out VALIDATION discrimination;
#   - governed development-model selection;
#   - persisted-model integrity;
#   - lifecycle boundary controls.
#
# This module does NOT:
#   - access the locked TEST partition;
#   - select a clinical operating threshold;
#   - establish clinical utility;
#   - authorize deployment.
# ============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

import pandas as pd
import yaml


# ============================================================
# D8.33 — REPORTING PATHS
# ============================================================

D8_MANIFEST_PATH = Path(
    "artifacts/manifests/D8_model_development_manifest.yaml"
)

D8_CONTRACT_REPORT_PATH = Path(
    "reports/governance/D8_model_development_contract.md"
)

D8_GATE_REPORT_PATH = Path(
    "reports/governance/D8_model_development_gate_decision.md"
)

D8_CANDIDATE_TABLE_PATH = Path(
    "reports/tables/D8_candidate_model_registry.csv"
)

D8_CV_TABLE_PATH = Path(
    "reports/tables/D8_group_aware_cv_summary.csv"
)

D8_TUNING_TABLE_PATH = Path(
    "reports/tables/D8_hyperparameter_optimization_summary.csv"
)

D8_VALIDATION_TABLE_PATH = Path(
    "reports/tables/D8_validation_model_comparison.csv"
)

D8_SELECTION_TABLE_PATH = Path(
    "reports/tables/D8_model_selection_summary.csv"
)

D8_ARTIFACT_INTEGRITY_TABLE_PATH = Path(
    "reports/tables/D8_model_artifact_integrity.csv"
)


# ============================================================
# D8 — GOVERNED MODEL ROLE DEFINITIONS
# ============================================================

D8_REPORTING_MODEL_ROLES = {
    "dummy_prevalence":
        "NO_SKILL_REFERENCE",

    "logistic_regression":
        "INTERPRETABLE_BASELINE",

    "random_forest":
        "NONLINEAR_CHALLENGER",

    "xgboost":
        "BOOSTED_TREE_CHALLENGER",
}


# ============================================================
# D8.34 — REPORTING DIRECTORY INITIALIZATION
# ============================================================

def ensure_d8_reporting_directories() -> None:
    """
    Create required D8 evidence directories.
    """

    directories = {
        D8_MANIFEST_PATH.parent,
        D8_CONTRACT_REPORT_PATH.parent,
        D8_CANDIDATE_TABLE_PATH.parent,
    }

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# D8.35 — JSON-SAFE VALUE NORMALIZATION
# ============================================================

def _json_safe(
    value: Any,
) -> Any:
    """
    Convert common NumPy/Pandas values into plain Python
    representations suitable for YAML/JSON evidence.
    """

    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, AttributeError):
            pass

    if isinstance(value, dict):
        return {
            str(key): _json_safe(item)
            for key, item in value.items()
        }

    if isinstance(
        value,
        (list, tuple),
    ):
        return [
            _json_safe(item)
            for item in value
        ]

    return value


# ============================================================
# D8.36 — CANDIDATE MODEL REGISTRY TABLE
# ============================================================

def build_d8_candidate_model_registry(
    candidate_factory: dict[str, Any],
) -> pd.DataFrame:
    """
    Build human-readable candidate-model registry evidence.

    The governance role is intentionally distinct from the
    estimator implementation class.

    Example:
        logistic_regression
            governance role = INTERPRETABLE_BASELINE
            estimator class = LogisticRegression
    """

    expected_models = set(
        D8_REPORTING_MODEL_ROLES
    )

    observed_models = set(
        candidate_factory
    )

    if observed_models != expected_models:
        raise RuntimeError(
            "D8 candidate-model factory does not match the "
            "governed reporting model set. "
            f"Expected={sorted(expected_models)}, "
            f"Observed={sorted(observed_models)}"
        )

    records = []

    for model_name, estimator in candidate_factory.items():

        records.append(
            {
                "model_name":
                    model_name,

                "model_role":
                    D8_REPORTING_MODEL_ROLES[
                        model_name
                    ],

                "estimator_class":
                    estimator.__class__.__name__,

                "included_in_hyperparameter_tuning":
                    model_name
                    != "dummy_prevalence",

                "development_stage":
                    "D8",

                "locked_test_access_permitted":
                    False,

                "clinical_threshold_selection_permitted":
                    False,

                "deployment_authorized":
                    False,
            }
        )

    registry = pd.DataFrame(
        records
    )

    if len(registry) != 4:
        raise RuntimeError(
            "D8 candidate-model registry must contain "
            "exactly four governed candidates."
        )

    if not registry[
        "model_name"
    ].is_unique:
        raise RuntimeError(
            "D8 candidate-model registry contains "
            "duplicate model names."
        )

    if not registry[
        "model_role"
    ].is_unique:
        raise RuntimeError(
            "D8 candidate-model registry contains "
            "duplicate governance roles."
        )

    return registry

# ============================================================
# D8.37 — MODEL SELECTION SUMMARY TABLE
# ============================================================

def build_d8_model_selection_summary(
    selection_bundle: dict[str, Any],
) -> pd.DataFrame:
    """
    Convert governed model-selection evidence into a
    one-row reporting table.
    """

    return pd.DataFrame(
        [
            {
                "selected_model":
                    selection_bundle[
                        "selected_model_name"
                    ],

                "selected_model_role":
                    selection_bundle[
                        "selected_model_role"
                    ],

                "selection_metric":
                    selection_bundle[
                        "selection_metric"
                    ],

                "best_train_cv_pr_auc":
                    selection_bundle[
                        "best_train_cv_pr_auc"
                    ],

                "train_pr_auc":
                    selection_bundle[
                        "train_pr_auc"
                    ],

                "validation_pr_auc":
                    selection_bundle[
                        "validation_pr_auc"
                    ],

                "validation_roc_auc":
                    selection_bundle[
                        "validation_roc_auc"
                    ],

                "pr_auc_generalization_gap":
                    selection_bundle[
                        "pr_auc_generalization_gap"
                    ],

                "roc_auc_generalization_gap":
                    selection_bundle[
                        "roc_auc_generalization_gap"
                    ],

                "runner_up_model":
                    selection_bundle[
                        "runner_up_model"
                    ],

                "runner_up_validation_pr_auc":
                    selection_bundle[
                        "runner_up_validation_pr_auc"
                    ],

                "pr_auc_margin_vs_runner_up":
                    selection_bundle[
                        "pr_auc_margin_vs_runner_up"
                    ],

                "development_candidate_only":
                    True,

                "clinical_superiority_claimed":
                    False,

                "clinical_utility_established":
                    False,

                "locked_test_accessed":
                    False,

                "clinical_threshold_selected":
                    False,

                "deployment_authorized":
                    False,
            }
        ]
    )


# ============================================================
# D8.38 — MODEL ARTIFACT INTEGRITY TABLE
# ============================================================

def build_d8_artifact_integrity_table(
    persistence_bundle: dict[str, Any],
) -> pd.DataFrame:
    """
    Build persisted-model integrity evidence.
    """

    return pd.DataFrame(
        [
            {
                "selected_model":
                    persistence_bundle[
                        "selected_model"
                    ],

                "model_artifact_path":
                    persistence_bundle[
                        "model_artifact_path"
                    ],

                "metadata_artifact_path":
                    persistence_bundle[
                        "metadata_artifact_path"
                    ],

                "model_sha256":
                    persistence_bundle[
                        "model_sha256"
                    ],

                "metadata_sha256":
                    persistence_bundle[
                        "metadata_sha256"
                    ],

                "locked_test_accessed":
                    False,

                "clinical_threshold_selected":
                    False,

                "deployment_authorized":
                    False,
            }
        ]
    )

# ============================================================
# D8.39 — HYPERPARAMETER OPTIMIZATION SUMMARY TABLE
# ============================================================

def build_d8_tuning_summary(
    tuning_bundle: dict[str, Any],
) -> pd.DataFrame:
    """
    Build governed TRAIN-only hyperparameter optimization
    evidence from the validated D8 tuning bundle.
    """

    tuning_summary = tuning_bundle[
        "tuning_summary"
    ].copy()

    required_columns = {
        "model_name",
        "search_method",
        "search_iterations",
        "cv_folds",
        "primary_metric",
        "best_cv_pr_auc",
        "best_parameters",
        "fit_partition",
        "external_validation_used_for_tuning",
        "locked_test_accessed",
        "clinical_threshold_selected",
    }

    missing_columns = (
        required_columns
        - set(tuning_summary.columns)
    )

    if missing_columns:
        raise RuntimeError(
            "D8 tuning summary is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    return tuning_summary


# ============================================================
# D8.40 — VALIDATION MODEL-COMPARISON TABLE
# ============================================================

def build_d8_validation_comparison(
    performance_table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build held-out VALIDATION discrimination evidence.
    """

    required_columns = {
        "model_name",
        "model_role",
        "best_train_cv_pr_auc",
        "train_pr_auc",
        "validation_pr_auc",
        "pr_auc_generalization_gap",
        "train_roc_auc",
        "validation_roc_auc",
        "roc_auc_generalization_gap",
        "best_parameters",
        "primary_selection_metric",
        "fit_partition",
        "validation_used_for_fit",
        "locked_test_accessed",
        "clinical_threshold_selected",
    }

    missing_columns = (
        required_columns
        - set(performance_table.columns)
    )

    if missing_columns:
        raise RuntimeError(
            "D8 validation comparison is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    return (
        performance_table
        .sort_values(
            by=[
                "validation_pr_auc",
                "validation_roc_auc",
            ],
            ascending=[
                False,
                False,
            ],
            kind="mergesort",
        )
        .reset_index(drop=True)
        .copy()
    )


# ============================================================
# D8.41 — GROUP-AWARE CV SUMMARY TABLE
# ============================================================

def build_d8_cv_summary(
    cv_bundle: dict[str, Any],
) -> pd.DataFrame:
    """
    Extract patient-disjoint TRAIN cross-validation evidence.
    """

    if "fold_summary" not in cv_bundle:
        raise RuntimeError(
            "D8 CV bundle does not contain fold_summary."
        )

    cv_summary = cv_bundle[
        "fold_summary"
    ].copy()

    if cv_summary.empty:
        raise RuntimeError(
            "D8 CV fold summary is empty."
        )

    return cv_summary

# ============================================================
# D8.42 — WRITE GOVERNANCE CONTRACT
# ============================================================

def write_d8_model_development_contract() -> None:
    """
    Write human-readable D8 lifecycle and governance contract.
    """

    content = """# D8 — Governed Model Development & Selection Contract

## Purpose

D8 develops and selects a development-stage model for prediction
of 30-day hospital readmission in the governed diabetes cohort.

The stage consumes the frozen D7 preprocessing pathway and does
not modify the D1-D7 lifecycle decisions.

## Development Boundary

- Model fitting occurs on TRAIN only.
- Hyperparameter optimization occurs on TRAIN only.
- Cross-validation is patient-disjoint at the model-fitting level.
- VALIDATION is excluded from hyperparameter optimization.
- VALIDATION is used for development-stage model comparison.
- The locked TEST partition is inaccessible during D8.
- No clinical operating threshold is selected during D8.
- No deployment authorization is granted during D8.

## Candidate Architecture

The governed candidate architecture contains:

- DummyClassifier as the no-skill reference.
- Logistic Regression as the interpretable baseline.
- Random Forest as the nonlinear tree challenger.
- XGBoost as the boosted-tree challenger.

The dummy reference is not hyperparameter tuned.

## Primary Selection Metric

The pre-specified primary development-selection metric is
held-out VALIDATION PR-AUC.

VALIDATION ROC-AUC is retained as secondary discrimination
evidence.

Accuracy is not the primary selection criterion because the
30-day readmission outcome is imbalanced.

## Hyperparameter Optimization

Hyperparameter optimization uses five-fold patient-disjoint
StratifiedGroupKFold cross-validation within TRAIN.

The optimization scoring metric is average precision.

VALIDATION and locked TEST do not contribute to tuning.

## Internal CV Preprocessing Interpretation

D8 hyperparameter cross-validation operates on the frozen D7
transformed TRAIN representation.

The D7 preprocessing state was fitted once on the complete TRAIN
partition before D8 model-development cross-validation. The
preprocessing pipeline was not independently re-fitted within
each internal D8 cross-validation fold.

Accordingly, patient grouping prevents patient overlap between
the model-fitting and model-validation portions of each D8 CV
fold, but the internal CV scores are interpreted as
hyperparameter-tuning evidence conditional on the frozen D7
representation.

They are not represented as fully nested, unbiased estimates of
generalization performance.

This limitation does not introduce external VALIDATION or locked
TEST observations into D8 hyperparameter tuning. External
VALIDATION remains the held-out development-stage model
comparison partition, and locked TEST remains untouched.

## Selection Interpretation

Selection identifies a development candidate only.

It does not establish:

- clinical superiority;
- clinical utility;
- an approved clinical operating threshold;
- locked-test generalization;
- deployment readiness.

Those questions are addressed in later lifecycle stages.

## D8 Exit Requirement

D8 may close only when:

1. candidate-model evidence is complete;
2. TRAIN-only tuning evidence is complete;
3. patient-disjoint model-level CV controls pass;
4. the frozen-D7 preprocessing interpretation is explicitly documented;
5. VALIDATION discrimination evidence passes;
6. the development-model selection decision passes;
7. the selected model is persisted and checksum protected;
8. locked TEST remains untouched;
9. no clinical threshold has been selected;
10. deployment remains unauthorized.
"""

    D8_CONTRACT_REPORT_PATH.write_text(
        content,
        encoding="utf-8",
    )

# ============================================================
# D8.43 — WRITE GOVERNANCE GATE DECISION
# ============================================================

def write_d8_gate_decision(
    selection_bundle: dict[str, Any],
    persistence_bundle: dict[str, Any],
) -> None:
    """
    Write the formal D8 exit-gate decision.
    """

    selected_model = selection_bundle[
        "selected_model_name"
    ]

    validation_pr_auc = selection_bundle[
        "validation_pr_auc"
    ]

    validation_roc_auc = selection_bundle[
        "validation_roc_auc"
    ]

    runner_up = selection_bundle[
        "runner_up_model"
    ]

    margin = selection_bundle[
        "pr_auc_margin_vs_runner_up"
    ]

    model_sha256 = persistence_bundle[
        "model_sha256"
    ]

    content = f"""# D8 — Model Development & Selection Gate Decision

## Gate Status

**PASS**

D8 has satisfied the governed requirements for development-stage
model selection.

## Selected Development Candidate

**Model:** {selected_model}

**Held-out VALIDATION PR-AUC:** {validation_pr_auc:.6f}

**Held-out VALIDATION ROC-AUC:** {validation_roc_auc:.6f}

**Runner-up:** {runner_up}

**PR-AUC margin versus runner-up:** {margin:.6f}

The model was selected under the pre-specified primary criterion
of held-out VALIDATION PR-AUC.

The observed margin is retained as quantitative evidence and is
not interpreted as proof of clinical superiority.

## Internal CV Preprocessing Limitation

D8 hyperparameter cross-validation was performed on the frozen
D7 transformed TRAIN representation.

D7 preprocessing was fitted once on the complete TRAIN partition
before D8 cross-validation and was not independently re-fitted
within each internal CV fold.

Patient-level separation was maintained between model-training
and model-validation portions of each D8 CV fold. However,
because preprocessing was not re-estimated independently within
each fold, the internal CV scores are interpreted as
hyperparameter-tuning evidence conditional on the frozen D7
representation rather than as fully nested estimates of
generalization performance.

External VALIDATION was not used for hyperparameter tuning and
the locked TEST partition remained untouched.

Held-out VALIDATION therefore remains the development-stage
comparison evidence, while final locked-test generalization is
reserved for the authorized later lifecycle stage.

## Artifact Integrity

**Selected-model SHA256:**

`{model_sha256}`

The selected estimator is persisted as a development artifact
with checksum-based integrity verification.

## Governance Boundary

At D8 exit:

- development-model selection is complete;
- internal CV preprocessing limitations are explicitly documented;
- clinical superiority is not claimed;
- clinical utility has not yet been established;
- no clinical operating threshold has been selected;
- the locked TEST partition remains untouched;
- deployment is not authorized.

## Authorization

D8 authorizes progression to:

**D9 — Clinical Utility & Threshold Governance**

D8 does not authorize locked-test evaluation or clinical
deployment.
"""

    D8_GATE_REPORT_PATH.write_text(
        content,
        encoding="utf-8",
    )

# ============================================================
# D8.44 — BUILD D8 MANIFEST
# ============================================================

def build_d8_manifest(
    selection_bundle: dict[str, Any],
    persistence_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Build machine-readable D8 governance manifest.

    Internal D8 cross-validation operates on the frozen D7
    transformed TRAIN representation. D7 preprocessing was fitted
    once on the complete TRAIN partition and was not independently
    re-fitted within each D8 CV fold.

    Internal CV scores are therefore interpreted as
    hyperparameter-tuning evidence conditional on the frozen D7
    representation rather than as fully nested estimates of
    generalization performance.

    External VALIDATION remains excluded from hyperparameter
    tuning, and locked TEST remains untouched.
    """

    return {
        "stage":
            "D8",

        "stage_name":
            "Governed Model Development & Selection",

        "gate_status":
            "PASS",

        "selected_development_model":
            selection_bundle[
                "selected_model_name"
            ],

        "selection": {
            "primary_metric":
                selection_bundle[
                    "selection_metric"
                ],

            "validation_pr_auc":
                float(
                    selection_bundle[
                        "validation_pr_auc"
                    ]
                ),

            "validation_roc_auc":
                float(
                    selection_bundle[
                        "validation_roc_auc"
                    ]
                ),

            "runner_up_model":
                selection_bundle[
                    "runner_up_model"
                ],

            "runner_up_validation_pr_auc":
                float(
                    selection_bundle[
                        "runner_up_validation_pr_auc"
                    ]
                ),

            "pr_auc_margin_vs_runner_up":
                float(
                    selection_bundle[
                        "pr_auc_margin_vs_runner_up"
                    ]
                ),
        },

        "selected_parameters":
            _json_safe(
                selection_bundle[
                    "selected_parameters"
                ]
            ),

        "artifact_integrity": {
            "model_artifact_path":
                persistence_bundle[
                    "model_artifact_path"
                ],

            "metadata_artifact_path":
                persistence_bundle[
                    "metadata_artifact_path"
                ],

            "model_sha256":
                persistence_bundle[
                    "model_sha256"
                ],

            "metadata_sha256":
                persistence_bundle[
                    "metadata_sha256"
                ],
        },

        "governance": {
            "fit_partition":
                "train",

            "hyperparameter_tuning_partition":
                "train",

            "patient_disjoint_cv":
                True,

            "validation_used_for_hyperparameter_tuning":
                False,

            "validation_used_for_model_comparison":
                True,

            "development_candidate_only":
                True,

            "clinical_superiority_claimed":
                False,

            "clinical_utility_established":
                False,

            "locked_test_accessed":
                False,

            "clinical_threshold_selected":
                False,

            "deployment_authorized":
                False,
        },

        "cv_preprocessing": {
            "representation":
                "frozen_D7_train_transformation",

            "preprocessing_fitted_on":
                "complete_train_partition",

            "preprocessing_refit_within_cv_fold":
                False,

            "patient_disjoint_model_cv":
                True,

            "interpretation":
                (
                    "hyperparameter_tuning_evidence_conditional_"
                    "on_frozen_D7_representation"
                ),

            "fully_nested_generalization_estimate":
                False,

            "external_validation_used_for_preprocessing_fit":
                False,

            "external_validation_used_for_hyperparameter_tuning":
                False,

            "locked_test_accessed":
                False,
        },

        "authorized_next_stage":
            "D9 — Clinical Utility & Threshold Governance",
    }

# ============================================================
# D8.45 — WRITE D8 MANIFEST
# ============================================================

def write_d8_manifest(
    manifest: dict[str, Any],
) -> None:
    """
    Persist machine-readable D8 manifest.
    """

    with D8_MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as file_handle:

        yaml.safe_dump(
            manifest,
            file_handle,
            sort_keys=False,
            allow_unicode=True,
        )


# ============================================================
# D8.46 — GENERATE COMPLETE D8 EVIDENCE PACKAGE
# ============================================================

def generate_d8_evidence_package(
    *,
    candidate_factory: dict[str, Any],
    cv_bundle: dict[str, Any],
    tuning_bundle: dict[str, Any],
    performance_table: pd.DataFrame,
    selection_bundle: dict[str, Any],
    persistence_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate the complete reproducible D8 governance evidence
    package from already validated D8 runtime objects.
    """

    ensure_d8_reporting_directories()

    candidate_table = (
        build_d8_candidate_model_registry(
            candidate_factory
        )
    )

    cv_table = build_d8_cv_summary(
        cv_bundle
    )

    tuning_table = build_d8_tuning_summary(
        tuning_bundle
    )

    validation_table = (
        build_d8_validation_comparison(
            performance_table
        )
    )

    selection_table = (
        build_d8_model_selection_summary(
            selection_bundle
        )
    )

    artifact_table = (
        build_d8_artifact_integrity_table(
            persistence_bundle
        )
    )

    candidate_table.to_csv(
        D8_CANDIDATE_TABLE_PATH,
        index=False,
    )

    cv_table.to_csv(
        D8_CV_TABLE_PATH,
        index=False,
    )

    tuning_table.to_csv(
        D8_TUNING_TABLE_PATH,
        index=False,
    )

    validation_table.to_csv(
        D8_VALIDATION_TABLE_PATH,
        index=False,
    )

    selection_table.to_csv(
        D8_SELECTION_TABLE_PATH,
        index=False,
    )

    artifact_table.to_csv(
        D8_ARTIFACT_INTEGRITY_TABLE_PATH,
        index=False,
    )

    write_d8_model_development_contract()

    write_d8_gate_decision(
        selection_bundle,
        persistence_bundle,
    )

    manifest = build_d8_manifest(
        selection_bundle,
        persistence_bundle,
    )

    write_d8_manifest(
        manifest
    )

    generated_paths = [
        D8_MANIFEST_PATH,
        D8_CONTRACT_REPORT_PATH,
        D8_GATE_REPORT_PATH,
        D8_CANDIDATE_TABLE_PATH,
        D8_CV_TABLE_PATH,
        D8_TUNING_TABLE_PATH,
        D8_VALIDATION_TABLE_PATH,
        D8_SELECTION_TABLE_PATH,
        D8_ARTIFACT_INTEGRITY_TABLE_PATH,
    ]

    all_artifacts_exist = all(
        path.exists()
        for path in generated_paths
    )

    return {
        "generated_artifact_count":
            len(generated_paths),

        "all_artifacts_exist":
            all_artifacts_exist,

        "generated_artifacts":
            [
                str(path)
                for path in generated_paths
            ],

        "selected_model":
            selection_bundle[
                "selected_model_name"
            ],

        "model_sha256":
            persistence_bundle[
                "model_sha256"
            ],

        "metadata_sha256":
            persistence_bundle[
                "metadata_sha256"
            ],

        "locked_test_accessed":
            False,

        "clinical_threshold_selected":
            False,

        "deployment_authorized":
            False,

        "validation_status":
            (
                "PASS"
                if all_artifacts_exist
                else "FAIL"
            ),
    }