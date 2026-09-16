# ============================================================
# D3 — GOVERNED COHORT & OUTCOME ENGINEERING TESTS
# ============================================================

import pandas as pd
import pytest

from src.data.validation import load_raw_dataset
from src.data.cohort import (
    SOURCE_TARGET_COLUMN,
    DERIVED_TARGET_COLUMN,
    POSITIVE_TARGET_VALUE,
    PATIENT_ID_COLUMN,
    ENCOUNTER_ID_COLUMN,
    DISCHARGE_COLUMN,
    EXPIRED_DISPOSITION_IDS,
    HOSPICE_DISPOSITION_IDS,
    assess_cohort_eligibility,
    construct_governed_cohort,
    engineer_readmission_outcome,
    build_governed_modeling_cohort,
)


# ============================================================
# D3.1 — SHARED TEST FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def raw_df():
    return load_raw_dataset()


@pytest.fixture(scope="module")
def governed_df(raw_df):
    cohort, _ = build_governed_modeling_cohort(raw_df)
    return cohort


# ============================================================
# D3.2 — COHORT ELIGIBILITY RULE TESTS
# ============================================================

def test_governed_expired_disposition_ids():
    assert EXPIRED_DISPOSITION_IDS == frozenset(
        {11, 19, 20, 21}
    )


def test_hospice_dispositions_are_not_expired():
    assert EXPIRED_DISPOSITION_IDS.isdisjoint(
        HOSPICE_DISPOSITION_IDS
    )


def test_eligibility_assessment_counts(raw_df):
    assessment = assess_cohort_eligibility(raw_df)

    assert assessment["source_encounters"] == 101_766
    assert assessment["excluded_encounters"] == 1_652
    assert assessment["retained_encounters"] == 100_114
    assert assessment["excluded_positive_30d"] == 0
    assert assessment["hospice_encounters_retained"] == 771


# ============================================================
# D3.3 — GOVERNED COHORT CONSTRUCTION TESTS
# ============================================================

def test_governed_cohort_row_count(governed_df):
    assert len(governed_df) == 100_114


def test_expired_dispositions_removed(governed_df):
    assert not governed_df[
        DISCHARGE_COLUMN
    ].isin(EXPIRED_DISPOSITION_IDS).any()


def test_hospice_encounters_retained(governed_df):
    hospice_count = int(
        governed_df[
            DISCHARGE_COLUMN
        ].isin(HOSPICE_DISPOSITION_IDS).sum()
    )

    assert hospice_count == 771


def test_encounter_ids_remain_unique(governed_df):
    assert governed_df[
        ENCOUNTER_ID_COLUMN
    ].duplicated().sum() == 0


def test_patient_ids_remain_complete(governed_df):
    assert governed_df[
        PATIENT_ID_COLUMN
    ].isna().sum() == 0


def test_governed_unique_patient_count(governed_df):
    assert governed_df[
        PATIENT_ID_COLUMN
    ].nunique() == 70_439


# ============================================================
# D3.4 — RAW DATA IMMUTABILITY TEST
# ============================================================

def test_cohort_construction_does_not_mutate_raw(raw_df):
    original = raw_df.copy(deep=True)

    _ = construct_governed_cohort(raw_df)

    pd.testing.assert_frame_equal(
        raw_df,
        original,
    )


# ============================================================
# D3.5 — FORMAL OUTCOME ENGINEERING TESTS
# ============================================================

def test_formal_target_exists(governed_df):
    assert DERIVED_TARGET_COLUMN in governed_df.columns


def test_formal_target_is_binary(governed_df):
    assert set(
        governed_df[
            DERIVED_TARGET_COLUMN
        ].unique()
    ) == {0, 1}


def test_formal_target_has_no_missing_values(governed_df):
    assert governed_df[
        DERIVED_TARGET_COLUMN
    ].isna().sum() == 0


def test_formal_target_positive_count(governed_df):
    assert int(
        governed_df[
            DERIVED_TARGET_COLUMN
        ].sum()
    ) == 11_357


def test_formal_target_distribution(governed_df):
    distribution = (
        governed_df[
            DERIVED_TARGET_COLUMN
        ]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    assert distribution == {
        0: 88_757,
        1: 11_357,
    }


def test_positive_target_mapping_is_exact(governed_df):
    expected = (
        governed_df[
            SOURCE_TARGET_COLUMN
        ]
        .eq(POSITIVE_TARGET_VALUE)
        .astype("int8")
    )

    pd.testing.assert_series_equal(
        governed_df[
            DERIVED_TARGET_COLUMN
        ],
        expected,
        check_names=False,
    )


def test_negative_target_mapping_is_exact(governed_df):
    negatives = governed_df.loc[
        governed_df[
            SOURCE_TARGET_COLUMN
        ].isin({"NO", ">30"})
    ]

    assert (
        negatives[
            DERIVED_TARGET_COLUMN
        ]
        == 0
    ).all()


# ============================================================
# D3.6 — SOURCE TARGET PRESERVATION TEST
# ============================================================

def test_source_target_is_preserved(raw_df, governed_df):
    expected_source_target = (
        raw_df.loc[
            ~raw_df[
                DISCHARGE_COLUMN
            ].isin(EXPIRED_DISPOSITION_IDS),
            SOURCE_TARGET_COLUMN,
        ]
        .reset_index(drop=True)
    )

    pd.testing.assert_series_equal(
        governed_df[
            SOURCE_TARGET_COLUMN
        ],
        expected_source_target,
        check_names=False,
    )


# ============================================================
# D3.7 — OUTCOME ENGINEERING SAFETY TESTS
# ============================================================

def test_outcome_engineering_does_not_mutate_input(raw_df):
    eligible = construct_governed_cohort(raw_df)

    original = eligible.copy(deep=True)

    _ = engineer_readmission_outcome(
        eligible
    )

    pd.testing.assert_frame_equal(
        eligible,
        original,
    )


def test_outcome_engineering_refuses_overwrite(raw_df):
    eligible = construct_governed_cohort(raw_df)

    engineered = engineer_readmission_outcome(
        eligible
    )

    with pytest.raises(
        ValueError,
        match="Derived target already exists",
    ):
        engineer_readmission_outcome(
            engineered
        )


# ============================================================
# D3.8 — END-TO-END PIPELINE TEST
# ============================================================

def test_d3_end_to_end_pipeline_passes(raw_df):
    cohort, validation = (
        build_governed_modeling_cohort(
            raw_df
        )
    )

    assert validation[
        "validation_status"
    ] == "PASS"

    assert len(cohort) == 100_114

    assert validation[
        "positive_30d_count"
    ] == 11_357

    assert all(
        validation[
            "validation_checks"
        ].values()
    )