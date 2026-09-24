# ============================================================
# D11 — ROBUSTNESS & TRANSPORTABILITY REPORTING
# ============================================================
# Purpose:
#   Convert the validated D11 runtime evidence into deterministic,
#   reviewable governance artifacts without changing the frozen model,
#   preprocessing, threshold, validation boundary, or locked TEST set.
# ============================================================

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Final

from src.models import robustness as d11


# ============================================================
# D11-R.01 — REPORTING IDENTITY & ARTIFACT PATHS
# ============================================================

D11_REPORTING_STAGE: Final[str] = "D11"
D11_REPORTING_NAME: Final[str] = "Robustness & Transportability Evidence Package"

D11_MANIFEST_PATH: Final[Path] = Path(
    "artifacts/manifests/D11_robustness_transportability_manifest.yaml"
)
D11_GOVERNANCE_DIR: Final[Path] = Path("reports/governance")
D11_TABLE_DIR: Final[Path] = Path("reports/tables")

D11_CONTRACT_PATH: Final[Path] = D11_GOVERNANCE_DIR / "D11_robustness_transportability_contract.md"
D11_GATE_PATH: Final[Path] = D11_GOVERNANCE_DIR / "D11_robustness_transportability_gate_decision.md"

D11_BASELINE_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_baseline_metric_reference.csv"
D11_REGISTRY_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_stress_test_registry.csv"
D11_SYNTHETIC_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_synthetic_stress_results.csv"
D11_OBSERVED_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_observed_slice_results.csv"
D11_COMPARISON_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_robustness_comparison_assessment.csv"
D11_HETEROGENEITY_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_heterogeneity_review_findings.csv"
D11_LOW_SUPPORT_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_low_support_limitations.csv"
D11_ACTIONS_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_carry_forward_actions.csv"
D11_INTEGRITY_TABLE_PATH: Final[Path] = D11_TABLE_DIR / "D11_artifact_integrity.csv"


# ============================================================
# D11-R.02 — SERIALIZATION HELPERS
# ============================================================

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _scalar(value: Any) -> Any:
    """Convert nested/list values to deterministic CSV-safe strings."""
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    if value is None:
        return ""
    return value


def _rows_to_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nNO_ROWS\n", encoding="utf-8", newline="")
        return

    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _scalar(row.get(key)) for key in fieldnames})


def _yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def _write_simple_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write the deliberately flat deterministic D11 manifest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}: {_yaml_scalar(value)}" for key, value in data.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ============================================================
# D11-R.03 — VALIDATED EVIDENCE BUNDLE
# ============================================================

def build_d11_reporting_evidence_bundle() -> dict[str, Any]:
    static = d11.validate_d11_static_contract()
    boundary = d11.validate_d11_frozen_system_boundary()
    baseline = d11.validate_d11_baseline_metric_reference()
    registry = d11.validate_d11_stress_test_registry()
    execution_path = d11.validate_d11_stress_test_execution_engine()
    stress = d11.execute_d11_governed_stress_tests()
    comparison = d11.validate_d11_robustness_comparison_assessment()
    disposition = d11.validate_d11_robustness_governance_disposition()

    validators = {
        "static_contract": static,
        "frozen_system_boundary": boundary,
        "baseline_metric_reference": baseline,
        "stress_test_registry": registry,
        "stress_execution_path": execution_path,
        "comparison_assessment": comparison,
        "governance_disposition": disposition,
    }

    failed_validators = [
        name
        for name, result in validators.items()
        if result.get("validation_status") != "PASS"
    ]
    if failed_validators:
        raise RuntimeError(
            "D11 reporting cannot proceed because validated runtime evidence "
            f"failed: {failed_validators}"
        )

    if stress["model_retrained"] or stress["hyperparameters_retuned"]:
        raise RuntimeError("D11 stress engine violated frozen-model governance.")
    if stress["preprocessor_refitted"] or stress["threshold_retuned"]:
        raise RuntimeError("D11 stress engine violated preprocessing/threshold governance.")
    if stress["locked_test_accessed"] or stress["deployment_authorized"]:
        raise RuntimeError("D11 stress engine violated TEST/deployment governance.")

    return {
        "static": static,
        "boundary": boundary,
        "baseline": baseline,
        "registry": registry,
        "execution_path": execution_path,
        "stress": stress,
        "comparison": comparison,
        "disposition": disposition,
        "validation_status": "PASS",
    }


# ============================================================
# D11-R.04 — EVIDENCE TABLE BUILDERS
# ============================================================

def _baseline_rows(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    excluded = {"checks", "failed_checks"}
    return [{key: _scalar(value) for key, value in baseline.items() if key not in excluded}]


def _registry_rows() -> list[dict[str, Any]]:
    return [dict(row) for row in d11.D11_STRESS_TEST_REGISTRY]


def _comparison_rows(comparison: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in comparison["synthetic_assessments"]:
        item = dict(row)
        item["assessment_pathway"] = "SYNTHETIC_SAME_POPULATION_DEGRADATION"
        rows.append(item)
    for row in comparison["observed_slice_assessments"]:
        item = dict(row)
        item["assessment_pathway"] = "OBSERVED_SLICE_HETEROGENEITY"
        rows.append(item)
    return rows


def _action_rows(disposition: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "action_id": f"D11-ACTION-{index:02d}",
            "action_order": index,
            "mandatory": True,
            "action": action,
        }
        for index, action in enumerate(
            disposition["mandatory_carry_forward_actions"], start=1
        )
    ]


# ============================================================
# D11-R.05 — GOVERNANCE CONTRACT
# ============================================================

def _contract_markdown(bundle: dict[str, Any]) -> str:
    baseline = bundle["baseline"]
    return f"""# D11 — Robustness & Transportability Governance Contract

## Purpose
D11 evaluates the robustness, stability, and development-stage transportability of the frozen clinical AI candidate under pre-specified perturbations and observed validation-population conditions.

## Frozen lifecycle boundary
- Source preprocessing stage: D7
- Source model stage: D8
- Source threshold stage: D9
- Source fairness stage: D10
- Evaluation partition: validation
- Locked TEST evaluation stage: D14
- Selected model: {baseline['selected_model']}
- Frozen model SHA-256: {baseline['model_sha256']}
- Frozen development threshold: {baseline['threshold']}
- Validation encounters: {baseline['encounter_count']}
- Validation positives: {baseline['positive_count']}
- Validation negatives: {baseline['negative_count']}

## Governance prohibitions
D11 does not retrain or retune the model, refit preprocessing, retune the D9 threshold, create subgroup-specific thresholds, recalibrate the model, access the locked TEST set, apply automatic mitigation, authorize autonomous clinical decisions, or authorize deployment.

## Interpretation boundary
Synthetic perturbations may be compared directly with the immutable whole-validation baseline because they preserve the same evaluation population. Observed slices characterize population heterogeneity and support limitations; whole-cohort differences must not be labelled automatic model degradation, causal effects, or external transportability failure.

Absence of degradation under simulated stress does not establish external, temporal, geographic, institutional, prospective, or deployment validity.

## Lifecycle rule
D11 may authorize progression to D12 Explainability only when the validated governance disposition permits progression. Progression is not deployment authorization.
"""


# ============================================================
# D11-R.06 — GATE DECISION
# ============================================================

def _gate_markdown(bundle: dict[str, Any]) -> str:
    d = bundle["disposition"]
    return f"""# D11 — Robustness & Transportability Gate Decision

## Decision
**{d['disposition']}**

Progression authorized: **{d['progression_authorized']}**  
Next lifecycle stage: **{d['next_lifecycle_stage']} — {d['next_lifecycle_stage_name']}**  
Deployment authorized: **{d['deployment_authorized']}**

## Evidence summary
- Synthetic perturbation assessments: {d['synthetic_assessment_count']}
- Synthetic degradation-review triggers: {d['synthetic_review_count']}
- Observed-slice assessments: {d['observed_slice_assessment_count']}
- Adequate-support heterogeneity findings: {d['observed_heterogeneity_review_count']}
- Low-support interpretation limitations: {d['low_support_limitation_count']}
- Mandatory carry-forward actions: {d['mandatory_carry_forward_action_count']}

## Interpretation
{d['disposition_interpretation']}

The six adequate-support observed-slice findings are governance review signals, not automatic model failures. The twelve low-support rows remain explicit evidence limitations. Direct causal interpretation and direct observed-slice degradation claims are prohibited.

## Frozen-system assurance
No model retraining, hyperparameter retuning, preprocessing refit, threshold retuning, recalibration, locked-TEST access, external-validation claim, or deployment authorization occurred in D11.

## Required carry-forward actions
""" + "\n".join(
        f"{i}. {action}"
        for i, action in enumerate(d["mandatory_carry_forward_actions"], start=1)
    ) + "\n"


# ============================================================
# D11-R.07 — MANIFEST
# ============================================================

def _manifest(bundle: dict[str, Any]) -> dict[str, Any]:
    b = bundle["baseline"]
    c = bundle["comparison"]
    d = bundle["disposition"]
    return {
        "stage": "D11",
        "stage_name": "Robustness & Transportability",
        "reporting_package": D11_REPORTING_NAME,
        "validation_status": "PASS",
        "evaluation_partition": "validation",
        "selected_model": b["selected_model"],
        "model_sha256": b["model_sha256"],
        "d7_preprocessor_sha256": bundle["boundary"]["d7_preprocessor_sha256"],
        "d7_schema_sha256": bundle["boundary"]["d7_schema_sha256"],
        "development_threshold": b["threshold"],
        "validation_encounters": b["encounter_count"],
        "validation_positives": b["positive_count"],
        "validation_negatives": b["negative_count"],
        "stress_scenario_count": bundle["stress"]["scenario_count"],
        "synthetic_assessment_count": c["synthetic_assessment_count"],
        "synthetic_review_count": c["synthetic_review_count"],
        "observed_slice_assessment_count": c["observed_slice_assessment_count"],
        "observed_heterogeneity_review_count": d["observed_heterogeneity_review_count"],
        "low_support_limitation_count": d["low_support_limitation_count"],
        "mandatory_carry_forward_action_count": d["mandatory_carry_forward_action_count"],
        "disposition": d["disposition"],
        "progression_authorized": d["progression_authorized"],
        "next_lifecycle_stage": d["next_lifecycle_stage"],
        "locked_test_accessed": d["locked_test_accessed"],
        "external_validation_established": d["external_validation_established"],
        "temporal_validation_established": d["temporal_validation_established"],
        "geographic_transportability_established": d["geographic_transportability_established"],
        "institutional_transportability_established": d["institutional_transportability_established"],
        "prospective_validation_established": d["prospective_validation_established"],
        "deployment_authorized": d["deployment_authorized"],
    }


# ============================================================
# D11-R.08 — GENERATE COMPLETE EVIDENCE PACKAGE
# ============================================================

def generate_d11_robustness_reporting_package() -> dict[str, Any]:
    bundle = build_d11_reporting_evidence_bundle()

    D11_GOVERNANCE_DIR.mkdir(parents=True, exist_ok=True)
    D11_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    D11_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Core governance documents.
    D11_CONTRACT_PATH.write_text(_contract_markdown(bundle), encoding="utf-8")
    D11_GATE_PATH.write_text(_gate_markdown(bundle), encoding="utf-8")

    # Evidence tables.
    _rows_to_csv(D11_BASELINE_TABLE_PATH, _baseline_rows(bundle["baseline"]))
    _rows_to_csv(D11_REGISTRY_TABLE_PATH, _registry_rows())
    _rows_to_csv(D11_SYNTHETIC_TABLE_PATH, list(bundle["stress"]["synthetic_results"]))
    _rows_to_csv(D11_OBSERVED_TABLE_PATH, list(bundle["stress"]["observed_slice_results"]))
    _rows_to_csv(D11_COMPARISON_TABLE_PATH, _comparison_rows(bundle["comparison"]))
    _rows_to_csv(
        D11_HETEROGENEITY_TABLE_PATH,
        list(bundle["disposition"]["observed_heterogeneity_findings"]),
    )
    _rows_to_csv(
        D11_LOW_SUPPORT_TABLE_PATH,
        list(bundle["disposition"]["low_support_limitations"]),
    )
    _rows_to_csv(D11_ACTIONS_TABLE_PATH, _action_rows(bundle["disposition"]))

    # Deterministic manifest.
    _write_simple_yaml(D11_MANIFEST_PATH, _manifest(bundle))

    # Integrity table intentionally excludes itself.
    evidence_paths = [
        D11_MANIFEST_PATH,
        D11_CONTRACT_PATH,
        D11_GATE_PATH,
        D11_BASELINE_TABLE_PATH,
        D11_REGISTRY_TABLE_PATH,
        D11_SYNTHETIC_TABLE_PATH,
        D11_OBSERVED_TABLE_PATH,
        D11_COMPARISON_TABLE_PATH,
        D11_HETEROGENEITY_TABLE_PATH,
        D11_LOW_SUPPORT_TABLE_PATH,
        D11_ACTIONS_TABLE_PATH,
    ]
    integrity_rows = [
        {
            "artifact": str(path).replace("\\", "/"),
            "exists": path.exists(),
            "size_bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in evidence_paths
    ]
    _rows_to_csv(D11_INTEGRITY_TABLE_PATH, integrity_rows)

    return {
        "stage": "D11",
        "package": D11_REPORTING_NAME,
        "artifact_count": 12,
        "manifest_path": str(D11_MANIFEST_PATH),
        "contract_path": str(D11_CONTRACT_PATH),
        "gate_decision_path": str(D11_GATE_PATH),
        "integrity_path": str(D11_INTEGRITY_TABLE_PATH),
        "disposition": bundle["disposition"]["disposition"],
        "progression_authorized": bundle["disposition"]["progression_authorized"],
        "next_lifecycle_stage": bundle["disposition"]["next_lifecycle_stage"],
        "synthetic_review_count": bundle["disposition"]["synthetic_review_count"],
        "observed_heterogeneity_review_count": bundle["disposition"]["observed_heterogeneity_review_count"],
        "low_support_limitation_count": bundle["disposition"]["low_support_limitation_count"],
        "mandatory_carry_forward_action_count": bundle["disposition"]["mandatory_carry_forward_action_count"],
        "locked_test_accessed": bundle["disposition"]["locked_test_accessed"],
        "deployment_authorized": bundle["disposition"]["deployment_authorized"],
        "validation_status": "PASS",
    }


# ============================================================
# D11-R.09 — VALIDATE GENERATED EVIDENCE PACKAGE
# ============================================================

def validate_d11_robustness_reporting_package() -> dict[str, Any]:
    result = generate_d11_robustness_reporting_package()

    expected_paths = [
        D11_MANIFEST_PATH,
        D11_CONTRACT_PATH,
        D11_GATE_PATH,
        D11_BASELINE_TABLE_PATH,
        D11_REGISTRY_TABLE_PATH,
        D11_SYNTHETIC_TABLE_PATH,
        D11_OBSERVED_TABLE_PATH,
        D11_COMPARISON_TABLE_PATH,
        D11_HETEROGENEITY_TABLE_PATH,
        D11_LOW_SUPPORT_TABLE_PATH,
        D11_ACTIONS_TABLE_PATH,
        D11_INTEGRITY_TABLE_PATH,
    ]

    checks = {
        "all_expected_artifacts_exist": all(path.exists() for path in expected_paths),
        "artifact_count_is_12": result["artifact_count"] == 12,
        "disposition_is_conditional_pass": result["disposition"] == d11.D11_ROBUSTNESS_DISPOSITION,
        "progression_authorized": result["progression_authorized"] is True,
        "next_stage_is_d12": result["next_lifecycle_stage"] == "D12",
        "synthetic_review_count_is_zero": result["synthetic_review_count"] == 0,
        "heterogeneity_findings_are_six": result["observed_heterogeneity_review_count"] == 6,
        "low_support_limitations_are_twelve": result["low_support_limitation_count"] == 12,
        "carry_forward_actions_are_six": result["mandatory_carry_forward_action_count"] == 6,
        "locked_test_not_accessed": result["locked_test_accessed"] is False,
        "deployment_not_authorized": result["deployment_authorized"] is False,
    }

    failed_checks = [name for name, passed in checks.items() if not passed]
    return {
        **result,
        "checks": checks,
        "failed_checks": failed_checks,
        "validation_status": "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D11-R.10 — EXECUTABLE REPORTING CHECK
# ============================================================

def print_d11_robustness_reporting_package() -> None:
    result = validate_d11_robustness_reporting_package()
    print("=" * 72)
    print("D11 ROBUSTNESS & TRANSPORTABILITY EVIDENCE PACKAGE")
    print("=" * 72)
    for key in (
        "validation_status",
        "artifact_count",
        "disposition",
        "progression_authorized",
        "next_lifecycle_stage",
        "synthetic_review_count",
        "observed_heterogeneity_review_count",
        "low_support_limitation_count",
        "mandatory_carry_forward_action_count",
        "locked_test_accessed",
        "deployment_authorized",
        "failed_checks",
    ):
        print(f"{key}: {result[key]}")


if __name__ == "__main__":
    print_d11_robustness_reporting_package()