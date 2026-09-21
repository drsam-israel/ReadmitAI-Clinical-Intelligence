# ============================================================
# D10 — FAIRNESS & SUBGROUP EVALUATION REPORTING TESTS
# ============================================================
from __future__ import annotations
from pathlib import Path
import pandas as pd
import pytest
import yaml
from src.models import fairness_reporting as d10r

@pytest.fixture(scope="session")
def reporting_input_validation():
    return d10r.validate_d10_reporting_inputs()

@pytest.fixture(scope="session")
def evidence_package():
    return d10r.generate_d10_evidence_package()

@pytest.fixture(scope="session")
def manifest():
    path = Path("artifacts/manifests/D10_fairness_subgroup_manifest.yaml")
    assert path.exists()
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)

@pytest.fixture(scope="session")
def subgroup_performance():
    return pd.read_csv("reports/tables/D10_subgroup_performance.csv")

@pytest.fixture(scope="session")
def disparity_summary():
    return pd.read_csv("reports/tables/D10_disparity_summary.csv")

@pytest.fixture(scope="session")
def subgroup_uncertainty():
    return pd.read_csv("reports/tables/D10_subgroup_uncertainty.csv")

@pytest.fixture(scope="session")
def subgroup_calibration():
    return pd.read_csv("reports/tables/D10_subgroup_calibration.csv")

@pytest.fixture(scope="session")
def subgroup_calibration_bins():
    return pd.read_csv("reports/tables/D10_subgroup_calibration_bins.csv")

@pytest.fixture(scope="session")
def governance_findings():
    return pd.read_csv("reports/tables/D10_governance_findings_registry.csv")

# ============================================================
# D10.R01 — REPORTING INPUT VALIDATION
# ============================================================
def test_reporting_input_validation_passes(reporting_input_validation):
    assert reporting_input_validation["validation_status"] == "PASS"
    assert reporting_input_validation["failed_components"] == []

def test_reporting_validates_all_components(reporting_input_validation):
    assert reporting_input_validation["validated_components"] == [
        "static_contract", "cross_stage_alignment", "fairness_evaluation_frame",
        "stability_policy", "subgroup_performance", "disparity_analysis",
        "subgroup_uncertainty", "subgroup_calibration", "governance_findings",
    ]

# ============================================================
# D10.R02 — EVIDENCE PACKAGE & LIFECYCLE GATE
# ============================================================
def test_evidence_package_passes(evidence_package):
    assert evidence_package["stage"] == "D10"
    assert evidence_package["validation_status"] == "PASS"
    assert evidence_package["evidence_package_status"] == "PASS"

def test_evidence_package_has_nine_artifacts(evidence_package):
    assert evidence_package["artifact_count"] == 9
    assert len(evidence_package["artifacts"]) == 9
    assert evidence_package["missing_artifacts"] == []
    assert evidence_package["empty_artifacts"] == []

def test_expected_artifact_paths(evidence_package):
    expected = {
        "artifacts/manifests/D10_fairness_subgroup_manifest.yaml",
        "reports/governance/D10_fairness_subgroup_contract.md",
        "reports/governance/D10_fairness_subgroup_gate_decision.md",
        "reports/tables/D10_subgroup_performance.csv",
        "reports/tables/D10_disparity_summary.csv",
        "reports/tables/D10_subgroup_uncertainty.csv",
        "reports/tables/D10_subgroup_calibration.csv",
        "reports/tables/D10_subgroup_calibration_bins.csv",
        "reports/tables/D10_governance_findings_registry.csv",
    }
    assert set(evidence_package["artifacts"]) == expected

def test_all_artifacts_exist_and_nonempty(evidence_package):
    for artifact in evidence_package["artifacts"]:
        p = Path(artifact)
        assert p.is_file(), artifact
        assert p.stat().st_size > 0, artifact

def test_gate_is_conditional_pass(evidence_package):
    assert evidence_package["gate_decision"] == "CONDITIONAL PASS"

def test_gate_authorizes_d11(evidence_package):
    assert evidence_package["authorized_next_stage"] == "D11 — Robustness & Transportability"

def test_no_deployment_or_locked_test(evidence_package):
    assert evidence_package["deployment_authorized"] is False
    assert evidence_package["locked_test_accessed"] is False

# ============================================================
# D10.R03 — MANIFEST & GOVERNANCE DOCUMENTS
# ============================================================
def test_manifest_is_nonempty_mapping(manifest):
    assert isinstance(manifest, dict)
    assert manifest

def test_manifest_contains_d10_governance_context(manifest):
    text = str(manifest).lower()
    assert "d10" in text
    assert "fairness" in text
    assert "validation" in text
    assert "deployment" in text
    assert "locked" in text
    assert "test" in text

def test_governance_contract_exists():
    p = Path("reports/governance/D10_fairness_subgroup_contract.md")
    text = p.read_text(encoding="utf-8")
    assert text.strip()
    assert "D10" in text
    assert "fairness" in text.lower()

def test_gate_document_preserves_conditional_progression():
    p = Path("reports/governance/D10_fairness_subgroup_gate_decision.md")
    text = p.read_text(encoding="utf-8")
    assert "CONDITIONAL PASS" in text
    assert "D11" in text
    assert "deployment" in text.lower()

# ============================================================
# D10.R04 — TABLE ARTIFACT INTEGRITY
# ============================================================
def test_subgroup_performance_integrity(subgroup_performance):
    assert len(subgroup_performance) == 18
    assert set(subgroup_performance["subgroup"]) == {"race", "gender", "age"}
    counts = subgroup_performance["support_classification"].value_counts().to_dict()
    assert counts.get("ADEQUATE_SUPPORT", 0) == 14
    assert counts.get("LOW_SUPPORT", 0) == 4

def test_unknown_race_retained(subgroup_performance):
    row = subgroup_performance[
        (subgroup_performance["subgroup"] == "race")
        & (subgroup_performance["subgroup_value"].astype(str) == "?")
    ]
    assert len(row) == 1
    assert int(row.iloc[0]["encounter_count"]) == 345

def test_disparity_summary_integrity(disparity_summary):
    assert len(disparity_summary) == 39
    assert disparity_summary.groupby("subgroup").size().to_dict() == {
        "age": 13, "gender": 13, "race": 13
    }
    eligible = disparity_summary.groupby("subgroup")["eligible_group_count"].first().astype(int).to_dict()
    assert eligible == {"age": 8, "gender": 2, "race": 3}

def test_uncertainty_integrity(subgroup_uncertainty):
    assert len(subgroup_uncertainty) == 18
    assert len([c for c in subgroup_uncertainty.columns if c.endswith("_ci_lower")]) == 8
    assert len([c for c in subgroup_uncertainty.columns if c.endswith("_ci_upper")]) == 8
    assert int((subgroup_uncertainty["support_classification"] == "LOW_SUPPORT").sum()) == 4

def test_calibration_summary_integrity(subgroup_calibration):
    assert len(subgroup_calibration) == 18

def test_calibration_bins_integrity(subgroup_calibration_bins):
    assert len(subgroup_calibration_bins) == 90

def test_calibration_bins_reconcile(subgroup_calibration_bins, subgroup_calibration):
    observed = subgroup_calibration_bins.groupby(
        ["subgroup", "subgroup_value"], dropna=False
    )["encounter_count"].sum().sort_index()
    expected = subgroup_calibration.set_index(
        ["subgroup", "subgroup_value"]
    )["encounter_count"].sort_index()
    pd.testing.assert_series_equal(
        observed.astype(int), expected.astype(int), check_names=False
    )

# ============================================================
# D10.R05 — GOVERNANCE FINDINGS ARTIFACT
# ============================================================
def test_governance_findings_complete(governance_findings):
    assert len(governance_findings) == 7
    assert governance_findings["finding_id"].tolist() == [
        "D10-F01", "D10-F02", "D10-F03", "D10-F04",
        "D10-F05", "D10-F06", "D10-F07",
    ]

def test_governance_dispositions(governance_findings):
    assert governance_findings["disposition"].value_counts().to_dict() == {
        "REVIEW_REQUIRED": 2,
        "CLINICAL_REVIEW_REQUIRED": 1,
        "MONITOR": 1,
        "MONITOR_AND_REVIEW": 1,
        "INSUFFICIENT_EVIDENCE": 1,
        "DATA_GOVERNANCE_REVIEW": 1,
    }

def test_findings_do_not_authorize_prohibited_actions(governance_findings):
    columns = [
        "fairness_violation_determined", "causal_bias_determined",
        "subgroup_threshold_change_authorized", "automatic_mitigation_authorized",
        "model_recalibration_authorized", "deployment_authorized",
        "locked_test_accessed",
    ]
    for column in columns:
        assert column in governance_findings.columns
        normalized = governance_findings[column].astype(str).str.strip().str.lower()
        assert normalized.isin({"false", "0"}).all(), column

def test_f01_clinical_review_required(governance_findings):
    row = governance_findings.set_index("finding_id").loc["D10-F01"]
    assert row["disposition"] == "CLINICAL_REVIEW_REQUIRED"
    assert row["deployment_implication"] == "UNRESOLVED_BEFORE_DEPLOYMENT"

def test_f06_evidence_limitation(governance_findings):
    row = governance_findings.set_index("finding_id").loc["D10-F06"]
    assert row["disposition"] == "INSUFFICIENT_EVIDENCE"
    assert row["deployment_implication"] == "EVIDENCE_LIMITATION_TO_CARRY_FORWARD"

def test_f07_data_governance_action(governance_findings):
    row = governance_findings.set_index("finding_id").loc["D10-F07"]
    assert row["disposition"] == "DATA_GOVERNANCE_REVIEW"
    assert row["deployment_implication"] == "DATA_QUALITY_ACTION_REQUIRED"
