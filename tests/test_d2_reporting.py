# ============================================================
# D2 — GOVERNANCE ARTIFACT TESTS
# ============================================================

from pathlib import Path

import pandas as pd
import yaml

from src.data.quality_reporting import (
    OUTPUT_FILES,
    generate_d2_evidence_package,
)


# ============================================================
# 1. ARTIFACT GENERATION
# ============================================================

def test_d2_evidence_package_generation():
    result = generate_d2_evidence_package()

    assert result["status"] == "SUCCESS"

    assert (
        result["gate_decision"]
        == "CONDITIONAL PASS"
    )

    assert (
        result["clinical_deployment_status"]
        == "NOT APPROVED"
    )


# ============================================================
# 2. ALL NINE ARTIFACTS EXIST
# ============================================================

def test_all_d2_artifacts_exist():
    assert len(OUTPUT_FILES) == 9

    for path in OUTPUT_FILES.values():
        assert path.exists()
        assert path.is_file()
        assert path.stat().st_size > 0


# ============================================================
# 3. SCORECARD CONTRACT
# ============================================================

def test_d2_scorecard_contract():
    scorecard = pd.read_csv(
        OUTPUT_FILES["scorecard"]
    )

    expected_dimensions = {
        "Accuracy / Conformance",
        "Completeness",
        "Currency",
        "Consistency",
        "Representation",
        "Bias",
    }

    assert len(scorecard) == 6

    assert (
        set(scorecard["dimension"])
        == expected_dimensions
    )

    assert (
        set(scorecard["status"])
        == {"CONDITIONAL PASS"}
    )


# ============================================================
# 4. ISSUE LOG CONTRACT
# ============================================================

def test_d2_issue_log_contract():
    issue_log = pd.read_csv(
        OUTPUT_FILES["issue_log"]
    )

    assert len(issue_log) == 10

    assert issue_log["issue_id"].is_unique

    assert issue_log["issue_id"].notna().all()

    assert {
        "dimension",
        "severity",
        "downstream_impact",
        "control",
        "status",
    }.issubset(issue_log.columns)


# ============================================================
# 5. BIAS RISK REGISTER CONTRACT
# ============================================================

def test_d2_bias_register_contract():
    register = pd.read_csv(
        OUTPUT_FILES["bias_register"]
    )

    expected_risks = {
        "Temporal bias",
        "Representation bias",
        "Measurement / missingness bias",
        "Repeated-patient weighting",
        "Label / outcome bias",
    }

    assert len(register) == 5

    assert register["risk_id"].is_unique

    assert (
        set(register["risk_type"])
        == expected_risks
    )


# ============================================================
# 6. REPRESENTATION ARTIFACT CONTRACT
# ============================================================

def test_d2_representation_artifact():
    representation = pd.read_csv(
        OUTPUT_FILES["representation"]
    )

    assert {
        "analysis_level",
        "dimension",
        "category",
        "count",
        "percentage",
    }.issubset(representation.columns)

    assert set(
        representation["analysis_level"]
    ) == {
        "encounter",
        "patient",
    }

    assert set(
        representation["dimension"]
    ) == {
        "age",
        "gender",
        "race",
    }


# ============================================================
# 7. SUBGROUP MEASUREMENT ARTIFACT CONTRACT
# ============================================================

def test_d2_subgroup_measurement_artifact():
    audit = pd.read_csv(
        OUTPUT_FILES["subgroup_measurement"]
    )

    assert {
        "dimension",
        "group",
        "encounters",
    }.issubset(audit.columns)

    assert set(
        audit["dimension"]
    ) == {
        "race",
        "gender",
        "age",
    }


# ============================================================
# 8. FORMAL GATE DECISION
# ============================================================

def test_d2_gate_decision():
    text = OUTPUT_FILES[
        "gate_decision"
    ].read_text(
        encoding="utf-8"
    )

    assert "CONDITIONAL PASS" in text

    assert (
        "NOT APPROVED FOR CLINICAL DEPLOYMENT"
        in text
    )

    assert (
        "D3 — Cohort & Outcome"
        in text
    )


# ============================================================
# 9. MASTER AUDIT REPORT
# ============================================================

def test_d2_master_audit_report():
    text = OUTPUT_FILES[
        "audit_report"
    ].read_text(
        encoding="utf-8"
    )

    required_sections = [
        "Accuracy / Conformance",
        "Completeness",
        "Currency",
        "Consistency",
        "Representation",
        "Pre-Model Bias Assessment",
        "Overall D2 Decision",
    ]

    for section in required_sections:
        assert section in text


# ============================================================
# 10. MANIFEST CONTRACT
# ============================================================

def test_d2_manifest_contract():
    with OUTPUT_FILES[
        "manifest"
    ].open(
        "r",
        encoding="utf-8",
    ) as file:

        manifest = yaml.safe_load(file)

    assert (
        manifest["gate_decision"]
        == "CONDITIONAL PASS"
    )

    assert (
        manifest[
            "clinical_deployment_status"
        ]
        == "NOT APPROVED"
    )

    assert manifest["framework"] == [
        "Accuracy",
        "Completeness",
        "Currency",
        "Consistency",
        "Representation",
        "Bias",
    ]

    assert len(
        manifest["generated_files"]
    ) == 8


# ============================================================
# 11. COMPLETENESS ARTIFACT EXISTS AND IS POPULATED
# ============================================================

def test_d2_completeness_artifact():
    completeness = pd.read_csv(
        OUTPUT_FILES["completeness"]
    )

    assert not completeness.empty

    assert len(completeness) == 50