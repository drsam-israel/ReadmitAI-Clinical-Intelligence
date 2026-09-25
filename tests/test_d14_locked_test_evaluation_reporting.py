# ============================================================
# D14 — LOCKED-TEST REPORTING & EVIDENCE TESTS
# ============================================================


from __future__ import annotations

from pathlib import Path

import pytest

import src.models.locked_test_evaluation as d14
import src.models.locked_test_evaluation_reporting as report


# ============================================================
# MODULE-SCOPED REPORTING BUNDLE
# ============================================================


@pytest.fixture(scope="module")
def reporting_bundle():
    return report.build_d14_reporting_bundle()


@pytest.fixture(scope="module")
def reporting_validation(
    reporting_bundle,
):
    return report.validate_d14_reporting_bundle(
        reporting_bundle
    )


# ============================================================
# REPORTING BUNDLE
# ============================================================


def test_d14_reporting_bundle_contains_all_domains(
    reporting_bundle,
):
    expected = {
        "performance",
        "subgroup",
        "robustness",
        "explainability",
        "residual_risks",
        "integrated_evidence",
        "gate",
        "final_record",
    }

    assert expected.issubset(
        reporting_bundle.keys()
    )


def test_d14_reporting_bundle_preserves_registry_identity(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "registry_id"
    ] == d14.D14_EXPECTED_REGISTRY_ID


def test_d14_reporting_bundle_preserves_candidate_hash(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "candidate_system_sha256"
    ] == d14.D14_EXPECTED_CANDIDATE_SYSTEM_SHA256


def test_d14_reporting_bundle_preserves_gate_pass(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "gate_integrity_status"
    ] == "PASS"


def test_d14_reporting_bundle_preserves_disposition(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "disposition"
    ] == d14.D14_FINAL_DISPOSITION


def test_d14_reporting_bundle_preserves_d15_progression(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "next_lifecycle_stage"
    ] == d14.D14_FINAL_NEXT_STAGE


def test_d14_reporting_bundle_preserves_seven_risks(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "residual_risk_count"
    ] == 7

    assert reporting_bundle[
        "final_record"
    ][
        "unresolved_residual_risk_count"
    ] == 7


def test_d14_reporting_bundle_does_not_authorize_deployment(
    reporting_bundle,
):
    assert reporting_bundle[
        "final_record"
    ][
        "deployment_authorized"
    ] is False


# ============================================================
# REPORTING VALIDATION
# ============================================================


def test_d14_reporting_validation_passes(
    reporting_validation,
):
    assert reporting_validation[
        "overall_pass"
    ] is True

    assert reporting_validation[
        "validation_status"
    ] == "PASS"


@pytest.mark.parametrize(
    "check_name",
    [
        "performance_validation_passed",
        "subgroup_validation_passed",
        "robustness_validation_passed",
        "explainability_validation_passed",
        "gate_integrity_passed",
        "disposition_preserved",
        "next_stage_preserved",
        "seven_residual_risks_retained",
        "all_residual_risks_unresolved",
        "external_validation_not_claimed",
        "clinical_effectiveness_not_claimed",
        "deployment_not_authorized",
    ],
)
def test_d14_each_reporting_validation_check_passes(
    reporting_validation,
    check_name,
):
    assert reporting_validation[
        "checks"
    ][
        check_name
    ] is True


# ============================================================
# PERFORMANCE TABLE
# ============================================================


def test_d14_performance_reporting_has_one_row(
    reporting_bundle,
):
    rows = report.build_d14_performance_rows(
        reporting_bundle
    )

    assert len(
        rows
    ) == 1


def test_d14_performance_reporting_preserves_test_population(
    reporting_bundle,
):
    row = report.build_d14_performance_rows(
        reporting_bundle
    )[0]

    assert row[
        "encounter_count"
    ] == d14.D14_EXPECTED_TEST_ENCOUNTERS

    assert row[
        "positive_count"
    ] == d14.D14_EXPECTED_TEST_POSITIVES

    assert row[
        "negative_count"
    ] == d14.D14_EXPECTED_TEST_NEGATIVES


def test_d14_performance_reporting_preserves_pr_auc(
    reporting_bundle,
):
    row = report.build_d14_performance_rows(
        reporting_bundle
    )[0]

    assert row[
        "pr_auc"
    ] == pytest.approx(
        0.182040618234,
        abs=1e-12,
    )


def test_d14_performance_reporting_preserves_roc_auc(
    reporting_bundle,
):
    row = report.build_d14_performance_rows(
        reporting_bundle
    )[0]

    assert row[
        "roc_auc"
    ] == pytest.approx(
        0.623405163566,
        abs=1e-12,
    )


# ============================================================
# VALIDATION-TEST COMPARISON
# ============================================================


def test_d14_validation_test_comparison_is_not_empty(
    reporting_bundle,
):
    rows = (
        report.build_d14_validation_test_comparison_rows(
            reporting_bundle
        )
    )

    assert len(
        rows
    ) > 0


def test_d14_validation_test_comparison_contains_pr_auc(
    reporting_bundle,
):
    rows = (
        report.build_d14_validation_test_comparison_rows(
            reporting_bundle
        )
    )

    metrics = {
        row[
            "metric"
        ]
        for row in rows
    }

    assert "pr_auc" in metrics


def test_d14_validation_test_comparison_contains_roc_auc(
    reporting_bundle,
):
    rows = (
        report.build_d14_validation_test_comparison_rows(
            reporting_bundle
        )
    )

    metrics = {
        row[
            "metric"
        ]
        for row in rows
    }

    assert "roc_auc" in metrics


# ============================================================
# SUBGROUP / ROBUSTNESS / EXPLAINABILITY TABLES
# ============================================================


def test_d14_subgroup_reporting_has_18_rows(
    reporting_bundle,
):
    rows = report.build_d14_subgroup_rows(
        reporting_bundle
    )

    assert len(
        rows
    ) == 18


def test_d14_robustness_reporting_has_35_rows(
    reporting_bundle,
):
    rows = report.build_d14_robustness_rows(
        reporting_bundle
    )

    assert len(
        rows
    ) == 35


def test_d14_explainability_reporting_has_10_source_families(
    reporting_bundle,
):
    rows = report.build_d14_explainability_rows(
        reporting_bundle
    )

    assert len(
        rows
    ) == 10


def test_d14_local_explanation_reporting_has_five_cases(
    reporting_bundle,
):
    rows = report.build_d14_local_explanation_rows(
        reporting_bundle
    )

    assert len(
        rows
    ) == 5


def test_d14_residual_risk_reporting_has_seven_rows(
    reporting_bundle,
):
    rows = report.build_d14_residual_risk_rows(
        reporting_bundle
    )

    assert len(
        rows
    ) == 7


# ============================================================
# GOVERNANCE DOCUMENTS
# ============================================================


def test_d14_contract_identifies_locked_test(
    reporting_bundle,
):
    text = (
        report.build_d14_evaluation_contract_markdown(
            reporting_bundle
        )
    )

    assert "Locked-Test Evaluation" in text
    assert "LOCKED_TEST" in text


def test_d14_contract_prohibits_test_driven_retraining(
    reporting_bundle,
):
    text = (
        report.build_d14_evaluation_contract_markdown(
            reporting_bundle
        )
    )

    assert "retrain the candidate" in text


def test_d14_contract_explicitly_denies_deployment_authorization(
    reporting_bundle,
):
    text = (
        report.build_d14_evaluation_contract_markdown(
            reporting_bundle
        )
    )

    assert (
        "**Deployment authorized:** False"
        in text
    )


def test_d14_gate_document_preserves_conditional_pass(
    reporting_bundle,
):
    text = (
        report.build_d14_gate_decision_markdown(
            reporting_bundle
        )
    )

    assert (
        d14.D14_FINAL_DISPOSITION
        in text
    )


def test_d14_gate_document_preserves_external_validation_boundary(
    reporting_bundle,
):
    text = (
        report.build_d14_gate_decision_markdown(
            reporting_bundle
        )
    )

    assert (
        "does **not** establish external validation"
        in text
    )


# ============================================================
# REPORTING PATH CONTRACT
# ============================================================


@pytest.mark.parametrize(
    "path",
    [
        report.D14_MANIFEST_PATH,
        report.D14_CONTRACT_PATH,
        report.D14_GATE_DECISION_PATH,
        report.D14_FINAL_GOVERNANCE_RECORD_PATH,
        report.D14_PERFORMANCE_TABLE_PATH,
        report.D14_VALIDATION_TEST_COMPARISON_PATH,
        report.D14_SUBGROUP_TABLE_PATH,
        report.D14_ROBUSTNESS_TABLE_PATH,
        report.D14_EXPLAINABILITY_TABLE_PATH,
        report.D14_LOCAL_EXPLANATION_TABLE_PATH,
        report.D14_RESIDUAL_RISK_TABLE_PATH,
    ],
)
def test_d14_reporting_paths_are_inside_project(
    path,
):
    assert isinstance(
        path,
        Path
    )

    assert report.PROJECT_ROOT in (
        path.parents
    )


# ============================================================
# FAIL-CLOSED REPORTING VALIDATION
# ============================================================


def test_d14_reporting_validation_fails_if_deployment_authorized(
    reporting_bundle,
):
    tampered = dict(
        reporting_bundle
    )

    final_record = dict(
        reporting_bundle[
            "final_record"
        ]
    )

    final_record[
        "deployment_authorized"
    ] = True

    tampered[
        "final_record"
    ] = final_record

    validation = (
        report.validate_d14_reporting_bundle(
            tampered
        )
    )

    assert validation[
        "overall_pass"
    ] is False


def test_d14_reporting_validation_fails_if_risks_removed(
    reporting_bundle,
):
    tampered = dict(
        reporting_bundle
    )

    final_record = dict(
        reporting_bundle[
            "final_record"
        ]
    )

    final_record[
        "residual_risk_count"
    ] = 0

    final_record[
        "unresolved_residual_risk_count"
    ] = 0

    tampered[
        "final_record"
    ] = final_record

    validation = (
        report.validate_d14_reporting_bundle(
            tampered
        )
    )

    assert validation[
        "overall_pass"
    ] is False


def test_d14_reporting_validation_fails_if_disposition_changes(
    reporting_bundle,
):
    tampered = dict(
        reporting_bundle
    )

    final_record = dict(
        reporting_bundle[
            "final_record"
        ]
    )

    final_record[
        "disposition"
    ] = "TAMPERED"

    tampered[
        "final_record"
    ] = final_record

    validation = (
        report.validate_d14_reporting_bundle(
            tampered
        )
    )

    assert validation[
        "overall_pass"
    ] is False