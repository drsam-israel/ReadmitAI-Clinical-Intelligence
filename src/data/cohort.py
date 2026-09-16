# ============================================================
# D3 — GOVERNED COHORT & OUTCOME ENGINEERING
# ============================================================
"""
Governed cohort construction and outcome engineering.

Lifecycle stage:
    D3 — Cohort & Outcome Engineering

Purpose:
    Define the eligible modeling population and formal
    30-day readmission outcome using explicit, auditable,
    reproducible rules.

Governance principles:
    1. Raw source data remain immutable.
    2. Exclusions must be explicitly defined and quantified.
    3. Exclusions occur before model splitting.
    4. Outcome engineering must be deterministic.
    5. The raw source target is preserved.
    6. Patient identifiers are retained for later patient-level
       splitting but are never modeling features.
"""

# ============================================================
# D3.1 — IMPORTS AND GOVERNED CONSTANTS
# ============================================================

from pathlib import Path
from typing import Any
import csv
import hashlib

import pandas as pd

from src.data.config import get_supporting_dataset_path
from src.data.validation import load_raw_dataset


SOURCE_TARGET_COLUMN = "readmitted"
DERIVED_TARGET_COLUMN = "readmitted_30d"

POSITIVE_TARGET_VALUE = "<30"

EXPECTED_SOURCE_TARGET_VALUES = {
    "NO",
    ">30",
    "<30",
}

PATIENT_ID_COLUMN = "patient_nbr"
ENCOUNTER_ID_COLUMN = "encounter_id"
DISCHARGE_COLUMN = "discharge_disposition_id"

EXPECTED_MAPPING_SHA256 = (
    "F1BB82B471CB34649352597572C9B1FB00BD27F77B9F5A22A03DC3EB1039749E"
)

EXPIRED_DISPOSITION_IDS = frozenset(
    {
        11,  # Expired
        19,  # Expired at home
        20,  # Expired in medical facility
        21,  # Expired, place unknown
    }
)

HOSPICE_DISPOSITION_IDS = frozenset(
    {
        13,  # Hospice / home
        14,  # Hospice / medical facility
    }
)


# ============================================================
# D3.2 — RAW COHORT PROFILE
# ============================================================

def assess_raw_cohort(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Profile the source population before cohort exclusion
    or formal outcome engineering.
    """

    required_columns = {
        ENCOUNTER_ID_COLUMN,
        PATIENT_ID_COLUMN,
        DISCHARGE_COLUMN,
        SOURCE_TARGET_COLUMN,
    }

    missing_columns = sorted(
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Required cohort columns are missing: "
            f"{missing_columns}"
        )

    target_counts = (
        df[SOURCE_TARGET_COLUMN]
        .value_counts(dropna=False)
        .to_dict()
    )

    discharge_counts = (
        df[DISCHARGE_COLUMN]
        .value_counts(dropna=False)
        .sort_index()
        .to_dict()
    )

    return {
        "total_source_encounters":
            int(len(df)),
        "unique_source_patients":
            int(
                df[PATIENT_ID_COLUMN].nunique()
            ),
        "duplicate_encounter_ids":
            int(
                df[
                    ENCOUNTER_ID_COLUMN
                ].duplicated().sum()
            ),
        "missing_patient_ids":
            int(
                df[
                    PATIENT_ID_COLUMN
                ].isna().sum()
            ),
        "missing_discharge_disposition":
            int(
                df[
                    DISCHARGE_COLUMN
                ].isna().sum()
            ),
        "source_target_distribution": {
            str(key): int(value)
            for key, value
            in target_counts.items()
        },
        "discharge_disposition_distribution": {
            str(key): int(value)
            for key, value
            in discharge_counts.items()
        },
    }


# ============================================================
# D3.3 — DISCHARGE DISPOSITION PROFILE
# ============================================================

def assess_discharge_dispositions(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Quantify discharge disposition categories before
    exclusion.

    The temporary audit outcome is diagnostic only and is not
    the formal modeling target.
    """

    required_columns = {
        ENCOUNTER_ID_COLUMN,
        PATIENT_ID_COLUMN,
        DISCHARGE_COLUMN,
        SOURCE_TARGET_COLUMN,
    }

    missing_columns = sorted(
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Required discharge assessment columns "
            f"are missing: {missing_columns}"
        )

    summary = (
        df.groupby(
            DISCHARGE_COLUMN,
            dropna=False,
        )
        .agg(
            encounters=(
                ENCOUNTER_ID_COLUMN,
                "count",
            ),
            unique_patients=(
                PATIENT_ID_COLUMN,
                "nunique",
            ),
        )
        .reset_index()
    )

    summary["encounter_pct"] = (
        summary["encounters"]
        / len(df)
        * 100
    ).round(4)

    audit_df = df[
        [
            DISCHARGE_COLUMN,
            SOURCE_TARGET_COLUMN,
        ]
    ].copy()

    audit_df["_audit_readmitted_30d"] = (
        audit_df[
            SOURCE_TARGET_COLUMN
        ]
        == POSITIVE_TARGET_VALUE
    ).astype(int)

    positive_counts = (
        audit_df.groupby(
            DISCHARGE_COLUMN,
            dropna=False,
        )["_audit_readmitted_30d"]
        .agg(
            positive_30d_count="sum",
            raw_30d_rate="mean",
        )
        .reset_index()
    )

    positive_counts["raw_30d_rate"] = (
        positive_counts["raw_30d_rate"]
        * 100
    ).round(4)

    summary = summary.merge(
        positive_counts,
        on=DISCHARGE_COLUMN,
        how="left",
        validate="one_to_one",
    )

    return (
        summary.sort_values(
            "encounters",
            ascending=False,
        )
        .reset_index(drop=True)
    )


# ============================================================
# D3.4 — SUPPORTING MAPPING INTEGRITY VALIDATION
# ============================================================

def calculate_file_sha256(
    file_path: Path,
) -> str:
    """
    Calculate SHA-256 checksum.
    """

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:

        for block in iter(
            lambda: file.read(
                1024 * 1024
            ),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


def validate_supporting_mapping(
) -> dict[str, Any]:
    """
    Validate the presence and integrity of the governed
    UCI identifier mapping file.
    """

    mapping_path = (
        get_supporting_dataset_path()
    )

    if not mapping_path.exists():
        raise FileNotFoundError(
            "Supporting mapping file "
            f"not found: {mapping_path}"
        )

    observed_hash = (
        calculate_file_sha256(
            mapping_path
        )
    )

    hash_match = (
        observed_hash
        == EXPECTED_MAPPING_SHA256
    )

    if not hash_match:
        raise ValueError(
            "Supporting mapping SHA-256 "
            "does not match the governed checksum."
        )

    return {
        "file_exists": True,
        "path": str(mapping_path),
        "sha256": observed_hash,
        "sha256_match": hash_match,
        "file_size_bytes": int(
            mapping_path.stat().st_size
        ),
        "validation_status": "PASS",
    }


# ============================================================
# D3.5 — DISCHARGE DISPOSITION SEMANTIC EXTRACTION
# ============================================================

def extract_discharge_disposition_mapping(
) -> pd.DataFrame:
    """
    Extract discharge-disposition semantics from the
    UCI companion mapping file.
    """

    mapping_path = (
        get_supporting_dataset_path()
    )

    rows: list[dict[str, Any]] = []

    inside_discharge_section = False

    with mapping_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            if not row:
                continue

            first_cell = row[0].strip()

            if (
                first_cell
                == "discharge_disposition_id"
            ):
                inside_discharge_section = True
                continue

            if (
                inside_discharge_section
                and first_cell
                in {
                    "admission_type_id",
                    "admission_source_id",
                }
            ):
                break

            if not inside_discharge_section:
                continue

            if len(row) < 2:
                continue

            raw_id = row[0].strip()
            description = row[1].strip()

            if not raw_id.isdigit():
                continue

            rows.append(
                {
                    "discharge_disposition_id":
                        int(raw_id),
                    "description":
                        description,
                }
            )

    mapping_df = pd.DataFrame(rows)

    if mapping_df.empty:
        raise ValueError(
            "No discharge disposition mappings "
            "were extracted."
        )

    if mapping_df[
        "discharge_disposition_id"
    ].duplicated().any():
        raise ValueError(
            "Duplicate discharge disposition IDs "
            "found in supporting mapping."
        )

    if (
        mapping_df["description"]
        .isna()
        .any()
    ):
        raise ValueError(
            "Missing disposition descriptions "
            "found in mapping."
        )

    return (
        mapping_df.sort_values(
            "discharge_disposition_id"
        )
        .reset_index(drop=True)
    )


# ============================================================
# D3.6 — DISPOSITION SEMANTIC EVIDENCE
# ============================================================

def build_disposition_semantic_evidence(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine observed disposition frequencies with
    source-derived semantics.
    """

    observed = (
        assess_discharge_dispositions(df)
    )

    semantics = (
        extract_discharge_disposition_mapping()
    )

    evidence = observed.merge(
        semantics,
        on="discharge_disposition_id",
        how="left",
        validate="many_to_one",
    )

    evidence[
        "mapping_description_available"
    ] = evidence["description"].notna()

    return evidence[
        [
            "discharge_disposition_id",
            "description",
            "mapping_description_available",
            "encounters",
            "unique_patients",
            "encounter_pct",
            "positive_30d_count",
            "raw_30d_rate",
        ]
    ]


# ============================================================
# D3.7 — PRE-EXCLUSION EVIDENCE VALIDATION
# ============================================================

def validate_pre_exclusion_evidence(
    df: pd.DataFrame,
    semantic_evidence: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate semantic evidence before implementing the
    governed exclusion rule.
    """

    observed_disposition_ids = set(
        df[DISCHARGE_COLUMN]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    mapped_disposition_ids = set(
        semantic_evidence.loc[
            semantic_evidence[
                "mapping_description_available"
            ],
            "discharge_disposition_id",
        ]
        .astype(int)
        .tolist()
    )

    unmapped_observed_ids = sorted(
        observed_disposition_ids
        - mapped_disposition_ids
    )

    status = (
        "PASS"
        if not unmapped_observed_ids
        else "REVIEW"
    )

    return {
        "observed_disposition_count":
            len(observed_disposition_ids),
        "mapped_observed_disposition_count":
            len(
                observed_disposition_ids
                & mapped_disposition_ids
            ),
        "unmapped_observed_disposition_ids":
            unmapped_observed_ids,
        "all_observed_dispositions_mapped":
            not unmapped_observed_ids,
        "cohort_exclusion_applied":
            False,
        "formal_target_engineered":
            False,
        "pre_exclusion_evidence_status":
            status,
    }


# ============================================================
# D3.8 — GOVERNED COHORT ELIGIBILITY DECISION
# ============================================================

def assess_cohort_eligibility(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Quantify the governed cohort eligibility rule.

    Primary rule:
        Exclude death / expired discharge dispositions.

    Hospice dispositions remain eligible for the primary
    cohort and will be evaluated later in sensitivity
    analysis.
    """

    expired_mask = (
        df[DISCHARGE_COLUMN]
        .isin(EXPIRED_DISPOSITION_IDS)
    )

    hospice_mask = (
        df[DISCHARGE_COLUMN]
        .isin(HOSPICE_DISPOSITION_IDS)
    )

    excluded_encounters = int(
        expired_mask.sum()
    )

    excluded_positive_30d = int(
        (
            expired_mask
            & (
                df[SOURCE_TARGET_COLUMN]
                == POSITIVE_TARGET_VALUE
            )
        ).sum()
    )

    return {
        "source_encounters":
            int(len(df)),
        "exclusion_basis":
            "Death / expired discharge disposition",
        "expired_disposition_ids":
            sorted(EXPIRED_DISPOSITION_IDS),
        "hospice_disposition_ids_retained":
            sorted(HOSPICE_DISPOSITION_IDS),
        "excluded_encounters":
            excluded_encounters,
        "excluded_encounter_pct":
            round(
                excluded_encounters
                / len(df)
                * 100,
                4,
            ),
        "excluded_positive_30d":
            excluded_positive_30d,
        "hospice_encounters_retained":
            int(
                hospice_mask.sum()
            ),
        "retained_encounters":
            int(
                (~expired_mask).sum()
            ),
        "cohort_rule_status":
            "DEFINED",
    }


# ============================================================
# D3.9 — GOVERNED COHORT CONSTRUCTION
# ============================================================

def construct_governed_cohort(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply the approved cohort eligibility rule.

    Excluded:
        Encounters with death / expired discharge disposition.

    Retained:
        All other eligible encounters, including hospice
        encounters.

    The supplied dataframe is never modified in place.
    """

    required_columns = {
        ENCOUNTER_ID_COLUMN,
        PATIENT_ID_COLUMN,
        DISCHARGE_COLUMN,
        SOURCE_TARGET_COLUMN,
    }

    missing_columns = sorted(
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Required cohort construction columns "
            f"are missing: {missing_columns}"
        )

    governed_df = df.loc[
        ~df[DISCHARGE_COLUMN].isin(
            EXPIRED_DISPOSITION_IDS
        )
    ].copy()

    governed_df = (
        governed_df.reset_index(
            drop=True
        )
    )

    return governed_df


# ============================================================
# D3.10 — FORMAL 30-DAY OUTCOME ENGINEERING
# ============================================================

def engineer_readmission_outcome(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Engineer the formal binary 30-day readmission outcome.

    Mapping:
        <30  -> 1
        >30  -> 0
        NO   -> 0

    The original source target is preserved.
    """

    if SOURCE_TARGET_COLUMN not in df.columns:
        raise ValueError(
            "Source target column is missing: "
            f"{SOURCE_TARGET_COLUMN}"
        )

    if DERIVED_TARGET_COLUMN in df.columns:
        raise ValueError(
            "Derived target already exists. "
            "Outcome engineering will not overwrite it."
        )

    if (
        df[SOURCE_TARGET_COLUMN]
        .isna()
        .any()
    ):
        raise ValueError(
            "Source target contains missing values."
        )

    observed_values = set(
        df[SOURCE_TARGET_COLUMN]
        .unique()
        .tolist()
    )

    unexpected_values = sorted(
        observed_values
        - EXPECTED_SOURCE_TARGET_VALUES
    )

    if unexpected_values:
        raise ValueError(
            "Unexpected source target values: "
            f"{unexpected_values}"
        )

    outcome_df = df.copy()

    outcome_df[DERIVED_TARGET_COLUMN] = (
        outcome_df[
            SOURCE_TARGET_COLUMN
        ]
        .eq(POSITIVE_TARGET_VALUE)
        .astype("int8")
    )

    return outcome_df


# ============================================================
# D3.11 — POST-CONSTRUCTION COHORT VALIDATION
# ============================================================

def validate_governed_cohort(
    raw_df: pd.DataFrame,
    governed_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate structural and outcome invariants after cohort
    construction and target engineering.
    """

    required_columns = {
        ENCOUNTER_ID_COLUMN,
        PATIENT_ID_COLUMN,
        DISCHARGE_COLUMN,
        SOURCE_TARGET_COLUMN,
        DERIVED_TARGET_COLUMN,
    }

    missing_columns = sorted(
        required_columns
        - set(governed_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Governed cohort is missing required columns: "
            f"{missing_columns}"
        )

    source_encounters = int(
        len(raw_df)
    )

    governed_encounters = int(
        len(governed_df)
    )

    excluded_encounters = (
        source_encounters
        - governed_encounters
    )

    expired_remaining = int(
        governed_df[
            DISCHARGE_COLUMN
        ]
        .isin(
            EXPIRED_DISPOSITION_IDS
        )
        .sum()
    )

    duplicate_encounter_ids = int(
        governed_df[
            ENCOUNTER_ID_COLUMN
        ]
        .duplicated()
        .sum()
    )

    missing_patient_ids = int(
        governed_df[
            PATIENT_ID_COLUMN
        ]
        .isna()
        .sum()
    )

    target_missing = int(
        governed_df[
            DERIVED_TARGET_COLUMN
        ]
        .isna()
        .sum()
    )

    target_values = sorted(
        governed_df[
            DERIVED_TARGET_COLUMN
        ]
        .unique()
        .tolist()
    )

    positive_count = int(
        governed_df[
            DERIVED_TARGET_COLUMN
        ].sum()
    )

    source_positive_count = int(
        (
            raw_df[
                SOURCE_TARGET_COLUMN
            ]
            == POSITIVE_TARGET_VALUE
        ).sum()
    )

    source_target_preserved = bool(
        governed_df[
            SOURCE_TARGET_COLUMN
        ].equals(
            raw_df.loc[
                ~raw_df[
                    DISCHARGE_COLUMN
                ].isin(
                    EXPIRED_DISPOSITION_IDS
                ),
                SOURCE_TARGET_COLUMN,
            ].reset_index(
                drop=True
            )
        )
    )

    target_mapping_consistent = bool(
        (
            governed_df[
                DERIVED_TARGET_COLUMN
            ]
            == (
                governed_df[
                    SOURCE_TARGET_COLUMN
                ]
                == POSITIVE_TARGET_VALUE
            ).astype("int8")
        ).all()
    )

    expected_excluded = int(
        raw_df[
            DISCHARGE_COLUMN
        ]
        .isin(
            EXPIRED_DISPOSITION_IDS
        )
        .sum()
    )

    expected_governed_encounters = (
        source_encounters
        - expected_excluded
    )

    validation_checks = {
        "expected_encounter_count_match":
            governed_encounters
            == expected_governed_encounters,
        "excluded_count_match":
            excluded_encounters
            == expected_excluded,
        "no_expired_dispositions_remaining":
            expired_remaining == 0,
        "encounter_ids_unique":
            duplicate_encounter_ids == 0,
        "patient_ids_complete":
            missing_patient_ids == 0,
        "target_complete":
            target_missing == 0,
        "target_binary":
            set(target_values)
            == {0, 1},
        "source_target_preserved":
            source_target_preserved,
        "target_mapping_consistent":
            target_mapping_consistent,
        "positive_outcomes_preserved":
            positive_count
            == source_positive_count,
    }

    validation_status = (
        "PASS"
        if all(
            validation_checks.values()
        )
        else "FAIL"
    )

    return {
        "source_encounters":
            source_encounters,
        "expected_excluded_encounters":
            expected_excluded,
        "actual_excluded_encounters":
            excluded_encounters,
        "governed_encounters":
            governed_encounters,
        "unique_governed_patients":
            int(
                governed_df[
                    PATIENT_ID_COLUMN
                ].nunique()
            ),
        "expired_dispositions_remaining":
            expired_remaining,
        "duplicate_encounter_ids":
            duplicate_encounter_ids,
        "missing_patient_ids":
            missing_patient_ids,
        "target_missing":
            target_missing,
        "target_values":
            target_values,
        "positive_30d_count":
            positive_count,
        "positive_30d_rate_pct":
            round(
                positive_count
                / governed_encounters
                * 100,
                4,
            ),
        "source_positive_30d_count":
            source_positive_count,
        "validation_checks":
            validation_checks,
        "validation_status":
            validation_status,
    }


# ============================================================
# D3.12 — END-TO-END COHORT & OUTCOME PIPELINE
# ============================================================

def build_governed_modeling_cohort(
    raw_df: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    dict[str, Any],
]:
    """
    Execute the complete governed D3 cohort transformation.

    Sequence:
        1. Validate source cohort.
        2. Validate supporting mapping.
        3. Validate disposition semantics.
        4. Construct eligible cohort.
        5. Engineer formal binary outcome.
        6. Validate all post-construction invariants.

    Returns:
        Governed dataframe and validation evidence.
    """

    assess_raw_cohort(
        raw_df
    )

    validate_supporting_mapping()

    semantic_evidence = (
        build_disposition_semantic_evidence(
            raw_df
        )
    )

    pre_exclusion_validation = (
        validate_pre_exclusion_evidence(
            raw_df,
            semantic_evidence,
        )
    )

    if (
        pre_exclusion_validation[
            "pre_exclusion_evidence_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "Pre-exclusion evidence gate "
            "did not pass."
        )

    governed_df = (
        construct_governed_cohort(
            raw_df
        )
    )

    governed_df = (
        engineer_readmission_outcome(
            governed_df
        )
    )

    validation = (
        validate_governed_cohort(
            raw_df,
            governed_df,
        )
    )

    if (
        validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "Governed cohort validation failed."
        )

    return governed_df, validation


# ============================================================
# D3.13 — COMMAND-LINE VALIDATION
# ============================================================

if __name__ == "__main__":

    raw_df = load_raw_dataset()

    raw_profile = (
        assess_raw_cohort(
            raw_df
        )
    )

    mapping_validation = (
        validate_supporting_mapping()
    )

    disposition_evidence = (
        build_disposition_semantic_evidence(
            raw_df
        )
    )

    pre_exclusion_validation = (
        validate_pre_exclusion_evidence(
            raw_df,
            disposition_evidence,
        )
    )

    eligibility = (
        assess_cohort_eligibility(
            raw_df
        )
    )

    governed_df, governed_validation = (
        build_governed_modeling_cohort(
            raw_df
        )
    )

    print("=" * 70)
    print(
        "D3 — GOVERNED COHORT & "
        "OUTCOME ENGINEERING"
    )
    print("=" * 70)

    print()
    print(
        "D3.2 — RAW COHORT PROFILE"
    )
    print("-" * 70)

    print(
        "source_encounters:",
        raw_profile[
            "total_source_encounters"
        ],
    )

    print(
        "source_patients:",
        raw_profile[
            "unique_source_patients"
        ],
    )

    print(
        "source_target_distribution:",
        raw_profile[
            "source_target_distribution"
        ],
    )

    print()
    print(
        "D3.4 — SUPPORTING MAPPING "
        "INTEGRITY"
    )
    print("-" * 70)

    print(
        "validation_status:",
        mapping_validation[
            "validation_status"
        ],
    )

    print(
        "sha256_match:",
        mapping_validation[
            "sha256_match"
        ],
    )

    print()
    print(
        "D3.7 — PRE-EXCLUSION "
        "EVIDENCE GATE"
    )
    print("-" * 70)

    for key, value in (
        pre_exclusion_validation.items()
    ):
        print(
            f"{key}: {value}"
        )

    print()
    print(
        "D3.8 — COHORT "
        "ELIGIBILITY DECISION"
    )
    print("-" * 70)

    for key, value in (
        eligibility.items()
    ):
        print(
            f"{key}: {value}"
        )

    print()
    print(
        "D3.11 — GOVERNED COHORT "
        "VALIDATION"
    )
    print("-" * 70)

    for key, value in (
        governed_validation.items()
    ):

        if key != "validation_checks":
            print(
                f"{key}: {value}"
            )

    print()
    print(
        "VALIDATION CHECKS"
    )
    print("-" * 70)

    for key, value in (
        governed_validation[
            "validation_checks"
        ].items()
    ):
        print(
            f"{key}: {value}"
        )

    print()
    print(
        "FORMAL TARGET DISTRIBUTION"
    )
    print("-" * 70)

    print(
        governed_df[
            DERIVED_TARGET_COLUMN
        ]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    print()
    print("=" * 70)

    if (
        governed_validation[
            "validation_status"
        ]
        == "PASS"
    ):
        print(
            "D3 governed cohort construction "
            "and outcome engineering: PASS"
        )
    else:
        print(
            "D3 governed cohort construction "
            "and outcome engineering: FAIL"
        )

    print("=" * 70)