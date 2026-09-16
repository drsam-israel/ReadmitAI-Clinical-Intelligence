# ============================================================
# D4 — LEAKAGE & FEATURE GOVERNANCE TESTS
# ============================================================

import pytest

from src.data.feature_governance import (
    APPROVED,
    CONDITIONAL,
    BLOCKED,
    IDENTIFIER_ONLY,
    TARGET_ONLY,
    APPROVED_SOURCE_FEATURES,
    CONDITIONAL_SOURCE_FEATURES,
    BLOCKED_SOURCE_FEATURES,
    CLINICAL_DECISION_POINT,
    PREDICTION_TIME_CONTRACT,
    LEAKAGE_TAXONOMY,
    build_complete_feature_governance,
)


# ============================================================
# D4.1 — SHARED TEST STATE
# ============================================================

@pytest.fixture(scope="module")
def d4_state():
    return build_complete_feature_governance()


# ============================================================
# D4.2 — PREDICTION-TIME CONTRACT TESTS
# ============================================================

def test_prediction_timestamp_defined():
    assert CLINICAL_DECISION_POINT.prediction_timestamp


def test_prediction_horizon_is_30_day_readmission():
    assert "30 days" in CLINICAL_DECISION_POINT.prediction_horizon


def test_locked_test_protection_defined():
    assert "locked test" in PREDICTION_TIME_CONTRACT["locked_test"].lower()


def test_target_leakage_taxonomy_defined():
    assert "TARGET_LEAKAGE" in LEAKAGE_TAXONOMY


def test_temporal_leakage_taxonomy_defined():
    assert "TEMPORAL_LEAKAGE" in LEAKAGE_TAXONOMY


def test_aggregation_leakage_taxonomy_defined():
    assert "AGGREGATION_LEAKAGE" in LEAKAGE_TAXONOMY


# ============================================================
# D4.3 — INVENTORY COMPLETENESS TESTS
# ============================================================

def test_complete_inventory_contains_51_fields(d4_state):
    _, inventory, _ = d4_state
    assert len(inventory) == 51


def test_no_feature_remains_unassessed(d4_state):
    _, inventory, _ = d4_state

    assert not (
        inventory["governance_disposition"]
        == "UNASSESSED"
    ).any()


def test_complete_governance_validation_passes(d4_state):
    _, _, validation = d4_state

    assert validation["validation_status"] == "PASS"


# ============================================================
# D4.4 — POLICY SET INTEGRITY TESTS
# ============================================================

def test_approved_conditional_sets_are_disjoint():
    assert APPROVED_SOURCE_FEATURES.isdisjoint(
        CONDITIONAL_SOURCE_FEATURES
    )


def test_approved_blocked_sets_are_disjoint():
    assert APPROVED_SOURCE_FEATURES.isdisjoint(
        BLOCKED_SOURCE_FEATURES
    )


def test_conditional_blocked_sets_are_disjoint():
    assert CONDITIONAL_SOURCE_FEATURES.isdisjoint(
        BLOCKED_SOURCE_FEATURES
    )


def test_non_reserved_policy_contains_47_fields():
    governed_features = (
        APPROVED_SOURCE_FEATURES
        | CONDITIONAL_SOURCE_FEATURES
        | BLOCKED_SOURCE_FEATURES
    )

    assert len(governed_features) == 47


# ============================================================
# D4.5 — GOVERNANCE COUNT TESTS
# ============================================================

def test_approved_feature_count(d4_state):
    _, _, validation = d4_state
    assert validation["approved_features"] == 8


def test_conditional_feature_count(d4_state):
    _, _, validation = d4_state
    assert validation["conditional_features"] == 33


def test_blocked_feature_count(d4_state):
    _, _, validation = d4_state
    assert validation["blocked_features"] == 6


def test_identifier_only_count(d4_state):
    _, _, validation = d4_state
    assert validation["identifier_only_fields"] == 2


def test_target_only_count(d4_state):
    _, _, validation = d4_state
    assert validation["target_only_fields"] == 2


# ============================================================
# D4.6 — IDENTIFIER GOVERNANCE TESTS
# ============================================================

def test_encounter_id_is_governance_only(d4_state):
    _, inventory, _ = d4_state

    disposition = inventory.loc[
        inventory["feature"] == "encounter_id",
        "governance_disposition",
    ].iloc[0]

    assert disposition == IDENTIFIER_ONLY


def test_patient_nbr_is_governance_only(d4_state):
    _, inventory, _ = d4_state

    disposition = inventory.loc[
        inventory["feature"] == "patient_nbr",
        "governance_disposition",
    ].iloc[0]

    assert disposition == IDENTIFIER_ONLY


# ============================================================
# D4.7 — TARGET LEAKAGE PROTECTION TESTS
# ============================================================

def test_raw_target_is_target_only(d4_state):
    _, inventory, _ = d4_state

    disposition = inventory.loc[
        inventory["feature"] == "readmitted",
        "governance_disposition",
    ].iloc[0]

    assert disposition == TARGET_ONLY


def test_engineered_target_is_target_only(d4_state):
    _, inventory, _ = d4_state

    disposition = inventory.loc[
        inventory["feature"] == "readmitted_30d",
        "governance_disposition",
    ].iloc[0]

    assert disposition == TARGET_ONLY


def test_targets_not_in_candidate_feature_sets():
    governed_features = (
        APPROVED_SOURCE_FEATURES
        | CONDITIONAL_SOURCE_FEATURES
        | BLOCKED_SOURCE_FEATURES
    )

    assert "readmitted" not in governed_features
    assert "readmitted_30d" not in governed_features


# ============================================================
# D4.8 — BLOCKED FEATURE PROTECTION TESTS
# ============================================================

@pytest.mark.parametrize(
    "feature",
    [
        "discharge_disposition_id",
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_diagnoses",
    ],
)
def test_retrospective_features_are_blocked(
    d4_state,
    feature,
):
    _, inventory, _ = d4_state

    disposition = inventory.loc[
        inventory["feature"] == feature,
        "governance_disposition",
    ].iloc[0]

    assert disposition == BLOCKED


def test_blocked_features_not_approved():
    assert APPROVED_SOURCE_FEATURES.isdisjoint(
        BLOCKED_SOURCE_FEATURES
    )


# ============================================================
# D4.9 — APPROVED FEATURE TESTS
# ============================================================

@pytest.mark.parametrize(
    "feature",
    [
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
    ],
)
def test_baseline_features_are_approved(
    d4_state,
    feature,
):
    _, inventory, _ = d4_state

    disposition = inventory.loc[
        inventory["feature"] == feature,
        "governance_disposition",
    ].iloc[0]

    assert disposition == APPROVED


# ============================================================
# D4.10 — CONDITIONAL FEATURE PROTECTION TESTS
# ============================================================

def test_conditional_features_not_directly_approved(d4_state):
    _, inventory, _ = d4_state

    rows = inventory[
        inventory["feature"].isin(
            CONDITIONAL_SOURCE_FEATURES
        )
    ]

    assert (
        rows["governance_disposition"]
        == CONDITIONAL
    ).all()


def test_conditional_features_require_governance(d4_state):
    _, inventory, _ = d4_state

    rows = inventory[
        inventory["governance_disposition"]
        == CONDITIONAL
    ]

    assert rows["permitted_use"].str.contains(
        "Requires governed",
        regex=False,
    ).all()


# ============================================================
# D4.11 — PRIMARY MODEL SAFETY TEST
# ============================================================

def test_primary_model_directly_authorized_features_are_only_approved(
    d4_state,
):
    _, inventory, _ = d4_state

    directly_authorized = inventory[
        inventory["governance_disposition"]
        == APPROVED
    ]["feature"]

    assert set(directly_authorized) == set(
        APPROVED_SOURCE_FEATURES
    )