# ============================================================
# D15 — DEPLOYMENT & MONITORING DESIGN
# REPORTING & PERSISTED-EVIDENCE TEST SUITE
# ============================================================

from pathlib import Path

import src.models.deployment_monitoring as d15
import src.models.deployment_monitoring_reporting as reporting


# ============================================================
# SECTION 01 — REPORTING CONTRACT
# ============================================================

def test_d15_reporting_contract_passes():
    result = reporting.validate_d15_reporting_contract()

    assert result["overall_pass"] is True


def test_d15_reporting_registry_contains_15_artifacts():
    assert len(
        reporting.D15_EVIDENCE_ARTIFACT_REGISTRY
    ) == 15


def test_d15_required_artifact_contract_contains_15_keys():
    assert len(
        reporting.D15_REQUIRED_EVIDENCE_ARTIFACT_KEYS
    ) == 15


def test_d15_registry_matches_required_artifact_contract():
    assert set(
        reporting.D15_EVIDENCE_ARTIFACT_REGISTRY
    ) == set(
        reporting.D15_REQUIRED_EVIDENCE_ARTIFACT_KEYS
    )


# ============================================================
# SECTION 02 — ARCHITECTURE REPORTING
# ============================================================

def test_d15_architecture_reporting_passes():
    result = (
        reporting
        .validate_d15_reporting_architecture_evidence()
    )

    assert result["overall_pass"] is True


def test_d15_architecture_control_rows_are_complete():
    rows = (
        reporting
        .build_d15_architecture_control_table_rows()
    )

    assert len(rows) == 19


def test_d15_architecture_reporting_preserves_frozen_system_boundary():
    result = (
        reporting
        .build_d15_architecture_evidence()
    )

    assert (
        result["expected_primary_feature_count"]
        == 10
    )

    assert (
        result["expected_transformed_feature_count"]
        == 49
    )

    assert tuple(
        result["required_raw_source_features"]
    ) == (
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
    )

    assert tuple(
        result["expected_engineered_primary_features"]
    ) == (
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
        "prior_outpatient_use",
        "prior_emergency_use",
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
    )

    assert (
        result["production_deployment_authorized"]
        is False
    )


def test_d15_architecture_reporting_preserves_advisory_output():
    result = (
        reporting
        .build_d15_architecture_evidence()
    )

    assert (
        result["output_classification"]
        == "CLINICAL_DECISION_SUPPORT_ADVISORY"
    )

    assert (
        result["production_deployment_authorized"]
        is False
    )


# ============================================================
# SECTION 03 — MONITORING REPORTING
# ============================================================

def test_d15_monitoring_reporting_passes():
    result = (
        reporting
        .validate_d15_monitoring_reporting_evidence()
    )

    assert result["overall_pass"] is True


def test_d15_monitoring_catalogue_has_17_controls():
    rows = (
        reporting
        .build_d15_monitoring_control_table_rows()
    )

    assert len(rows) == 17


def test_d15_quantitative_reference_table_has_6_rows():
    rows = (
        reporting
        .build_d15_quantitative_reference_table_rows()
    )

    assert len(rows) == 6


def test_d15_known_risk_slice_table_has_5_rows():
    rows = (
        reporting
        .build_d15_known_risk_slice_table_rows()
    )

    assert len(rows) == 5


def test_d15_escalation_catalogue_has_17_rows():
    rows = (
        reporting
        .build_d15_escalation_trigger_table_rows()
    )

    assert len(rows) == 17


def test_d15_reference_bands_are_not_production_targets():
    rows = (
        reporting
        .build_d15_quantitative_reference_table_rows()
    )

    assert all(
        row["production_acceptance_limit"] is False
        for row in rows
    )

    assert all(
        row["clinical_acceptability_limit"] is False
        for row in rows
    )


def test_d15_known_risk_slices_are_not_acceptable_targets():
    rows = (
        reporting
        .build_d15_known_risk_slice_table_rows()
    )

    assert all(
        row["acceptable_target"] is False
        for row in rows
    )


# ============================================================
# SECTION 04 — BOOTSTRAP REPORTING STRUCTURE
# ============================================================

def test_d15_bootstrap_reporting_configuration_is_frozen():
    assert (
        reporting.D15_REPORTING_BOOTSTRAP_REPLICATES
        == 2000
    )

    assert (
        reporting.D15_REPORTING_BOOTSTRAP_CONFIDENCE_LEVEL
        == 0.95
    )

    assert (
        reporting.D15_REPORTING_BOOTSTRAP_RANDOM_SEED
        == 42
    )


def test_d15_persisted_bootstrap_table_has_two_metrics():
    path = (
        reporting.D15_EVIDENCE_ARTIFACT_REGISTRY[
            "bootstrap_discrimination_uncertainty"
        ]
    )

    assert (
        reporting._count_d15_csv_data_rows(
            path
        )
        == 2
    )


# ============================================================
# SECTION 05 — OPERATIONAL GOVERNANCE REPORTING
# ============================================================

def test_d15_operational_risk_reporting_passes():
    result = (
        reporting
        .validate_d15_operational_risk_reporting_evidence()
    )

    assert result["overall_pass"] is True


def test_d15_residual_risk_rows_preserve_all_seven_risks():
    rows = (
        reporting
        .build_d15_residual_risk_reporting_rows()
    )

    assert len(rows) == 7

    assert {
        row["risk_id"]
        for row in rows
    } == set(
        d15.D15_REQUIRED_D14_RESIDUAL_RISKS
    )


def test_d15_residual_risks_remain_unresolved():
    rows = (
        reporting
        .build_d15_residual_risk_reporting_rows()
    )

    assert all(
        row["handoff_status"]
        == "UNRESOLVED_CARRY_FORWARD"
        for row in rows
    )


def test_d15_operational_control_table_has_16_rows():
    rows = (
        reporting
        .build_d15_operational_control_reporting_rows()
    )

    assert len(rows) == 16


def test_d15_does_not_claim_live_incident_management():
    evidence = (
        reporting
        .build_d15_operational_governance_evidence()
    )

    assert (
        evidence["incident_management_implemented"]
        is False
    )


def test_d15_does_not_claim_live_rollback_implementation():
    evidence = (
        reporting
        .build_d15_operational_governance_evidence()
    )

    assert (
        evidence["rollback_implemented"]
        is False
    )


def test_d15_business_continuity_preserves_clinical_workflow():
    evidence = (
        reporting
        .build_d15_operational_governance_evidence()
    )

    continuity = (
        evidence["business_continuity_control"]
    )

    assert (
        continuity[
            "clinical_workflow_must_continue_without_ai"
        ]
        is True
    )

    assert (
        continuity[
            "ai_unavailability_blocks_clinical_care"
        ]
        is False
    )

    assert (
        continuity[
            "clinical_team_retains_decision_authority"
        ]
        is True
    )


# ============================================================
# SECTION 06 — PERSISTED EVIDENCE INTEGRITY
# ============================================================

def test_d15_persisted_evidence_package_passes():
    result = (
        reporting
        .validate_d15_persisted_evidence_package()
    )

    assert result["overall_pass"] is True


def test_d15_all_registered_artifacts_exist():
    for path in (
        reporting
        .D15_EVIDENCE_ARTIFACT_REGISTRY
        .values()
    ):
        assert path.exists()


def test_d15_all_registered_artifacts_are_nonempty():
    for path in (
        reporting
        .D15_EVIDENCE_ARTIFACT_REGISTRY
        .values()
    ):
        assert path.stat().st_size > 0


def test_d15_manifest_contains_14_child_artifacts():
    result = (
        reporting
        ._parse_d15_persisted_manifest()
    )

    assert len(
        result["artifacts"]
    ) == 14


def test_d15_manifest_child_paths_match_registry():
    result = (
        reporting
        ._parse_d15_persisted_manifest()
    )

    for record in result["artifacts"]:

        key = record["artifact_key"]

        path = (
            reporting
            .D15_EVIDENCE_ARTIFACT_REGISTRY[
                key
            ]
        )

        assert (
            record["path"]
            == reporting._d15_relative_path(
                path
            )
        )


def test_d15_manifest_child_hashes_match_files():
    result = (
        reporting
        ._parse_d15_persisted_manifest()
    )

    for record in result["artifacts"]:

        path = (
            reporting
            .D15_EVIDENCE_ARTIFACT_REGISTRY[
                record["artifact_key"]
            ]
        )

        assert (
            record["sha256"]
            == reporting._d15_sha256_file(
                path
            )
        )


def test_d15_manifest_child_sizes_match_files():
    result = (
        reporting
        ._parse_d15_persisted_manifest()
    )

    for record in result["artifacts"]:

        path = (
            reporting
            .D15_EVIDENCE_ARTIFACT_REGISTRY[
                record["artifact_key"]
            ]
        )

        assert int(
            record["size_bytes"]
        ) == path.stat().st_size


# ============================================================
# SECTION 07 — PERSISTED STRUCTURED-EVIDENCE COUNTS
# ============================================================

def test_d15_persisted_structured_evidence_counts():
    result = (
        reporting
        .validate_d15_persisted_evidence_package()
    )

    counts = result[
        "csv_row_counts"
    ]

    assert counts[
        "architecture_controls"
    ] == 19

    assert counts[
        "monitoring_control_catalogue"
    ] == 17

    assert counts[
        "quantitative_reference_bands"
    ] == 6

    assert counts[
        "bootstrap_discrimination_uncertainty"
    ] == 2

    assert counts[
        "known_risk_slice_references"
    ] == 5

    assert counts[
        "escalation_trigger_catalogue"
    ] == 17

    assert counts[
        "residual_risk_traceability"
    ] == 7

    assert counts[
        "operational_control_evidence"
    ] == 16


# ============================================================
# SECTION 08 — GOVERNANCE BOUNDARY ASSERTIONS
# ============================================================

def test_d15_gate_progresses_only_to_d16():
    path = (
        reporting.D15_EVIDENCE_ARTIFACT_REGISTRY[
            "gate_decision"
        ]
    )

    text = path.read_text(
        encoding="utf-8"
    )

    assert (
        "CONDITIONAL PASS"
        in text
    )

    assert (
        "PROGRESS TO D16 WITH DOCUMENTED RESIDUAL RISKS"
        in text
    )


def test_d15_gate_does_not_authorize_production():
    path = (
        reporting.D15_EVIDENCE_ARTIFACT_REGISTRY[
            "gate_decision"
        ]
    )

    text = path.read_text(
        encoding="utf-8"
    )

    assert (
        "PRODUCTION DEPLOYMENT NOT AUTHORIZED"
        in text
    )


def test_d15_external_validation_remains_unestablished():
    result = (
        reporting
        ._parse_d15_persisted_manifest()
    )

    assert (
        result["metadata"][
            "external_validation_established"
        ]
        == "false"
    )


def test_d15_clinical_effectiveness_remains_unestablished():
    result = (
        reporting
        ._parse_d15_persisted_manifest()
    )

    assert (
        result["metadata"][
            "clinical_effectiveness_established"
        ]
        == "false"
    )


def test_d15_production_deployment_remains_unauthorized():
    result = (
        reporting
        .validate_d15_persisted_evidence_package()
    )

    assert (
        result[
            "production_deployment_authorized"
        ]
        is False
    )