# ============================================================
# D5 — GOVERNED PATIENT-LEVEL DATA SPLITTING
# ============================================================
"""
Create deterministic, patient-disjoint train, validation, and
locked-test partitions for the Diabetes Readmission Clinical AI
project.

Governance principles:
1. patient_nbr is the grouping unit.
2. A patient may belong to one and only one partition.
3. The split is deterministic and reproducible.
4. Outcome prevalence should remain reasonably balanced.
5. The locked test partition is created but must not be used for
   model-development decisions.
6. Split assignments must be persistable and independently
   auditable.
7. No model training occurs in D5.
"""

# ============================================================
# D5.1 — IMPORTS
# ============================================================

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.data.config import load_data_config


# ============================================================
# D5.2 — SPLIT GOVERNANCE CONSTANTS
# ============================================================

GROUP_COLUMN = "patient_nbr"
TARGET_COLUMN = "readmitted_30d"

TRAIN_LABEL = "train"
VALIDATION_LABEL = "validation"
TEST_LABEL = "test"

RANDOM_SEED = 42

TRAIN_FRACTION = 0.70
VALIDATION_FRACTION = 0.15
TEST_FRACTION = 0.15

SPLIT_LABELS = (
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
)

LOCKED_TEST_STATUS = "LOCKED"


# ============================================================
# D5.3 — SPLIT GOVERNANCE CONTRACT
# ============================================================

@dataclass(frozen=True)
class SplitGovernanceContract:
    """
    Formal D5 split-governance contract.
    """

    grouping_unit: str
    target: str
    train_fraction: float
    validation_fraction: float
    test_fraction: float
    random_seed: int
    patient_overlap_permitted: bool
    locked_test_status: str
    locked_test_permitted_use: str
    validation_permitted_use: str
    reproducibility_rule: str


SPLIT_GOVERNANCE_CONTRACT = SplitGovernanceContract(
    grouping_unit=GROUP_COLUMN,

    target=TARGET_COLUMN,

    train_fraction=TRAIN_FRACTION,

    validation_fraction=VALIDATION_FRACTION,

    test_fraction=TEST_FRACTION,

    random_seed=RANDOM_SEED,

    patient_overlap_permitted=False,

    locked_test_status=LOCKED_TEST_STATUS,

    locked_test_permitted_use=(
        "Final locked evaluation only after feature engineering, "
        "preprocessing, model selection, calibration, and threshold "
        "decisions have been frozen."
    ),

    validation_permitted_use=(
        "Model development, model comparison, calibration assessment, "
        "threshold selection, and other explicitly governed development "
        "decisions."
    ),

    reproducibility_rule=(
        "The same governed cohort, patient-level outcome representation, "
        "split fractions, algorithm, and random seed must reproduce the "
        "same patient assignment."
    ),
)


# ============================================================
# D5.4 — CONFIGURATION VALIDATION
# ============================================================

def validate_split_configuration() -> dict[str, Any]:
    """
    Validate the formal split configuration before any assignment
    is generated.
    """

    fractions = (
        TRAIN_FRACTION
        + VALIDATION_FRACTION
        + TEST_FRACTION
    )

    checks = {
        "fractions_sum_to_one":
            bool(
                np.isclose(
                    fractions,
                    1.0,
                )
            ),

        "all_fractions_positive":
            bool(
                TRAIN_FRACTION > 0
                and VALIDATION_FRACTION > 0
                and TEST_FRACTION > 0
            ),

        "patient_overlap_prohibited":
            (
                SPLIT_GOVERNANCE_CONTRACT
                .patient_overlap_permitted
                is False
            ),

        "locked_test_declared":
            (
                SPLIT_GOVERNANCE_CONTRACT
                .locked_test_status
                == "LOCKED"
            ),

        "random_seed_is_integer":
            isinstance(
                RANDOM_SEED,
                int,
            ),
    }

    status = (
        "PASS"
        if all(checks.values())
        else "FAIL"
    )

    return {
        **checks,
        "validation_status":
            status,
    }


# ============================================================
# D5.5 — GOVERNED COHORT PATH RESOLUTION
# ============================================================

def resolve_governed_cohort_path() -> Path:
    """
    Resolve the persisted D3 governed modeling cohort.

    The D3 cohort is the only authorized input to D5.
    """

    project_root = Path(
        __file__
    ).resolve().parents[2]

    cohort_path = (
        project_root
        / "data"
        / "interim"
        / "D3_governed_modeling_cohort.parquet"
    )

    return cohort_path


# ============================================================
# D5.6 — LOAD GOVERNED D3 COHORT
# ============================================================

def load_governed_cohort() -> pd.DataFrame:
    """
    Load and validate the persisted D3 governed modeling cohort.
    """

    cohort_path = (
        resolve_governed_cohort_path()
    )

    if not cohort_path.exists():
        raise FileNotFoundError(
            "Governed D3 modeling cohort not found: "
            f"{cohort_path}"
        )

    df = pd.read_parquet(
        cohort_path
    )

    required_columns = {
        GROUP_COLUMN,
        TARGET_COLUMN,
        "encounter_id",
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Governed cohort is missing required "
            f"D5 columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError(
            "Governed D3 cohort is empty."
        )

    if df[GROUP_COLUMN].isna().any():
        raise ValueError(
            "patient_nbr contains missing values."
        )

    if df[TARGET_COLUMN].isna().any():
        raise ValueError(
            "readmitted_30d contains missing values."
        )

    target_values = set(
        df[TARGET_COLUMN]
        .astype(int)
        .unique()
        .tolist()
    )

    if not target_values.issubset(
        {0, 1}
    ):
        raise ValueError(
            "readmitted_30d must be binary 0/1."
        )

    if df["encounter_id"].duplicated().any():
        raise ValueError(
            "Duplicate encounter_id values detected "
            "in governed D3 cohort."
        )

    return df


# ============================================================
# D5.7 — BUILD PATIENT-LEVEL SPLIT FRAME
# ============================================================

def build_patient_level_frame(
    cohort: pd.DataFrame,
) -> pd.DataFrame:
    """
    Collapse the encounter-level cohort to one row per patient.

    patient_positive = 1 when the patient has at least one
    eligible encounter with a 30-day readmission outcome.

    This patient-level outcome is used only to improve balance
    during split assignment. It is not a modeling feature.
    """

    patient_frame = (
        cohort
        .groupby(
            GROUP_COLUMN,
            as_index=False,
        )
        .agg(
            patient_positive=(
                TARGET_COLUMN,
                "max",
            ),
            encounter_count=(
                "encounter_id",
                "count",
            ),
            positive_encounter_count=(
                TARGET_COLUMN,
                "sum",
            ),
        )
    )

    patient_frame[
        "patient_positive"
    ] = (
        patient_frame[
            "patient_positive"
        ]
        .astype(int)
    )

    patient_frame[
        "encounter_count"
    ] = (
        patient_frame[
            "encounter_count"
        ]
        .astype(int)
    )

    patient_frame[
        "positive_encounter_count"
    ] = (
        patient_frame[
            "positive_encounter_count"
        ]
        .astype(int)
    )

    if (
        patient_frame[
            GROUP_COLUMN
        ].duplicated().any()
    ):
        raise RuntimeError(
            "Patient-level frame contains "
            "duplicate patient_nbr values."
        )

    return patient_frame


# ============================================================
# D5.8 — DETERMINISTIC STRATIFIED PATIENT ASSIGNMENT
# ============================================================

def assign_patients_to_splits(
    patient_frame: pd.DataFrame,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Deterministically assign patients to train, validation, and
    locked-test partitions.

    Stratification is performed at the patient level using
    patient_positive.

    Assignment is performed independently inside each patient
    outcome stratum and then recombined.
    """

    required_columns = {
        GROUP_COLUMN,
        "patient_positive",
    }

    missing_columns = (
        required_columns
        - set(patient_frame.columns)
    )

    if missing_columns:
        raise ValueError(
            "Patient frame is missing required "
            f"columns: {sorted(missing_columns)}"
        )

    if (
        patient_frame[
            GROUP_COLUMN
        ].duplicated().any()
    ):
        raise ValueError(
            "Patient frame must contain exactly "
            "one row per patient."
        )

    assignments = []

    for stratum_value in sorted(
        patient_frame[
            "patient_positive"
        ].unique()
    ):

        stratum = (
            patient_frame.loc[
                patient_frame[
                    "patient_positive"
                ]
                == stratum_value
            ]
            .copy()
            .sort_values(
                GROUP_COLUMN
            )
            .reset_index(drop=True)
        )

        # Separate deterministic RNG stream per stratum.
        rng = np.random.default_rng(
            random_seed
            + int(stratum_value)
        )

        permutation = (
            rng.permutation(
                len(stratum)
            )
        )

        stratum = (
            stratum
            .iloc[permutation]
            .reset_index(drop=True)
        )

        n_patients = len(
            stratum
        )

        n_train = int(
            np.floor(
                n_patients
                * TRAIN_FRACTION
            )
        )

        n_validation = int(
            np.floor(
                n_patients
                * VALIDATION_FRACTION
            )
        )

        n_test = (
            n_patients
            - n_train
            - n_validation
        )

        split_values = (
            [TRAIN_LABEL]
            * n_train
            + [VALIDATION_LABEL]
            * n_validation
            + [TEST_LABEL]
            * n_test
        )

        if len(split_values) != n_patients:
            raise RuntimeError(
                "Split assignment length mismatch."
            )

        stratum[
            "split"
        ] = split_values

        assignments.append(
            stratum
        )

    assignment = (
        pd.concat(
            assignments,
            ignore_index=True,
        )
        .sort_values(
            GROUP_COLUMN
        )
        .reset_index(drop=True)
    )

    return assignment


# ============================================================
# D5.9 — ATTACH SPLITS TO ENCOUNTER-LEVEL COHORT
# ============================================================

def attach_split_assignments(
    cohort: pd.DataFrame,
    patient_assignment: pd.DataFrame,
) -> pd.DataFrame:
    """
    Attach the patient-level split assignment to every eligible
    encounter in the D3 governed cohort.
    """

    assignment_columns = [
        GROUP_COLUMN,
        "split",
    ]

    if (
        patient_assignment[
            GROUP_COLUMN
        ].duplicated().any()
    ):
        raise ValueError(
            "Patient assignment contains duplicate "
            "patient_nbr values."
        )

    split_cohort = cohort.merge(
        patient_assignment[
            assignment_columns
        ],
        on=GROUP_COLUMN,
        how="left",
        validate="many_to_one",
    )

    if split_cohort[
        "split"
    ].isna().any():
        raise RuntimeError(
            "One or more encounters did not receive "
            "a split assignment."
        )

    if len(split_cohort) != len(cohort):
        raise RuntimeError(
            "Encounter count changed while attaching "
            "split assignments."
        )

    return split_cohort


# ============================================================
# D5.10 — PATIENT OVERLAP AUDIT
# ============================================================

def audit_patient_overlap(
    split_cohort: pd.DataFrame,
) -> dict[str, int]:
    """
    Confirm that no patient appears in more than one partition.
    """

    patient_split_counts = (
        split_cohort
        .groupby(
            GROUP_COLUMN
        )[
            "split"
        ]
        .nunique()
    )

    multi_split_patients = int(
        (
            patient_split_counts
            > 1
        ).sum()
    )

    train_patients = set(
        split_cohort.loc[
            split_cohort[
                "split"
            ] == TRAIN_LABEL,
            GROUP_COLUMN,
        ]
    )

    validation_patients = set(
        split_cohort.loc[
            split_cohort[
                "split"
            ] == VALIDATION_LABEL,
            GROUP_COLUMN,
        ]
    )

    test_patients = set(
        split_cohort.loc[
            split_cohort[
                "split"
            ] == TEST_LABEL,
            GROUP_COLUMN,
        ]
    )

    return {
        "multi_split_patients":
            multi_split_patients,

        "train_validation_overlap":
            len(
                train_patients
                & validation_patients
            ),

        "train_test_overlap":
            len(
                train_patients
                & test_patients
            ),

        "validation_test_overlap":
            len(
                validation_patients
                & test_patients
            ),
    }


# ============================================================
# D5.11 — SPLIT SUMMARY
# ============================================================

def build_split_summary(
    split_cohort: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarize encounter counts, patient counts, positive outcomes,
    and outcome prevalence for each split.
    """

    summary = (
        split_cohort
        .groupby(
            "split",
            as_index=False,
        )
        .agg(
            encounters=(
                "encounter_id",
                "count",
            ),
            patients=(
                GROUP_COLUMN,
                "nunique",
            ),
            positive_encounters=(
                TARGET_COLUMN,
                "sum",
            ),
        )
    )

    summary[
        "readmission_rate"
    ] = (
        summary[
            "positive_encounters"
        ]
        / summary[
            "encounters"
        ]
    )

    split_order = {
        TRAIN_LABEL: 0,
        VALIDATION_LABEL: 1,
        TEST_LABEL: 2,
    }

    summary[
        "_order"
    ] = (
        summary[
            "split"
        ]
        .map(
            split_order
        )
    )

    summary = (
        summary
        .sort_values(
            "_order"
        )
        .drop(
            columns="_order"
        )
        .reset_index(drop=True)
    )

    return summary


# ============================================================
# D5.12 — COMPLETE SPLIT VALIDATION
# ============================================================

def validate_complete_split(
    cohort: pd.DataFrame,
    patient_assignment: pd.DataFrame,
    split_cohort: pd.DataFrame,
) -> dict[str, Any]:
    """
    Perform the complete D5 split-integrity validation.
    """

    overlap = audit_patient_overlap(
        split_cohort
    )

    source_patients = int(
        cohort[
            GROUP_COLUMN
        ].nunique()
    )

    assigned_patients = int(
        patient_assignment[
            GROUP_COLUMN
        ].nunique()
    )

    source_encounters = int(
        len(cohort)
    )

    assigned_encounters = int(
        len(split_cohort)
    )

    split_labels_found = set(
        split_cohort[
            "split"
        ].unique()
    )

    checks = {
        "all_source_patients_assigned":
            (
                source_patients
                == assigned_patients
            ),

        "all_source_encounters_preserved":
            (
                source_encounters
                == assigned_encounters
            ),

        "all_required_splits_present":
            (
                split_labels_found
                == set(
                    SPLIT_LABELS
                )
            ),

        "no_multi_split_patients":
            (
                overlap[
                    "multi_split_patients"
                ]
                == 0
            ),

        "no_train_validation_overlap":
            (
                overlap[
                    "train_validation_overlap"
                ]
                == 0
            ),

        "no_train_test_overlap":
            (
                overlap[
                    "train_test_overlap"
                ]
                == 0
            ),

        "no_validation_test_overlap":
            (
                overlap[
                    "validation_test_overlap"
                ]
                == 0
            ),

        "no_missing_split_assignments":
            bool(
                split_cohort[
                    "split"
                ]
                .notna()
                .all()
            ),

        "patient_assignment_unique":
            bool(
                not patient_assignment[
                    GROUP_COLUMN
                ].duplicated().any()
            ),
    }

    status = (
        "PASS"
        if all(
            checks.values()
        )
        else "FAIL"
    )

    return {
        "source_encounters":
            source_encounters,

        "source_patients":
            source_patients,

        "assigned_encounters":
            assigned_encounters,

        "assigned_patients":
            assigned_patients,

        **overlap,

        **checks,

        "validation_status":
            status,
    }


# ============================================================
# D5.13 — REPRODUCIBILITY AUDIT
# ============================================================

def validate_split_reproducibility(
    patient_frame: pd.DataFrame,
) -> dict[str, Any]:
    """
    Independently regenerate the assignment twice and verify that
    the same patient receives the same partition.
    """

    assignment_a = (
        assign_patients_to_splits(
            patient_frame,
            random_seed=RANDOM_SEED,
        )
        [[GROUP_COLUMN, "split"]]
        .sort_values(
            GROUP_COLUMN
        )
        .reset_index(drop=True)
    )

    assignment_b = (
        assign_patients_to_splits(
            patient_frame,
            random_seed=RANDOM_SEED,
        )
        [[GROUP_COLUMN, "split"]]
        .sort_values(
            GROUP_COLUMN
        )
        .reset_index(drop=True)
    )

    reproducible = (
        assignment_a.equals(
            assignment_b
        )
    )

    return {
        "same_seed_same_assignment":
            bool(
                reproducible
            ),

        "validation_status":
            (
                "PASS"
                if reproducible
                else "FAIL"
            ),
    }


# ============================================================
# D5.14 — BUILD COMPLETE GOVERNED SPLIT
# ============================================================

def build_governed_patient_split():
    """
    Execute the complete in-memory D5 governed split workflow.

    Persistence and evidence generation are handled separately.
    """

    configuration_validation = (
        validate_split_configuration()
    )

    if (
        configuration_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D5 split configuration validation failed."
        )

    cohort = load_governed_cohort()

    patient_frame = (
        build_patient_level_frame(
            cohort
        )
    )

    patient_assignment = (
        assign_patients_to_splits(
            patient_frame
        )
    )

    split_cohort = (
        attach_split_assignments(
            cohort,
            patient_assignment,
        )
    )

    split_validation = (
        validate_complete_split(
            cohort,
            patient_assignment,
            split_cohort,
        )
    )

    reproducibility_validation = (
        validate_split_reproducibility(
            patient_frame
        )
    )

    if (
        split_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D5 patient-level split validation failed."
        )

    if (
        reproducibility_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D5 split reproducibility validation failed."
        )

    split_summary = (
        build_split_summary(
            split_cohort
        )
    )

    return (
        cohort,
        patient_frame,
        patient_assignment,
        split_cohort,
        split_summary,
        split_validation,
        reproducibility_validation,
    )


# ============================================================
# D5.15 — COMMAND-LINE VALIDATION
# ============================================================

if __name__ == "__main__":

    (
        cohort,
        patient_frame,
        patient_assignment,
        split_cohort,
        split_summary,
        split_validation,
        reproducibility_validation,
    ) = build_governed_patient_split()

    print(
        "=" * 72
    )
    print(
        "D5 — GOVERNED PATIENT-LEVEL SPLITTING"
    )
    print(
        "=" * 72
    )

    print()
    print(
        "SPLIT GOVERNANCE CONTRACT"
    )
    print(
        "-" * 72
    )

    print(
        f"grouping_unit: "
        f"{SPLIT_GOVERNANCE_CONTRACT.grouping_unit}"
    )

    print(
        f"target: "
        f"{SPLIT_GOVERNANCE_CONTRACT.target}"
    )

    print(
        f"train_fraction: "
        f"{TRAIN_FRACTION:.2f}"
    )

    print(
        f"validation_fraction: "
        f"{VALIDATION_FRACTION:.2f}"
    )

    print(
        f"test_fraction: "
        f"{TEST_FRACTION:.2f}"
    )

    print(
        f"random_seed: "
        f"{RANDOM_SEED}"
    )

    print(
        f"locked_test_status: "
        f"{LOCKED_TEST_STATUS}"
    )

    print()
    print(
        "SOURCE COHORT"
    )
    print(
        "-" * 72
    )

    print(
        f"encounters: "
        f"{len(cohort):,}"
    )

    print(
        f"patients: "
        f"{cohort[GROUP_COLUMN].nunique():,}"
    )

    print(
        f"positive_encounters: "
        f"{int(cohort[TARGET_COLUMN].sum()):,}"
    )

    print(
        f"readmission_rate: "
        f"{cohort[TARGET_COLUMN].mean():.4%}"
    )

    print()
    print(
        "PATIENT-LEVEL STRATIFICATION FRAME"
    )
    print(
        "-" * 72
    )

    print(
        f"patients: "
        f"{len(patient_frame):,}"
    )

    print(
        f"patients_with_at_least_one_positive_encounter: "
        f"{int(patient_frame['patient_positive'].sum()):,}"
    )

    print()
    print(
        "SPLIT SUMMARY"
    )
    print(
        "-" * 72
    )

    print(
        split_summary.to_string(
            index=False
        )
    )

    print()
    print(
        "PATIENT OVERLAP AUDIT"
    )
    print(
        "-" * 72
    )

    print(
        f"multi_split_patients: "
        f"{split_validation['multi_split_patients']}"
    )

    print(
        f"train_validation_overlap: "
        f"{split_validation['train_validation_overlap']}"
    )

    print(
        f"train_test_overlap: "
        f"{split_validation['train_test_overlap']}"
    )

    print(
        f"validation_test_overlap: "
        f"{split_validation['validation_test_overlap']}"
    )

    print()
    print(
        "VALIDATION"
    )
    print(
        "-" * 72
    )

    print(
        f"split_validation_status: "
        f"{split_validation['validation_status']}"
    )

    print(
        f"reproducibility_validation_status: "
        f"{reproducibility_validation['validation_status']}"
    )

    print(
        f"same_seed_same_assignment: "
        f"{reproducibility_validation['same_seed_same_assignment']}"
    )

    print()
    print(
        "=" * 72
    )
    print(
        "D5 governed patient-level splitting: PASS"
    )
    print(
        "Locked test partition: CREATED BUT PROTECTED"
    )
    print(
        "No model training has occurred."
    )
    print(
        "=" * 72
    )