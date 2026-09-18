# ============================================================
# D7 — GOVERNED PREPROCESSING PIPELINE
# ============================================================
"""
Governed preprocessing for the Diabetes Readmission Clinical AI
project.

D7 converts the frozen D6 primary candidate feature matrix into
model-ready representations while preserving the project's
prediction-time, leakage-prevention, patient-split, and locked-test
governance controls.

D7 PRINCIPLES
-------------
1. D6 determines which features are authorized.
2. D7 does not redesign or promote D6 features.
3. Preprocessing is developed using TRAIN + VALIDATION only.
4. Any preprocessing component that learns parameters from data
   MUST be fitted on TRAIN only.
5. VALIDATION may be transformed using the TRAIN-fitted pipeline.
6. VALIDATION must never contribute to fitting.
7. LOCKED TEST remains unavailable during D7 development.
8. Identifiers and outcomes are never model inputs.
9. D6-CONDITIONAL features remain excluded from the primary pathway.
10. The fitted preprocessing pipeline will be persisted,
    checksummed, tested, and governed before D8 modeling begins.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import hashlib
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer


# ============================================================
# D7.01 — PROJECT & FROZEN D6 DEPENDENCIES
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

D6_DEVELOPMENT_ARTIFACT = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "D6_development_engineered.parquet"
)

EXPECTED_D6_DEVELOPMENT_SHA256 = (
    "B4A38DFE8D316E2C74C8B08F31C0EC1060B880741304FC3971371DBFBA21C3C0"
)

EXPECTED_D6_DEVELOPMENT_ENCOUNTERS = 85076
EXPECTED_D6_DEVELOPMENT_PATIENTS = 59871
EXPECTED_D6_COMBINED_COLUMNS = 44

TARGET_COLUMN = "readmitted_30d"
GROUP_COLUMN = "patient_nbr"
SPLIT_COLUMN = "split"

TRAIN_LABEL = "train"
VALIDATION_LABEL = "validation"
LOCKED_TEST_LABEL = "test"


# ============================================================
# D7.02 — FROZEN PRIMARY FEATURE SCHEMA
# ============================================================

PRIMARY_CANDIDATE_FEATURES = [
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

CATEGORICAL_FEATURES = [
    "race",
    "gender",
    "age",
    "admission_type_id",
    "admission_source_id",
]

NUMERIC_FEATURES = [
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
]


# ============================================================
# D7.03 — PROHIBITED PRIMARY MODEL INPUTS
# ============================================================

IDENTIFIER_COLUMNS = {
    "encounter_id",
    "patient_nbr",
}

OUTCOME_COLUMNS = {
    "readmitted",
    "readmitted_30d",
}

D4_HARD_BLOCKED_RAW_FEATURES = {
    "discharge_disposition_id",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_diagnoses",
}

GOVERNANCE_COLUMNS = {
    "encounter_id",
    GROUP_COLUMN,
    TARGET_COLUMN,
    SPLIT_COLUMN,
}

PROHIBITED_PRIMARY_INPUTS = (
    IDENTIFIER_COLUMNS
    | OUTCOME_COLUMNS
    | D4_HARD_BLOCKED_RAW_FEATURES
    | GOVERNANCE_COLUMNS
)


# ============================================================
# D7.04 — PREPROCESSING POLICY
# ============================================================

CATEGORICAL_MISSING_STRATEGY = "most_frequent"
NUMERIC_MISSING_STRATEGY = "median"

UNKNOWN_CATEGORY_POLICY = "ignore"

ONE_HOT_DROP_POLICY = None

SPARSE_OUTPUT_POLICY = False


# ============================================================
# D7.05 — PREPROCESSING CONTRACT
# ============================================================

@dataclass(frozen=True)
class PreprocessingContract:
    """
    Machine-readable D7 preprocessing governance contract.
    """

    prediction_point: str

    target_column: str
    group_column: str
    split_column: str

    train_label: str
    validation_label: str
    locked_test_label: str

    primary_features: tuple[str, ...]
    categorical_features: tuple[str, ...]
    numeric_features: tuple[str, ...]

    categorical_missing_strategy: str
    numeric_missing_strategy: str

    unknown_category_policy: str
    one_hot_drop_policy: str | None
    sparse_output: bool

    fit_partition: str

    validation_fit_permitted: bool
    locked_test_access_permitted: bool


D7_PREPROCESSING_CONTRACT = PreprocessingContract(
    prediction_point=(
        "Before discharge, at the point when model output "
        "would support discharge-planning decisions."
    ),

    target_column=TARGET_COLUMN,
    group_column=GROUP_COLUMN,
    split_column=SPLIT_COLUMN,

    train_label=TRAIN_LABEL,
    validation_label=VALIDATION_LABEL,
    locked_test_label=LOCKED_TEST_LABEL,

    primary_features=tuple(
        PRIMARY_CANDIDATE_FEATURES
    ),

    categorical_features=tuple(
        CATEGORICAL_FEATURES
    ),

    numeric_features=tuple(
        NUMERIC_FEATURES
    ),

    categorical_missing_strategy=(
        CATEGORICAL_MISSING_STRATEGY
    ),

    numeric_missing_strategy=(
        NUMERIC_MISSING_STRATEGY
    ),

    unknown_category_policy=(
        UNKNOWN_CATEGORY_POLICY
    ),

    one_hot_drop_policy=(
        ONE_HOT_DROP_POLICY
    ),

    sparse_output=(
        SPARSE_OUTPUT_POLICY
    ),

    fit_partition=TRAIN_LABEL,

    validation_fit_permitted=False,

    locked_test_access_permitted=False,
)


# ============================================================
# D7.06 — STATIC CONTRACT VALIDATION
# ============================================================

def validate_d7_preprocessing_contract() -> dict[str, Any]:
    """
    Validate the D7 preprocessing contract before any data is
    loaded or any transformer is fitted.
    """

    primary = PRIMARY_CANDIDATE_FEATURES
    categorical = CATEGORICAL_FEATURES
    numeric = NUMERIC_FEATURES

    primary_set = set(primary)
    categorical_set = set(categorical)
    numeric_set = set(numeric)

    categorical_numeric_overlap = (
        categorical_set
        & numeric_set
    )

    schema_union = (
        categorical_set
        | numeric_set
    )

    missing_from_schema = (
        primary_set
        - schema_union
    )

    unexpected_in_schema = (
        schema_union
        - primary_set
    )

    prohibited_primary_features = (
        primary_set
        & PROHIBITED_PRIMARY_INPUTS
    )

    duplicate_primary_features = (
        len(primary)
        != len(primary_set)
    )

    duplicate_categorical_features = (
        len(categorical)
        != len(categorical_set)
    )

    duplicate_numeric_features = (
        len(numeric)
        != len(numeric_set)
    )

    checks = {
        "primary_feature_count":
            len(primary),

        "categorical_feature_count":
            len(categorical),

        "numeric_feature_count":
            len(numeric),

        "categorical_numeric_overlap":
            sorted(
                categorical_numeric_overlap
            ),

        "missing_from_preprocessing_schema":
            sorted(
                missing_from_schema
            ),

        "unexpected_in_preprocessing_schema":
            sorted(
                unexpected_in_schema
            ),

        "prohibited_primary_features":
            sorted(
                prohibited_primary_features
            ),

        "duplicate_primary_features":
            duplicate_primary_features,

        "duplicate_categorical_features":
            duplicate_categorical_features,

        "duplicate_numeric_features":
            duplicate_numeric_features,

        "fit_partition":
            D7_PREPROCESSING_CONTRACT.fit_partition,

        "validation_fit_permitted":
            D7_PREPROCESSING_CONTRACT.validation_fit_permitted,

        "locked_test_access_permitted":
            D7_PREPROCESSING_CONTRACT.locked_test_access_permitted,
    }

    passed = (
        len(primary) == 10
        and len(categorical) == 5
        and len(numeric) == 5
        and not categorical_numeric_overlap
        and not missing_from_schema
        and not unexpected_in_schema
        and not prohibited_primary_features
        and not duplicate_primary_features
        and not duplicate_categorical_features
        and not duplicate_numeric_features
        and (
            D7_PREPROCESSING_CONTRACT.fit_partition
            == TRAIN_LABEL
        )
        and (
            D7_PREPROCESSING_CONTRACT.validation_fit_permitted
            is False
        )
        and (
            D7_PREPROCESSING_CONTRACT.locked_test_access_permitted
            is False
        )
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D7.07 — FILE CHECKSUM UTILITY
# ============================================================

def calculate_file_sha256(
    path: Path,
) -> str:
    """
    Calculate an uppercase SHA-256 checksum for a file.
    """

    sha256 = hashlib.sha256()

    with path.open("rb") as file_handle:
        for block in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


# ============================================================
# D7.08 — LOAD & VERIFY FROZEN D6 DEVELOPMENT ARTIFACT
# ============================================================

def load_verified_d6_development_artifact(
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Load the frozen D6 development artifact and verify its
    checksum, dimensions, patient count, partitions, required
    governance columns, and primary feature schema.

    The D6 artifact must contain development data only:
    TRAIN + VALIDATION.

    LOCKED TEST must not be present.
    """

    if not D6_DEVELOPMENT_ARTIFACT.exists():
        raise FileNotFoundError(
            "Frozen D6 development artifact not found: "
            f"{D6_DEVELOPMENT_ARTIFACT}"
        )

    observed_checksum = calculate_file_sha256(
        D6_DEVELOPMENT_ARTIFACT
    )

    checksum_verified = (
        observed_checksum
        == EXPECTED_D6_DEVELOPMENT_SHA256
    )

    if not checksum_verified:
        raise RuntimeError(
            "Frozen D6 development artifact checksum mismatch. "
            f"Expected {EXPECTED_D6_DEVELOPMENT_SHA256}, "
            f"observed {observed_checksum}."
        )

    development_df = pd.read_parquet(
        D6_DEVELOPMENT_ARTIFACT
    )

    required_governance_columns = {
        "encounter_id",
        GROUP_COLUMN,
        TARGET_COLUMN,
        SPLIT_COLUMN,
    }

    missing_governance_columns = sorted(
        required_governance_columns
        - set(development_df.columns)
    )

    missing_primary_features = sorted(
        set(PRIMARY_CANDIDATE_FEATURES)
        - set(development_df.columns)
    )

    observed_splits = sorted(
        development_df[
            SPLIT_COLUMN
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    locked_test_present = (
        LOCKED_TEST_LABEL
        in observed_splits
    )

    unexpected_splits = sorted(
        set(observed_splits)
        - {
            TRAIN_LABEL,
            VALIDATION_LABEL,
        }
    )

    encounter_ids_unique = (
        not development_df[
            "encounter_id"
        ]
        .duplicated()
        .any()
    )

    target_missing_count = int(
        development_df[
            TARGET_COLUMN
        ]
        .isna()
        .sum()
    )

    target_values = sorted(
        development_df[
            TARGET_COLUMN
        ]
        .dropna()
        .unique()
        .tolist()
    )

    target_is_binary = (
        set(target_values)
        .issubset({0, 1})
    )

    checks = {
        "d6_checksum":
            observed_checksum,

        "d6_checksum_verified":
            checksum_verified,

        "development_encounters":
            int(len(development_df)),

        "development_patients":
            int(
                development_df[
                    GROUP_COLUMN
                ].nunique()
            ),

        "combined_columns":
            int(
                development_df.shape[1]
            ),

        "observed_splits":
            observed_splits,

        "locked_test_present":
            locked_test_present,

        "unexpected_splits":
            unexpected_splits,

        "missing_governance_columns":
            missing_governance_columns,

        "missing_primary_features":
            missing_primary_features,

        "encounter_ids_unique":
            encounter_ids_unique,

        "target_missing_count":
            target_missing_count,

        "target_values":
            target_values,

        "target_is_binary":
            target_is_binary,
    }

    passed = (
        checksum_verified
        and (
            len(development_df)
            == EXPECTED_D6_DEVELOPMENT_ENCOUNTERS
        )
        and (
            development_df[
                GROUP_COLUMN
            ].nunique()
            == EXPECTED_D6_DEVELOPMENT_PATIENTS
        )
        and (
            development_df.shape[1]
            == EXPECTED_D6_COMBINED_COLUMNS
        )
        and (
            set(observed_splits)
            == {
                TRAIN_LABEL,
                VALIDATION_LABEL,
            }
        )
        and not locked_test_present
        and not unexpected_splits
        and not missing_governance_columns
        and not missing_primary_features
        and encounter_ids_unique
        and target_missing_count == 0
        and target_is_binary
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    if not passed:
        raise RuntimeError(
            "Frozen D6 development artifact failed D7 "
            "ingestion validation."
        )

    return development_df, checks


# ============================================================
# D7.09 — BUILD GOVERNED TRAIN / VALIDATION PARTITIONS
# ============================================================

def build_d7_train_validation_partitions(
) -> dict[str, Any]:
    """
    Construct the governed D7 development partitions.

    TRAIN:
        Authorized for preprocessing FIT + TRANSFORM.

    VALIDATION:
        Authorized for TRANSFORM only.

    LOCKED TEST:
        Not available in the D6 development artifact and therefore
        cannot participate in D7 preprocessing development.
    """

    development_df, d6_validation = (
        load_verified_d6_development_artifact()
    )

    train_df = (
        development_df.loc[
            development_df[
                SPLIT_COLUMN
            ]
            == TRAIN_LABEL
        ]
        .copy()
    )

    validation_df = (
        development_df.loc[
            development_df[
                SPLIT_COLUMN
            ]
            == VALIDATION_LABEL
        ]
        .copy()
    )

    X_train = train_df[
        PRIMARY_CANDIDATE_FEATURES
    ].copy()

    y_train = train_df[
        TARGET_COLUMN
    ].copy()

    X_validation = validation_df[
        PRIMARY_CANDIDATE_FEATURES
    ].copy()

    y_validation = validation_df[
        TARGET_COLUMN
    ].copy()

    train_encounter_ids = (
        train_df[
            "encounter_id"
        ].copy()
    )

    validation_encounter_ids = (
        validation_df[
            "encounter_id"
        ].copy()
    )

    train_patient_ids = set(
        train_df[
            GROUP_COLUMN
        ].unique()
    )

    validation_patient_ids = set(
        validation_df[
            GROUP_COLUMN
        ].unique()
    )

    patient_overlap = (
        train_patient_ids
        & validation_patient_ids
    )

    return {
        "development_df":
            development_df,

        "train_df":
            train_df,

        "validation_df":
            validation_df,

        "X_train":
            X_train,

        "y_train":
            y_train,

        "X_validation":
            X_validation,

        "y_validation":
            y_validation,

        "train_encounter_ids":
            train_encounter_ids,

        "validation_encounter_ids":
            validation_encounter_ids,

        "d6_validation":
            d6_validation,

        "patient_overlap":
            patient_overlap,
    }


# ============================================================
# D7.10 — VALIDATE TRAIN / VALIDATION BOUNDARY
# ============================================================

def validate_d7_train_validation_boundary(
    partitions: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate that D7 preserves the frozen patient-level
    train/validation boundary before preprocessing is fitted.
    """

    train_df = partitions["train_df"]
    validation_df = partitions[
        "validation_df"
    ]

    X_train = partitions["X_train"]
    y_train = partitions["y_train"]

    X_validation = partitions[
        "X_validation"
    ]
    y_validation = partitions[
        "y_validation"
    ]

    patient_overlap = partitions[
        "patient_overlap"
    ]

    train_encounter_overlap = (
        set(
            train_df[
                "encounter_id"
            ].tolist()
        )
        & set(
            validation_df[
                "encounter_id"
            ].tolist()
        )
    )

    train_target_values = set(
        y_train
        .dropna()
        .unique()
        .tolist()
    )

    validation_target_values = set(
        y_validation
        .dropna()
        .unique()
        .tolist()
    )

    prohibited_in_train_X = sorted(
        set(X_train.columns)
        & PROHIBITED_PRIMARY_INPUTS
    )

    prohibited_in_validation_X = sorted(
        set(X_validation.columns)
        & PROHIBITED_PRIMARY_INPUTS
    )

    checks = {
        "train_encounters":
            int(len(train_df)),

        "validation_encounters":
            int(len(validation_df)),

        "development_encounters":
            int(
                len(train_df)
                + len(validation_df)
            ),

        "train_patients":
            int(
                train_df[
                    GROUP_COLUMN
                ].nunique()
            ),

        "validation_patients":
            int(
                validation_df[
                    GROUP_COLUMN
                ].nunique()
            ),

        "patient_overlap_count":
            int(len(patient_overlap)),

        "encounter_overlap_count":
            int(
                len(
                    train_encounter_overlap
                )
            ),

        "X_train_shape":
            tuple(X_train.shape),

        "X_validation_shape":
            tuple(
                X_validation.shape
            ),

        "y_train_rows":
            int(len(y_train)),

        "y_validation_rows":
            int(
                len(y_validation)
            ),

        "train_target_values":
            sorted(
                train_target_values
            ),

        "validation_target_values":
            sorted(
                validation_target_values
            ),

        "prohibited_in_train_X":
            prohibited_in_train_X,

        "prohibited_in_validation_X":
            prohibited_in_validation_X,

        "train_feature_order_correct":
            (
                list(X_train.columns)
                == PRIMARY_CANDIDATE_FEATURES
            ),

        "validation_feature_order_correct":
            (
                list(
                    X_validation.columns
                )
                == PRIMARY_CANDIDATE_FEATURES
            ),

        "locked_test_present":
            bool(
                LOCKED_TEST_LABEL
                in set(
                    partitions[
                        "development_df"
                    ][
                        SPLIT_COLUMN
                    ].unique()
                )
            ),
    }

    passed = (
        (
            len(train_df)
            + len(validation_df)
            == EXPECTED_D6_DEVELOPMENT_ENCOUNTERS
        )
        and len(patient_overlap) == 0
        and len(
            train_encounter_overlap
        ) == 0
        and X_train.shape[1] == 10
        and X_validation.shape[1] == 10
        and len(X_train) == len(y_train)
        and (
            len(X_validation)
            == len(y_validation)
        )
        and train_target_values.issubset(
            {0, 1}
        )
        and validation_target_values.issubset(
            {0, 1}
        )
        and not prohibited_in_train_X
        and not prohibited_in_validation_X
        and (
            list(X_train.columns)
            == PRIMARY_CANDIDATE_FEATURES
        )
        and (
            list(X_validation.columns)
            == PRIMARY_CANDIDATE_FEATURES
        )
        and not checks[
            "locked_test_present"
        ]
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D7.11 — BUILD UNFITTED PREPROCESSING PIPELINE
# ============================================================

def build_primary_preprocessor() -> ColumnTransformer:
    """
    Construct the governed primary preprocessing pipeline.

    IMPORTANT:
    This function only constructs the transformer.
    It does NOT fit anything.

    Categorical pathway:
        1. Most-frequent imputation
        2. One-hot encoding
        3. Unknown validation categories are ignored

    Numeric pathway:
        1. Median imputation

    No scaling is applied in D7 at this stage because the current
    numeric features are binary/count-based utilization features.
    Model-specific scaling, if required, will be governed within
    the downstream modeling pipeline rather than silently embedded
    here without justification.
    """

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy=(
                        CATEGORICAL_MISSING_STRATEGY
                    )
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown=(
                        UNKNOWN_CATEGORY_POLICY
                    ),
                    drop=ONE_HOT_DROP_POLICY,
                    sparse_output=(
                        SPARSE_OUTPUT_POLICY
                    ),
                ),
            ),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy=(
                        NUMERIC_MISSING_STRATEGY
                    )
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )

    return preprocessor


# ============================================================
# D7.12 — FIT ON TRAIN ONLY
# ============================================================

def fit_primary_preprocessor_on_train(
    partitions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Fit the D7 preprocessing pipeline exclusively on TRAIN.

    VALIDATION is not passed to .fit().
    LOCKED TEST is unavailable.

    Returns the fitted transformer together with transformed
    TRAIN and VALIDATION matrices and governance metadata.
    """

    if partitions is None:
        partitions = (
            build_d7_train_validation_partitions()
        )

    boundary_validation = (
        validate_d7_train_validation_boundary(
            partitions
        )
    )

    if (
        boundary_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D7 preprocessing fit blocked because the "
            "train/validation governance boundary failed."
        )

    X_train = partitions["X_train"]
    y_train = partitions["y_train"]

    X_validation = partitions[
        "X_validation"
    ]
    y_validation = partitions[
        "y_validation"
    ]

    preprocessor = (
        build_primary_preprocessor()
    )

    # --------------------------------------------------------
    # CRITICAL GOVERNANCE CONTROL
    # FIT occurs on TRAIN ONLY.
    # --------------------------------------------------------

    preprocessor.fit(
        X_train
    )

    # --------------------------------------------------------
    # TRAIN and VALIDATION are transformed using the SAME
    # train-fitted preprocessing state.
    # --------------------------------------------------------

    X_train_transformed = (
        preprocessor.transform(
            X_train
        )
    )

    X_validation_transformed = (
        preprocessor.transform(
            X_validation
        )
    )

    transformed_feature_names = (
        preprocessor
        .get_feature_names_out()
        .tolist()
    )

    X_train_transformed = pd.DataFrame(
        X_train_transformed,
        columns=transformed_feature_names,
        index=X_train.index,
    )

    X_validation_transformed = pd.DataFrame(
        X_validation_transformed,
        columns=transformed_feature_names,
        index=X_validation.index,
    )

    return {
        "preprocessor":
            preprocessor,

        "X_train_raw":
            X_train,

        "X_validation_raw":
            X_validation,

        "X_train_transformed":
            X_train_transformed,

        "X_validation_transformed":
            X_validation_transformed,

        "y_train":
            y_train,

        "y_validation":
            y_validation,

        "transformed_feature_names":
            transformed_feature_names,

        "boundary_validation":
            boundary_validation,
    }


# ============================================================
# D7.13 — VALIDATE FITTED PREPROCESSING OUTPUT
# ============================================================

def validate_fitted_primary_preprocessor(
    fitted_bundle: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate the fitted D7 preprocessing pipeline and transformed
    TRAIN/VALIDATION matrices.

    This validates:
    - row preservation;
    - identical transformed schema;
    - absence of missing values;
    - finite numeric representation;
    - target alignment;
    - unique transformed feature names;
    - preservation of TRAIN/VALIDATION isolation.
    """

    X_train_raw = fitted_bundle[
        "X_train_raw"
    ]

    X_validation_raw = fitted_bundle[
        "X_validation_raw"
    ]

    X_train_transformed = fitted_bundle[
        "X_train_transformed"
    ]

    X_validation_transformed = fitted_bundle[
        "X_validation_transformed"
    ]

    y_train = fitted_bundle["y_train"]

    y_validation = fitted_bundle[
        "y_validation"
    ]

    transformed_feature_names = (
        fitted_bundle[
            "transformed_feature_names"
        ]
    )

    train_missing_values = int(
        X_train_transformed
        .isna()
        .sum()
        .sum()
    )

    validation_missing_values = int(
        X_validation_transformed
        .isna()
        .sum()
        .sum()
    )

    train_values = (
        X_train_transformed
        .to_numpy(
            dtype=float
        )
    )

    validation_values = (
        X_validation_transformed
        .to_numpy(
            dtype=float
        )
    )

    train_nonfinite_values = int(
        np.size(train_values)
        - np.isfinite(
            train_values
        ).sum()
    )

    validation_nonfinite_values = int(
        np.size(validation_values)
        - np.isfinite(
            validation_values
        ).sum()
    )

    transformed_schema_identical = (
        list(
            X_train_transformed.columns
        )
        == list(
            X_validation_transformed.columns
        )
    )

    transformed_feature_names_unique = (
        len(transformed_feature_names)
        == len(
            set(
                transformed_feature_names
            )
        )
    )

    train_row_preservation = (
        len(X_train_raw)
        == len(
            X_train_transformed
        )
        == len(y_train)
    )

    validation_row_preservation = (
        len(X_validation_raw)
        == len(
            X_validation_transformed
        )
        == len(y_validation)
    )

    train_index_alignment = (
        X_train_transformed.index.equals(
            y_train.index
        )
    )

    validation_index_alignment = (
        X_validation_transformed.index.equals(
            y_validation.index
        )
    )

    checks = {
        "raw_train_shape":
            tuple(
                X_train_raw.shape
            ),

        "raw_validation_shape":
            tuple(
                X_validation_raw.shape
            ),

        "transformed_train_shape":
            tuple(
                X_train_transformed.shape
            ),

        "transformed_validation_shape":
            tuple(
                X_validation_transformed.shape
            ),

        "transformed_feature_count":
            int(
                X_train_transformed.shape[1]
            ),

        "train_row_preservation":
            train_row_preservation,

        "validation_row_preservation":
            validation_row_preservation,

        "transformed_schema_identical":
            transformed_schema_identical,

        "transformed_feature_names_unique":
            transformed_feature_names_unique,

        "train_missing_values":
            train_missing_values,

        "validation_missing_values":
            validation_missing_values,

        "train_nonfinite_values":
            train_nonfinite_values,

        "validation_nonfinite_values":
            validation_nonfinite_values,

        "train_index_alignment":
            train_index_alignment,

        "validation_index_alignment":
            validation_index_alignment,

        "fit_partition":
            TRAIN_LABEL,

        "validation_contributed_to_fit":
            False,

        "locked_test_accessed":
            False,
    }

    passed = (
        train_row_preservation
        and validation_row_preservation
        and transformed_schema_identical
        and transformed_feature_names_unique
        and train_missing_values == 0
        and validation_missing_values == 0
        and train_nonfinite_values == 0
        and validation_nonfinite_values == 0
        and train_index_alignment
        and validation_index_alignment
        and (
            checks[
                "fit_partition"
            ]
            == TRAIN_LABEL
        )
        and (
            checks[
                "validation_contributed_to_fit"
            ]
            is False
        )
        and (
            checks[
                "locked_test_accessed"
            ]
            is False
        )
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks


# ============================================================
# D7.14 — BUILD, FIT & VALIDATE PRIMARY PREPROCESSING
# ============================================================

def build_fitted_d7_primary_preprocessing(
) -> dict[str, Any]:
    """
    Execute the governed D7 primary preprocessing workflow.

    This remains a DEVELOPMENT-ONLY operation:
        TRAIN      -> FIT + TRANSFORM
        VALIDATION -> TRANSFORM ONLY
        LOCKED TEST -> NOT ACCESSED
    """

    contract_validation = (
        validate_d7_preprocessing_contract()
    )

    if (
        contract_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D7 preprocessing contract validation failed."
        )

    partitions = (
        build_d7_train_validation_partitions()
    )

    fitted_bundle = (
        fit_primary_preprocessor_on_train(
            partitions
        )
    )

    preprocessing_validation = (
        validate_fitted_primary_preprocessor(
            fitted_bundle
        )
    )

    if (
        preprocessing_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D7 fitted preprocessing validation failed."
        )

    fitted_bundle[
        "contract_validation"
    ] = contract_validation

    fitted_bundle[
        "preprocessing_validation"
    ] = preprocessing_validation

    return fitted_bundle

# ============================================================
# D7.15 — SOURCE-SPECIFIC UNKNOWN CATEGORY POLICY
# ============================================================

SOURCE_UNKNOWN_CATEGORY_VALUES = {
    "race": {
        "?",
    },

    "gender": {
        "Unknown/Invalid",
        "?",
    },

    "age": {
        "?",
    },

    "admission_type_id": set(),

    "admission_source_id": set(),
}

CANONICAL_UNKNOWN_CATEGORY = "__MISSING_OR_UNKNOWN__"


# ============================================================
# D7.16 — AUDIT SOURCE UNKNOWN CATEGORIES
# ============================================================

def audit_source_unknown_categories(
    X_train: pd.DataFrame,
    X_validation: pd.DataFrame,
) -> pd.DataFrame:
    """
    Quantify source-specific missing/unknown categorical values
    before preprocessing.

    This audit is descriptive only. It does not learn any
    parameters and therefore does not introduce validation
    leakage.
    """

    records = []

    for feature in CATEGORICAL_FEATURES:

        configured_unknowns = (
            SOURCE_UNKNOWN_CATEGORY_VALUES.get(
                feature,
                set(),
            )
        )

        for partition_name, frame in (
            (TRAIN_LABEL, X_train),
            (VALIDATION_LABEL, X_validation),
        ):

            series = frame[feature]

            explicit_unknown_mask = (
                series.isin(
                    configured_unknowns
                )
                if configured_unknowns
                else pd.Series(
                    False,
                    index=series.index,
                )
            )

            native_missing_mask = (
                series.isna()
            )

            combined_unknown_mask = (
                explicit_unknown_mask
                | native_missing_mask
            )

            records.append(
                {
                    "partition":
                        partition_name,

                    "feature":
                        feature,

                    "rows":
                        int(len(series)),

                    "native_missing_count":
                        int(
                            native_missing_mask.sum()
                        ),

                    "explicit_unknown_count":
                        int(
                            explicit_unknown_mask.sum()
                        ),

                    "total_missing_or_unknown":
                        int(
                            combined_unknown_mask.sum()
                        ),

                    "missing_or_unknown_rate":
                        float(
                            combined_unknown_mask.mean()
                        ),
                }
            )

    return pd.DataFrame(records)


# ============================================================
# D7.17 — NORMALIZE EXPLICIT UNKNOWN CATEGORIES
# ============================================================

def normalize_source_unknown_categories(
    X: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert source-specific explicit unknown-category markers to
    a canonical, transparent unknown category.

    Examples:
        race == "?" -> "__MISSING_OR_UNKNOWN__"
        gender == "Unknown/Invalid" -> "__MISSING_OR_UNKNOWN__"

    This preserves demographic uncertainty rather than imputing an
    unknown demographic value into an observed demographic group.

    The transformation is deterministic and does not learn from
    TRAIN, VALIDATION, or LOCKED TEST.
    """

    normalized = X.copy()

    for (
        feature,
        unknown_values,
    ) in SOURCE_UNKNOWN_CATEGORY_VALUES.items():

        if feature not in normalized.columns:
            raise KeyError(
                "Unknown-category normalization expected "
                f"feature '{feature}', but it was absent."
            )

        if not unknown_values:
            continue

        normalized.loc[
            normalized[
                feature
            ].isin(
                unknown_values
            ),
            feature,
        ] = CANONICAL_UNKNOWN_CATEGORY

    return normalized


# ============================================================
# D7.18 — VALIDATE UNKNOWN-CATEGORY NORMALIZATION
# ============================================================

def validate_unknown_category_normalization(
    raw_X: pd.DataFrame,
    normalized_X: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate deterministic source-unknown normalization.
    """

    if len(raw_X) != len(normalized_X):
        raise RuntimeError(
            "Unknown-category normalization changed row count."
        )

    if list(raw_X.columns) != list(
        normalized_X.columns
    ):
        raise RuntimeError(
            "Unknown-category normalization changed schema."
        )

    residual_explicit_unknowns = {}

    for (
        feature,
        unknown_values,
    ) in SOURCE_UNKNOWN_CATEGORY_VALUES.items():

        if unknown_values:
            residual_explicit_unknowns[
                feature
            ] = int(
                normalized_X[
                    feature
                ]
                .isin(
                    unknown_values
                )
                .sum()
            )

    nonzero_residuals = {
        feature: count
        for feature, count
        in residual_explicit_unknowns.items()
        if count != 0
    }

    canonical_unknown_counts = {
        feature: int(
            (
                normalized_X[feature]
                == CANONICAL_UNKNOWN_CATEGORY
            ).sum()
        )
        for feature, unknown_values
        in SOURCE_UNKNOWN_CATEGORY_VALUES.items()
        if unknown_values
    }

    noncategorical_features_unchanged = all(
        raw_X[feature].equals(
            normalized_X[feature]
        )
        for feature
        in NUMERIC_FEATURES
    )

    checks = {
        "rows_preserved":
            len(raw_X)
            == len(normalized_X),

        "columns_preserved":
            list(raw_X.columns)
            == list(
                normalized_X.columns
            ),

        "residual_explicit_unknowns":
            residual_explicit_unknowns,

        "nonzero_residual_explicit_unknowns":
            nonzero_residuals,

        "canonical_unknown_counts":
            canonical_unknown_counts,

        "numeric_features_unchanged":
            noncategorical_features_unchanged,
    }

    passed = (
        checks["rows_preserved"]
        and checks["columns_preserved"]
        and not nonzero_residuals
        and noncategorical_features_unchanged
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks

# ============================================================
# D7.19 — SKLEARN-COMPATIBLE UNKNOWN NORMALIZER
# ============================================================

def normalize_categorical_unknowns_for_pipeline(
    X: pd.DataFrame,
) -> pd.DataFrame:
    """
    Deterministically normalize configured explicit source
    unknown-category markers before categorical imputation.

    This function is embedded inside the persisted sklearn
    preprocessing pipeline so the same rule is applied during
    training, validation, future inference, and eventual
    locked-test transformation.

    It learns no parameters from the data.
    """

    normalized = X.copy()

    for feature in CATEGORICAL_FEATURES:

        unknown_values = (
            SOURCE_UNKNOWN_CATEGORY_VALUES.get(
                feature,
                set(),
            )
        )

        if not unknown_values:
            continue

        normalized.loc[
            normalized[
                feature
            ].isin(
                unknown_values
            ),
            feature,
        ] = CANONICAL_UNKNOWN_CATEGORY

    return normalized


# ============================================================
# D7.20 — BUILD GOVERNED PREPROCESSOR WITH UNKNOWN NORMALIZATION
# ============================================================

def build_governed_primary_preprocessor(
) -> ColumnTransformer:
    """
    Construct the complete governed D7 preprocessing pipeline.

    CATEGORICAL
    -----------
    1. Normalize source-specific explicit unknown markers to a
       canonical transparent unknown category.
    2. Fit most-frequent imputation on TRAIN only for true/native
       missing values.
    3. Fit one-hot encoding on TRAIN only.
    4. Ignore genuinely unseen categories during later transformation.

    NUMERIC
    -------
    1. Fit median imputation on TRAIN only.

    LOCKED TEST
    -----------
    Never accessed during D7 development.
    """

    categorical_pipeline = Pipeline(
        steps=[
            (
                "unknown_normalizer",
                FunctionTransformer(
                    normalize_categorical_unknowns_for_pipeline,
                    validate=False,
                    feature_names_out="one-to-one",
                ),
            ),
            (
                "imputer",
                SimpleImputer(
                    strategy=(
                        CATEGORICAL_MISSING_STRATEGY
                    )
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown=(
                        UNKNOWN_CATEGORY_POLICY
                    ),
                    drop=ONE_HOT_DROP_POLICY,
                    sparse_output=(
                        SPARSE_OUTPUT_POLICY
                    ),
                ),
            ),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy=(
                        NUMERIC_MISSING_STRATEGY
                    )
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )


# ============================================================
# D7.21 — FIT GOVERNED PREPROCESSOR ON TRAIN ONLY
# ============================================================

def fit_governed_primary_preprocessor(
) -> dict[str, Any]:
    """
    Fit the final governed D7 preprocessing architecture.

    TRAIN:
        FIT + TRANSFORM

    VALIDATION:
        TRANSFORM ONLY

    LOCKED TEST:
        NOT ACCESSED
    """

    partitions = (
        build_d7_train_validation_partitions()
    )

    boundary_validation = (
        validate_d7_train_validation_boundary(
            partitions
        )
    )

    if (
        boundary_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D7 train/validation boundary failed."
        )

    X_train = partitions["X_train"]
    X_validation = partitions[
        "X_validation"
    ]

    y_train = partitions["y_train"]
    y_validation = partitions[
        "y_validation"
    ]

    unknown_category_audit = (
        audit_source_unknown_categories(
            X_train,
            X_validation,
        )
    )

    train_normalized = (
        normalize_source_unknown_categories(
            X_train
        )
    )

    validation_normalized = (
        normalize_source_unknown_categories(
            X_validation
        )
    )

    train_normalization_validation = (
        validate_unknown_category_normalization(
            X_train,
            train_normalized,
        )
    )

    validation_normalization_validation = (
        validate_unknown_category_normalization(
            X_validation,
            validation_normalized,
        )
    )

    if (
        train_normalization_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "TRAIN unknown-category normalization failed."
        )

    if (
        validation_normalization_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "VALIDATION unknown-category normalization failed."
        )

    preprocessor = (
        build_governed_primary_preprocessor()
    )

    # --------------------------------------------------------
    # CRITICAL:
    # Only TRAIN is supplied to fit().
    # --------------------------------------------------------

    preprocessor.fit(
        X_train
    )

    X_train_transformed_array = (
        preprocessor.transform(
            X_train
        )
    )

    X_validation_transformed_array = (
        preprocessor.transform(
            X_validation
        )
    )

    transformed_feature_names = (
        preprocessor
        .get_feature_names_out()
        .tolist()
    )

    X_train_transformed = pd.DataFrame(
        X_train_transformed_array,
        columns=transformed_feature_names,
        index=X_train.index,
    )

    X_validation_transformed = pd.DataFrame(
        X_validation_transformed_array,
        columns=transformed_feature_names,
        index=X_validation.index,
    )

    bundle = {
        "preprocessor":
            preprocessor,

        "X_train_raw":
            X_train,

        "X_validation_raw":
            X_validation,

        "X_train_transformed":
            X_train_transformed,

        "X_validation_transformed":
            X_validation_transformed,

        "y_train":
            y_train,

        "y_validation":
            y_validation,

        "transformed_feature_names":
            transformed_feature_names,

        "unknown_category_audit":
            unknown_category_audit,

        "train_normalization_validation":
            train_normalization_validation,

        "validation_normalization_validation":
            validation_normalization_validation,

        "boundary_validation":
            boundary_validation,
    }

    preprocessing_validation = (
        validate_fitted_primary_preprocessor(
            bundle
        )
    )

    bundle[
        "preprocessing_validation"
    ] = preprocessing_validation

    return bundle

# ============================================================
# D7.22 — PERSISTED PREPROCESSING ARTIFACT PATHS
# ============================================================

PREPROCESSOR_ARTIFACT_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "preprocessors"
)

D7_PREPROCESSOR_PATH = (
    PREPROCESSOR_ARTIFACT_DIR
    / "D7_primary_preprocessor.joblib"
)

D7_TRANSFORMED_SCHEMA_PATH = (
    PREPROCESSOR_ARTIFACT_DIR
    / "D7_transformed_feature_schema.txt"
)

EXPECTED_D7_RAW_FEATURE_COUNT = 10
EXPECTED_D7_TRANSFORMED_FEATURE_COUNT = 49

EXPECTED_D7_TRAIN_ENCOUNTERS = 70024
EXPECTED_D7_VALIDATION_ENCOUNTERS = 15052


# ============================================================
# D7.23 — PREPARE PREPROCESSOR ARTIFACT DIRECTORY
# ============================================================

def prepare_d7_preprocessor_artifact_directory(
) -> None:
    """
    Ensure the governed D7 preprocessing artifact directory exists.
    """

    PREPROCESSOR_ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# D7.24 — PERSIST FITTED PRIMARY PREPROCESSOR
# ============================================================

def persist_fitted_primary_preprocessor(
    fitted_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Persist the TRAIN-fitted D7 preprocessing transformer and
    transformed feature schema.

    The persisted transformer contains the learned TRAIN-only:

    - categorical imputation state;
    - categorical vocabulary;
    - one-hot encoding state;
    - numeric median imputation state;
    - deterministic source-unknown normalization logic.

    VALIDATION contributes no fitted state.
    LOCKED TEST remains unaccessed.
    """

    if fitted_bundle is None:
        fitted_bundle = (
            fit_governed_primary_preprocessor()
        )

    preprocessing_validation = (
        fitted_bundle[
            "preprocessing_validation"
        ]
    )

    if (
        preprocessing_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D7 preprocessor persistence blocked because "
            "preprocessing validation failed."
        )

    transformed_feature_names = (
        fitted_bundle[
            "transformed_feature_names"
        ]
    )

    if (
        len(transformed_feature_names)
        != EXPECTED_D7_TRANSFORMED_FEATURE_COUNT
    ):
        raise RuntimeError(
            "Unexpected D7 transformed feature count. "
            f"Expected "
            f"{EXPECTED_D7_TRANSFORMED_FEATURE_COUNT}, "
            f"observed "
            f"{len(transformed_feature_names)}."
        )

    prepare_d7_preprocessor_artifact_directory()

    # --------------------------------------------------------
    # Persist fitted sklearn preprocessing object.
    # --------------------------------------------------------

    joblib.dump(
        fitted_bundle[
            "preprocessor"
        ],
        D7_PREPROCESSOR_PATH,
    )

    # --------------------------------------------------------
    # Persist authoritative transformed feature order.
    # --------------------------------------------------------

    D7_TRANSFORMED_SCHEMA_PATH.write_text(
        "\n".join(
            transformed_feature_names
        )
        + "\n",
        encoding="utf-8",
    )

    preprocessor_sha256 = (
        calculate_file_sha256(
            D7_PREPROCESSOR_PATH
        )
    )

    schema_sha256 = (
        calculate_file_sha256(
            D7_TRANSFORMED_SCHEMA_PATH
        )
    )

    return {
        "preprocessor_path":
            str(D7_PREPROCESSOR_PATH),

        "preprocessor_sha256":
            preprocessor_sha256,

        "schema_path":
            str(
                D7_TRANSFORMED_SCHEMA_PATH
            ),

        "schema_sha256":
            schema_sha256,

        "raw_feature_count":
            EXPECTED_D7_RAW_FEATURE_COUNT,

        "transformed_feature_count":
            len(
                transformed_feature_names
            ),

        "train_encounters":
            int(
                len(
                    fitted_bundle[
                        "X_train_raw"
                    ]
                )
            ),

        "validation_encounters":
            int(
                len(
                    fitted_bundle[
                        "X_validation_raw"
                    ]
                )
            ),

        "fit_partition":
            TRAIN_LABEL,

        "validation_contributed_to_fit":
            False,

        "locked_test_accessed":
            False,

        "validation_status":
            "PASS",
    }


# ============================================================
# D7.25 — LOAD PERSISTED PREPROCESSOR
# ============================================================

def load_persisted_primary_preprocessor(
) -> ColumnTransformer:
    """
    Load the persisted D7 TRAIN-fitted primary preprocessor.
    """

    if not D7_PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            "Persisted D7 preprocessor not found: "
            f"{D7_PREPROCESSOR_PATH}"
        )

    preprocessor = joblib.load(
        D7_PREPROCESSOR_PATH
    )

    return preprocessor


# ============================================================
# D7.26 — LOAD PERSISTED TRANSFORMED SCHEMA
# ============================================================

def load_persisted_transformed_schema(
) -> list[str]:
    """
    Load the authoritative D7 transformed feature order.
    """

    if not D7_TRANSFORMED_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            "Persisted D7 transformed schema not found: "
            f"{D7_TRANSFORMED_SCHEMA_PATH}"
        )

    feature_names = [
        line.strip()
        for line
        in D7_TRANSFORMED_SCHEMA_PATH
        .read_text(
            encoding="utf-8"
        )
        .splitlines()
        if line.strip()
    ]

    return feature_names


# ============================================================
# D7.27 — VALIDATE PERSISTED PREPROCESSOR
# ============================================================

def validate_persisted_primary_preprocessor(
    original_bundle: dict[str, Any],
    persistence_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Reload the persisted preprocessor and prove that it reproduces
    the original TRAIN and VALIDATION transformations exactly.

    This is the reproducibility gate for the fitted D7 transformer.
    """

    loaded_preprocessor = (
        load_persisted_primary_preprocessor()
    )

    persisted_schema = (
        load_persisted_transformed_schema()
    )

    X_train_raw = (
        original_bundle[
            "X_train_raw"
        ]
    )

    X_validation_raw = (
        original_bundle[
            "X_validation_raw"
        ]
    )

    original_train = (
        original_bundle[
            "X_train_transformed"
        ]
    )

    original_validation = (
        original_bundle[
            "X_validation_transformed"
        ]
    )

    reloaded_train_array = (
        loaded_preprocessor.transform(
            X_train_raw
        )
    )

    reloaded_validation_array = (
        loaded_preprocessor.transform(
            X_validation_raw
        )
    )

    loaded_feature_names = (
        loaded_preprocessor
        .get_feature_names_out()
        .tolist()
    )

    reloaded_train = pd.DataFrame(
        reloaded_train_array,
        columns=loaded_feature_names,
        index=X_train_raw.index,
    )

    reloaded_validation = pd.DataFrame(
        reloaded_validation_array,
        columns=loaded_feature_names,
        index=X_validation_raw.index,
    )

    train_reproduction_exact = (
        np.array_equal(
            original_train.to_numpy(),
            reloaded_train.to_numpy(),
            equal_nan=True,
        )
    )

    validation_reproduction_exact = (
        np.array_equal(
            original_validation.to_numpy(),
            reloaded_validation.to_numpy(),
            equal_nan=True,
        )
    )

    original_schema = (
        original_bundle[
            "transformed_feature_names"
        ]
    )

    schema_matches_original = (
        persisted_schema
        == original_schema
    )

    loaded_schema_matches_original = (
        loaded_feature_names
        == original_schema
    )

    preprocessor_checksum_verified = (
        calculate_file_sha256(
            D7_PREPROCESSOR_PATH
        )
        == persistence_result[
            "preprocessor_sha256"
        ]
    )

    schema_checksum_verified = (
        calculate_file_sha256(
            D7_TRANSFORMED_SCHEMA_PATH
        )
        == persistence_result[
            "schema_sha256"
        ]
    )

    canonical_unknown_features = [
        feature
        for feature
        in persisted_schema
        if (
            CANONICAL_UNKNOWN_CATEGORY
            in feature
        )
    ]

    raw_race_unknown_feature_present = any(
        "race_?"
        in feature
        for feature
        in persisted_schema
    )

    raw_gender_unknown_feature_present = any(
        "gender_Unknown/Invalid"
        in feature
        for feature
        in persisted_schema
    )

    checks = {
        "persisted_preprocessor_exists":
            D7_PREPROCESSOR_PATH.exists(),

        "persisted_schema_exists":
            D7_TRANSFORMED_SCHEMA_PATH.exists(),

        "preprocessor_checksum_verified":
            preprocessor_checksum_verified,

        "schema_checksum_verified":
            schema_checksum_verified,

        "persisted_feature_count":
            len(
                persisted_schema
            ),

        "loaded_feature_count":
            len(
                loaded_feature_names
            ),

        "schema_matches_original":
            schema_matches_original,

        "loaded_schema_matches_original":
            loaded_schema_matches_original,

        "train_reproduction_exact":
            train_reproduction_exact,

        "validation_reproduction_exact":
            validation_reproduction_exact,

        "canonical_unknown_features":
            canonical_unknown_features,

        "raw_race_unknown_feature_present":
            raw_race_unknown_feature_present,

        "raw_gender_unknown_feature_present":
            raw_gender_unknown_feature_present,

        "fit_partition":
            TRAIN_LABEL,

        "validation_contributed_to_fit":
            False,

        "locked_test_accessed":
            False,
    }

    passed = (
        checks[
            "persisted_preprocessor_exists"
        ]
        and checks[
            "persisted_schema_exists"
        ]
        and preprocessor_checksum_verified
        and schema_checksum_verified
        and (
            len(persisted_schema)
            == EXPECTED_D7_TRANSFORMED_FEATURE_COUNT
        )
        and (
            len(loaded_feature_names)
            == EXPECTED_D7_TRANSFORMED_FEATURE_COUNT
        )
        and schema_matches_original
        and loaded_schema_matches_original
        and train_reproduction_exact
        and validation_reproduction_exact
        and (
            len(
                canonical_unknown_features
            )
            == 2
        )
        and not raw_race_unknown_feature_present
        and not raw_gender_unknown_feature_present
        and (
            checks[
                "fit_partition"
            ]
            == TRAIN_LABEL
        )
        and (
            checks[
                "validation_contributed_to_fit"
            ]
            is False
        )
        and (
            checks[
                "locked_test_accessed"
            ]
            is False
        )
    )

    checks["validation_status"] = (
        "PASS"
        if passed
        else "FAIL"
    )

    return checks


# ============================================================
# D7.28 — FIT, PERSIST, RELOAD & VERIFY
# ============================================================

def build_persisted_d7_primary_preprocessor(
) -> dict[str, Any]:
    """
    Execute the complete governed D7 preprocessing persistence
    workflow.

    1. Fit on TRAIN only.
    2. Transform TRAIN and VALIDATION.
    3. Persist fitted transformer.
    4. Persist transformed feature schema.
    5. Calculate SHA-256 checksums.
    6. Reload persisted transformer.
    7. Reproduce TRAIN and VALIDATION transformations.
    8. Validate exact reproducibility.

    LOCKED TEST remains untouched.
    """

    fitted_bundle = (
        fit_governed_primary_preprocessor()
    )

    persistence_result = (
        persist_fitted_primary_preprocessor(
            fitted_bundle
        )
    )

    persistence_validation = (
        validate_persisted_primary_preprocessor(
            fitted_bundle,
            persistence_result,
        )
    )

    if (
        persistence_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "Persisted D7 preprocessor failed "
            "reproducibility validation."
        )

    return {
        "fitted_bundle":
            fitted_bundle,

        "persistence_result":
            persistence_result,

        "persistence_validation":
            persistence_validation,
    }