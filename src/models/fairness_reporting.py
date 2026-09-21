"""
D10 — Fairness & Subgroup Evaluation Reporting
===============================================

Generates the governed D10 evidence package from validated D10 runtime evidence.
This module does not retrain, retune, recalibrate, create subgroup thresholds,
access the locked TEST set, or authorize deployment.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

import pandas as pd

from src.models.fairness import (
    D10_STAGE,
    D10_STAGE_NAME,
    D10_TARGET,
    D10_EVALUATION_PARTITION,
    D10_EXPECTED_DEVELOPMENT_THRESHOLD,
    D10_EXPECTED_SELECTED_MODEL,
    D10_EXPECTED_MODEL_SHA256,
    D10_LOCKED_TEST_EVALUATION_STAGE,
    D10_PRIMARY_SUBGROUP_VARIABLES,
    D10_CALIBRATION_BIN_COUNT,
    D10_CALIBRATION_METHOD,
    D10_MIN_SUBGROUP_ENCOUNTERS,
    D10_MIN_POSITIVE_OUTCOMES,
    D10_MIN_NEGATIVE_OUTCOMES,
    validate_d10_static_contract,
    validate_d10_cross_stage_alignment,
    validate_d10_fairness_evaluation_frame,
    validate_d10_stability_policy,
    validate_d10_subgroup_performance_table,
    validate_d10_disparity_analysis,
    validate_d10_subgroup_uncertainty,
    validate_d10_subgroup_calibration,
    validate_d10_governance_findings_registry,
    build_d10_subgroup_performance_table,
    build_d10_disparity_summary,
    build_d10_subgroup_uncertainty_table,
    build_d10_subgroup_calibration_table,
    build_d10_subgroup_calibration_summary,
    build_d10_governance_findings_registry,
)


# ============================================================
# D10.30 — EVIDENCE PACKAGE PATHS
# ============================================================

D10_MANIFEST_PATH = Path("artifacts/manifests/D10_fairness_subgroup_manifest.yaml")
D10_CONTRACT_PATH = Path("reports/governance/D10_fairness_subgroup_contract.md")
D10_GATE_PATH = Path("reports/governance/D10_fairness_subgroup_gate_decision.md")

D10_TABLE_PATHS = {
    "subgroup_performance": Path("reports/tables/D10_subgroup_performance.csv"),
    "disparity_summary": Path("reports/tables/D10_disparity_summary.csv"),
    "subgroup_uncertainty": Path("reports/tables/D10_subgroup_uncertainty.csv"),
    "subgroup_calibration": Path("reports/tables/D10_subgroup_calibration.csv"),
    "subgroup_calibration_bins": Path("reports/tables/D10_subgroup_calibration_bins.csv"),
    "governance_findings": Path("reports/tables/D10_governance_findings_registry.csv"),
}

D10_GATE_DECISION = "CONDITIONAL PASS"
D10_NEXT_STAGE = "D11 — Robustness & Transportability"
D10_DEPLOYMENT_STATUS = "NOT AUTHORIZED"


# ============================================================
# D10.31 — VALIDATION ORCHESTRATOR
# ============================================================

def validate_d10_reporting_inputs() -> dict[str, Any]:
    """Run every D10 source validator before writing governed evidence."""
    validators = {
        "static_contract": validate_d10_static_contract(),
        "cross_stage_alignment": validate_d10_cross_stage_alignment(),
        "fairness_evaluation_frame": validate_d10_fairness_evaluation_frame(),
        "stability_policy": validate_d10_stability_policy(),
        "subgroup_performance": validate_d10_subgroup_performance_table(),
        "disparity_analysis": validate_d10_disparity_analysis(),
        "subgroup_uncertainty": validate_d10_subgroup_uncertainty(),
        "subgroup_calibration": validate_d10_subgroup_calibration(),
        "governance_findings": validate_d10_governance_findings_registry(),
    }
    failed = [k for k, v in validators.items() if v.get("validation_status") != "PASS"]
    if failed:
        raise RuntimeError(f"D10 reporting inputs failed validation: {failed}")
    return {"validation_status": "PASS", "validated_components": list(validators), "failed_components": []}


# ============================================================
# D10.32 — TABLE EVIDENCE GENERATION
# ============================================================

def build_d10_reporting_tables() -> dict[str, pd.DataFrame]:
    """Build the six governed D10 tabular evidence artifacts."""
    validate_d10_reporting_inputs()
    return {
        "subgroup_performance": build_d10_subgroup_performance_table(),
        "disparity_summary": build_d10_disparity_summary(),
        "subgroup_uncertainty": build_d10_subgroup_uncertainty_table(),
        "subgroup_calibration": build_d10_subgroup_calibration_summary(),
        "subgroup_calibration_bins": build_d10_subgroup_calibration_table(),
        "governance_findings": build_d10_governance_findings_registry(),
    }


def write_d10_reporting_tables() -> dict[str, dict[str, Any]]:
    tables = build_d10_reporting_tables()
    evidence: dict[str, dict[str, Any]] = {}
    for name, frame in tables.items():
        path = D10_TABLE_PATHS[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(path, index=False)
        evidence[name] = {
            "path": path.as_posix(),
            "rows": int(len(frame)),
            "columns": int(len(frame.columns)),
        }
    return evidence


# ============================================================
# D10.33 — GOVERNANCE CONTRACT
# ============================================================

def build_d10_governance_contract() -> str:
    return f"""# D10 — Fairness & Subgroup Evaluation Governance Contract

## Purpose
D10 evaluates development-validation subgroup performance, uncertainty, calibration, representation, error burden, and operational burden for the frozen D8 development model operating at the frozen D9 threshold.

## Governed boundary
- **Model:** {D10_EXPECTED_SELECTED_MODEL}
- **Model SHA256:** `{D10_EXPECTED_MODEL_SHA256}`
- **Evaluation partition:** {D10_EVALUATION_PARTITION.upper()}
- **Frozen development threshold:** {D10_EXPECTED_DEVELOPMENT_THRESHOLD:.2f}
- **Primary subgroup variables:** {', '.join(D10_PRIMARY_SUBGROUP_VARIABLES)}
- **Locked TEST evaluation:** reserved for {D10_LOCKED_TEST_EVALUATION_STAGE}

## Analytical support policy
A subgroup is classified as analytically adequate only when it has at least {D10_MIN_SUBGROUP_ENCOUNTERS} encounters, {D10_MIN_POSITIVE_OUTCOMES} positive outcomes, and {D10_MIN_NEGATIVE_OUTCOMES} negative outcomes. Low-support groups remain visible in evidence but are not used as the sole basis for primary disparity extrema or governance conclusions. These minima are analytical stability rules, not fairness, clinical, or regulatory thresholds.

## Fairness interpretation contract
D10 does **not** treat numerical subgroup differences as proof of unlawful discrimination, causal bias, or clinical inequity. Differences may reflect sample size, prevalence, data quality, measurement, clinical pathways, or model behavior. PR-AUC is interpreted with subgroup prevalence. Unknown/not-recorded race remains visible as a data-quality category and is not treated as an observed demographic group for primary disparity comparisons.

## Calibration contract
Subgroup calibration uses {D10_CALIBRATION_BIN_COUNT} within-subgroup equal-frequency quantile bins (`{D10_CALIBRATION_METHOD}`). Calibration analysis is diagnostic only. D10 does not recalibrate the model and does not establish external probability calibration.

## Prohibited actions in D10
D10 does not permit model retraining, hyperparameter retuning, preprocessor refitting, threshold retuning, subgroup-specific thresholds, automatic fairness mitigation, autonomous clinical decision-making, locked TEST access, or deployment authorization.

## Sensitive-attribute disclosure
Race, gender, and age are both D10 subgroup evaluation variables and source features in the frozen primary model pathway. Their inclusion therefore requires explicit lifecycle governance, subgroup monitoring, data-quality review, and later locked-test assessment. D10 does not infer that inclusion is either acceptable or unacceptable solely from the present validation evidence.

## Required downstream handling
All D10 governance findings must be carried forward into D11 robustness/transportability analysis and subsequently into D14 locked-test evaluation and deployment-readiness governance. No D10 finding may be silently resolved by changing the global threshold for a subgroup.
"""


# ============================================================
# D10.34 — GATE DECISION
# ============================================================

def build_d10_gate_decision() -> str:
    findings = build_d10_governance_findings_registry()
    rows = []
    for r in findings.itertuples(index=False):
        rows.append(
            f"| {r.finding_id} | {r.domain} | {r.disposition} | {r.deployment_implication} |"
        )
    finding_table = "\n".join(rows)

    return f"""# D10 — Fairness & Subgroup Evaluation Gate Decision

## Gate decision
**{D10_GATE_DECISION} — AUTHORIZED TO PROCEED TO {D10_NEXT_STAGE.upper()}**

This decision authorizes lifecycle progression only. **Deployment remains {D10_DEPLOYMENT_STATUS}.**

## Basis for decision
D10 completed governed subgroup performance evaluation, disparity analysis, 95% uncertainty analysis, subgroup calibration analysis, and a seven-finding governance registry on the held-out development VALIDATION partition. The frozen D8 model and frozen D9 threshold of {D10_EXPECTED_DEVELOPMENT_THRESHOLD:.2f} were preserved. No subgroup-specific threshold, automatic mitigation, model recalibration, or locked TEST evaluation was performed.

## Findings carried forward
| Finding | Domain | Disposition | Deployment implication |
|---|---|---|---|
{finding_table}

## Governance interpretation
The D10 evidence does not establish that the model is globally "fair" or "unfair." It establishes development-validation evidence requiring differentiated monitoring, review, evidence-sufficiency controls, and data-governance action. In particular, the false-negative burden and age-related heterogeneity remain unresolved before deployment.

## Conditions for progression
D11 must assess whether the identified performance/calibration signals remain stable under robustness and transportability analyses. D14 must repeat the governed evaluation on the locked TEST partition without using TEST evidence to retroactively tune the development model or threshold. Deployment authorization requires later lifecycle evidence and explicit governance approval.

## Status
- D10 analytical evaluation: **COMPLETE**
- D10 governance findings: **COMPLETE**
- D10 gate: **{D10_GATE_DECISION}**
- Authorized next stage: **{D10_NEXT_STAGE}**
- Locked TEST accessed: **NO**
- Deployment authorized: **NO**
"""


# ============================================================
# D10.35 — MANIFEST SERIALIZATION
# ============================================================

def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def _yaml_lines(obj: Any, indent: int = 0) -> list[str]:
    pad = " " * indent
    lines: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.extend(_yaml_lines(value, indent + 2))
            else:
                lines.append(f"{pad}{key}: {_yaml_scalar(value)}")
    elif isinstance(obj, list):
        for value in obj:
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}-")
                lines.extend(_yaml_lines(value, indent + 2))
            else:
                lines.append(f"{pad}- {_yaml_scalar(value)}")
    return lines


def build_d10_manifest(table_evidence: dict[str, dict[str, Any]]) -> dict[str, Any]:
    alignment = validate_d10_cross_stage_alignment()
    performance = validate_d10_subgroup_performance_table()
    calibration = validate_d10_subgroup_calibration()
    findings = validate_d10_governance_findings_registry()

    return {
        "stage": D10_STAGE,
        "stage_name": D10_STAGE_NAME,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": D10_TARGET,
        "evaluation_partition": D10_EVALUATION_PARTITION,
        "source_model": {
            "selected_model": D10_EXPECTED_SELECTED_MODEL,
            "sha256": D10_EXPECTED_MODEL_SHA256,
        },
        "source_threshold": {
            "value": D10_EXPECTED_DEVELOPMENT_THRESHOLD,
            "status": "FROZEN_D9_DEVELOPMENT_THRESHOLD",
            "subgroup_specific_thresholds_created": False,
        },
        "validation_population": {
            "encounters": alignment["validation_encounter_count"],
            "positive_outcomes": alignment["validation_positive_count"],
            "negative_outcomes": alignment["validation_negative_count"],
        },
        "subgroup_evaluation": {
            "variables": list(D10_PRIMARY_SUBGROUP_VARIABLES),
            "rows": performance["subgroup_table_rows"],
            "adequate_support_rows": performance["adequate_support_rows"],
            "low_support_rows": performance["low_support_rows"],
            "support_policy": {
                "minimum_encounters": D10_MIN_SUBGROUP_ENCOUNTERS,
                "minimum_positive_outcomes": D10_MIN_POSITIVE_OUTCOMES,
                "minimum_negative_outcomes": D10_MIN_NEGATIVE_OUTCOMES,
                "fairness_standard": False,
            },
        },
        "calibration": {
            "method": D10_CALIBRATION_METHOD,
            "requested_bins_per_subgroup": D10_CALIBRATION_BIN_COUNT,
            "calibration_bin_rows": calibration["calibration_bin_rows"],
            "model_recalibrated": False,
            "probability_calibration_established": False,
        },
        "governance_findings": {
            "count": findings["governance_finding_count"],
            "finding_ids": findings["finding_ids"],
            "disposition_counts": findings["disposition_counts"],
            "fairness_violation_determined": False,
            "causal_bias_determined": False,
        },
        "controls": {
            "model_retrained": False,
            "hyperparameters_retuned": False,
            "preprocessor_refitted": False,
            "threshold_retuned": False,
            "automatic_mitigation_applied": False,
            "locked_test_accessed": False,
            "deployment_authorized": False,
        },
        "gate": {
            "decision": D10_GATE_DECISION,
            "authorized_next_stage": D10_NEXT_STAGE,
            "deployment_authorized": False,
        },
        "artifacts": {
            "manifest": D10_MANIFEST_PATH.as_posix(),
            "governance_contract": D10_CONTRACT_PATH.as_posix(),
            "gate_decision": D10_GATE_PATH.as_posix(),
            "tables": table_evidence,
        },
    }


# ============================================================
# D10.36 — COMPLETE EVIDENCE PACKAGE GENERATION
# ============================================================

def generate_d10_evidence_package() -> dict[str, Any]:
    validation = validate_d10_reporting_inputs()
    table_evidence = write_d10_reporting_tables()

    D10_CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    D10_GATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    D10_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    D10_CONTRACT_PATH.write_text(build_d10_governance_contract(), encoding="utf-8")
    D10_GATE_PATH.write_text(build_d10_gate_decision(), encoding="utf-8")

    manifest = build_d10_manifest(table_evidence)
    D10_MANIFEST_PATH.write_text("\n".join(_yaml_lines(manifest)) + "\n", encoding="utf-8")

    expected_paths = [D10_MANIFEST_PATH, D10_CONTRACT_PATH, D10_GATE_PATH, *D10_TABLE_PATHS.values()]
    missing = [p.as_posix() for p in expected_paths if not p.exists()]
    empty = [p.as_posix() for p in expected_paths if p.exists() and p.stat().st_size == 0]
    if missing or empty:
        raise RuntimeError(f"D10 evidence package validation failed. missing={missing}, empty={empty}")

    return {
        "stage": D10_STAGE,
        "validation_status": validation["validation_status"],
        "gate_decision": D10_GATE_DECISION,
        "authorized_next_stage": D10_NEXT_STAGE,
        "deployment_authorized": False,
        "locked_test_accessed": False,
        "artifact_count": len(expected_paths),
        "artifacts": [p.as_posix() for p in expected_paths],
        "missing_artifacts": [],
        "empty_artifacts": [],
        "evidence_package_status": "PASS",
    }


# ============================================================
# D10.37 — COMMAND-LINE REPORT GENERATION
# ============================================================

if __name__ == "__main__":
    import pprint

    print("\nD10 REPORTING INPUT VALIDATION")
    print("=" * 60)
    pprint.pp(validate_d10_reporting_inputs())

    print("\nD10 EVIDENCE PACKAGE GENERATION")
    print("=" * 60)
    pprint.pp(generate_d10_evidence_package())
