# ============================================================
# D15 — OPERATIONAL GOVERNANCE TEST SUITE
# Monitoring, Drift, Escalation, Incident, Change,
# Rollback & Business Continuity
# ============================================================

import pytest

import src.models.deployment_monitoring as d15

# ============================================================
# D15.120 — MONITORING CATALOGUE
# ============================================================


def test_d15_monitoring_catalogue_passes():
    evidence = d15.validate_d15_monitoring_control_catalogue()

    assert evidence["overall_pass"] is True
    assert evidence["checks"]["seventeen_monitoring_controls_declared"] is True
    assert evidence["checks"]["all_seven_d14_residual_risks_covered"] is True
    assert evidence["checks"]["incident_control_covers_all_residual_risks"] is True


def test_d15_monitoring_prohibits_automatic_model_change():
    evidence = d15.validate_d15_monitoring_control_catalogue()

    assert evidence["checks"]["automatic_retraining_prohibited"] is True
    assert evidence["checks"]["automatic_recalibration_prohibited"] is True
    assert evidence["checks"]["automatic_threshold_adjustment_prohibited"] is True
    assert evidence["checks"]["subgroup_threshold_adjustment_prohibited"] is True


# ============================================================
# D15.121 — QUANTITATIVE MONITORING LIMITS
# ============================================================


def test_d15_wilson_interval_is_valid():
    result = d15.calculate_d15_wilson_interval(
        events=50,
        denominator=100,
    )

    assert (
        0.0
        <= result["lower_bound"]
        <= result["observed_rate"]
        <= result["upper_bound"]
        <= 1.0
    )


def test_d15_wilson_interval_rejects_invalid_denominator():
    with pytest.raises(ValueError):
        d15.calculate_d15_wilson_interval(
            events=0,
            denominator=0,
        )


def test_d15_reference_bands_are_complete():
    bands = d15.build_d15_internal_rate_reference_bands()

    assert set(bands) == {
        "prevalence",
        "alert_rate",
        "sensitivity",
        "specificity",
        "ppv",
        "npv",
    }

    assert all(
        item["production_acceptance_limit"] is False
        for item in bands.values()
    )


def test_d15_known_risk_history_is_not_acceptability_target():
    assert all(
        item["acceptable_target"] is False
        for item in d15.D15_D14_KNOWN_RISK_SLICE_REFERENCES.values()
    )


def test_d15_insufficient_sample_does_not_default_normal():
    result = d15.assess_d15_monitoring_sample_sufficiency(
        encounter_count=100,
        positive_count=10,
        negative_count=90,
    )

    assert result["sufficient"] is False
    assert result["interpretation_status"] == "INSUFFICIENT_EVIDENCE"


def test_d15_quantitative_limit_foundation_passes():
    evidence = d15.validate_d15_quantitative_monitoring_limit_foundation()

    assert evidence["overall_pass"] is True
    assert evidence["production_deployment_authorized"] is False


# ============================================================
# D15.122 — STATISTICAL SIGNAL & PERSISTENCE
# ============================================================


def test_d15_insufficient_rate_signal_is_not_assessable():
    result = d15.evaluate_d15_binary_rate_signal(
        metric_name="alert_rate",
        observed_events=20,
        observed_denominator=100,
        encounter_count=100,
    )

    assert result["status"] == "NOT_ASSESSABLE"


def test_d15_large_rate_shift_generates_watch():
    result = d15.evaluate_d15_binary_rate_signal(
        metric_name="alert_rate",
        observed_events=700,
        observed_denominator=1000,
        encounter_count=1000,
    )

    assert result["status"] == "WATCH"
    assert result["statistical_signal"] == "REFERENCE_SHIFT_SIGNAL"
    assert result["automatic_model_change"] is False
    assert result["automatic_threshold_change"] is False


def test_d15_single_watch_is_not_persistent():
    result = d15.evaluate_d15_signal_persistence(
        ["NORMAL", "WATCH"]
    )

    assert result["persistent_signal"] is False


def test_d15_two_consecutive_watch_windows_are_persistent():
    result = d15.evaluate_d15_signal_persistence(
        ["NORMAL", "WATCH", "WATCH"]
    )

    assert result["persistent_signal"] is True
    assert result["consecutive_watch_or_higher"] == 2


def test_d15_unassessable_windows_do_not_create_drift_claim():
    result = d15.evaluate_d15_signal_persistence(
        ["NOT_ASSESSABLE", "NOT_ASSESSABLE"]
    )

    assert result["status"] == "NOT_ASSESSABLE"
    assert result["persistent_signal"] is False


# ============================================================
# D15.123 — MATERIALITY GOVERNANCE
# ============================================================


def test_d15_materiality_cannot_self_authorize():
    result = d15.build_d15_materiality_review_record(
        clinical_materiality_confirmed=True,
        reviewer_authorized=False,
        review_documented=False,
    )

    assert result["materiality_confirmed"] is False
    assert result["automatic_confirmation_permitted"] is False


def test_d15_authorized_documented_materiality_can_confirm():
    result = d15.build_d15_materiality_review_record(
        clinical_materiality_confirmed=True,
        reviewer_authorized=True,
        review_documented=True,
    )

    assert result["materiality_confirmed"] is True


# ============================================================
# D15.124 — INTEGRATED WATCH / ALERT ENGINE
# ============================================================


@pytest.mark.parametrize(
    "structural_status,metric_status,persistent,material,expected",
    [
        ("NORMAL", "NORMAL", False, False, "NORMAL"),
        ("NORMAL", "WATCH", False, False, "WATCH"),
        ("NORMAL", "WATCH", True, False, "ALERT"),
        ("NORMAL", "WATCH", False, True, "ALERT"),
        ("CRITICAL", "NORMAL", False, False, "CRITICAL"),
        ("NORMAL", "NOT_ASSESSABLE", False, False, "NOT_ASSESSABLE"),
    ],
)
def test_d15_integrated_status_resolution(
    structural_status,
    metric_status,
    persistent,
    material,
    expected,
):
    result = d15.resolve_d15_integrated_monitoring_status(
        structural_status=structural_status,
        metric_status=metric_status,
        persistent_signal=persistent,
        materiality_confirmed=material,
    )

    assert result["status"] == expected
    assert result["automatic_model_change"] is False
    assert result["automatic_recalibration"] is False
    assert result["automatic_threshold_change"] is False


def test_d15_integrated_control_engine_passes():
    evidence = d15.validate_d15_integrated_watch_alert_control_engine()

    assert evidence["overall_pass"] is True
    assert evidence["production_deployment_authorized"] is False


# ============================================================
# D15.125 — INCIDENT MANAGEMENT
# ============================================================


def _build_test_incident(
    severity="SEV1",
):
    return d15.build_d15_incident_record(
        incident_id="D15-PYTEST-INCIDENT-001",
        severity=severity,
        incident_type="FROZEN_ARTIFACT_IDENTITY_FAILURE",
        detection_source="PYTEST",
        affected_component="FROZEN_MODEL_ARTIFACT",
        clinical_safety_relevance=True,
        affected_population="SYNTHETIC_TEST_POPULATION",
        immediate_containment="BLOCK_AI_INFERENCE",
        ai_service_status="SUSPENDED",
        human_workflow_status="STANDARD_CLINICIAN_LED_WORKFLOW_ACTIVE",
        governance_owner="MODEL_GOVERNANCE",
    )


def test_d15_sev1_incident_requires_revalidation():
    incident = _build_test_incident("SEV1")

    assert incident["revalidation_required"] is True
    assert incident["automatic_model_change"] is False
    assert incident["automatic_threshold_change"] is False


def test_d15_incident_record_preserves_frozen_identity():
    incident = _build_test_incident()

    validation = d15.validate_d15_incident_record(
        incident
    )

    assert validation["overall_pass"] is True
    assert validation["checks"]["candidate_identity_preserved"] is True
    assert validation["checks"]["threshold_identity_preserved"] is True


# ============================================================
# D15.126 — CHANGE CONTROL
# ============================================================


def _build_model_change():
    return d15.build_d15_change_request(
        change_id="D15-PYTEST-CHANGE-001",
        change_classification="MODEL_AFFECTING",
        change_type="OPERATING_THRESHOLD",
        change_description="Synthetic threshold change.",
        rationale="CONTROL_TEST_ONLY",
        requested_by="PYTEST",
    )


def test_d15_model_affecting_change_requires_revalidation_and_version():
    request = _build_model_change()

    assert request["model_affecting"] is True
    assert request["revalidation_required"] is True
    assert request["new_version_required"] is True
    assert request["implementation_authorized"] is False


def test_d15_unapproved_change_is_blocked():
    decision = d15.evaluate_d15_change_authorization(
        _build_model_change()
    )

    assert decision["authorized_to_progress"] is False
    assert decision["authorization_status"] == "NOT_AUTHORIZED_TO_IMPLEMENT"
    assert decision["current_frozen_candidate_modified"] is False


def test_d15_fully_reviewed_change_can_progress_controlled_path():
    decision = d15.evaluate_d15_change_authorization(
        _build_model_change(),
        governance_approved=True,
        clinical_review_completed=True,
        technical_review_completed=True,
        responsible_ai_review_completed=True,
        revalidation_completed=True,
        version_registered=True,
    )

    assert decision["authorized_to_progress"] is True
    assert (
        decision["authorization_status"]
        == "AUTHORIZED_TO_PROGRESS_THROUGH_CONTROLLED_CHANGE"
    )
    assert decision["current_frozen_candidate_modified"] is False


# ============================================================
# D15.127 — ROLLBACK
# ============================================================


def test_d15_unsafe_rollback_target_suspends_ai():
    decision = d15.build_d15_rollback_decision(
        trigger="FROZEN_ARTIFACT_IDENTITY_FAILURE",
        rollback_target_available=False,
        rollback_target_authorized=False,
        rollback_target_integrity_verified=False,
    )

    assert decision["disposition"] == "AI_SERVICE_SUSPENSION_REQUIRED"
    assert (
        decision["fallback"]
        == "STANDARD_CLINICIAN_LED_WORKFLOW_WITHOUT_AI"
    )
    assert decision["replacement_prediction_generated"] is False


def test_d15_verified_authorized_rollback_is_eligible():
    decision = d15.build_d15_rollback_decision(
        trigger="FROZEN_ARTIFACT_IDENTITY_FAILURE",
        rollback_target_available=True,
        rollback_target_authorized=True,
        rollback_target_integrity_verified=True,
    )

    assert decision["disposition"] == "CONTROLLED_ROLLBACK_ELIGIBLE"
    assert decision["automatic_model_change"] is False
    assert decision["automatic_threshold_change"] is False


# ============================================================
# D15.128 — BUSINESS CONTINUITY
# ============================================================


def test_d15_ai_failure_does_not_block_clinical_care():
    result = d15.evaluate_d15_business_continuity(
        ai_service_available=False,
        artifact_integrity_valid=False,
        unresolved_critical_incident=True,
    )

    assert result["ai_use_permitted"] is False
    assert result["clinical_care_blocked"] is False
    assert result["clinical_decision_authority"] == "HUMAN_CLINICAL_TEAM"

    assert (
        result["clinical_workflow"]
        == "STANDARD_CLINICIAN_LED_DISCHARGE_AND_READMISSION_PREVENTION_WORKFLOW"
    )


def test_d15_ai_failure_creates_no_replacement_prediction():
    result = d15.evaluate_d15_business_continuity(
        ai_service_available=False,
        artifact_integrity_valid=False,
        unresolved_critical_incident=True,
    )

    assert result["manual_replacement_ai_score_required"] is False
    assert result["synthetic_replacement_prediction_generated"] is False


def test_d15_healthy_service_remains_human_led():
    result = d15.evaluate_d15_business_continuity(
        ai_service_available=True,
        artifact_integrity_valid=True,
        unresolved_critical_incident=False,
    )

    assert result["ai_use_permitted"] is True
    assert result["workflow_status"] == "AI_ADVISORY_SERVICE_AVAILABLE"
    assert result["clinical_decision_authority"] == "HUMAN_CLINICAL_TEAM"


# ============================================================
# D15.129 — SERVICE RESTORATION
# ============================================================


def test_d15_incomplete_remediation_blocks_restoration():
    result = d15.evaluate_d15_service_restoration(
        artifact_integrity_verified=True,
        root_cause_resolved=False,
        corrective_action_completed=False,
        required_revalidation_completed=False,
        governance_clearance_completed=False,
    )

    assert result["restoration_eligible"] is False
    assert result["restoration_status"] == "SERVICE_RESTORATION_BLOCKED"


def test_d15_complete_remediation_is_restoration_eligible():
    result = d15.evaluate_d15_service_restoration(
        artifact_integrity_verified=True,
        root_cause_resolved=True,
        corrective_action_completed=True,
        required_revalidation_completed=True,
        governance_clearance_completed=True,
    )

    assert result["restoration_eligible"] is True

    assert (
        result["restoration_status"]
        == "ELIGIBLE_FOR_CONTROLLED_SERVICE_RESTORATION"
    )

    assert result["automatic_restoration"] is False


def test_d15_operational_governance_suite_passes():
    evidence = (
        d15.validate_d15_incident_change_rollback_continuity_controls()
    )

    assert evidence["overall_pass"] is True
    assert evidence["production_deployment_authorized"] is False