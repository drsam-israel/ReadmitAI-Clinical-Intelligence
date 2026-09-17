# ============================================================
# D5 — GOVERNED PATIENT-LEVEL SPLITTING TESTS
# ============================================================

import pandas as pd
import pytest

from src.data.splitting import (
    GROUP_COLUMN,
    TARGET_COLUMN,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
    RANDOM_SEED,
    TRAIN_FRACTION,
    VALIDATION_FRACTION,
    TEST_FRACTION,
    SPLIT_GOVERNANCE_CONTRACT,
    validate_split_configuration,
    load_governed_cohort,
    build_patient_level_frame,
    assign_patients_to_splits,
    attach_split_assignments,
    audit_patient_overlap,
    build_split_summary,
    validate_complete_split,
    validate_split_reproducibility,
    build_governed_patient_split,
)


# ============================================================
# D5.T1 — SHARED GOVERNED SPLIT
# ============================================================

@pytest.fixture(scope="module")
def governed_split():
    return build_governed_patient_split()


# ============================================================
# D5.T2 — SPLIT GOVERNANCE CONTRACT
# ============================================================

def test_grouping_unit_is_patient():
    assert GROUP_COLUMN == "patient_nbr"


def test_target_is_governed_d3_outcome():
    assert TARGET_COLUMN == "readmitted_30d"


def test_split_fractions_sum_to_one():
    assert (
        TRAIN_FRACTION
        + VALIDATION_FRACTION
        + TEST_FRACTION
    ) == pytest.approx(1.0)


def test_random_seed_is_frozen():
    assert RANDOM_SEED == 42


def test_patient_overlap_is_prohibited():
    assert (
        SPLIT_GOVERNANCE_CONTRACT
        .patient_overlap_permitted
        is False
    )


def test_locked_test_is_declared_locked():
    assert (
        SPLIT_GOVERNANCE_CONTRACT
        .locked_test_status
        == "LOCKED"
    )


def test_split_configuration_passes():
    result = validate_split_configuration()

    assert (
        result["validation_status"]
        == "PASS"
    )


# ============================================================
# D5.T3 — GOVERNED SOURCE COHORT
# ============================================================

def test_governed_cohort_has_expected_encounter_count(
    governed_split,
):
    cohort = governed_split[0]

    assert len(cohort) == 100_114


def test_governed_cohort_has_expected_patient_count(
    governed_split,
):
    cohort = governed_split[0]

    assert (
        cohort[GROUP_COLUMN].nunique()
        == 70_439
    )


def test_governed_cohort_target_is_binary(
    governed_split,
):
    cohort = governed_split[0]

    assert set(
        cohort[TARGET_COLUMN]
        .astype(int)
        .unique()
    ) == {0, 1}


def test_governed_cohort_has_unique_encounters(
    governed_split,
):
    cohort = governed_split[0]

    assert not cohort[
        "encounter_id"
    ].duplicated().any()


# ============================================================
# D5.T4 — PATIENT-LEVEL FRAME
# ============================================================

def test_patient_frame_has_one_row_per_patient(
    governed_split,
):
    patient_frame = governed_split[1]

    assert len(patient_frame) == 70_439

    assert not patient_frame[
        GROUP_COLUMN
    ].duplicated().any()


def test_patient_positive_is_binary(
    governed_split,
):
    patient_frame = governed_split[1]

    assert set(
        patient_frame[
            "patient_positive"
        ].unique()
    ) == {0, 1}


def test_patient_frame_encounter_counts_reconcile(
    governed_split,
):
    patient_frame = governed_split[1]

    assert int(
        patient_frame[
            "encounter_count"
        ].sum()
    ) == 100_114


def test_patient_frame_positive_encounters_reconcile(
    governed_split,
):
    patient_frame = governed_split[1]

    assert int(
        patient_frame[
            "positive_encounter_count"
        ].sum()
    ) == 11_357


# ============================================================
# D5.T5 — PATIENT ASSIGNMENT
# ============================================================

def test_every_patient_has_exactly_one_assignment(
    governed_split,
):
    patient_assignment = governed_split[2]

    assert len(patient_assignment) == 70_439

    assert not patient_assignment[
        GROUP_COLUMN
    ].duplicated().any()


def test_only_required_split_labels_exist(
    governed_split,
):
    patient_assignment = governed_split[2]

    assert set(
        patient_assignment[
            "split"
        ].unique()
    ) == {
        TRAIN_LABEL,
        VALIDATION_LABEL,
        TEST_LABEL,
    }


def test_no_missing_patient_split_assignments(
    governed_split,
):
    patient_assignment = governed_split[2]

    assert patient_assignment[
        "split"
    ].notna().all()


# ============================================================
# D5.T6 — ENCOUNTER PRESERVATION
# ============================================================

def test_split_cohort_preserves_all_encounters(
    governed_split,
):
    cohort = governed_split[0]
    split_cohort = governed_split[3]

    assert len(split_cohort) == len(cohort)


def test_every_encounter_has_split_assignment(
    governed_split,
):
    split_cohort = governed_split[3]

    assert split_cohort[
        "split"
    ].notna().all()


def test_split_cohort_preserves_unique_encounter_ids(
    governed_split,
):
    split_cohort = governed_split[3]

    assert not split_cohort[
        "encounter_id"
    ].duplicated().any()


# ============================================================
# D5.T7 — PATIENT LEAKAGE PROTECTION
# ============================================================

def test_no_patient_appears_in_multiple_splits(
    governed_split,
):
    split_cohort = governed_split[3]

    counts = (
        split_cohort
        .groupby(GROUP_COLUMN)["split"]
        .nunique()
    )

    assert int(
        (counts > 1).sum()
    ) == 0


def test_train_validation_patient_overlap_is_zero(
    governed_split,
):
    split_cohort = governed_split[3]

    audit = audit_patient_overlap(
        split_cohort
    )

    assert (
        audit[
            "train_validation_overlap"
        ]
        == 0
    )


def test_train_test_patient_overlap_is_zero(
    governed_split,
):
    split_cohort = governed_split[3]

    audit = audit_patient_overlap(
        split_cohort
    )

    assert (
        audit[
            "train_test_overlap"
        ]
        == 0
    )


def test_validation_test_patient_overlap_is_zero(
    governed_split,
):
    split_cohort = governed_split[3]

    audit = audit_patient_overlap(
        split_cohort
    )

    assert (
        audit[
            "validation_test_overlap"
        ]
        == 0
    )


# ============================================================
# D5.T8 — SPLIT COUNTS
# ============================================================

def test_split_patient_counts_reconcile(
    governed_split,
):
    summary = governed_split[4]

    assert int(
        summary["patients"].sum()
    ) == 70_439


def test_split_encounter_counts_reconcile(
    governed_split,
):
    summary = governed_split[4]

    assert int(
        summary["encounters"].sum()
    ) == 100_114


def test_split_positive_counts_reconcile(
    governed_split,
):
    summary = governed_split[4]

    assert int(
        summary[
            "positive_encounters"
        ].sum()
    ) == 11_357


# ============================================================
# D5.T9 — OUTCOME BALANCE
# ============================================================

def test_each_split_contains_positive_outcomes(
    governed_split,
):
    summary = governed_split[4]

    assert (
        summary[
            "positive_encounters"
        ] > 0
    ).all()


def test_each_split_contains_negative_outcomes(
    governed_split,
):
    summary = governed_split[4]

    negatives = (
        summary["encounters"]
        - summary["positive_encounters"]
    )

    assert (
        negatives > 0
    ).all()


def test_split_readmission_rates_are_reasonably_balanced(
    governed_split,
):
    summary = governed_split[4]

    rates = summary[
        "readmission_rate"
    ]

    assert (
        rates.max()
        - rates.min()
    ) < 0.01


# ============================================================
# D5.T10 — COMPLETE SPLIT VALIDATION
# ============================================================

def test_complete_split_validation_passes(
    governed_split,
):
    validation = governed_split[5]

    assert (
        validation[
            "validation_status"
        ]
        == "PASS"
    )


def test_all_source_patients_are_assigned(
    governed_split,
):
    validation = governed_split[5]

    assert (
        validation[
            "all_source_patients_assigned"
        ]
        is True
    )


def test_all_source_encounters_are_preserved(
    governed_split,
):
    validation = governed_split[5]

    assert (
        validation[
            "all_source_encounters_preserved"
        ]
        is True
    )


# ============================================================
# D5.T11 — REPRODUCIBILITY
# ============================================================

def test_same_seed_reproduces_same_assignment(
    governed_split,
):
    patient_frame = governed_split[1]

    result = validate_split_reproducibility(
        patient_frame
    )

    assert (
        result[
            "same_seed_same_assignment"
        ]
        is True
    )

    assert (
        result[
            "validation_status"
        ]
        == "PASS"
    )


def test_direct_regeneration_is_identical(
    governed_split,
):
    patient_frame = governed_split[1]

    first = (
        assign_patients_to_splits(
            patient_frame,
            random_seed=RANDOM_SEED,
        )
        [[GROUP_COLUMN, "split"]]
        .sort_values(GROUP_COLUMN)
        .reset_index(drop=True)
    )

    second = (
        assign_patients_to_splits(
            patient_frame,
            random_seed=RANDOM_SEED,
        )
        [[GROUP_COLUMN, "split"]]
        .sort_values(GROUP_COLUMN)
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(
        first,
        second,
    )


# ============================================================
# D5.T12 — LOCKED-TEST EXISTENCE
# ============================================================

def test_locked_test_partition_exists(
    governed_split,
):
    split_cohort = governed_split[3]

    assert TEST_LABEL in set(
        split_cohort["split"]
    )


def test_locked_test_contains_patients(
    governed_split,
):
    split_cohort = governed_split[3]

    test_patients = (
        split_cohort.loc[
            split_cohort["split"]
            == TEST_LABEL,
            GROUP_COLUMN,
        ]
        .nunique()
    )

    assert test_patients > 0