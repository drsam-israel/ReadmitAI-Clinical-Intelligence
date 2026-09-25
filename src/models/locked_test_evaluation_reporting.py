# ============================================================
# D14 — LOCKED-TEST EVALUATION REPORTING & EVIDENCE
# ============================================================
#
# Purpose:
# Persist the authoritative D14 locked-test evaluation evidence
# into auditable lifecycle artifacts.
#
# Reporting architecture:
#
#   authoritative D14 runtime evidence
#           ↓
#   reporting bundle
#           ↓
#   reporting validation
#           ↓
#   persisted tables / governance documents / manifest
#
# This module does not:
#   - retrain the model,
#   - refit preprocessing,
#   - retune the threshold,
#   - recalibrate the model,
#   - modify the candidate,
#   - authorize deployment.
# ============================================================


from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.models.locked_test_evaluation import (
    D14_STAGE_ID,
    D14_STAGE_NAME,
    D14_SOURCE_GIT_COMMIT,
    D14_EVALUATION_PARTITION,
    D14_EVALUATION_MODE,
    D14_EXPECTED_REGISTRY_ID,
    D14_EXPECTED_CANDIDATE_SYSTEM_SHA256,
    D14_EXPECTED_DEVELOPMENT_THRESHOLD,
    D14_EXPECTED_TEST_ENCOUNTERS,
    D14_EXPECTED_TEST_PATIENTS,
    D14_EXPECTED_TEST_POSITIVES,
    D14_EXPECTED_TEST_NEGATIVES,
    D14_FINAL_DISPOSITION,
    D14_FINAL_NEXT_STAGE,
    build_d14_confirmatory_performance_evidence,
    build_d14_subgroup_confirmation_evidence,
    build_d14_robustness_confirmation_evidence,
    build_d14_explainability_confirmation_evidence,
    build_d14_residual_risk_register,
    evaluate_d14_integrated_governance_gate,
    validate_d14_integrated_governance_disposition,
)


# ============================================================
# D14.R01 — REPORTING PATHS
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[2]

D14_MANIFEST_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "manifests"
    / "D14_locked_test_evaluation_manifest.yaml"
)

D14_GOVERNANCE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "governance"
)

D14_TABLE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "tables"
)

D14_CONTRACT_PATH = (
    D14_GOVERNANCE_DIR
    / "D14_locked_test_evaluation_contract.md"
)

D14_GATE_DECISION_PATH = (
    D14_GOVERNANCE_DIR
    / "D14_locked_test_evaluation_gate_decision.md"
)

D14_FINAL_GOVERNANCE_RECORD_PATH = (
    D14_GOVERNANCE_DIR
    / "D14_final_governance_record.json"
)

D14_PERFORMANCE_TABLE_PATH = (
    D14_TABLE_DIR
    / "D14_locked_test_performance.csv"
)

D14_VALIDATION_TEST_COMPARISON_PATH = (
    D14_TABLE_DIR
    / "D14_validation_test_comparison.csv"
)

D14_SUBGROUP_TABLE_PATH = (
    D14_TABLE_DIR
    / "D14_locked_test_subgroup_evidence.csv"
)

D14_ROBUSTNESS_TABLE_PATH = (
    D14_TABLE_DIR
    / "D14_locked_test_robustness_evidence.csv"
)

D14_EXPLAINABILITY_TABLE_PATH = (
    D14_TABLE_DIR
    / "D14_locked_test_explainability_attribution.csv"
)

D14_LOCAL_EXPLANATION_TABLE_PATH = (
    D14_TABLE_DIR
    / "D14_locked_test_local_explanations.csv"
)

D14_RESIDUAL_RISK_TABLE_PATH = (
    D14_TABLE_DIR
    / "D14_residual_risk_register.csv"
)


# ============================================================
# D14.R02 — HASHING / SERIALIZATION UTILITIES
# ============================================================


def _sha256_file(
    path: Path,
) -> str:
    """
    Calculate SHA256 for a persisted evidence artifact.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest().upper()


def _json_safe(
    value: Any,
) -> Any:
    """
    Convert common NumPy / pandas values into JSON-safe values.
    """

    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        ),
    ) or value is None:
        return value

    if hasattr(
        value,
        "item",
    ):
        try:
            return value.item()
        except (ValueError, TypeError):
            pass

    if isinstance(
        value,
        dict,
    ):
        return {
            str(key): _json_safe(item)
            for key, item in value.items()
        }

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        return [
            _json_safe(item)
            for item in value
        ]

    return str(value)


# ============================================================
# D14.R03 — BUILD AUTHORITATIVE REPORTING BUNDLE
# ============================================================


def build_d14_reporting_bundle(
) -> dict[str, Any]:
    """
    Build the authoritative D14 reporting bundle.

    Each expensive analytical evidence builder is executed only
    once within this reporting run.
    """

    performance = (
        build_d14_confirmatory_performance_evidence()
    )

    subgroup = (
        build_d14_subgroup_confirmation_evidence()
    )

    robustness = (
        build_d14_robustness_confirmation_evidence()
    )

    explainability = (
        build_d14_explainability_confirmation_evidence()
    )

    residual_risks = (
        build_d14_residual_risk_register()
    )

    integrated_evidence = {
        "registry_id": (
            D14_EXPECTED_REGISTRY_ID
        ),

        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "evaluation_partition": (
            D14_EVALUATION_PARTITION
        ),

        "evaluation_mode": (
            D14_EVALUATION_MODE
        ),

        "performance_evidence": performance,

        "subgroup_evidence": subgroup,

        "robustness_evidence": robustness,

        "explainability_evidence": explainability,

        "residual_risks": residual_risks,

        "residual_risk_count": (
            len(residual_risks)
        ),

        "unresolved_residual_risk_count": (
            sum(
                not risk["resolved"]
                for risk in residual_risks
            )
        ),

        "external_validation_completed": False,

        "clinical_effectiveness_established": False,

        "deployment_authorized": False,
    }

    gate = (
        evaluate_d14_integrated_governance_gate(
            integrated_evidence
        )
    )

    disposition_validation = (
        validate_d14_integrated_governance_disposition(
            gate
        )
    )

    final_record = {
        "stage_id": D14_STAGE_ID,
        "stage_name": D14_STAGE_NAME,

        "registry_id": (
            D14_EXPECTED_REGISTRY_ID
        ),

        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "source_git_commit": (
            D14_SOURCE_GIT_COMMIT
        ),

        "evaluation_partition": (
            D14_EVALUATION_PARTITION
        ),

        "evaluation_mode": (
            D14_EVALUATION_MODE
        ),

        "internal_validation_classification": (
            gate[
                "internal_validation_classification"
            ]
        ),

        "external_validation_status": (
            gate[
                "external_validation_status"
            ]
        ),

        "clinical_effectiveness_status": (
            gate[
                "clinical_effectiveness_status"
            ]
        ),

        "deployment_status": (
            gate[
                "deployment_status"
            ]
        ),

        "residual_risk_count": (
            len(residual_risks)
        ),

        "unresolved_residual_risk_count": (
            sum(
                not risk["resolved"]
                for risk in residual_risks
            )
        ),

        "residual_risks": residual_risks,

        "gate_integrity_status": (
            gate[
                "gate_integrity_status"
            ]
        ),

        "gate_checks": (
            gate[
                "checks"
            ]
        ),

        "disposition": (
            gate[
                "disposition"
            ]
        ),

        "next_lifecycle_stage": (
            gate[
                "next_lifecycle_stage"
            ]
        ),

        "model_retrained_using_test": False,
        "threshold_retuned_using_test": False,
        "preprocessor_refitted_using_test": False,
        "feature_set_changed_using_test": False,
        "recalibration_performed_using_test": False,
        "subgroup_thresholds_created_using_test": False,
        "test_driven_candidate_selection": False,
        "test_driven_redesign": False,

        "external_validation_completed": False,
        "clinical_effectiveness_established": False,
        "deployment_authorized": False,

        "validation": (
            disposition_validation
        ),
    }

    return {
        "performance": performance,
        "subgroup": subgroup,
        "robustness": robustness,
        "explainability": explainability,
        "residual_risks": residual_risks,
        "integrated_evidence": (
            integrated_evidence
        ),
        "gate": gate,
        "final_record": final_record,
    }


# ============================================================
# D14.R04 — PERFORMANCE TABLE
# ============================================================


def build_d14_performance_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Build one-row locked TEST performance evidence table.
    """

    result = (
        bundle[
            "performance"
        ]["test_result"]
    )

    fields = (
        "encounter_count",
        "positive_count",
        "negative_count",
        "prevalence",
        "pr_auc",
        "roc_auc",
        "brier_score",
        "log_loss",
        "true_positives",
        "false_positives",
        "true_negatives",
        "false_negatives",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "f1_score",
        "alert_count",
        "alert_rate",
        "alerts_per_100_encounters",
        "number_needed_to_evaluate",
    )

    row = {
        "registry_id": (
            D14_EXPECTED_REGISTRY_ID
        ),

        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "frozen_threshold": (
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),
    }

    for field in fields:
        row[field] = result[field]

    return [row]


# ============================================================
# D14.R05 — VALIDATION VS TEST COMPARISON TABLE
# ============================================================


def build_d14_validation_test_comparison_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Convert the authoritative validation-to-TEST comparison
    into a flat reporting table.
    """

    comparison = (
        bundle[
            "performance"
        ]["validation_test_comparison"]
    )

    metrics = comparison[
        "metrics"
    ]

    rows: list[dict[str, Any]] = []

    for metric_name, metric_values in (
        metrics.items()
    ):
        row = {
            "metric": metric_name,
        }

        if isinstance(
            metric_values,
            dict,
        ):
            row.update(
                _json_safe(
                    metric_values
                )
            )
        else:
            row[
                "comparison_value"
            ] = _json_safe(
                metric_values
            )

        rows.append(
            row
        )

    return rows


# ============================================================
# D14.R06 — SUBGROUP TABLE
# ============================================================


def build_d14_subgroup_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Persist authoritative locked TEST subgroup evidence.
    """

    table = (
        bundle[
            "subgroup"
        ]["subgroup_table"]
    )

    if isinstance(
        table,
        pd.DataFrame,
    ):
        return (
            table
            .to_dict(
                orient="records"
            )
        )

    return list(
        table
    )


# ============================================================
# D14.R07 — ROBUSTNESS TABLE
# ============================================================


def build_d14_robustness_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Persist authoritative locked TEST robustness evidence.
    """

    table = (
        bundle[
            "robustness"
        ]["robustness_table"]
    )

    if isinstance(
        table,
        pd.DataFrame,
    ):
        return (
            table
            .to_dict(
                orient="records"
            )
        )

    return list(
        table
    )


# ============================================================
# D14.R08 — EXPLAINABILITY TABLES
# ============================================================


def build_d14_explainability_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Persist global source-family locked TEST attribution.
    """

    table = (
        bundle[
            "explainability"
        ][
            "family_evidence"
        ][
            "global_attribution_table"
        ]
    )

    if isinstance(
        table,
        pd.DataFrame,
    ):
        return (
            table
            .to_dict(
                orient="records"
            )
        )

    return list(
        table
    )


def build_d14_local_explanation_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Flatten the five deterministic local explanation cases.
    """

    cases = (
        bundle[
            "explainability"
        ][
            "local_evidence"
        ][
            "cases"
        ]
    )

    rows: list[dict[str, Any]] = []

    for case in cases:
        rows.append(
            {
                "case_type": (
                    case[
                        "case_type"
                    ]
                ),

                "test_row_position": (
                    case[
                        "test_row_position"
                    ]
                ),

                "true_outcome": (
                    case[
                        "true_outcome"
                    ]
                ),

                "predicted_class": (
                    case[
                        "predicted_class"
                    ]
                ),

                "model_probability": (
                    case[
                        "model_probability"
                    ]
                ),

                "distance_from_threshold": (
                    case[
                        "distance_from_threshold"
                    ]
                ),

                "reconstructed_probability": (
                    case[
                        "reconstructed_probability"
                    ]
                ),

                "probability_reconstruction_error": (
                    case[
                        "probability_reconstruction_error"
                    ]
                ),

                "top_contributors_json": (
                    json.dumps(
                        _json_safe(
                            case[
                                "top_contributors"
                            ]
                        ),
                        sort_keys=True,
                    )
                ),

                "feature_attribution_is_causal": (
                    case[
                        "feature_attribution_is_causal"
                    ]
                ),
            }
        )

    return rows


# ============================================================
# D14.R09 — RESIDUAL-RISK REGISTER
# ============================================================


def build_d14_residual_risk_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Build persisted D14 residual-risk register.
    """

    return [
        _json_safe(
            risk
        )
        for risk in bundle[
            "residual_risks"
        ]
    ]


# ============================================================
# D14.R10 — GOVERNANCE CONTRACT
# ============================================================


def build_d14_evaluation_contract_markdown(
    bundle: dict[str, Any],
) -> str:
    """
    Build the formal D14 locked-test evaluation contract.
    """

    return f"""# D14 — Locked-Test Evaluation Governance Contract

## 1. Lifecycle Stage

**Stage:** {D14_STAGE_ID} — {D14_STAGE_NAME}

**Registered Candidate:** {D14_EXPECTED_REGISTRY_ID}

**Candidate System SHA256:** `{D14_EXPECTED_CANDIDATE_SYSTEM_SHA256}`

**Source Git Commit:** `{D14_SOURCE_GIT_COMMIT}`

---

## 2. Evaluation Purpose

D14 performs the one-time confirmatory evaluation of the frozen registered development candidate on the previously locked patient-level TEST partition.

The purpose is to determine whether development-stage evidence generalizes to the internal held-out TEST cohort without TEST-driven model modification.

---

## 3. Frozen Evaluation Boundary

- Evaluation partition: **{D14_EVALUATION_PARTITION}**
- Evaluation mode: **{D14_EVALUATION_MODE}**
- Frozen operating threshold: **{D14_EXPECTED_DEVELOPMENT_THRESHOLD}**
- Expected TEST encounters: **{D14_EXPECTED_TEST_ENCOUNTERS:,}**
- Expected TEST patients: **{D14_EXPECTED_TEST_PATIENTS:,}**
- Expected TEST positives: **{D14_EXPECTED_TEST_POSITIVES:,}**
- Expected TEST negatives: **{D14_EXPECTED_TEST_NEGATIVES:,}**

The registered model, preprocessing state, feature contract, operating threshold, and candidate identity are frozen.

---

## 4. Confirmatory Evidence Domains

D14 evaluates:

1. Predictive discrimination and calibration.
2. Frozen-threshold operating performance.
3. Validation-to-TEST performance consistency.
4. Pre-specified subgroup operating characteristics.
5. Pre-specified robustness and internal transportability slices.
6. Confirmatory SHAP explainability and source-family attribution.
7. Residual clinical, operational, fairness, and transportability risk.

---

## 5. Prohibited TEST-Driven Activities

The locked TEST partition must not be used to:

- retrain the candidate;
- retune hyperparameters;
- refit preprocessing;
- recalibrate probabilities;
- alter the feature set;
- optimize the operating threshold;
- create subgroup-specific thresholds;
- select a replacement candidate;
- redesign the candidate based on TEST outcomes.

Unfavorable findings are retained as evidence rather than optimized away.

---

## 6. Interpretation Boundary

Successful D14 completion establishes internal locked-test validation evidence only.

It does not establish:

- external transportability;
- prospective clinical effectiveness;
- causal clinical relationships;
- autonomous clinical decision authority;
- production deployment authorization.

---

## 7. Governance Outcome

**Disposition:** {bundle["gate"]["disposition"]}

**Next lifecycle stage:** {bundle["gate"]["next_lifecycle_stage"]}

**Deployment authorized:** {bundle["gate"]["deployment_authorized"]}

Material and unresolved residual risks are carried forward to D15 and the final Clinical AI Validation Protocol & Evidence Report.
"""


# ============================================================
# D14.R11 — GATE DECISION MARKDOWN
# ============================================================


def build_d14_gate_decision_markdown(
    bundle: dict[str, Any],
) -> str:
    """
    Build formal D14 lifecycle gate decision.
    """

    record = bundle[
        "final_record"
    ]

    risk_lines = "\n".join(
        (
            f"- **{risk['risk_id']} — "
            f"{risk['severity_classification']} — "
            f"{risk['risk_domain']}**: "
            f"{risk['finding']}"
        )
        for risk in record[
            "residual_risks"
        ]
    )

    return f"""# D14 — Locked-Test Evaluation Gate Decision

## Executive Decision

**Gate integrity status:** {record["gate_integrity_status"]}

**Final disposition:** {record["disposition"]}

**Next lifecycle stage:** {record["next_lifecycle_stage"]}

**Deployment authorized:** {record["deployment_authorized"]}

---

## Internal Validation Decision

The registered candidate completed the pre-specified one-time internal locked-TEST evaluation without TEST-driven retraining, threshold retuning, preprocessing refit, recalibration, feature modification, candidate replacement, or redesign.

Internal held-out generalization is supported within the evaluated dataset context.

This decision does **not** establish external validation, clinical effectiveness, or deployment readiness.

---

## Residual Risks

{risk_lines}

---

## Governance Interpretation

The candidate may progress to D15 for deployment and monitoring **design** activities.

Progression does not constitute clinical deployment authorization.

The residual risks documented above remain open and must be explicitly represented in monitoring design, external-validation requirements, prospective evaluation planning, clinical workflow controls, and the final Clinical AI Validation Protocol & Evidence Report.
"""


# ============================================================
# D14.R12 — REPORTING BUNDLE VALIDATION
# ============================================================


def validate_d14_reporting_bundle(
    bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate reporting evidence before persistence.
    """

    performance = bundle[
        "performance"
    ]

    subgroup = bundle[
        "subgroup"
    ]

    robustness = bundle[
        "robustness"
    ]

    explainability = bundle[
        "explainability"
    ]

    final_record = bundle[
        "final_record"
    ]

    checks = {
        "performance_validation_passed": (
            performance[
                "evaluation_validation"
            ][
                "overall_pass"
            ]
            is True
        ),

        "subgroup_validation_passed": (
            subgroup[
                "validation"
            ][
                "overall_pass"
            ]
            is True
        ),

        "robustness_validation_passed": (
            robustness[
                "validation"
            ][
                "overall_pass"
            ]
            is True
        ),

        "explainability_validation_passed": (
            explainability[
                "overall_pass"
            ]
            is True
        ),

        "gate_integrity_passed": (
            final_record[
                "gate_integrity_status"
            ]
            == "PASS"
        ),

        "disposition_preserved": (
            final_record[
                "disposition"
            ]
            == D14_FINAL_DISPOSITION
        ),

        "next_stage_preserved": (
            final_record[
                "next_lifecycle_stage"
            ]
            == D14_FINAL_NEXT_STAGE
        ),

        "seven_residual_risks_retained": (
            final_record[
                "residual_risk_count"
            ]
            == 7
        ),

        "all_residual_risks_unresolved": (
            final_record[
                "unresolved_residual_risk_count"
            ]
            == 7
        ),

        "external_validation_not_claimed": (
            final_record[
                "external_validation_completed"
            ]
            is False
        ),

        "clinical_effectiveness_not_claimed": (
            final_record[
                "clinical_effectiveness_established"
            ]
            is False
        ),

        "deployment_not_authorized": (
            final_record[
                "deployment_authorized"
            ]
            is False
        ),
    }

    overall_pass = bool(
        all(
            checks.values()
        )
    )

    return {
        "validation_status": (
            "PASS"
            if overall_pass
            else "FAIL"
        ),

        "overall_pass": (
            overall_pass
        ),

        "checks": checks,
    }


# ============================================================
# D14.R13 — CSV WRITER
# ============================================================


def _write_csv_rows(
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    """
    Write dictionaries to CSV with deterministic column order
    based on first appearance.
    """

    if not rows:
        raise RuntimeError(
            f"No rows supplied for {path.name}."
        )

    fieldnames: list[str] = []

    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(
                    key
                )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    key: _json_safe(
                        row.get(key)
                    )
                    for key in fieldnames
                }
            )


# ============================================================
# D14.R14 — PERSIST REPORTING EVIDENCE
# ============================================================


def persist_d14_reporting_evidence(
) -> dict[str, Any]:
    """
    Validate and persist the complete D14 evidence package.
    """

    bundle = (
        build_d14_reporting_bundle()
    )

    validation = (
        validate_d14_reporting_bundle(
            bundle
        )
    )

    if not validation[
        "overall_pass"
    ]:
        raise RuntimeError(
            "D14 reporting bundle failed validation."
        )

    D14_GOVERNANCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    D14_TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    D14_MANIFEST_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Persist tables
    # --------------------------------------------------------

    _write_csv_rows(
        D14_PERFORMANCE_TABLE_PATH,
        build_d14_performance_rows(
            bundle
        ),
    )

    _write_csv_rows(
        D14_VALIDATION_TEST_COMPARISON_PATH,
        build_d14_validation_test_comparison_rows(
            bundle
        ),
    )

    _write_csv_rows(
        D14_SUBGROUP_TABLE_PATH,
        build_d14_subgroup_rows(
            bundle
        ),
    )

    _write_csv_rows(
        D14_ROBUSTNESS_TABLE_PATH,
        build_d14_robustness_rows(
            bundle
        ),
    )

    _write_csv_rows(
        D14_EXPLAINABILITY_TABLE_PATH,
        build_d14_explainability_rows(
            bundle
        ),
    )

    _write_csv_rows(
        D14_LOCAL_EXPLANATION_TABLE_PATH,
        build_d14_local_explanation_rows(
            bundle
        ),
    )

    _write_csv_rows(
        D14_RESIDUAL_RISK_TABLE_PATH,
        build_d14_residual_risk_rows(
            bundle
        ),
    )

    # --------------------------------------------------------
    # Persist governance documents
    # --------------------------------------------------------

    D14_CONTRACT_PATH.write_text(
        build_d14_evaluation_contract_markdown(
            bundle
        ),
        encoding="utf-8",
    )

    D14_GATE_DECISION_PATH.write_text(
        build_d14_gate_decision_markdown(
            bundle
        ),
        encoding="utf-8",
    )

    D14_FINAL_GOVERNANCE_RECORD_PATH.write_text(
        json.dumps(
            _json_safe(
                bundle[
                    "final_record"
                ]
            ),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Build artifact inventory before manifest
    # --------------------------------------------------------

    persisted_paths = [
        D14_CONTRACT_PATH,
        D14_GATE_DECISION_PATH,
        D14_FINAL_GOVERNANCE_RECORD_PATH,
        D14_PERFORMANCE_TABLE_PATH,
        D14_VALIDATION_TEST_COMPARISON_PATH,
        D14_SUBGROUP_TABLE_PATH,
        D14_ROBUSTNESS_TABLE_PATH,
        D14_EXPLAINABILITY_TABLE_PATH,
        D14_LOCAL_EXPLANATION_TABLE_PATH,
        D14_RESIDUAL_RISK_TABLE_PATH,
    ]

    artifact_inventory = []

    for path in persisted_paths:
        artifact_inventory.append(
            {
                "path": str(
                    path.relative_to(
                        PROJECT_ROOT
                    )
                ).replace(
                    "\\",
                    "/",
                ),

                "sha256": (
                    _sha256_file(
                        path
                    )
                ),

                "size_bytes": (
                    path.stat().st_size
                ),
            }
        )

    manifest = {
        "stage_id": D14_STAGE_ID,
        "stage_name": D14_STAGE_NAME,

        "generated_at_utc": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),

        "registry_id": (
            D14_EXPECTED_REGISTRY_ID
        ),

        "candidate_system_sha256": (
            D14_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "source_git_commit": (
            D14_SOURCE_GIT_COMMIT
        ),

        "evaluation_partition": (
            D14_EVALUATION_PARTITION
        ),

        "evaluation_mode": (
            D14_EVALUATION_MODE
        ),

        "frozen_threshold": (
            D14_EXPECTED_DEVELOPMENT_THRESHOLD
        ),

        "test_population": {
            "encounters": (
                D14_EXPECTED_TEST_ENCOUNTERS
            ),

            "patients": (
                D14_EXPECTED_TEST_PATIENTS
            ),

            "positives": (
                D14_EXPECTED_TEST_POSITIVES
            ),

            "negatives": (
                D14_EXPECTED_TEST_NEGATIVES
            ),
        },

        "gate_integrity_status": (
            bundle[
                "final_record"
            ][
                "gate_integrity_status"
            ]
        ),

        "disposition": (
            bundle[
                "final_record"
            ][
                "disposition"
            ]
        ),

        "next_lifecycle_stage": (
            bundle[
                "final_record"
            ][
                "next_lifecycle_stage"
            ]
        ),

        "residual_risk_count": (
            bundle[
                "final_record"
            ][
                "residual_risk_count"
            ]
        ),

        "unresolved_residual_risk_count": (
            bundle[
                "final_record"
            ][
                "unresolved_residual_risk_count"
            ]
        ),

        "external_validation_completed": False,

        "clinical_effectiveness_established": False,

        "deployment_authorized": False,

        "reporting_validation": (
            validation
        ),

        "artifact_inventory": (
            artifact_inventory
        ),
    }

    D14_MANIFEST_PATH.write_text(
        yaml.safe_dump(
            _json_safe(
                manifest
            ),
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    return {
        "validation": validation,
        "manifest": manifest,
        "manifest_path": (
            D14_MANIFEST_PATH
        ),
        "persisted_paths": (
            persisted_paths
        ),
    }


# ============================================================
# D14.R15 — PRINT REPORTING SUMMARY
# ============================================================


def print_d14_reporting_evidence_summary(
) -> None:
    """
    Persist and print the complete D14 evidence package summary.
    """

    result = (
        persist_d14_reporting_evidence()
    )

    manifest = result[
        "manifest"
    ]

    print("=" * 104)
    print(
        "D14 — LOCKED-TEST EVALUATION"
    )
    print(
        "FORMAL REPORTING & EVIDENCE PACKAGE"
    )
    print("=" * 104)

    print()
    print("Reporting validation")
    print("-" * 104)

    for check_name, passed in (
        result[
            "validation"
        ]["checks"].items()
    ):
        print(
            f"{check_name:<62} "
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()
    print("Evidence package")
    print("-" * 104)

    for artifact in (
        manifest[
            "artifact_inventory"
        ]
    ):
        print(
            f"{artifact['path']:<74} "
            f"{artifact['size_bytes']:>10,} bytes"
        )

    print(
        f"{str(D14_MANIFEST_PATH.relative_to(PROJECT_ROOT)).replace(chr(92), '/'):<74} "
        f"{D14_MANIFEST_PATH.stat().st_size:>10,} bytes"
    )

    print()
    print("Governance closeout")
    print("-" * 104)

    print(
        f"Registry ID:                         "
        f"{manifest['registry_id']}"
    )

    print(
        f"Gate integrity status:               "
        f"{manifest['gate_integrity_status']}"
    )

    print(
        f"Final disposition:                   "
        f"{manifest['disposition']}"
    )

    print(
        f"Residual risks:                      "
        f"{manifest['residual_risk_count']}"
    )

    print(
        f"Unresolved residual risks:           "
        f"{manifest['unresolved_residual_risk_count']}"
    )

    print(
        f"External validation completed:       "
        f"{manifest['external_validation_completed']}"
    )

    print(
        f"Clinical effectiveness established:  "
        f"{manifest['clinical_effectiveness_established']}"
    )

    print(
        f"Deployment authorized:               "
        f"{manifest['deployment_authorized']}"
    )

    print(
        f"Next lifecycle stage:                "
        f"{manifest['next_lifecycle_stage']}"
    )

    print()
    print(
        "REPORTING EVIDENCE STATUS:           "
        f"{result['validation']['validation_status']}"
    )

    print("=" * 104)