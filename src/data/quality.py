# ============================================================
# D2 — DATA QUALITY & BIAS ASSESSMENT
# D2.1 — ACCURACY ASSESSMENT
# ============================================================

from __future__ import annotations

from typing import Any

import pandas as pd

from src.data.validation import load_raw_dataset


# ============================================================
# 1. GOVERNED VALID-VALUE DOMAINS
# ============================================================

VALID_GENDER_VALUES = {
    "Male",
    "Female",
    "Unknown/Invalid",
}

VALID_AGE_VALUES = {
    "[0-10)",
    "[10-20)",
    "[20-30)",
    "[30-40)",
    "[40-50)",
    "[50-60)",
    "[60-70)",
    "[70-80)",
    "[80-90)",
    "[90-100)",
}

VALID_READMISSION_VALUES = {
    "NO",
    ">30",
    "<30",
}

VALID_CHANGE_VALUES = {
    "No",
    "Ch",
}

VALID_DIABETES_MED_VALUES = {
    "No",
    "Yes",
}

VALID_A1C_VALUES = {
    "None",
    "Norm",
    ">7",
    ">8",
}

VALID_MAX_GLUCOSE_VALUES = {
    "None",
    "Norm",
    ">200",
    ">300",
}


# ============================================================
# 2. HELPER — INVALID DOMAIN VALUES
# ============================================================

def find_invalid_values(
    series: pd.Series,
    valid_values: set[str],
) -> list[str]:
    """
    Return observed non-null values outside the governed domain.
    """

    observed = set(
        series.dropna().astype(str).unique()
    )

    return sorted(observed - valid_values)


# ============================================================
# 3. HELPER — NUMERIC RANGE VIOLATIONS
# ============================================================

def count_range_violations(
    series: pd.Series,
    minimum: float | None = None,
    maximum: float | None = None,
) -> int:
    """
    Count numeric values outside an explicitly governed range.
    """

    numeric = pd.to_numeric(series, errors="coerce")

    violation = pd.Series(
        False,
        index=series.index,
    )

    if minimum is not None:
        violation |= numeric < minimum

    if maximum is not None:
        violation |= numeric > maximum

    return int(violation.sum())


# ============================================================
# 4. ACCURACY / CONFORMANCE ASSESSMENT
# ============================================================

def assess_accuracy(
    df: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Assess domain conformance and basic value plausibility.

    This assessment does not claim verification against an
    external clinical ground truth.
    """

    if df is None:
        df = load_raw_dataset()

    results: dict[str, Any] = {}

    # --------------------------------------------------------
    # Categorical domain conformance
    # --------------------------------------------------------

    domain_checks = {
        "gender": VALID_GENDER_VALUES,
        "age": VALID_AGE_VALUES,
        "readmitted": VALID_READMISSION_VALUES,
        "change": VALID_CHANGE_VALUES,
        "diabetesMed": VALID_DIABETES_MED_VALUES,
        "A1Cresult": VALID_A1C_VALUES,
        "max_glu_serum": VALID_MAX_GLUCOSE_VALUES,
    }

    categorical_results = {}

    for column, valid_values in domain_checks.items():
        invalid_values = find_invalid_values(
            df[column],
            valid_values,
        )

        categorical_results[column] = {
            "invalid_values": invalid_values,
            "invalid_value_count": int(
                df[column]
                .astype(str)
                .isin(invalid_values)
                .sum()
            ),
            "status": (
                "PASS"
                if len(invalid_values) == 0
                else "REVIEW"
            ),
        }

    results["categorical_domain_checks"] = categorical_results

    # --------------------------------------------------------
    # Numeric plausibility checks
    # --------------------------------------------------------

    numeric_ranges = {
        "time_in_hospital": (1, 14),
        "num_lab_procedures": (0, None),
        "num_procedures": (0, None),
        "num_medications": (0, None),
        "number_outpatient": (0, None),
        "number_emergency": (0, None),
        "number_inpatient": (0, None),
        "number_diagnoses": (0, None),
    }

    numeric_results = {}

    for column, (minimum, maximum) in numeric_ranges.items():
        violations = count_range_violations(
            df[column],
            minimum=minimum,
            maximum=maximum,
        )

        numeric_results[column] = {
            "minimum_observed": float(
                pd.to_numeric(
                    df[column],
                    errors="coerce",
                ).min()
            ),
            "maximum_observed": float(
                pd.to_numeric(
                    df[column],
                    errors="coerce",
                ).max()
            ),
            "range_violation_count": violations,
            "status": (
                "PASS"
                if violations == 0
                else "REVIEW"
            ),
        }

    results["numeric_plausibility_checks"] = numeric_results

    # --------------------------------------------------------
    # Identifier plausibility
    # --------------------------------------------------------

    results["identifier_checks"] = {
        "nonpositive_encounter_ids": int(
            (df["encounter_id"] <= 0).sum()
        ),
        "nonpositive_patient_ids": int(
            (df["patient_nbr"] <= 0).sum()
        ),
    }

    # --------------------------------------------------------
    # Missing-like sentinel inventory
    # --------------------------------------------------------

    missing_like_tokens = {
        "?",
        "Unknown/Invalid",
    }

    sentinel_results = {}

    for column in df.columns:
        counts = (
            df[column]
            .astype(str)
            .value_counts()
        )

        detected = {
            token: int(counts.get(token, 0))
            for token in missing_like_tokens
            if int(counts.get(token, 0)) > 0
        }

        if detected:
            sentinel_results[column] = detected

    results["missing_like_sentinels"] = sentinel_results

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    categorical_reviews = sum(
        item["status"] == "REVIEW"
        for item in categorical_results.values()
    )

    numeric_reviews = sum(
        item["status"] == "REVIEW"
        for item in numeric_results.values()
    )

    identifier_issues = sum(
        results["identifier_checks"].values()
    )

    results["summary"] = {
        "categorical_domains_requiring_review":
            int(categorical_reviews),

        "numeric_fields_requiring_review":
            int(numeric_reviews),

        "identifier_issues":
            int(identifier_issues),

        "missing_like_sentinel_columns":
            int(len(sentinel_results)),
    }

    return results

# ============================================================
# 5. D2.2 — COMPLETENESS ASSESSMENT
# ============================================================

MISSING_SENTINELS = {
    "?",
    "Unknown/Invalid",
}


def assess_completeness(
    df: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Assess physical and semantic completeness.

    Missingness includes:
    1. native null/NaN values;
    2. governed missing-like sentinel values.

    Dataset-defined categories such as "None" are not automatically
    treated as missing because their semantics may represent
    "not measured" rather than an unrecorded value.
    """

    if df is None:
        df = load_raw_dataset()

    total_rows = len(df)
    column_results: dict[str, Any] = {}

    for column in df.columns:

        native_missing_mask = df[column].isna()

        string_values = df[column].astype("string")

        sentinel_missing_mask = string_values.isin(
            MISSING_SENTINELS
        ).fillna(False)

        combined_missing_mask = (
            native_missing_mask | sentinel_missing_mask
        )

        native_missing = int(native_missing_mask.sum())
        sentinel_missing = int(sentinel_missing_mask.sum())
        total_missing = int(combined_missing_mask.sum())

        completeness_pct = (
            ((total_rows - total_missing) / total_rows) * 100
        )

        column_results[column] = {
            "native_missing_count": native_missing,
            "sentinel_missing_count": sentinel_missing,
            "total_missing_count": total_missing,
            "missing_pct": round(
                (total_missing / total_rows) * 100,
                4,
            ),
            "completeness_pct": round(
                completeness_pct,
                4,
            ),
        }

    # --------------------------------------------------------
    # Rank variables by missingness
    # --------------------------------------------------------

    ranked_missingness = sorted(
        (
            {
                "column": column,
                **metrics,
            }
            for column, metrics in column_results.items()
            if metrics["total_missing_count"] > 0
        ),
        key=lambda item: item["missing_pct"],
        reverse=True,
    )

    # --------------------------------------------------------
    # Encounter-level completeness burden
    # --------------------------------------------------------

    missing_matrix = pd.DataFrame(
        {
            column: (
                df[column].isna()
                | df[column]
                    .astype("string")
                    .isin(MISSING_SENTINELS)
                    .fillna(False)
            )
            for column in df.columns
        }
    )

    missing_fields_per_encounter = missing_matrix.sum(axis=1)

    encounter_summary = {
        "encounters_with_any_missing": int(
            (missing_fields_per_encounter > 0).sum()
        ),
        "encounters_with_any_missing_pct": round(
            (
                (missing_fields_per_encounter > 0).mean()
                * 100
            ),
            4,
        ),
        "median_missing_fields_per_encounter": float(
            missing_fields_per_encounter.median()
        ),
        "maximum_missing_fields_per_encounter": int(
            missing_fields_per_encounter.max()
        ),
    }

    # --------------------------------------------------------
    # Dataset-level summary
    # --------------------------------------------------------

    columns_with_missingness = len(ranked_missingness)

    results = {
        "total_rows": int(total_rows),
        "total_columns": int(df.shape[1]),
        "columns_with_missingness": int(
            columns_with_missingness
        ),
        "columns_without_missingness": int(
            df.shape[1] - columns_with_missingness
        ),
        "ranked_missingness": ranked_missingness,
        "encounter_level_summary": encounter_summary,
    }

    return results
# ============================================================
# 6. D2.3 — CURRENCY ASSESSMENT
# ============================================================

from datetime import date


def assess_currency() -> dict[str, Any]:
    """
    Assess temporal currency using documented dataset provenance.

    The source dataset contains encounters from 1999–2008.
    It does not contain encounter-level calendar dates suitable
    for direct temporal recency analysis.
    """

    source_start_year = 1999
    source_end_year = 2008
    assessment_year = date.today().year

    years_since_latest_source_data = (
        assessment_year - source_end_year
    )

    results = {
        "source_start_year": source_start_year,
        "source_end_year": source_end_year,
        "assessment_year": assessment_year,
        "years_since_latest_source_data":
            years_since_latest_source_data,

        "encounter_level_dates_available": False,

        "temporal_recency_status": "HIGH RISK",

        "currency_finding": (
            "The dataset is historically valuable for model "
            "development and methodological demonstration, but "
            "is not temporally current for direct contemporary "
            "clinical deployment."
        ),

        "potential_drift_domains": [
            "clinical practice",
            "diabetes management",
            "medication use",
            "laboratory testing practices",
            "coding practices",
            "hospital workflows",
            "readmission management",
            "population case mix",
            "healthcare policy and reimbursement",
        ],

        "deployment_control": (
            "Contemporary external validation and temporal "
            "recalibration are required before clinical deployment."
        ),

        "status": "CONDITIONAL PASS",
    }

    return results

# ============================================================
# 7. D2.4 — CONSISTENCY ASSESSMENT
# ============================================================

def assess_consistency(
    df: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Assess internal consistency and cross-field logical coherence.

    Findings indicate records requiring review and do not
    automatically imply that the source record is clinically wrong.
    """

    if df is None:
        df = load_raw_dataset()

    results: dict[str, Any] = {}

    # --------------------------------------------------------
    # 1. Duplicate record consistency
    # --------------------------------------------------------

    results["duplicate_checks"] = {
        "duplicate_encounter_ids": int(
            df["encounter_id"].duplicated().sum()
        ),
        "fully_duplicate_rows": int(
            df.duplicated().sum()
        ),
    }

    # --------------------------------------------------------
    # 2. Diabetes medication source columns
    # --------------------------------------------------------

    medication_columns = [
        "metformin",
        "repaglinide",
        "nateglinide",
        "chlorpropamide",
        "glimepiride",
        "acetohexamide",
        "glipizide",
        "glyburide",
        "tolbutamide",
        "pioglitazone",
        "rosiglitazone",
        "acarbose",
        "miglitol",
        "troglitazone",
        "tolazamide",
        "examide",
        "citoglipton",
        "insulin",
        "glyburide-metformin",
        "glipizide-metformin",
        "glimepiride-pioglitazone",
        "metformin-rosiglitazone",
        "metformin-pioglitazone",
    ]

    missing_medication_columns = sorted(
        set(medication_columns) - set(df.columns)
    )

    results["medication_schema"] = {
        "expected_medication_columns":
            len(medication_columns),
        "missing_medication_columns":
            missing_medication_columns,
    }

    # --------------------------------------------------------
    # 3. Medication value-domain consistency
    # --------------------------------------------------------

    valid_medication_states = {
        "No",
        "Steady",
        "Up",
        "Down",
    }

    medication_domain_issues = {}

    for column in medication_columns:

        if column not in df.columns:
            continue

        observed = set(
            df[column]
            .dropna()
            .astype(str)
            .unique()
        )

        invalid = sorted(
            observed - valid_medication_states
        )

        if invalid:
            medication_domain_issues[column] = invalid

    results["medication_domain_issues"] = (
        medication_domain_issues
    )

    # --------------------------------------------------------
    # 4. Derive medication exposure from source columns
    # --------------------------------------------------------

    available_medication_columns = [
        column
        for column in medication_columns
        if column in df.columns
    ]

    medication_exposure = (
        df[available_medication_columns]
        .ne("No")
        .any(axis=1)
    )

    # --------------------------------------------------------
    # 5. diabetesMed cross-field consistency
    # --------------------------------------------------------

    diabetes_med_yes_without_exposure = (
        df["diabetesMed"].eq("Yes")
        & ~medication_exposure
    )

    diabetes_med_no_with_exposure = (
        df["diabetesMed"].eq("No")
        & medication_exposure
    )

    results["diabetes_medication_consistency"] = {
        "diabetesMed_yes_without_recorded_exposure":
            int(
                diabetes_med_yes_without_exposure.sum()
            ),

        "diabetesMed_no_with_recorded_exposure":
            int(
                diabetes_med_no_with_exposure.sum()
            ),
    }

    # --------------------------------------------------------
    # 6. Medication-change consistency
    # --------------------------------------------------------

    medication_change_recorded = (
        df[available_medication_columns]
        .isin(["Up", "Down"])
        .any(axis=1)
    )

    change_ch_without_medication_change = (
        df["change"].eq("Ch")
        & ~medication_change_recorded
    )

    change_no_with_medication_change = (
        df["change"].eq("No")
        & medication_change_recorded
    )

    results["medication_change_consistency"] = {
        "change_Ch_without_up_or_down":
            int(
                change_ch_without_medication_change.sum()
            ),

        "change_No_with_up_or_down":
            int(
                change_no_with_medication_change.sum()
            ),
    }

    # --------------------------------------------------------
    # 7. Diagnosis hierarchy completeness consistency
    # --------------------------------------------------------

    diag1_missing = df["diag_1"].astype("string").eq("?")
    diag2_missing = df["diag_2"].astype("string").eq("?")
    diag3_missing = df["diag_3"].astype("string").eq("?")

    results["diagnosis_sequence_consistency"] = {
        "diag1_missing_but_diag2_present":
            int(
                (
                    diag1_missing
                    & ~diag2_missing
                ).sum()
            ),

        "diag1_missing_but_diag3_present":
            int(
                (
                    diag1_missing
                    & ~diag3_missing
                ).sum()
            ),

        "diag2_missing_but_diag3_present":
            int(
                (
                    diag2_missing
                    & ~diag3_missing
                ).sum()
            ),
    }

    # --------------------------------------------------------
    # 8. Readmission value consistency
    # --------------------------------------------------------

    results["readmission_consistency"] = {
        "missing_readmission_values":
            int(df["readmitted"].isna().sum()),

        "unexpected_readmission_values":
            int(
                (
                    ~df["readmitted"].isin(
                        VALID_READMISSION_VALUES
                    )
                ).sum()
            ),
    }

    # --------------------------------------------------------
    # 9. Summary
    # --------------------------------------------------------

    contradiction_count = (
        results[
            "diabetes_medication_consistency"
        ][
            "diabetesMed_yes_without_recorded_exposure"
        ]
        +
        results[
            "diabetes_medication_consistency"
        ][
            "diabetesMed_no_with_recorded_exposure"
        ]
        +
        results[
            "medication_change_consistency"
        ][
            "change_Ch_without_up_or_down"
        ]
        +
        results[
            "medication_change_consistency"
        ][
            "change_No_with_up_or_down"
        ]
    )

    results["summary"] = {
        "duplicate_encounter_ids":
            results["duplicate_checks"][
                "duplicate_encounter_ids"
            ],

        "fully_duplicate_rows":
            results["duplicate_checks"][
                "fully_duplicate_rows"
            ],

        "medication_columns_missing":
            len(missing_medication_columns),

        "medication_columns_with_invalid_domains":
            len(medication_domain_issues),

        "cross_field_medication_flags_for_review":
            int(contradiction_count),
    }

    return results

# ============================================================
# 8. D2.5 — REPRESENTATION ASSESSMENT
# ============================================================

def _distribution_table(
    series: pd.Series,
) -> list[dict[str, Any]]:
    """
    Return count and percentage distribution for a variable.
    Missing/sentinel states are retained rather than silently removed.
    """

    counts = (
        series
        .astype("string")
        .fillna("<MISSING>")
        .value_counts(dropna=False)
    )

    total = len(series)

    return [
        {
            "category": str(category),
            "count": int(count),
            "percentage": round(
                (count / total) * 100,
                4,
            ),
        }
        for category, count in counts.items()
    ]


def assess_representation(
    df: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Assess representation across demographic, patient-frequency,
    diagnostic and prior-utilization dimensions.

    This is descriptive representation assessment.
    It does not by itself establish bias.
    """

    if df is None:
        df = load_raw_dataset()

    results: dict[str, Any] = {}

    # --------------------------------------------------------
    # 1. Encounter and patient population
    # --------------------------------------------------------

    patient_encounter_counts = (
        df.groupby("patient_nbr")
        .size()
    )

    results["population_structure"] = {
        "total_encounters": int(len(df)),
        "unique_patients": int(
            df["patient_nbr"].nunique()
        ),
        "patients_with_multiple_encounters": int(
            (patient_encounter_counts > 1).sum()
        ),
        "maximum_encounters_per_patient": int(
            patient_encounter_counts.max()
        ),
        "median_encounters_per_patient": float(
            patient_encounter_counts.median()
        ),
    }

    # --------------------------------------------------------
    # 2. Demographic representation — encounter level
    # --------------------------------------------------------

    results["encounter_level_demographics"] = {
        "age": _distribution_table(df["age"]),
        "gender": _distribution_table(df["gender"]),
        "race": _distribution_table(df["race"]),
    }

    # --------------------------------------------------------
    # 3. Patient-level demographic representation
    # --------------------------------------------------------

    first_patient_record = (
        df.sort_values("encounter_id")
        .drop_duplicates(
            subset="patient_nbr",
            keep="first",
        )
    )

    results["patient_level_demographics"] = {
        "age": _distribution_table(
            first_patient_record["age"]
        ),
        "gender": _distribution_table(
            first_patient_record["gender"]
        ),
        "race": _distribution_table(
            first_patient_record["race"]
        ),
    }

    # --------------------------------------------------------
    # 4. Prior healthcare-utilization representation
    # --------------------------------------------------------

    prior_utilization = (
        df["number_outpatient"]
        + df["number_emergency"]
        + df["number_inpatient"]
    )

    results["prior_utilization"] = {
        "no_prior_utilization": int(
            (prior_utilization == 0).sum()
        ),
        "any_prior_utilization": int(
            (prior_utilization > 0).sum()
        ),
        "any_prior_utilization_pct": round(
            (prior_utilization > 0).mean() * 100,
            4,
        ),
        "high_prior_utilization_4plus": int(
            (prior_utilization >= 4).sum()
        ),
        "high_prior_utilization_4plus_pct": round(
            (prior_utilization >= 4).mean() * 100,
            4,
        ),
    }

    # --------------------------------------------------------
    # 5. Diagnosis availability representation
    # --------------------------------------------------------

    results["diagnosis_availability"] = {
        "diag_1_available_pct": round(
            (~df["diag_1"].astype("string").eq("?"))
            .mean() * 100,
            4,
        ),
        "diag_2_available_pct": round(
            (~df["diag_2"].astype("string").eq("?"))
            .mean() * 100,
            4,
        ),
        "diag_3_available_pct": round(
            (~df["diag_3"].astype("string").eq("?"))
            .mean() * 100,
            4,
        ),
    }

    # --------------------------------------------------------
    # 6. Source outcome representation
    # --------------------------------------------------------

    results["readmission_distribution"] = (
        _distribution_table(df["readmitted"])
    )

    results["readmission_under_30_days"] = {
        "count": int(
            df["readmitted"].eq("<30").sum()
        ),
        "percentage": round(
            df["readmitted"].eq("<30").mean()
            * 100,
            4,
        ),
    }

    # --------------------------------------------------------
    # 7. Representation flags
    # --------------------------------------------------------

    representation_flags = []

    race_counts = (
        df["race"]
        .astype("string")
        .value_counts(normalize=True)
        * 100
    )

    gender_counts = (
        df["gender"]
        .astype("string")
        .value_counts(normalize=True)
        * 100
    )

    for category, percentage in race_counts.items():
        if percentage < 5:
            representation_flags.append(
                {
                    "dimension": "race",
                    "category": str(category),
                    "encounter_percentage":
                        round(float(percentage), 4),
                    "finding":
                        "Low encounter representation",
                }
            )

    for category, percentage in gender_counts.items():
        if percentage < 5:
            representation_flags.append(
                {
                    "dimension": "gender",
                    "category": str(category),
                    "encounter_percentage":
                        round(float(percentage), 4),
                    "finding":
                        "Low encounter representation",
                }
            )

    results["representation_flags"] = (
        representation_flags
    )

    return results

# ============================================================
# 9. D2.6 — BIAS ASSESSMENT
# ============================================================

def assess_bias(
    df: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """
    Perform pre-model bias diagnostics.

    This assessment identifies potential bias mechanisms and
    disparities in data generation. It does not establish causal
    discrimination and does not evaluate model fairness because
    no model has yet been trained.
    """

    if df is None:
        df = load_raw_dataset()

    working = df.copy()

    # --------------------------------------------------------
    # 1. Governed missingness indicators
    # --------------------------------------------------------

    working["race_missing"] = (
        working["race"]
        .astype("string")
        .eq("?")
    )

    working["weight_missing"] = (
        working["weight"]
        .astype("string")
        .eq("?")
    )

    working["payer_missing"] = (
        working["payer_code"]
        .astype("string")
        .eq("?")
    )

    working["specialty_missing"] = (
        working["medical_specialty"]
        .astype("string")
        .eq("?")
    )

    working["a1c_missing"] = (
        working["A1Cresult"].isna()
    )

    working["max_glucose_missing"] = (
        working["max_glu_serum"].isna()
    )

    working["diag1_missing"] = (
        working["diag_1"]
        .astype("string")
        .eq("?")
    )

    working["diag2_missing"] = (
        working["diag_2"]
        .astype("string")
        .eq("?")
    )

    working["diag3_missing"] = (
        working["diag_3"]
        .astype("string")
        .eq("?")
    )

    # --------------------------------------------------------
    # 2. Raw 30-day outcome indicator — audit only
    # --------------------------------------------------------

    working["_audit_readmitted_30d"] = (
        working["readmitted"]
        .eq("<30")
        .astype(int)
    )

    # This is temporary audit evidence.
    # The governed modeling target will be created later in D3.

    # --------------------------------------------------------
    # 3. Helper — subgroup rates
    # --------------------------------------------------------

    def subgroup_rates(
        group_column: str,
        indicator_columns: list[str],
    ) -> list[dict[str, Any]]:

        records = []

        grouped = working.groupby(
            group_column,
            dropna=False,
            observed=False,
        )

        for group_value, group_df in grouped:

            record: dict[str, Any] = {
                "group": str(group_value),
                "encounters": int(len(group_df)),
            }

            for indicator in indicator_columns:
                record[f"{indicator}_pct"] = round(
                    float(group_df[indicator].mean() * 100),
                    4,
                )

            records.append(record)

        return records

    # --------------------------------------------------------
    # 4. Missingness / measurement patterns by race
    # --------------------------------------------------------

    measurement_indicators = [
        "weight_missing",
        "payer_missing",
        "specialty_missing",
        "a1c_missing",
        "max_glucose_missing",
        "diag1_missing",
        "diag2_missing",
        "diag3_missing",
    ]

    race_measurement = subgroup_rates(
        "race",
        measurement_indicators,
    )

    # --------------------------------------------------------
    # 5. Missingness / measurement patterns by gender
    # --------------------------------------------------------

    gender_measurement = subgroup_rates(
        "gender",
        measurement_indicators,
    )

    # --------------------------------------------------------
    # 6. Missingness / measurement patterns by age
    # --------------------------------------------------------

    age_measurement = subgroup_rates(
        "age",
        measurement_indicators,
    )

    # --------------------------------------------------------
    # 7. Raw outcome rates across demographic groups
    # --------------------------------------------------------

    race_outcomes = subgroup_rates(
        "race",
        ["_audit_readmitted_30d"],
    )

    gender_outcomes = subgroup_rates(
        "gender",
        ["_audit_readmitted_30d"],
    )

    age_outcomes = subgroup_rates(
        "age",
        ["_audit_readmitted_30d"],
    )

    # --------------------------------------------------------
    # 8. Repeated-encounter concentration
    # --------------------------------------------------------

    patient_frequency = (
        working.groupby("patient_nbr")
        .size()
        .rename("encounter_count")
    )

    working = working.join(
        patient_frequency,
        on="patient_nbr",
    )

    working["repeat_patient"] = (
        working["encounter_count"] > 1
    )

    repeat_encounter_pct = round(
        float(
            working["repeat_patient"].mean()
            * 100
        ),
        4,
    )

    # --------------------------------------------------------
    # 9. Representation-risk flags
    # --------------------------------------------------------

    representation_risk_flags = []

    for dimension in ["race", "gender", "age"]:

        distribution = (
            working[dimension]
            .astype("string")
            .value_counts(
                normalize=True,
                dropna=False,
            )
            * 100
        )

        for category, percentage in distribution.items():

            if percentage < 1:
                risk_level = "HIGH"
            elif percentage < 5:
                risk_level = "MODERATE"
            else:
                continue

            representation_risk_flags.append(
                {
                    "dimension": dimension,
                    "category": str(category),
                    "percentage": round(
                        float(percentage),
                        4,
                    ),
                    "risk_level": risk_level,
                    "risk":
                        "Limited subgroup representation may "
                        "reduce precision of downstream "
                        "performance and fairness estimates.",
                }
            )

    # --------------------------------------------------------
    # 10. Pre-model bias risk register
    # --------------------------------------------------------

    bias_risk_register = [
        {
            "risk_type": "Temporal bias",
            "risk_level": "HIGH",
            "evidence":
                "Source encounters are from 1999-2008.",
            "downstream_control":
                "Require contemporary external validation "
                "before clinical deployment.",
        },
        {
            "risk_type": "Representation bias",
            "risk_level": "REVIEW",
            "evidence":
                "Several demographic subgroups have low "
                "representation.",
            "downstream_control":
                "Require subgroup-specific performance "
                "estimation and uncertainty assessment.",
        },
        {
            "risk_type": "Measurement / missingness bias",
            "risk_level": "REVIEW",
            "evidence":
                "Major variables show substantial missingness; "
                "subgroup missingness rates require comparison.",
            "downstream_control":
                "Evaluate missingness patterns by demographic "
                "and clinical groups before feature approval.",
        },
        {
            "risk_type": "Repeated-patient weighting",
            "risk_level": "REVIEW",
            "evidence":
                "Some patients contribute multiple encounters.",
            "downstream_control":
                "Use patient-disjoint data splitting and "
                "patient-aware statistical evaluation.",
        },
        {
            "risk_type": "Label / outcome bias",
            "risk_level": "REVIEW",
            "evidence":
                "Observed readmission may reflect healthcare "
                "access, utilization, discharge processes and "
                "outcome ascertainment in addition to clinical "
                "risk.",
            "downstream_control":
                "Document label limitations and evaluate "
                "subgroup outcome and model-error patterns.",
        },
    ]

    return {
        "race_measurement_patterns": race_measurement,
        "gender_measurement_patterns": gender_measurement,
        "age_measurement_patterns": age_measurement,

        "race_raw_30d_outcome_rates": race_outcomes,
        "gender_raw_30d_outcome_rates": gender_outcomes,
        "age_raw_30d_outcome_rates": age_outcomes,

        "repeated_patient_structure": {
            "repeat_patient_encounter_pct":
                repeat_encounter_pct,
            "maximum_encounters_per_patient":
                int(patient_frequency.max()),
        },

        "representation_risk_flags":
            representation_risk_flags,

        "bias_risk_register":
            bias_risk_register,
    }