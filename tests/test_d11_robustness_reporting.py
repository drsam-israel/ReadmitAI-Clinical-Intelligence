# ============================================================
# D11 — ROBUSTNESS & TRANSPORTABILITY REPORTING TEST SUITE
# ============================================================
"""
Regression tests for the D11 reporting and governance-evidence layer.

These tests verify that validated D11 runtime evidence is converted
into a complete, internally consistent, reviewable evidence package
without changing the frozen clinical AI system.

The reporting package must preserve:
- 12 governed artifacts;
- validation-only evaluation;
- frozen D7/D8/D9 lifecycle identities;
- 2 synthetic assessments;
- 35 observed-slice assessments;
- 6 adequate-support heterogeneity findings;
- 12 low-support limitations;
- 6 mandatory carry-forward actions;
- progression to D12 only;
- locked TEST isolation;
- no deployment authorization;
- no unsupported external transportability claims.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.models import robustness as d11
from src.models import robustness_reporting as reporting


# ============================================================
# SECTION 01 — EXPECTED GOVERNANCE VALUES
# ============================================================

EXPECTED_ARTIFACT_COUNT = 12

EXPECTED_DISPOSITION = (
    "CONDITIONAL_PASS_PROGRESS_WITH_DOCUMENTED_ROBUSTNESS_FINDINGS"
)

EXPECTED_SYNTHETIC_ROWS = 2
EXPECTED_OBSERVED_ROWS = 35
EXPECTED_COMPARISON_ROWS = 37
EXPECTED_HETEROGENEITY_ROWS = 6
EXPECTED_LOW_SUPPORT_ROWS = 12
EXPECTED_ACTION_ROWS = 6
EXPECTED_REGISTRY_ROWS = 9
EXPECTED_INTEGRITY_ROWS = 11

EXPECTED_HETEROGENEITY_SLICES = {
    ("D11-STRESS-004", "admission_source_id=6"),
    ("D11-STRESS-005", "prior_utilization_domain_count=0"),
    ("D11-STRESS-006", "prior_utilization_domain_count=1"),
    ("D11-STRESS-007", "prior_utilization_domain_count>=2"),
    ("D11-STRESS-008", "prior_utilization_intensity>=3"),
    ("D11-STRESS-009", "age=[20-30)"),
}

EXPECTED_ARTIFACT_PATHS = (
    reporting.D11_MANIFEST_PATH,
    reporting.D11_CONTRACT_PATH,
    reporting.D11_GATE_PATH,
    reporting.D11_BASELINE_TABLE_PATH,
    reporting.D11_REGISTRY_TABLE_PATH,
    reporting.D11_SYNTHETIC_TABLE_PATH,
    reporting.D11_OBSERVED_TABLE_PATH,
    reporting.D11_COMPARISON_TABLE_PATH,
    reporting.D11_HETEROGENEITY_TABLE_PATH,
    reporting.D11_LOW_SUPPORT_TABLE_PATH,
    reporting.D11_ACTIONS_TABLE_PATH,
    reporting.D11_INTEGRITY_TABLE_PATH,
)


# ============================================================
# SECTION 02 — TEST HELPERS
# ============================================================

def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a governed CSV artifact as dictionaries."""

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def read_utf8(path: Path) -> str:
    """Read a governed text artifact using its required encoding."""

    return path.read_text(encoding="utf-8")


def parse_simple_manifest(path: Path) -> dict[str, str]:
    """
    Parse the deliberately flat D11 YAML manifest.

    The production writer intentionally emits one scalar key/value
    pair per line, so a full YAML dependency is unnecessary here.
    """

    result: dict[str, str] = {}

    for raw_line in read_utf8(path).splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()

    return result


# ============================================================
# SECTION 03 — REPORTING IDENTITY & PATH CONTRACT
# ============================================================

def test_d11_reporting_stage_identity():
    assert reporting.D11_REPORTING_STAGE == "D11"


def test_d11_reporting_package_name():
    assert (
        reporting.D11_REPORTING_NAME
        == "Robustness & Transportability Evidence Package"
    )


def test_d11_reporting_defines_exactly_twelve_artifacts():
    assert len(EXPECTED_ARTIFACT_PATHS) == EXPECTED_ARTIFACT_COUNT
    assert len(set(EXPECTED_ARTIFACT_PATHS)) == EXPECTED_ARTIFACT_COUNT


def test_d11_reporting_artifact_names_are_stage_scoped():
    for path in EXPECTED_ARTIFACT_PATHS:
        assert path.name.startswith("D11_")


# ============================================================
# SECTION 04 — VALIDATED EVIDENCE BUNDLE
# ============================================================

@pytest.fixture(scope="module")
def evidence_bundle():
    return reporting.build_d11_reporting_evidence_bundle()


def test_d11_reporting_evidence_bundle_passes(evidence_bundle):
    assert evidence_bundle["validation_status"] == "PASS"


def test_d11_reporting_bundle_contains_required_runtime_layers(
    evidence_bundle,
):
    expected = {
        "static",
        "boundary",
        "baseline",
        "registry",
        "execution_path",
        "stress",
        "comparison",
        "disposition",
        "validation_status",
    }

    assert expected.issubset(evidence_bundle.keys())


def test_d11_reporting_bundle_runtime_validators_pass(
    evidence_bundle,
):
    for key in (
        "static",
        "boundary",
        "baseline",
        "registry",
        "execution_path",
        "comparison",
        "disposition",
    ):
        assert evidence_bundle[key]["validation_status"] == "PASS"


def test_d11_reporting_bundle_preserves_frozen_system(
    evidence_bundle,
):
    stress = evidence_bundle["stress"]

    assert stress["model_retrained"] is False
    assert stress["hyperparameters_retuned"] is False
    assert stress["preprocessor_refitted"] is False
    assert stress["threshold_retuned"] is False
    assert stress["locked_test_accessed"] is False
    assert stress["deployment_authorized"] is False


def test_d11_reporting_bundle_preserves_final_disposition(
    evidence_bundle,
):
    disposition = evidence_bundle["disposition"]

    assert disposition["disposition"] == EXPECTED_DISPOSITION
    assert disposition["progression_authorized"] is True
    assert disposition["next_lifecycle_stage"] == "D12"
    assert disposition["deployment_authorized"] is False


# ============================================================
# SECTION 05 — GENERATE & VALIDATE COMPLETE PACKAGE
# ============================================================

@pytest.fixture(scope="module")
def generated_package():
    return reporting.validate_d11_robustness_reporting_package()


def test_d11_reporting_package_passes(generated_package):
    assert generated_package["validation_status"] == "PASS"
    assert generated_package["failed_checks"] == []


def test_d11_reporting_package_has_twelve_artifacts(
    generated_package,
):
    assert (
        generated_package["artifact_count"]
        == EXPECTED_ARTIFACT_COUNT
    )


def test_d11_reporting_package_disposition(generated_package):
    assert generated_package["disposition"] == EXPECTED_DISPOSITION


def test_d11_reporting_package_progresses_only_to_d12(
    generated_package,
):
    assert generated_package["progression_authorized"] is True
    assert generated_package["next_lifecycle_stage"] == "D12"
    assert generated_package["deployment_authorized"] is False


def test_d11_reporting_package_evidence_profile(
    generated_package,
):
    assert generated_package["synthetic_review_count"] == 0

    assert (
        generated_package["observed_heterogeneity_review_count"]
        == EXPECTED_HETEROGENEITY_ROWS
    )

    assert (
        generated_package["low_support_limitation_count"]
        == EXPECTED_LOW_SUPPORT_ROWS
    )

    assert (
        generated_package["mandatory_carry_forward_action_count"]
        == EXPECTED_ACTION_ROWS
    )


def test_d11_reporting_package_does_not_access_locked_test(
    generated_package,
):
    assert generated_package["locked_test_accessed"] is False


# ============================================================
# SECTION 06 — PHYSICAL ARTIFACT COMPLETENESS
# ============================================================

def test_d11_all_expected_artifacts_exist(generated_package):
    assert generated_package["validation_status"] == "PASS"

    for path in EXPECTED_ARTIFACT_PATHS:
        assert path.exists(), f"Missing D11 artifact: {path}"


def test_d11_all_expected_artifacts_are_files(generated_package):
    for path in EXPECTED_ARTIFACT_PATHS:
        assert path.is_file(), f"Not a regular file: {path}"


def test_d11_all_expected_artifacts_are_nonempty(generated_package):
    for path in EXPECTED_ARTIFACT_PATHS:
        assert path.stat().st_size > 0, (
            f"D11 artifact is empty: {path}"
        )


# ============================================================
# SECTION 07 — BASELINE TABLE
# ============================================================

def test_d11_baseline_table_has_one_row(generated_package):
    rows = read_csv_rows(reporting.D11_BASELINE_TABLE_PATH)

    assert len(rows) == 1


def test_d11_baseline_table_preserves_population(
    generated_package,
):
    row = read_csv_rows(
        reporting.D11_BASELINE_TABLE_PATH
    )[0]

    assert int(row["encounter_count"]) == 15052
    assert int(row["positive_count"]) == 1692
    assert int(row["negative_count"]) == 13360


def test_d11_baseline_table_preserves_threshold(
    generated_package,
):
    row = read_csv_rows(
        reporting.D11_BASELINE_TABLE_PATH
    )[0]

    assert float(row["threshold"]) == pytest.approx(
        0.12,
        abs=1e-12,
    )


def test_d11_baseline_table_preserves_alert_count(
    generated_package,
):
    row = read_csv_rows(
        reporting.D11_BASELINE_TABLE_PATH
    )[0]

    assert int(row["predicted_positive_count"]) == 4709


# ============================================================
# SECTION 08 — STRESS REGISTRY & EXECUTION TABLES
# ============================================================

def test_d11_registry_table_has_nine_rows(generated_package):
    rows = read_csv_rows(reporting.D11_REGISTRY_TABLE_PATH)

    assert len(rows) == EXPECTED_REGISTRY_ROWS


def test_d11_registry_table_has_unique_scenario_ids(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_REGISTRY_TABLE_PATH)

    scenario_ids = [row["scenario_id"] for row in rows]

    assert len(scenario_ids) == len(set(scenario_ids))


def test_d11_synthetic_results_have_two_rows(generated_package):
    rows = read_csv_rows(reporting.D11_SYNTHETIC_TABLE_PATH)

    assert len(rows) == EXPECTED_SYNTHETIC_ROWS


def test_d11_observed_slice_results_have_thirty_five_rows(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_OBSERVED_TABLE_PATH)

    assert len(rows) == EXPECTED_OBSERVED_ROWS


def test_d11_comparison_table_has_thirty_seven_rows(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_COMPARISON_TABLE_PATH)

    assert len(rows) == EXPECTED_COMPARISON_ROWS


def test_d11_comparison_table_has_two_pathways(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_COMPARISON_TABLE_PATH)

    pathways = {
        row["assessment_pathway"]
        for row in rows
    }

    assert pathways == {
        "SYNTHETIC_SAME_POPULATION_DEGRADATION",
        "OBSERVED_SLICE_HETEROGENEITY",
    }


def test_d11_comparison_pathway_counts(generated_package):
    rows = read_csv_rows(reporting.D11_COMPARISON_TABLE_PATH)

    synthetic = [
        row
        for row in rows
        if row["assessment_pathway"]
        == "SYNTHETIC_SAME_POPULATION_DEGRADATION"
    ]

    observed = [
        row
        for row in rows
        if row["assessment_pathway"]
        == "OBSERVED_SLICE_HETEROGENEITY"
    ]

    assert len(synthetic) == 2
    assert len(observed) == 35


# ============================================================
# SECTION 09 — HETEROGENEITY FINDINGS
# ============================================================

def test_d11_heterogeneity_table_has_six_rows(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_HETEROGENEITY_TABLE_PATH
    )

    assert len(rows) == EXPECTED_HETEROGENEITY_ROWS


def test_d11_heterogeneity_table_contains_exact_expected_slices(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_HETEROGENEITY_TABLE_PATH
    )

    observed = {
        (
            row["scenario_id"],
            row["slice_name"],
        )
        for row in rows
    }

    assert observed == EXPECTED_HETEROGENEITY_SLICES


def test_d11_heterogeneity_findings_are_adequate_support(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_HETEROGENEITY_TABLE_PATH
    )

    assert all(
        row["support_status"] == "ADEQUATE_SUPPORT"
        for row in rows
    )


def test_d11_heterogeneity_findings_have_review_signals(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_HETEROGENEITY_TABLE_PATH
    )

    assert all(
        row["review_signals"].strip()
        not in {"", "[]"}
        for row in rows
    )


# ============================================================
# SECTION 10 — LOW-SUPPORT LIMITATIONS
# ============================================================

def test_d11_low_support_table_has_twelve_rows(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_LOW_SUPPORT_TABLE_PATH
    )

    assert len(rows) == EXPECTED_LOW_SUPPORT_ROWS


def test_d11_low_support_rows_are_not_adequate_support(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_LOW_SUPPORT_TABLE_PATH
    )

    assert all(
        row["support_status"] != "ADEQUATE_SUPPORT"
        for row in rows
    )


def test_d11_low_support_rows_preserve_limitation_label(
    generated_package,
):
    rows = read_csv_rows(
        reporting.D11_LOW_SUPPORT_TABLE_PATH
    )

    assert all(
        row["limitation"]
        == "LOW_SUPPORT_LIMITS_STRONG_INTERPRETATION"
        for row in rows
    )


# ============================================================
# SECTION 11 — CARRY-FORWARD ACTIONS
# ============================================================

def test_d11_actions_table_has_six_rows(generated_package):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    assert len(rows) == EXPECTED_ACTION_ROWS


def test_d11_action_ids_are_sequential(generated_package):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    assert [
        row["action_id"]
        for row in rows
    ] == [
        "D11-ACTION-01",
        "D11-ACTION-02",
        "D11-ACTION-03",
        "D11-ACTION-04",
        "D11-ACTION-05",
        "D11-ACTION-06",
    ]


def test_d11_action_order_is_sequential(generated_package):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    assert [
        int(row["action_order"])
        for row in rows
    ] == [1, 2, 3, 4, 5, 6]


def test_d11_all_carry_forward_actions_are_mandatory(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    assert all(
        row["mandatory"].lower() == "true"
        for row in rows
    )


def test_d11_actions_match_runtime_contract(generated_package):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    observed_actions = [
        row["action"]
        for row in rows
    ]

    assert observed_actions == list(
        d11.D11_MANDATORY_CARRY_FORWARD_ACTIONS
    )


# ============================================================
# SECTION 12 — GOVERNANCE CONTRACT DOCUMENT
# ============================================================

def test_d11_contract_identifies_validation_boundary(
    generated_package,
):
    text = read_utf8(reporting.D11_CONTRACT_PATH)

    assert "Evaluation partition: validation" in text
    assert "Locked TEST evaluation stage: D14" in text


def test_d11_contract_preserves_frozen_threshold(
    generated_package,
):
    text = read_utf8(reporting.D11_CONTRACT_PATH)

    assert "Frozen development threshold: 0.12" in text


def test_d11_contract_prohibits_lifecycle_mutation(
    generated_package,
):
    text = read_utf8(reporting.D11_CONTRACT_PATH).lower()

    assert "does not retrain or retune the model" in text
    assert "refit preprocessing" in text
    assert "retune the d9 threshold" in text
    assert "recalibrate the model" in text


def test_d11_contract_preserves_test_and_deployment_boundary(
    generated_package,
):
    text = read_utf8(reporting.D11_CONTRACT_PATH).lower()

    assert "access the locked test set" in text
    assert "authorize deployment" in text


def test_d11_contract_rejects_external_validity_overclaim(
    generated_package,
):
    text = read_utf8(reporting.D11_CONTRACT_PATH).lower()

    for term in (
        "external",
        "temporal",
        "geographic",
        "institutional",
        "prospective",
    ):
        assert term in text


def test_d11_contract_distinguishes_observed_heterogeneity(
    generated_package,
):
    text = read_utf8(reporting.D11_CONTRACT_PATH).lower()

    assert "observed slices characterize population heterogeneity" in text
    assert "causal effects" in text
    assert "external transportability failure" in text


# ============================================================
# SECTION 13 — GATE DECISION DOCUMENT
# ============================================================

def test_d11_gate_contains_conditional_pass(generated_package):
    text = read_utf8(reporting.D11_GATE_PATH)

    assert EXPECTED_DISPOSITION in text


def test_d11_gate_authorizes_d12_progression(generated_package):
    text = read_utf8(reporting.D11_GATE_PATH)

    assert "Progression authorized: **True**" in text
    assert "D12" in text
    assert "Explainability" in text


def test_d11_gate_does_not_authorize_deployment(
    generated_package,
):
    text = read_utf8(reporting.D11_GATE_PATH)

    assert "Deployment authorized: **False**" in text


def test_d11_gate_contains_evidence_counts(generated_package):
    text = read_utf8(reporting.D11_GATE_PATH)

    assert "Synthetic perturbation assessments: 2" in text
    assert "Synthetic degradation-review triggers: 0" in text
    assert "Observed-slice assessments: 35" in text
    assert "Adequate-support heterogeneity findings: 6" in text
    assert "Low-support interpretation limitations: 12" in text
    assert "Mandatory carry-forward actions: 6" in text


def test_d11_gate_preserves_interpretation_boundary(
    generated_package,
):
    text = read_utf8(reporting.D11_GATE_PATH).lower()

    assert "not automatic model failures" in text
    assert "causal interpretation" in text
    assert "observed-slice degradation claims are prohibited" in text


def test_d11_gate_contains_all_six_actions(generated_package):
    text = read_utf8(reporting.D11_GATE_PATH)

    for action in d11.D11_MANDATORY_CARRY_FORWARD_ACTIONS:
        assert action in text


# ============================================================
# SECTION 14 — MANIFEST CONSISTENCY
# ============================================================

def test_d11_manifest_identifies_stage(generated_package):
    manifest = parse_simple_manifest(
        reporting.D11_MANIFEST_PATH
    )

    assert manifest["stage"] == '"D11"'
    assert manifest["evaluation_partition"] == '"validation"'


def test_d11_manifest_preserves_evidence_counts(
    generated_package,
):
    manifest = parse_simple_manifest(
        reporting.D11_MANIFEST_PATH
    )

    assert manifest["stress_scenario_count"] == "9"
    assert manifest["synthetic_assessment_count"] == "2"
    assert manifest["synthetic_review_count"] == "0"
    assert manifest["observed_slice_assessment_count"] == "35"
    assert (
        manifest["observed_heterogeneity_review_count"]
        == "6"
    )
    assert manifest["low_support_limitation_count"] == "12"
    assert (
        manifest["mandatory_carry_forward_action_count"]
        == "6"
    )


def test_d11_manifest_preserves_disposition(generated_package):
    manifest = parse_simple_manifest(
        reporting.D11_MANIFEST_PATH
    )

    assert (
        manifest["disposition"]
        == f'"{EXPECTED_DISPOSITION}"'
    )

    assert manifest["progression_authorized"] == "true"
    assert manifest["next_lifecycle_stage"] == '"D12"'


def test_d11_manifest_preserves_locked_test_boundary(
    generated_package,
):
    manifest = parse_simple_manifest(
        reporting.D11_MANIFEST_PATH
    )

    assert manifest["locked_test_accessed"] == "false"
    assert manifest["deployment_authorized"] == "false"


def test_d11_manifest_rejects_external_validation_claims(
    generated_package,
):
    manifest = parse_simple_manifest(
        reporting.D11_MANIFEST_PATH
    )

    assert manifest["external_validation_established"] == "false"
    assert manifest["temporal_validation_established"] == "false"
    assert (
        manifest["geographic_transportability_established"]
        == "false"
    )
    assert (
        manifest["institutional_transportability_established"]
        == "false"
    )
    assert (
        manifest["prospective_validation_established"]
        == "false"
    )


# ============================================================
# SECTION 15 — ARTIFACT INTEGRITY TABLE
# ============================================================

def test_d11_integrity_table_has_eleven_hashed_artifacts(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_INTEGRITY_TABLE_PATH)

    # The integrity table deliberately excludes itself.
    assert len(rows) == EXPECTED_INTEGRITY_ROWS


def test_d11_integrity_table_excludes_itself(generated_package):
    rows = read_csv_rows(reporting.D11_INTEGRITY_TABLE_PATH)

    artifact_names = {
        Path(row["artifact"]).name
        for row in rows
    }

    assert reporting.D11_INTEGRITY_TABLE_PATH.name not in artifact_names


def test_d11_integrity_table_reports_all_artifacts_existing(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_INTEGRITY_TABLE_PATH)

    assert all(
        row["exists"].lower() == "true"
        for row in rows
    )


def test_d11_integrity_table_reports_nonzero_sizes(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_INTEGRITY_TABLE_PATH)

    assert all(
        int(row["size_bytes"]) > 0
        for row in rows
    )


def test_d11_integrity_sha256_values_have_expected_shape(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_INTEGRITY_TABLE_PATH)

    for row in rows:
        digest = row["sha256"]

        assert len(digest) == 64
        assert digest == digest.upper()
        assert all(
            character in "0123456789ABCDEF"
            for character in digest
        )


def test_d11_integrity_hashes_match_physical_artifacts(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_INTEGRITY_TABLE_PATH)

    for row in rows:
        path = Path(row["artifact"])

        assert path.exists()

        observed_sha256 = reporting._sha256(path)

        assert observed_sha256 == row["sha256"]


# ============================================================
# SECTION 16 — CROSS-ARTIFACT CONSISTENCY
# ============================================================

def test_d11_heterogeneity_rows_do_not_overlap_low_support_rows(
    generated_package,
):
    heterogeneity = read_csv_rows(
        reporting.D11_HETEROGENEITY_TABLE_PATH
    )

    low_support = read_csv_rows(
        reporting.D11_LOW_SUPPORT_TABLE_PATH
    )

    heterogeneity_keys = {
        (row["scenario_id"], row["slice_name"])
        for row in heterogeneity
    }

    low_support_keys = {
        (row["scenario_id"], row["slice_name"])
        for row in low_support
    }

    assert heterogeneity_keys.isdisjoint(low_support_keys)


def test_d11_all_heterogeneity_rows_exist_in_observed_results(
    generated_package,
):
    findings = read_csv_rows(
        reporting.D11_HETEROGENEITY_TABLE_PATH
    )

    observed = read_csv_rows(
        reporting.D11_OBSERVED_TABLE_PATH
    )

    observed_keys = {
        (row["scenario_id"], row["slice_name"])
        for row in observed
    }

    for row in findings:
        assert (
            row["scenario_id"],
            row["slice_name"],
        ) in observed_keys


def test_d11_all_low_support_rows_exist_in_observed_results(
    generated_package,
):
    limitations = read_csv_rows(
        reporting.D11_LOW_SUPPORT_TABLE_PATH
    )

    observed = read_csv_rows(
        reporting.D11_OBSERVED_TABLE_PATH
    )

    observed_keys = {
        (row["scenario_id"], row["slice_name"])
        for row in observed
    }

    for row in limitations:
        assert (
            row["scenario_id"],
            row["slice_name"],
        ) in observed_keys


def test_d11_comparison_table_preserves_total_evidence_rows(
    generated_package,
):
    comparison = read_csv_rows(
        reporting.D11_COMPARISON_TABLE_PATH
    )

    assert len(comparison) == (
        EXPECTED_SYNTHETIC_ROWS
        + EXPECTED_OBSERVED_ROWS
    )


# ============================================================
# SECTION 17 — FINAL REPORTING SAFETY REGRESSION
# ============================================================

def test_d11_reporting_does_not_convert_progression_to_deployment(
    generated_package,
):
    assert generated_package["progression_authorized"] is True
    assert generated_package["next_lifecycle_stage"] == "D12"
    assert generated_package["deployment_authorized"] is False


def test_d11_reporting_retains_d14_locked_test_action(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    actions = " ".join(
        row["action"]
        for row in rows
    )

    assert "D14" in actions
    assert "locked TEST partition" in actions
    assert "without validation-driven threshold retuning" in actions


def test_d11_reporting_retains_external_validation_limitation(
    generated_package,
):
    rows = read_csv_rows(reporting.D11_ACTIONS_TABLE_PATH)

    actions = " ".join(
        row["action"]
        for row in rows
    ).lower()

    assert "do not authorize clinical deployment" in actions
    assert "external" in actions
    assert "temporal" in actions
    assert "institutional/geographic" in actions
    assert "prospective validation" in actions