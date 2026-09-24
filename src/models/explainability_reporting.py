
# D12 — EXPLAINABILITY & MODEL INTERPRETATION REPORTING
# ============================================================
# Purpose:
#   Convert validated D12 runtime evidence into deterministic,
#   reviewable governance artifacts without changing the frozen model,
#   preprocessing, D9 threshold, validation boundary, or locked TEST set.
# ============================================================

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Final

from src.models import explainability as d12


# ============================================================
# D12-R.01 — REPORTING IDENTITY & ARTIFACT PATHS
# ============================================================

D12_REPORTING_STAGE: Final[str] = "D12"
D12_REPORTING_NAME: Final[str] = (
    "Explainability & Model Interpretation Evidence Package"
)

D12_MANIFEST_PATH: Final[Path] = Path(
    "artifacts/manifests/D12_explainability_model_interpretation_manifest.yaml"
)

D12_GOVERNANCE_DIR: Final[Path] = Path("reports/governance")
D12_TABLE_DIR: Final[Path] = Path("reports/tables")

D12_CONTRACT_PATH: Final[Path] = (
    D12_GOVERNANCE_DIR
    / "D12_explainability_model_interpretation_contract.md"
)

D12_GATE_PATH: Final[Path] = (
    D12_GOVERNANCE_DIR
    / "D12_explainability_model_interpretation_gate_decision.md"
)

D12_GLOBAL_TRANSFORMED_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_global_transformed_feature_attribution.csv"
)

D12_GLOBAL_SOURCE_FAMILY_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_global_source_family_attribution.csv"
)

D12_DIRECTIONALITY_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_feature_directionality_evidence.csv"
)

D12_LOCAL_CASES_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_local_patient_explanation_cases.csv"
)

D12_LOCAL_CONTRIBUTORS_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_local_patient_explanation_contributors.csv"
)

D12_STABILITY_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_attribution_stability_slice_analysis.csv"
)

D12_CLINICAL_PLAUSIBILITY_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_clinical_plausibility_review.csv"
)

D12_D11_CARRY_FORWARD_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_D11_carry_forward_resolution.csv"
)

D12_LIMITATIONS_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_explainability_limitations_register.csv"
)

D12_INTEGRITY_PATH: Final[Path] = (
    D12_TABLE_DIR
    / "D12_artifact_integrity.csv"
)


# ============================================================
# D12-R.02 — SERIALIZATION HELPERS
# ============================================================

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest().upper()


def _scalar(value: Any) -> Any:
    if isinstance(
        value,
        (list, tuple, dict),
    ):
        return json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=False,
        )

    if value is None:
        return ""

    return value


def _rows_to_csv(
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        path.write_text(
            "status\nNO_ROWS\n",
            encoding="utf-8",
            newline="",
        )
        return

    fieldnames: list[str] = []
    seen: set[str] = set()

    for row in rows:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    key: _scalar(
                        row.get(key)
                    )
                    for key in fieldnames
                }
            )


def _yaml_scalar(value: Any) -> str:
    if isinstance(
        value,
        bool,
    ):
        return (
            "true"
            if value
            else "false"
        )

    if value is None:
        return "null"

    if isinstance(
        value,
        (int, float),
    ):
        return str(value)

    return json.dumps(
        str(value),
        ensure_ascii=False,
    )


def _write_simple_yaml(
    path: Path,
    data: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        f"{key}: {_yaml_scalar(value)}"
        for key, value in data.items()
    ]

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


# ============================================================
# D12-R.03 — VALIDATED EVIDENCE BUNDLE
# ============================================================

def build_d12_reporting_evidence_bundle() -> dict[str, Any]:
    """
    Build the complete validated D12 reporting bundle.

    Reporting is downstream-only. It consumes D12 evidence and must not
    mutate the frozen model, D7 preprocessing, D9 threshold, or TEST set.
    """

    static_boundary = (
        d12.build_d12_static_system_boundary()
    )

    static_validation = (
        d12.validate_d12_static_system_boundary(
            static_boundary
        )
    )

    runtime_boundary = (
        d12.build_d12_frozen_runtime_boundary()
    )

    runtime_validation = (
        d12.validate_d12_frozen_runtime_boundary(
            runtime_boundary
        )
    )

    foundation_validation = (
        d12.validate_d12_explainability_foundation()
    )

    global_attribution = (
        d12.build_d12_global_shap_attribution()
    )

    global_validation = (
        d12.validate_d12_global_shap_attribution(
            global_attribution
        )
    )

    directionality = (
        d12.build_d12_feature_directionality_evidence()
    )

    directionality_validation = (
        d12.validate_d12_feature_directionality_evidence(
            directionality
        )
    )

    local_explanations = (
        d12.build_d12_local_patient_explanation_evidence()
    )

    local_validation = (
        d12.validate_d12_local_patient_explanation_evidence(
            local_explanations
        )
    )

    stability = (
        d12.build_d12_attribution_stability_slice_evidence()
    )

    stability_validation = (
        d12.validate_d12_attribution_stability_slice_evidence(
            stability
        )
    )

    clinical_plausibility = (
        d12.build_d12_clinical_plausibility_review()
    )

    d11_carry_forward = (
        d12.build_d12_d11_carry_forward_resolution_register()
    )

    limitations = (
        d12.build_d12_explainability_limitations_register()
    )

    disposition = (
        d12.build_d12_governance_disposition()
    )

    disposition_validation = (
        d12.validate_d12_governance_disposition(
            disposition
        )
    )

    final_summary = (
        d12.build_d12_final_governance_summary()
    )

    validators = {
        "static_system_boundary":
            static_validation,

        "frozen_runtime_boundary":
            runtime_validation,

        "explainability_foundation":
            foundation_validation,

        "global_attribution":
            global_validation,

        "directionality":
            directionality_validation,

        "local_explanations":
            local_validation,

        "attribution_stability":
            stability_validation,

        "clinical_plausibility":
            clinical_plausibility,

        "d11_carry_forward":
            d11_carry_forward,

        "limitations":
            limitations,

        "governance_disposition":
            disposition_validation,

        "final_governance_summary":
            final_summary,
    }

    failed_validators = [
        name
        for name, result in validators.items()
        if result.get(
            "validation_status"
        ) != "PASS"
    ]

    if failed_validators:
        raise RuntimeError(
            "D12 reporting cannot proceed because validated "
            "runtime evidence failed: "
            f"{failed_validators}"
        )

    immutable_control_results = [
        global_attribution,
        directionality,
        local_explanations,
        stability,
        disposition,
    ]

    if any(
        result.get(
            "model_retrained",
            False,
        )
        for result in immutable_control_results
    ):
        raise RuntimeError(
            "D12 reporting detected model retraining."
        )

    if any(
        result.get(
            "preprocessor_refitted",
            False,
        )
        for result in immutable_control_results
    ):
        raise RuntimeError(
            "D12 reporting detected preprocessing refit."
        )

    if any(
        result.get(
            "threshold_retuned",
            False,
        )
        for result in immutable_control_results
    ):
        raise RuntimeError(
            "D12 reporting detected threshold retuning."
        )

    if any(
        result.get(
            "locked_test_accessed",
            False,
        )
        for result in immutable_control_results
    ):
        raise RuntimeError(
            "D12 reporting detected locked TEST access."
        )

    if any(
        result.get(
            "deployment_authorized",
            False,
        )
        for result in immutable_control_results
    ):
        raise RuntimeError(
            "D12 reporting detected deployment authorization."
        )

    return {
        "static_boundary":
            static_boundary,

        "static_validation":
            static_validation,

        "runtime_boundary":
            runtime_boundary,

        "runtime_validation":
            runtime_validation,

        "foundation_validation":
            foundation_validation,

        "global_attribution":
            global_attribution,

        "global_validation":
            global_validation,

        "directionality":
            directionality,

        "directionality_validation":
            directionality_validation,

        "local_explanations":
            local_explanations,

        "local_validation":
            local_validation,

        "stability":
            stability,

        "stability_validation":
            stability_validation,

        "clinical_plausibility":
            clinical_plausibility,

        "d11_carry_forward":
            d11_carry_forward,

        "limitations":
            limitations,

        "disposition":
            disposition,

        "disposition_validation":
            disposition_validation,

        "final_summary":
            final_summary,

        "validation_status":
            "PASS",
    }


# ============================================================
# D12-R.04 — EVIDENCE TABLE BUILDERS
# ============================================================

def _directionality_rows(
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for (
        source_family,
        feature_evidence,
    ) in evidence[
        "feature_evidence"
    ].items():
        for row in feature_evidence[
            "rows"
        ]:
            item = dict(row)

            item[
                "source_feature_family"
            ] = source_family

            item[
                "analysis_type"
            ] = feature_evidence[
                "analysis_type"
            ]

            rows.append(item)

    return rows


def _local_case_rows(
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for case in evidence[
        "cases"
    ]:
        rows.append(
            {
                "case_type":
                    case[
                        "case_type"
                    ],

                "validation_row_position":
                    case[
                        "validation_row_position"
                    ],

                "true_outcome":
                    case[
                        "true_outcome"
                    ],

                "predicted_class":
                    case[
                        "predicted_class"
                    ],

                "classification_correct":
                    case[
                        "classification_correct"
                    ],

                "development_threshold":
                    case[
                        "development_threshold"
                    ],

                "model_probability":
                    case[
                        "model_probability"
                    ],

                "distance_from_threshold":
                    case[
                        "distance_from_threshold"
                    ],

                "base_value_raw":
                    case[
                        "base_value_raw"
                    ],

                "shap_sum_raw":
                    case[
                        "shap_sum_raw"
                    ],

                "reconstructed_raw_output":
                    case[
                        "reconstructed_raw_output"
                    ],

                "reconstructed_probability":
                    case[
                        "reconstructed_probability"
                    ],

                "probability_reconstruction_error":
                    case[
                        "probability_reconstruction_error"
                    ],

                "raw_source_feature_values":
                    case[
                        "raw_source_feature_values"
                    ],

                "local_explanation_generalizable_to_population":
                    case[
                        "local_explanation_generalizable_to_population"
                    ],

                "feature_attribution_is_causal":
                    case[
                        "feature_attribution_is_causal"
                    ],
            }
        )

    return rows


def _local_contributor_rows(
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for case in evidence[
        "cases"
    ]:
        for (
            direction,
            key,
        ) in (
            (
                "UPWARD",
                "top_upward_contributors",
            ),
            (
                "DOWNWARD",
                "top_downward_contributors",
            ),
        ):
            for rank, contributor in enumerate(
                case[
                    key
                ],
                start=1,
            ):
                rows.append(
                    {
                        "case_type":
                            case[
                                "case_type"
                            ],

                        "validation_row_position":
                            case[
                                "validation_row_position"
                            ],

                        "direction":
                            direction,

                        "rank_within_direction":
                            rank,

                        "transformed_feature":
                            contributor[
                                "transformed_feature"
                            ],

                        "source_feature_family":
                            contributor[
                                "source_feature_family"
                            ],

                        "shap_value":
                            contributor[
                                "shap_value"
                            ],
                    }
                )

    return rows


def _stability_rows(
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in evidence[
        "slice_rows"
    ]:
        rows.append(
            {
                "slice_dimension":
                    row[
                        "slice_dimension"
                    ],

                "slice_value":
                    row[
                        "slice_value"
                    ],

                "support":
                    row[
                        "support"
                    ],

                "support_adequate":
                    row[
                        "support_adequate"
                    ],

                "total_variation_distance":
                    row[
                        "total_variation_distance"
                    ],

                "spearman_rank_correlation":
                    row[
                        "spearman_rank_correlation"
                    ],

                "top_k_jaccard":
                    row[
                        "top_k_jaccard"
                    ],

                "slice_top_source_family":
                    row[
                        "slice_top_source_family"
                    ],

                "slice_top_source_family_share":
                    row[
                        "slice_top_source_family_share"
                    ],

                "largest_share_shift_family":
                    row[
                        "largest_share_shift_family"
                    ],

                "largest_share_shift":
                    row[
                        "largest_share_shift"
                    ],

                "largest_absolute_share_shift":
                    row[
                        "largest_absolute_share_shift"
                    ],

                "bias_or_unfairness_conclusion":
                    row[
                        "bias_or_unfairness_conclusion"
                    ],

                "causal_conclusion":
                    row[
                        "causal_conclusion"
                    ],

                "source_family_profile":
                    row[
                        "profile_rows"
                    ],
            }
        )

    return rows


# ============================================================
# D12-R.05 — GOVERNANCE CONTRACT
# ============================================================

def _contract_markdown(
    bundle: dict[str, Any],
) -> str:
    boundary = bundle[
        "static_boundary"
    ]

    return f"""# D12 — Explainability & Model Interpretation Governance Contract

## Purpose
D12 evaluates whether the frozen development-stage clinical AI candidate can be explained at global, feature, patient, and subgroup or slice levels in a clinically interpretable and governance-defensible manner, and whether those explanations help investigate D11 robustness findings without changing the frozen system.

## Frozen lifecycle boundary
- Source lifecycle stage: {boundary['source_lifecycle_stage']}
- Source Git commit: {boundary['source_git_commit']}
- Selected model: {boundary['model_name']}
- Frozen model SHA-256: {boundary['expected_model_sha256']}
- Frozen D7 preprocessor SHA-256: {boundary['expected_d7_preprocessor_sha256']}
- Frozen D7 schema SHA-256: {boundary['expected_d7_schema_sha256']}
- Frozen development threshold: {boundary['development_threshold']}
- Validation encounters: {boundary['validation_encounters']}
- Validation positives: {boundary['validation_positives']}
- Validation negatives: {boundary['validation_negatives']}
- Transformed feature count: {boundary['transformed_feature_count']}
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
"""


# ============================================================
# D12-R.06 — GATE DECISION
# ============================================================

def _gate_markdown(
    bundle: dict[str, Any],
) -> str:
    summary = bundle[
        "final_summary"
    ]

    global_evidence = bundle[
        "global_attribution"
    ]

    stability = bundle[
        "stability"
    ]

    clinical = bundle[
        "clinical_plausibility"
    ]

    limitations = bundle[
        "limitations"
    ]

    carry_forward = bundle[
        "d11_carry_forward"
    ]

    return f"""# D12 — Explainability & Model Interpretation Gate Decision

## Decision
**{summary['governance_disposition']}**

Progression authorized: **{summary['progression_authorized']}**
Next lifecycle stage: **{summary['next_lifecycle_stage']}**
Deployment authorized: **{summary['deployment_authorized']}**

## Evidence summary
- Validation encounters: {summary['validation_encounters']}
- Transformed features: {summary['transformed_features']}
- Source feature families: {global_evidence['source_feature_family_count']}
- Prior-utilization absolute attribution share: {global_evidence['prior_utilization_absolute_attribution_percent']:.4f}%
- Attribution-stability slices: {stability['slice_count']}
- Adequate-support slices: {stability['adequate_support_slice_count']}
- Low-support slices: {stability['low_support_slice_count']}
- Clinical-plausibility review items: {clinical['review_item_count']}
- D11 carry-forward items accounted for: {carry_forward['resolution_count']}
- Explainability limitations: {limitations['limitation_count']}

## Governance conclusion
The frozen development-stage model is explainable at global, feature, patient, and slice levels with explicit interpretation safeguards and limitations. Prior healthcare utilization is a dominant model signal, and explanation heterogeneity is present in selected utilization, age, admission-source, and representation-related slices.

These findings characterize model behavior. They do not establish causality, clinical appropriateness, fairness, external transportability, prospective effectiveness, safety, or deployment readiness.

## Residual controls
- Clinical appropriateness established: {summary['clinical_appropriateness_established']}
- Fairness established: {summary['fairness_established']}
- Causality established: {summary['causality_established']}
- External validation established: {summary['external_validation_established']}
- D14 locked TEST reassessment required: {summary['locked_test_reassessment_required_in_d14']}
- Locked TEST accessed in D12: {summary['locked_test_accessed']}
- Deployment authorized: {summary['deployment_authorized']}

## Lifecycle disposition
D12 authorizes progression to D13 Model Registry & Artifact Freeze with the documented explainability limitations preserved as governance evidence. The locked TEST set remains reserved for D14.
"""


# ============================================================
# D12-R.07 — MANIFEST
# ============================================================

def _manifest(
    bundle: dict[str, Any],
) -> dict[str, Any]:
    boundary = bundle[
        "static_boundary"
    ]

    global_evidence = bundle[
        "global_attribution"
    ]

    local = bundle[
        "local_explanations"
    ]

    stability = bundle[
        "stability"
    ]

    clinical = bundle[
        "clinical_plausibility"
    ]

    carry_forward = bundle[
        "d11_carry_forward"
    ]

    limitations = bundle[
        "limitations"
    ]

    summary = bundle[
        "final_summary"
    ]

    return {
        "stage":
            "D12",

        "stage_name":
            d12.D12_STAGE_NAME,

        "reporting_package":
            D12_REPORTING_NAME,

        "validation_status":
            "PASS",

        "source_lifecycle_stage":
            boundary[
                "source_lifecycle_stage"
            ],

        "source_git_commit":
            boundary[
                "source_git_commit"
            ],

        "evaluation_partition":
            "validation",

        "selected_model":
            summary[
                "model_name"
            ],

        "model_sha256":
            summary[
                "model_sha256"
            ],

        "d7_preprocessor_sha256":
            boundary[
                "expected_d7_preprocessor_sha256"
            ],

        "d7_schema_sha256":
            boundary[
                "expected_d7_schema_sha256"
            ],

        "development_threshold":
            summary[
                "development_threshold"
            ],

        "validation_encounters":
            summary[
                "validation_encounters"
            ],

        "validation_positives":
            boundary[
                "validation_positives"
            ],

        "validation_negatives":
            boundary[
                "validation_negatives"
            ],

        "transformed_feature_count":
            summary[
                "transformed_features"
            ],

        "source_feature_family_count":
            global_evidence[
                "source_feature_family_count"
            ],

        "prior_utilization_absolute_attribution_percent":
            global_evidence[
                "prior_utilization_absolute_attribution_percent"
            ],

        "local_explanation_case_count":
            local[
                "case_count"
            ],

        "attribution_stability_slice_count":
            stability[
                "slice_count"
            ],

        "adequate_support_slice_count":
            stability[
                "adequate_support_slice_count"
            ],

        "low_support_slice_count":
            stability[
                "low_support_slice_count"
            ],

        "clinical_plausibility_review_item_count":
            clinical[
                "review_item_count"
            ],

        "d11_carry_forward_resolution_count":
            carry_forward[
                "resolution_count"
            ],

        "explainability_limitation_count":
            limitations[
                "limitation_count"
            ],

        "disposition":
            summary[
                "governance_disposition"
            ],

        "progression_authorized":
            summary[
                "progression_authorized"
            ],

        "next_lifecycle_stage":
            summary[
                "next_lifecycle_stage"
            ],

        "clinical_appropriateness_established":
            summary[
                "clinical_appropriateness_established"
            ],

        "fairness_established":
            summary[
                "fairness_established"
            ],

        "causality_established":
            summary[
                "causality_established"
            ],

        "external_validation_established":
            summary[
                "external_validation_established"
            ],

        "d14_locked_test_reassessment_required":
            summary[
                "locked_test_reassessment_required_in_d14"
            ],

        "locked_test_accessed":
            summary[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            summary[
                "deployment_authorized"
            ],
    }


# ============================================================
# D12-R.08 — GENERATE COMPLETE EVIDENCE PACKAGE
# ============================================================

def generate_d12_explainability_reporting_package() -> dict[str, Any]:
    bundle = (
        build_d12_reporting_evidence_bundle()
    )

    D12_GOVERNANCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    D12_TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    D12_MANIFEST_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Core governance documents.
    D12_CONTRACT_PATH.write_text(
        _contract_markdown(
            bundle
        ),
        encoding="utf-8",
    )

    D12_GATE_PATH.write_text(
        _gate_markdown(
            bundle
        ),
        encoding="utf-8",
    )

    # Global attribution evidence.
    _rows_to_csv(
        D12_GLOBAL_TRANSFORMED_PATH,
        list(
            bundle[
                "global_attribution"
            ][
                "transformed_feature_attribution"
            ]
        ),
    )

    _rows_to_csv(
        D12_GLOBAL_SOURCE_FAMILY_PATH,
        list(
            bundle[
                "global_attribution"
            ][
                "source_family_attribution"
            ]
        ),
    )

    # Directionality evidence.
    _rows_to_csv(
        D12_DIRECTIONALITY_PATH,
        _directionality_rows(
            bundle[
                "directionality"
            ]
        ),
    )

    # Local patient explanation evidence.
    _rows_to_csv(
        D12_LOCAL_CASES_PATH,
        _local_case_rows(
            bundle[
                "local_explanations"
            ]
        ),
    )

    _rows_to_csv(
        D12_LOCAL_CONTRIBUTORS_PATH,
        _local_contributor_rows(
            bundle[
                "local_explanations"
            ]
        ),
    )

    # Attribution stability.
    _rows_to_csv(
        D12_STABILITY_PATH,
        _stability_rows(
            bundle[
                "stability"
            ]
        ),
    )

    # Clinical/governance closeout registers.
    _rows_to_csv(
        D12_CLINICAL_PLAUSIBILITY_PATH,
        list(
            bundle[
                "clinical_plausibility"
            ][
                "review_items"
            ]
        ),
    )

    _rows_to_csv(
        D12_D11_CARRY_FORWARD_PATH,
        list(
            bundle[
                "d11_carry_forward"
            ][
                "resolution_rows"
            ]
        ),
    )

    _rows_to_csv(
        D12_LIMITATIONS_PATH,
        list(
            bundle[
                "limitations"
            ][
                "limitations"
            ]
        ),
    )

    # Deterministic manifest.
    _write_simple_yaml(
        D12_MANIFEST_PATH,
        _manifest(
            bundle
        ),
    )

    # Integrity table intentionally excludes itself.
    evidence_paths = [
        D12_MANIFEST_PATH,
        D12_CONTRACT_PATH,
        D12_GATE_PATH,
        D12_GLOBAL_TRANSFORMED_PATH,
        D12_GLOBAL_SOURCE_FAMILY_PATH,
        D12_DIRECTIONALITY_PATH,
        D12_LOCAL_CASES_PATH,
        D12_LOCAL_CONTRIBUTORS_PATH,
        D12_STABILITY_PATH,
        D12_CLINICAL_PLAUSIBILITY_PATH,
        D12_D11_CARRY_FORWARD_PATH,
        D12_LIMITATIONS_PATH,
    ]

    integrity_rows = [
        {
            "artifact":
                str(
                    path
                ).replace(
                    "\\",
                    "/",
                ),

            "exists":
                path.exists(),

            "size_bytes":
                path.stat().st_size,

            "sha256":
                _sha256(
                    path
                ),
        }
        for path in evidence_paths
    ]

    _rows_to_csv(
        D12_INTEGRITY_PATH,
        integrity_rows,
    )

    summary = bundle[
        "final_summary"
    ]

    return {
        "stage":
            "D12",

        "package":
            D12_REPORTING_NAME,

        "artifact_count":
            13,

        "manifest_path":
            str(
                D12_MANIFEST_PATH
            ),

        "contract_path":
            str(
                D12_CONTRACT_PATH
            ),

        "gate_decision_path":
            str(
                D12_GATE_PATH
            ),

        "integrity_path":
            str(
                D12_INTEGRITY_PATH
            ),

        "disposition":
            summary[
                "governance_disposition"
            ],

        "progression_authorized":
            summary[
                "progression_authorized"
            ],

        "next_lifecycle_stage":
            summary[
                "next_lifecycle_stage"
            ],

        "source_feature_family_count":
            bundle[
                "global_attribution"
            ][
                "source_feature_family_count"
            ],

        "local_explanation_case_count":
            bundle[
                "local_explanations"
            ][
                "case_count"
            ],

        "attribution_stability_slice_count":
            bundle[
                "stability"
            ][
                "slice_count"
            ],

        "adequate_support_slice_count":
            bundle[
                "stability"
            ][
                "adequate_support_slice_count"
            ],

        "low_support_slice_count":
            bundle[
                "stability"
            ][
                "low_support_slice_count"
            ],

        "clinical_plausibility_review_item_count":
            bundle[
                "clinical_plausibility"
            ][
                "review_item_count"
            ],

        "d11_carry_forward_resolution_count":
            bundle[
                "d11_carry_forward"
            ][
                "resolution_count"
            ],

        "explainability_limitation_count":
            bundle[
                "limitations"
            ][
                "limitation_count"
            ],

        "locked_test_accessed":
            summary[
                "locked_test_accessed"
            ],

        "deployment_authorized":
            summary[
                "deployment_authorized"
            ],

        "validation_status":
            "PASS",
    }


# ============================================================
# D12-R.09 — VALIDATE GENERATED EVIDENCE PACKAGE
# ============================================================

def validate_d12_explainability_reporting_package() -> dict[str, Any]:
    result = (
        generate_d12_explainability_reporting_package()
    )

    expected_paths = [
        D12_MANIFEST_PATH,
        D12_CONTRACT_PATH,
        D12_GATE_PATH,
        D12_GLOBAL_TRANSFORMED_PATH,
        D12_GLOBAL_SOURCE_FAMILY_PATH,
        D12_DIRECTIONALITY_PATH,
        D12_LOCAL_CASES_PATH,
        D12_LOCAL_CONTRIBUTORS_PATH,
        D12_STABILITY_PATH,
        D12_CLINICAL_PLAUSIBILITY_PATH,
        D12_D11_CARRY_FORWARD_PATH,
        D12_LIMITATIONS_PATH,
        D12_INTEGRITY_PATH,
    ]

    checks = {
        "all_expected_artifacts_exist":
            all(
                path.exists()
                for path in expected_paths
            ),

        "artifact_count_is_13":
            result[
                "artifact_count"
            ] == 13,

        "disposition_matches_d12":
            result[
                "disposition"
            ]
            == d12.D12_GOVERNANCE_DISPOSITION,

        "progression_authorized":
            result[
                "progression_authorized"
            ]
            is True,

        "next_stage_is_d13":
            result[
                "next_lifecycle_stage"
            ]
            == d12.D12_NEXT_LIFECYCLE_STAGE,

        "source_feature_families_are_10":
            result[
                "source_feature_family_count"
            ] == 10,

        "local_explanation_cases_are_5":
            result[
                "local_explanation_case_count"
            ] == 5,

        "stability_slices_are_42":
            result[
                "attribution_stability_slice_count"
            ] == 42,

        "adequate_support_slices_are_34":
            result[
                "adequate_support_slice_count"
            ] == 34,

        "low_support_slices_are_8":
            result[
                "low_support_slice_count"
            ] == 8,

        "clinical_plausibility_items_are_6":
            result[
                "clinical_plausibility_review_item_count"
            ] == 6,

        "d11_carry_forward_items_are_6":
            result[
                "d11_carry_forward_resolution_count"
            ] == 6,

        "limitations_are_8":
            result[
                "explainability_limitation_count"
            ] == 8,

        "locked_test_not_accessed":
            result[
                "locked_test_accessed"
            ]
            is False,

        "deployment_not_authorized":
            result[
                "deployment_authorized"
            ]
            is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **result,

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",
    }


# ============================================================
# D12-R.10 — EXECUTABLE REPORTING CHECK
# ============================================================

def print_d12_explainability_reporting_package() -> None:
    result = (
        validate_d12_explainability_reporting_package()
    )

    print("=" * 72)
    print(
        "D12 EXPLAINABILITY & MODEL INTERPRETATION EVIDENCE PACKAGE"
    )
    print("=" * 72)

    for key in (
        "validation_status",
        "artifact_count",
        "disposition",
        "progression_authorized",
        "next_lifecycle_stage",
        "source_feature_family_count",
        "local_explanation_case_count",
        "attribution_stability_slice_count",
        "adequate_support_slice_count",
        "low_support_slice_count",
        "clinical_plausibility_review_item_count",
        "d11_carry_forward_resolution_count",
        "explainability_limitation_count",
        "locked_test_accessed",
        "deployment_authorized",
        "failed_checks",
    ):
        print(
            f"{key}: {result[key]}"
        )


if __name__ == "__main__":
    print_d12_explainability_reporting_package()
