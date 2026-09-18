# ============================================================
# D7 — GOVERNED PREPROCESSING TEST SUITE
# ============================================================
"""
Automated controls for D7 Governed Preprocessing.

The suite verifies:

1. Frozen D6 dependency integrity.
2. D7 feature authorization.
3. TRAIN / VALIDATION development boundary.
4. Locked-test isolation.
5. Source-unknown demographic governance.
6. TRAIN-only fitted preprocessing.
7. Model-ready transformed output integrity.
8. Persisted-preprocessor reproducibility.
9. Artifact checksum integrity.
10. D7 evidence-package completeness.

No predictive model is trained here.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml

from src.features.preprocessing import (
    PROJECT_ROOT,
    D6_DEVELOPMENT_ARTIFACT,
    EXPECTED_D6_DEVELOPMENT_SHA256,
    PRIMARY_CANDIDATE_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    CANONICAL_UNKNOWN_CATEGORY,
    D7_PREPROCESSOR_PATH,
    D7_TRANSFORMED_SCHEMA_PATH,
    EXPECTED_D7_RAW_FEATURE_COUNT,
    EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
    EXPECTED_D7_TRAIN_ENCOUNTERS,
    EXPECTED_D7_VALIDATION_ENCOUNTERS,
    calculate_file_sha256,
    build_persisted_d7_primary_preprocessor,
)

from src.features.preprocessing_reporting import (
    D7_MANIFEST_PATH,
    D7_CONTRACT_REPORT_PATH,
    D7_GATE_DECISION_PATH,
    D7_SUMMARY_TABLE_PATH,
    D7_FEATURE_REGISTRY_PATH,
    D7_UNKNOWN_AUDIT_PATH,
    D7_LEARNED_STATE_PATH,
)


# ============================================================
# D7.T01 — BUILD SHARED GOVERNED WORKFLOW
# ============================================================

D7_WORKFLOW = build_persisted_d7_primary_preprocessor()

FITTED_BUNDLE = D7_WORKFLOW["fitted_bundle"]

PERSISTENCE = D7_WORKFLOW["persistence_result"]

PERSISTENCE_VALIDATION = D7_WORKFLOW[
    "persistence_validation"
]


# ============================================================
# D7.T02 — D6 DEPENDENCY INTEGRITY
# ============================================================

def test_d6_dependency_exists():
    assert D6_DEVELOPMENT_ARTIFACT.exists()


def test_d6_dependency_checksum():
    assert (
        calculate_file_sha256(
            D6_DEVELOPMENT_ARTIFACT
        )
        == EXPECTED_D6_DEVELOPMENT_SHA256
    )


# ============================================================
# D7.T03 — RAW FEATURE CONTRACT
# ============================================================

def test_primary_feature_count():
    assert len(
        PRIMARY_CANDIDATE_FEATURES
    ) == EXPECTED_D7_RAW_FEATURE_COUNT


def test_primary_features_are_unique():
    assert len(
        PRIMARY_CANDIDATE_FEATURES
    ) == len(
        set(PRIMARY_CANDIDATE_FEATURES)
    )


def test_categorical_numeric_partition():
    assert set(
        CATEGORICAL_FEATURES
    ).isdisjoint(
        NUMERIC_FEATURES
    )

    assert set(
        CATEGORICAL_FEATURES
    ).union(
        NUMERIC_FEATURES
    ) == set(
        PRIMARY_CANDIDATE_FEATURES
    )


def test_expected_categorical_count():
    assert len(
        CATEGORICAL_FEATURES
    ) == 5


def test_expected_numeric_count():
    assert len(
        NUMERIC_FEATURES
    ) == 5


# ============================================================
# D7.T04 — DEVELOPMENT BOUNDARY
# ============================================================

def test_train_encounter_count():
    assert len(
        FITTED_BUNDLE[
            "X_train_raw"
        ]
    ) == EXPECTED_D7_TRAIN_ENCOUNTERS


def test_validation_encounter_count():
    assert len(
        FITTED_BUNDLE[
            "X_validation_raw"
        ]
    ) == EXPECTED_D7_VALIDATION_ENCOUNTERS


def test_train_raw_feature_order():
    assert list(
        FITTED_BUNDLE[
            "X_train_raw"
        ].columns
    ) == PRIMARY_CANDIDATE_FEATURES


def test_validation_raw_feature_order():
    assert list(
        FITTED_BUNDLE[
            "X_validation_raw"
        ].columns
    ) == PRIMARY_CANDIDATE_FEATURES


def test_patient_overlap_is_zero():
    assert (
        FITTED_BUNDLE[
            "boundary_validation"
        ][
            "patient_overlap_count"
        ]
        == 0
    )


def test_encounter_overlap_is_zero():
    assert (
        FITTED_BUNDLE[
            "boundary_validation"
        ][
            "encounter_overlap_count"
        ]
        == 0
    )


def test_locked_test_not_accessed():
    assert (
        FITTED_BUNDLE[
            "preprocessing_validation"
        ][
            "locked_test_accessed"
        ]
        is False
    )


def test_validation_not_used_for_fit():
    assert (
        FITTED_BUNDLE[
            "preprocessing_validation"
        ][
            "validation_contributed_to_fit"
        ]
        is False
    )


# ============================================================
# D7.T05 — TARGET INTEGRITY
# ============================================================

def test_train_target_binary():
    values = set(
        FITTED_BUNDLE[
            "y_train"
        ].unique()
    )

    assert values.issubset(
        {0, 1}
    )


def test_validation_target_binary():
    values = set(
        FITTED_BUNDLE[
            "y_validation"
        ].unique()
    )

    assert values.issubset(
        {0, 1}
    )


def test_target_not_in_train_features():
    assert (
        "readmitted_30d"
        not in FITTED_BUNDLE[
            "X_train_raw"
        ].columns
    )


def test_target_not_in_validation_features():
    assert (
        "readmitted_30d"
        not in FITTED_BUNDLE[
            "X_validation_raw"
        ].columns
    )


# ============================================================
# D7.T06 — SOURCE UNKNOWN GOVERNANCE
# ============================================================

def test_train_unknown_normalization_passes():
    assert (
        FITTED_BUNDLE[
            "train_normalization_validation"
        ][
            "validation_status"
        ]
        == "PASS"
    )


def test_validation_unknown_normalization_passes():
    assert (
        FITTED_BUNDLE[
            "validation_normalization_validation"
        ][
            "validation_status"
        ]
        == "PASS"
    )


def test_train_race_unknown_count():
    assert (
        FITTED_BUNDLE[
            "train_normalization_validation"
        ][
            "canonical_unknown_counts"
        ][
            "race"
        ]
        == 1568
    )


def test_validation_race_unknown_count():
    assert (
        FITTED_BUNDLE[
            "validation_normalization_validation"
        ][
            "canonical_unknown_counts"
        ][
            "race"
        ]
        == 345
    )


def test_train_gender_unknown_count():
    assert (
        FITTED_BUNDLE[
            "train_normalization_validation"
        ][
            "canonical_unknown_counts"
        ][
            "gender"
        ]
        == 3
    )


def test_validation_gender_unknown_count():
    assert (
        FITTED_BUNDLE[
            "validation_normalization_validation"
        ][
            "canonical_unknown_counts"
        ][
            "gender"
        ]
        == 0
    )


# ============================================================
# D7.T07 — TRAIN-LEARNED CATEGORICAL STATE
# ============================================================

def test_race_vocabulary_contains_canonical_unknown():
    preprocessor = FITTED_BUNDLE[
        "preprocessor"
    ]

    encoder = (
        preprocessor
        .named_transformers_[
            "categorical"
        ]
        .named_steps[
            "encoder"
        ]
    )

    race_index = (
        CATEGORICAL_FEATURES.index(
            "race"
        )
    )

    assert (
        CANONICAL_UNKNOWN_CATEGORY
        in encoder.categories_[
            race_index
        ]
    )


def test_gender_vocabulary_contains_canonical_unknown():
    preprocessor = FITTED_BUNDLE[
        "preprocessor"
    ]

    encoder = (
        preprocessor
        .named_transformers_[
            "categorical"
        ]
        .named_steps[
            "encoder"
        ]
    )

    gender_index = (
        CATEGORICAL_FEATURES.index(
            "gender"
        )
    )

    assert (
        CANONICAL_UNKNOWN_CATEGORY
        in encoder.categories_[
            gender_index
        ]
    )


def test_numeric_train_medians_are_zero():
    preprocessor = FITTED_BUNDLE[
        "preprocessor"
    ]

    numeric_imputer = (
        preprocessor
        .named_transformers_[
            "numeric"
        ]
        .named_steps[
            "imputer"
        ]
    )

    assert np.array_equal(
        numeric_imputer.statistics_,
        np.zeros(
            len(NUMERIC_FEATURES)
        ),
    )


# ============================================================
# D7.T08 — TRANSFORMED OUTPUT INTEGRITY
# ============================================================

def test_train_transformed_shape():
    assert (
        FITTED_BUNDLE[
            "X_train_transformed"
        ].shape
        == (
            EXPECTED_D7_TRAIN_ENCOUNTERS,
            EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
        )
    )


def test_validation_transformed_shape():
    assert (
        FITTED_BUNDLE[
            "X_validation_transformed"
        ].shape
        == (
            EXPECTED_D7_VALIDATION_ENCOUNTERS,
            EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
        )
    )


def test_transformed_feature_count():
    assert len(
        FITTED_BUNDLE[
            "transformed_feature_names"
        ]
    ) == EXPECTED_D7_TRANSFORMED_FEATURE_COUNT


def test_transformed_feature_names_unique():
    names = FITTED_BUNDLE[
        "transformed_feature_names"
    ]

    assert len(names) == len(
        set(names)
    )


def test_train_has_no_missing_values():
    assert (
        FITTED_BUNDLE[
            "X_train_transformed"
        ]
        .isna()
        .sum()
        .sum()
        == 0
    )


def test_validation_has_no_missing_values():
    assert (
        FITTED_BUNDLE[
            "X_validation_transformed"
        ]
        .isna()
        .sum()
        .sum()
        == 0
    )


def test_train_has_no_nonfinite_values():
    values = (
        FITTED_BUNDLE[
            "X_train_transformed"
        ]
        .to_numpy(
            dtype=float
        )
    )

    assert np.isfinite(
        values
    ).all()


def test_validation_has_no_nonfinite_values():
    values = (
        FITTED_BUNDLE[
            "X_validation_transformed"
        ]
        .to_numpy(
            dtype=float
        )
    )

    assert np.isfinite(
        values
    ).all()


def test_raw_race_question_dummy_absent():
    names = FITTED_BUNDLE[
        "transformed_feature_names"
    ]

    assert not any(
        "race_?"
        in name
        for name in names
    )


def test_raw_gender_unknown_dummy_absent():
    names = FITTED_BUNDLE[
        "transformed_feature_names"
    ]

    assert not any(
        "gender_Unknown/Invalid"
        in name
        for name in names
    )


def test_canonical_race_unknown_dummy_present():
    names = FITTED_BUNDLE[
        "transformed_feature_names"
    ]

    expected = (
        "categorical__race_"
        + CANONICAL_UNKNOWN_CATEGORY
    )

    assert expected in names


def test_canonical_gender_unknown_dummy_present():
    names = FITTED_BUNDLE[
        "transformed_feature_names"
    ]

    expected = (
        "categorical__gender_"
        + CANONICAL_UNKNOWN_CATEGORY
    )

    assert expected in names


# ============================================================
# D7.T09 — PERSISTENCE INTEGRITY
# ============================================================

def test_persisted_preprocessor_exists():
    assert D7_PREPROCESSOR_PATH.exists()


def test_persisted_schema_exists():
    assert D7_TRANSFORMED_SCHEMA_PATH.exists()


def test_preprocessor_checksum_verifies():
    assert (
        calculate_file_sha256(
            D7_PREPROCESSOR_PATH
        )
        == PERSISTENCE[
            "preprocessor_sha256"
        ]
    )


def test_schema_checksum_verifies():
    assert (
        calculate_file_sha256(
            D7_TRANSFORMED_SCHEMA_PATH
        )
        == PERSISTENCE[
            "schema_sha256"
        ]
    )


def test_train_reload_reproduction_exact():
    assert (
        PERSISTENCE_VALIDATION[
            "train_reproduction_exact"
        ]
        is True
    )


def test_validation_reload_reproduction_exact():
    assert (
        PERSISTENCE_VALIDATION[
            "validation_reproduction_exact"
        ]
        is True
    )


def test_persisted_schema_matches_original():
    assert (
        PERSISTENCE_VALIDATION[
            "schema_matches_original"
        ]
        is True
    )


def test_loaded_schema_matches_original():
    assert (
        PERSISTENCE_VALIDATION[
            "loaded_schema_matches_original"
        ]
        is True
    )


# ============================================================
# D7.T10 — SERIALIZATION SMOKE TEST
# ============================================================

def test_joblib_preprocessor_reload():
    loaded = joblib.load(
        D7_PREPROCESSOR_PATH
    )

    assert hasattr(
        loaded,
        "transform",
    )


def test_reloaded_preprocessor_transforms_validation():
    loaded = joblib.load(
        D7_PREPROCESSOR_PATH
    )

    transformed = loaded.transform(
        FITTED_BUNDLE[
            "X_validation_raw"
        ]
    )

    assert transformed.shape == (
        EXPECTED_D7_VALIDATION_ENCOUNTERS,
        EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
    )


# ============================================================
# D7.T11 — EVIDENCE PACKAGE EXISTENCE
# ============================================================

def test_manifest_exists():
    assert D7_MANIFEST_PATH.exists()


def test_contract_exists():
    assert D7_CONTRACT_REPORT_PATH.exists()


def test_gate_decision_exists():
    assert D7_GATE_DECISION_PATH.exists()


def test_summary_table_exists():
    assert D7_SUMMARY_TABLE_PATH.exists()


def test_feature_registry_exists():
    assert D7_FEATURE_REGISTRY_PATH.exists()


def test_unknown_audit_exists():
    assert D7_UNKNOWN_AUDIT_PATH.exists()


def test_learned_state_exists():
    assert D7_LEARNED_STATE_PATH.exists()


# ============================================================
# D7.T12 — MANIFEST CONTROLS
# ============================================================

def test_manifest_stage_and_status():
    with D7_MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as handle:
        manifest = yaml.safe_load(
            handle
        )

    assert manifest[
        "stage"
    ] == "D7"

    assert manifest[
        "status"
    ] == "PASS"


def test_manifest_locked_test_not_accessed():
    with D7_MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as handle:
        manifest = yaml.safe_load(
            handle
        )

    assert (
        manifest[
            "development_boundary"
        ][
            "locked_test_accessed"
        ]
        is False
    )


def test_manifest_does_not_authorize_deployment():
    with D7_MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as handle:
        manifest = yaml.safe_load(
            handle
        )

    assert (
        manifest[
            "gate"
        ][
            "clinical_deployment_authorized"
        ]
        is False
    )


def test_manifest_does_not_authorize_locked_test():
    with D7_MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as handle:
        manifest = yaml.safe_load(
            handle
        )

    assert (
        manifest[
            "gate"
        ][
            "locked_test_evaluation_authorized"
        ]
        is False
    )


# ============================================================
# D7.T13 — EVIDENCE TABLE CONTROLS
# ============================================================

def test_feature_registry_has_49_rows():
    registry = pd.read_csv(
        D7_FEATURE_REGISTRY_PATH
    )

    assert len(
        registry
    ) == EXPECTED_D7_TRANSFORMED_FEATURE_COUNT


def test_feature_registry_all_authorized():
    registry = pd.read_csv(
        D7_FEATURE_REGISTRY_PATH
    )

    assert (
        registry[
            "authorized_for_primary_model"
        ]
        .astype(bool)
        .all()
    )


def test_unknown_audit_contains_race_and_gender():
    audit = pd.read_csv(
        D7_UNKNOWN_AUDIT_PATH
    )

    assert {
        "race",
        "gender",
    }.issubset(
        set(
            audit[
                "feature"
            ]
        )
    )


def test_learned_state_is_train_only():
    state = pd.read_csv(
        D7_LEARNED_STATE_PATH
    )

    assert set(
        state[
            "fit_partition"
        ]
    ) == {
        "train"
    }


# ============================================================
# D7.T14 — FINAL D7 GATE
# ============================================================

def test_d7_persistence_validation_passes():
    assert (
        PERSISTENCE_VALIDATION[
            "validation_status"
        ]
        == "PASS"
    )