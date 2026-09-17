# ============================================================
# D6 — COMBINED GOVERNED FEATURE MATRIX TESTS
# ============================================================
"""
Integration and governance tests for the complete D6 governed
feature-engineering matrix.

These tests verify that:

1. D6 consumes the frozen D5 patient split;
2. only train + validation encounters enter development;
3. the complete 40-feature registry is materialized;
4. CANDIDATE and CONDITIONAL features remain separated;
5. prohibited variables cannot enter the model feature set;
6. D4-CONDITIONAL lineage cannot silently enter the primary model;
7. identifiers and outcomes remain outside model inputs;
8. encounter integrity is preserved;
9. the primary X/y contract is correct;
10. the locked test partition remains protected.
"""

import pandas as pd

from src.data.splitting import (
    GROUP_COLUMN,
    TARGET_COLUMN,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
)

from src.features.engineering import (
    D6_CANDIDATE,
    D6_CONDITIONAL,
    FEATURE_SPECIFICATIONS,
    HARD_BLOCKED_RAW_FEATURES,
    IDENTIFIER_COLUMNS,
    OUTCOME_COLUMNS,
    D4_CONDITIONAL_SOURCE_FEATURES,
    EXPECTED_D5_ASSIGNMENT_SHA256,
    verify_frozen_split_assignment_checksum,
    build_combined_d6_development_features,
    build_primary_candidate_development_matrix,
    get_governed_d6_feature_lists,
)


# ============================================================
# D6 TEST CONSTANTS
# ============================================================

EXPECTED_DEVELOPMENT_ENCOUNTERS = 85076
EXPECTED_REGISTERED_FEATURES = 40
EXPECTED_CANDIDATE_FEATURES = 10
EXPECTED_CONDITIONAL_FEATURES = 30
EXPECTED_COMBINED_COLUMNS = 44

EXPECTED_PRIMARY_FEATURES = [
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
]


# ============================================================
# TEST 1 — FROZEN D5 CHECKSUM REMAINS AUTHORITATIVE
# ============================================================

def test_d5_frozen_assignment_checksum_is_verified():
    observed_checksum = (
        verify_frozen_split_assignment_checksum()
    )

    assert observed_checksum == (
        EXPECTED_D5_ASSIGNMENT_SHA256
    )


# ============================================================
# TEST 2 — FEATURE REGISTRY HAS EXACTLY 40 FEATURES
# ============================================================

def test_d6_registry_contains_exactly_40_features():
    assert len(FEATURE_SPECIFICATIONS) == (
        EXPECTED_REGISTERED_FEATURES
    )


# ============================================================
# TEST 3 — FEATURE REGISTRY NAMES ARE UNIQUE
# ============================================================

def test_d6_registry_feature_names_are_unique():
    feature_names = [
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
    ]

    assert len(feature_names) == len(
        set(feature_names)
    )


# ============================================================
# TEST 4 — GOVERNED FEATURE LIST COUNTS
# ============================================================

def test_governed_feature_list_counts_are_correct():
    feature_lists = get_governed_d6_feature_lists()

    assert len(
        feature_lists["candidate_features"]
    ) == EXPECTED_CANDIDATE_FEATURES

    assert len(
        feature_lists["conditional_features"]
    ) == EXPECTED_CONDITIONAL_FEATURES

    assert len(
        feature_lists["all_registered_model_features"]
    ) == EXPECTED_REGISTERED_FEATURES


# ============================================================
# TEST 5 — CANDIDATE AND CONDITIONAL SETS ARE DISJOINT
# ============================================================

def test_candidate_and_conditional_features_are_disjoint():
    feature_lists = get_governed_d6_feature_lists()

    overlap = (
        set(feature_lists["candidate_features"])
        & set(feature_lists["conditional_features"])
    )

    assert overlap == set()


# ============================================================
# TEST 6 — PRIMARY FEATURE LIST IS EXACT
# ============================================================

def test_primary_candidate_feature_list_is_exact():
    feature_lists = get_governed_d6_feature_lists()

    assert feature_lists["candidate_features"] == (
        EXPECTED_PRIMARY_FEATURES
    )


# ============================================================
# TEST 7 — CANDIDATES HAVE NO D4-CONDITIONAL LINEAGE
# ============================================================

def test_candidate_features_have_no_conditional_lineage():
    offending_features = [
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
        if (
            specification.disposition == D6_CANDIDATE
            and bool(
                set(specification.source_columns)
                & D4_CONDITIONAL_SOURCE_FEATURES
            )
        )
    ]

    assert offending_features == []


# ============================================================
# TEST 8 — COMBINED MATRIX PASSES GOVERNANCE VALIDATION
# ============================================================

def test_combined_matrix_validation_passes():
    _, audit = (
        build_combined_d6_development_features()
    )

    assert audit["validation_status"] == "PASS"


# ============================================================
# TEST 9 — DEVELOPMENT ROW COUNT IS FROZEN
# ============================================================

def test_combined_matrix_has_expected_development_rows():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    assert len(combined_df) == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS
    )


# ============================================================
# TEST 10 — COMBINED MATRIX HAS EXPECTED COLUMN COUNT
# ============================================================

def test_combined_matrix_has_expected_column_count():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    assert combined_df.shape[1] == (
        EXPECTED_COMBINED_COLUMNS
    )


# ============================================================
# TEST 11 — ALL 40 REGISTERED FEATURES ARE MATERIALIZED
# ============================================================

def test_all_registered_features_are_materialized():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    registered_features = {
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
    }

    missing_features = (
        registered_features
        - set(combined_df.columns)
    )

    assert missing_features == set()


# ============================================================
# TEST 12 — GOVERNANCE COLUMNS ARE PRESENT
# ============================================================

def test_required_governance_columns_are_present():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    required_governance_columns = {
        "encounter_id",
        GROUP_COLUMN,
        TARGET_COLUMN,
        "split",
    }

    assert required_governance_columns.issubset(
        combined_df.columns
    )


# ============================================================
# TEST 13 — LOCKED TEST IS ABSENT FROM DEVELOPMENT MATRIX
# ============================================================

def test_locked_test_partition_is_absent():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    observed_splits = set(
        combined_df["split"].unique()
    )

    assert TEST_LABEL not in observed_splits

    assert observed_splits == {
        TRAIN_LABEL,
        VALIDATION_LABEL,
    }


# ============================================================
# TEST 14 — ENCOUNTER IDS REMAIN UNIQUE
# ============================================================

def test_development_encounter_ids_are_unique():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    assert (
        combined_df["encounter_id"]
        .duplicated()
        .sum()
        == 0
    )


# ============================================================
# TEST 15 — PATIENTS CANNOT CROSS DEVELOPMENT SPLITS
# ============================================================

def test_patients_do_not_cross_train_validation_boundaries():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    patient_split_counts = (
        combined_df
        .groupby(GROUP_COLUMN)["split"]
        .nunique()
    )

    assert int(
        (patient_split_counts > 1).sum()
    ) == 0


# ============================================================
# TEST 16 — TARGET IS BINARY
# ============================================================

def test_development_target_is_binary():
    combined_df, _ = (
        build_combined_d6_development_features()
    )

    target_values = set(
        combined_df[TARGET_COLUMN]
        .dropna()
        .unique()
    )

    assert target_values.issubset({0, 1})

    assert combined_df[
        TARGET_COLUMN
    ].isna().sum() == 0


# ============================================================
# TEST 17 — NO HARD-BLOCKED RAW FEATURES ENTER MODEL SET
# ============================================================

def test_hard_blocked_raw_features_are_not_model_features():
    feature_lists = get_governed_d6_feature_lists()

    model_features = set(
        feature_lists[
            "all_registered_model_features"
        ]
    )

    assert (
        model_features
        & HARD_BLOCKED_RAW_FEATURES
    ) == set()


# ============================================================
# TEST 18 — IDENTIFIERS ARE NOT MODEL FEATURES
# ============================================================

def test_identifiers_are_not_model_features():
    feature_lists = get_governed_d6_feature_lists()

    model_features = set(
        feature_lists[
            "all_registered_model_features"
        ]
    )

    assert (
        model_features
        & IDENTIFIER_COLUMNS
    ) == set()


# ============================================================
# TEST 19 — OUTCOMES ARE NOT MODEL FEATURES
# ============================================================

def test_outcomes_are_not_model_features():
    feature_lists = get_governed_d6_feature_lists()

    model_features = set(
        feature_lists[
            "all_registered_model_features"
        ]
    )

    assert (
        model_features
        & OUTCOME_COLUMNS
    ) == set()


# ============================================================
# TEST 20 — PRIMARY MATRIX HAS EXPECTED SHAPE
# ============================================================

def test_primary_candidate_matrix_has_expected_shape():
    X, y, audit = (
        build_primary_candidate_development_matrix()
    )

    assert X.shape == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS,
        EXPECTED_CANDIDATE_FEATURES,
    )

    assert len(y) == (
        EXPECTED_DEVELOPMENT_ENCOUNTERS
    )

    assert (
        audit[
            "primary_matrix_validation_status"
        ]
        == "PASS"
    )


# ============================================================
# TEST 21 — PRIMARY X HAS EXACT GOVERNED FEATURES
# ============================================================

def test_primary_X_has_exact_candidate_features():
    X, _, _ = (
        build_primary_candidate_development_matrix()
    )

    assert list(X.columns) == (
        EXPECTED_PRIMARY_FEATURES
    )


# ============================================================
# TEST 22 — CONDITIONAL FEATURES CANNOT ENTER PRIMARY X
# ============================================================

def test_conditional_features_are_excluded_from_primary_X():
    X, _, _ = (
        build_primary_candidate_development_matrix()
    )

    conditional_features = {
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
        if specification.disposition
        == D6_CONDITIONAL
    }

    assert (
        set(X.columns)
        & conditional_features
    ) == set()


# ============================================================
# TEST 23 — IDENTIFIERS CANNOT ENTER PRIMARY X
# ============================================================

def test_identifiers_are_excluded_from_primary_X():
    X, _, _ = (
        build_primary_candidate_development_matrix()
    )

    assert (
        set(X.columns)
        & IDENTIFIER_COLUMNS
    ) == set()


# ============================================================
# TEST 24 — OUTCOMES CANNOT ENTER PRIMARY X
# ============================================================

def test_outcomes_are_excluded_from_primary_X():
    X, _, _ = (
        build_primary_candidate_development_matrix()
    )

    assert (
        set(X.columns)
        & OUTCOME_COLUMNS
    ) == set()


# ============================================================
# TEST 25 — HARD-BLOCKED FEATURES CANNOT ENTER PRIMARY X
# ============================================================

def test_hard_blocked_features_are_excluded_from_primary_X():
    X, _, _ = (
        build_primary_candidate_development_matrix()
    )

    assert (
        set(X.columns)
        & HARD_BLOCKED_RAW_FEATURES
    ) == set()


# ============================================================
# TEST 26 — X AND y INDICES REMAIN ALIGNED
# ============================================================

def test_primary_X_and_y_indices_are_aligned():
    X, y, _ = (
        build_primary_candidate_development_matrix()
    )

    assert X.index.equals(y.index)


# ============================================================
# TEST 27 — PRIMARY MATRIX HAS NO DUPLICATE FEATURE NAMES
# ============================================================

def test_primary_X_has_no_duplicate_columns():
    X, _, _ = (
        build_primary_candidate_development_matrix()
    )

    assert not X.columns.duplicated().any()


# ============================================================
# TEST 28 — COMBINED AUDIT REPORTS ZERO PROHIBITED FEATURES
# ============================================================

def test_combined_audit_reports_no_prohibited_features():
    _, audit = (
        build_combined_d6_development_features()
    )

    assert audit[
        "prohibited_model_features"
    ] == []

    assert audit[
        "candidate_features_with_conditional_lineage"
    ] == []

    assert audit[
        "candidate_conditional_overlap"
    ] == []