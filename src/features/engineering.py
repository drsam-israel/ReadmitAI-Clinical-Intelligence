# ============================================================
# D6 — GOVERNED FEATURE ENGINEERING PIPELINE
# ============================================================
"""
Governed deterministic feature engineering for the Diabetes
Readmission Clinical AI project.

D6 converts D4-permitted source information into clinically
meaningful model candidate features while respecting:

1. the D4 prediction-time contract;
2. the D4 feature-governance dispositions;
3. the frozen D5 patient partition assignment;
4. patient-level leakage controls;
5. locked-test protection;
6. reproducibility requirements.

D6 performs deterministic feature construction only.

D6 does NOT:
- fit imputers;
- fit encoders;
- scale variables;
- select models;
- tune hyperparameters;
- calibrate models;
- select decision thresholds;
- evaluate the locked test partition.

Those activities belong to downstream lifecycle stages.
"""

# ============================================================
# D6.1 — IMPORTS
# ============================================================

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import hashlib

import numpy as np
import pandas as pd

from src.data.splitting import (
    GROUP_COLUMN,
    TARGET_COLUMN,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    TEST_LABEL,
)


# ============================================================
# D6.2 — PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

GOVERNED_COHORT_PATH = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "D3_governed_modeling_cohort.parquet"
)

FROZEN_SPLIT_ASSIGNMENT_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "splits"
    / "D5_patient_split_assignment.csv"
)


# ============================================================
# D6.3 — FROZEN D5 ASSIGNMENT CHECKSUM
# ============================================================

EXPECTED_D5_ASSIGNMENT_SHA256 = (
    "D575A296909467EB4CDE7529978D5306C38BFE26959A4EBEA907CE209472977E"
)


# ============================================================
# D6.4 — FEATURE ENGINEERING CONTRACT
# ============================================================

@dataclass(frozen=True)
class FeatureEngineeringContract:
    """
    Formal D6 feature-engineering lifecycle contract.
    """

    prediction_point: str
    source_cohort: str
    split_source: str
    target: str
    grouping_key: str
    development_partitions: tuple[str, ...]
    locked_test_partition: str
    locked_test_development_use_permitted: bool
    transformations_must_be_deterministic: bool
    preprocessing_fitting_permitted: bool
    model_training_permitted: bool
    feature_selection_using_locked_test_permitted: bool


FEATURE_ENGINEERING_CONTRACT = FeatureEngineeringContract(
    prediction_point=(
        "Before discharge, at the point when model output would "
        "support discharge-planning decisions."
    ),

    source_cohort=(
        "D3_governed_modeling_cohort.parquet"
    ),

    split_source=(
        "D5_patient_split_assignment.csv"
    ),

    target=TARGET_COLUMN,

    grouping_key=GROUP_COLUMN,

    development_partitions=(
        TRAIN_LABEL,
        VALIDATION_LABEL,
    ),

    locked_test_partition=TEST_LABEL,

    locked_test_development_use_permitted=False,

    transformations_must_be_deterministic=True,

    preprocessing_fitting_permitted=False,

    model_training_permitted=False,

    feature_selection_using_locked_test_permitted=False,
)


# ============================================================
# D6.5 — FEATURE GOVERNANCE CLASSES
# ============================================================

FEATURE_CLASS_DEMOGRAPHIC = (
    "DEMOGRAPHIC"
)

FEATURE_CLASS_ADMISSION_CONTEXT = (
    "ADMISSION_CONTEXT"
)

FEATURE_CLASS_PRIOR_UTILIZATION = (
    "PRIOR_UTILIZATION"
)

FEATURE_CLASS_DIAGNOSIS = (
    "DIAGNOSIS"
)

FEATURE_CLASS_GLYCEMIC = (
    "GLYCEMIC"
)

FEATURE_CLASS_MEDICATION = (
    "MEDICATION"
)

FEATURE_CLASS_TREATMENT_STRUCTURE = (
    "TREATMENT_STRUCTURE"
)


# ============================================================
# D6.6 — D6 FEATURE DISPOSITIONS
# ============================================================

D6_CANDIDATE = "CANDIDATE"

D6_CONDITIONAL = "CONDITIONAL"

D6_BLOCKED = "BLOCKED"

D6_GOVERNANCE_ONLY = (
    "GOVERNANCE_ONLY"
)

D6_TARGET_ONLY = "TARGET_ONLY"


# ============================================================
# D6.7 — D4 HARD-BLOCKED RAW VARIABLES
# ============================================================

HARD_BLOCKED_RAW_FEATURES = frozenset(
    {
        "discharge_disposition_id",
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_diagnoses",
    }
)


# ============================================================
# D6.8 — IDENTIFIER & OUTCOME PROTECTION
# ============================================================

IDENTIFIER_COLUMNS = frozenset(
    {
        "encounter_id",
        "patient_nbr",
    }
)

OUTCOME_COLUMNS = frozenset(
    {
        "readmitted",
        "readmitted_30d",
    }
)


# ============================================================
# D6.9 — APPROVED D4 SOURCE VARIABLES
# ============================================================

D4_APPROVED_SOURCE_FEATURES = frozenset(
    {
        "race",
        "gender",
        "age",
        "admission_type_id",
        "admission_source_id",
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
    }
)


# ============================================================
# D6.10 — CONDITIONAL D4 SOURCE VARIABLES
# ============================================================

D4_CONDITIONAL_SOURCE_FEATURES = frozenset(
    {
        "weight",
        "payer_code",
        "medical_specialty",

        "diag_1",
        "diag_2",
        "diag_3",

        "max_glu_serum",
        "A1Cresult",

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

        "change",
        "diabetesMed",
    }
)


# ============================================================
# D6.11 — MEDICATION SOURCE VARIABLES
# ============================================================

MEDICATION_COLUMNS = (
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
)


# ============================================================
# D6.12 — DIAGNOSIS SOURCE VARIABLES
# ============================================================

DIAGNOSIS_COLUMNS = (
    "diag_1",
    "diag_2",
    "diag_3",
)


# ============================================================
# D6.13 — REQUIRED D6 SOURCE COLUMNS
# ============================================================

REQUIRED_D6_COLUMNS = frozenset(
    {
        "encounter_id",
        GROUP_COLUMN,
        TARGET_COLUMN,

        *D4_APPROVED_SOURCE_FEATURES,
        *D4_CONDITIONAL_SOURCE_FEATURES,
    }
)


# ============================================================
# D6.14 — FEATURE SPECIFICATION RECORD
# ============================================================

@dataclass(frozen=True)
class FeatureSpecification:
    """
    Governance specification for one engineered feature.
    """

    feature_name: str
    feature_class: str
    source_columns: tuple[str, ...]
    disposition: str
    transformation: str
    prediction_time_rationale: str
    permitted_use: str


# ============================================================
# D6.15 — COMPLETE GOVERNED FEATURE SPECIFICATIONS
# ============================================================

FEATURE_SPECIFICATIONS = (

    # --------------------------------------------------------
    # D6.15A — DEMOGRAPHIC FEATURES
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="race",
        feature_class=FEATURE_CLASS_DEMOGRAPHIC,
        source_columns=("race",),
        disposition=D6_CANDIDATE,
        transformation="Direct governed source representation.",
        prediction_time_rationale=(
            "D4-approved demographic information available before "
            "the discharge-planning prediction point."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="gender",
        feature_class=FEATURE_CLASS_DEMOGRAPHIC,
        source_columns=("gender",),
        disposition=D6_CANDIDATE,
        transformation="Direct governed source representation.",
        prediction_time_rationale=(
            "D4-approved demographic information available before "
            "the discharge-planning prediction point."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="age",
        feature_class=FEATURE_CLASS_DEMOGRAPHIC,
        source_columns=("age",),
        disposition=D6_CANDIDATE,
        transformation="Direct governed source representation.",
        prediction_time_rationale=(
            "D4-approved demographic information available before "
            "the discharge-planning prediction point."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    # --------------------------------------------------------
    # D6.15B — ADMISSION CONTEXT
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="admission_type_id",
        feature_class=FEATURE_CLASS_ADMISSION_CONTEXT,
        source_columns=("admission_type_id",),
        disposition=D6_CANDIDATE,
        transformation="Direct governed source representation.",
        prediction_time_rationale=(
            "D4-approved admission context available before the "
            "prediction point."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="admission_source_id",
        feature_class=FEATURE_CLASS_ADMISSION_CONTEXT,
        source_columns=("admission_source_id",),
        disposition=D6_CANDIDATE,
        transformation="Direct governed source representation.",
        prediction_time_rationale=(
            "D4-approved admission-source information available "
            "before the prediction point."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    # --------------------------------------------------------
    # D6.15C — PRIOR UTILIZATION
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="prior_outpatient_use",
        feature_class=FEATURE_CLASS_PRIOR_UTILIZATION,
        source_columns=("number_outpatient",),
        disposition=D6_CANDIDATE,
        transformation=(
            "Binary indicator: number_outpatient > 0."
        ),
        prediction_time_rationale=(
            "Derived deterministically from the D4-approved "
            "historical outpatient-utilization source."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="prior_emergency_use",
        feature_class=FEATURE_CLASS_PRIOR_UTILIZATION,
        source_columns=("number_emergency",),
        disposition=D6_CANDIDATE,
        transformation=(
            "Binary indicator: number_emergency > 0."
        ),
        prediction_time_rationale=(
            "Derived deterministically from the D4-approved "
            "historical emergency-utilization source."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="prior_inpatient_use",
        feature_class=FEATURE_CLASS_PRIOR_UTILIZATION,
        source_columns=("number_inpatient",),
        disposition=D6_CANDIDATE,
        transformation=(
            "Binary indicator: number_inpatient > 0."
        ),
        prediction_time_rationale=(
            "Derived deterministically from the D4-approved "
            "historical inpatient-utilization source."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="prior_utilization_intensity",
        feature_class=FEATURE_CLASS_PRIOR_UTILIZATION,
        source_columns=(
            "number_outpatient",
            "number_emergency",
            "number_inpatient",
        ),
        disposition=D6_CANDIDATE,
        transformation=(
            "Sum of prior outpatient, emergency, and inpatient "
            "utilization counts."
        ),
        prediction_time_rationale=(
            "Derived exclusively from D4-approved historical "
            "utilization sources."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    FeatureSpecification(
        feature_name="prior_utilization_domain_count",
        feature_class=FEATURE_CLASS_PRIOR_UTILIZATION,
        source_columns=(
            "number_outpatient",
            "number_emergency",
            "number_inpatient",
        ),
        disposition=D6_CANDIDATE,
        transformation=(
            "Count of utilization domains with prior use > 0."
        ),
        prediction_time_rationale=(
            "Derived exclusively from the three D4-approved "
            "historical utilization sources."
        ),
        permitted_use=(
            "Eligible for governed downstream preprocessing."
        ),
    ),

    # --------------------------------------------------------
    # D6.15D — DIAGNOSIS FEATURES
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="diag_1_domain",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=("diag_1",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Deterministic ICD-9-CM diagnosis-domain mapping."
        ),
        prediction_time_rationale=(
            "Diagnosis source is clinically meaningful but D4 "
            "classified diag_1 as conditional because exact "
            "prediction-time availability is not timestamped."
        ),
        permitted_use=(
            "Excluded from the primary candidate feature set until "
            "prediction-time availability is explicitly resolved."
        ),
    ),

    FeatureSpecification(
        feature_name="diag_2_domain",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=("diag_2",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Deterministic ICD-9-CM diagnosis-domain mapping."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diag_2."
        ),
        permitted_use=(
            "Conditional feature; not authorized for primary model "
            "entry without governance resolution."
        ),
    ),

    FeatureSpecification(
        feature_name="diag_3_domain",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=("diag_3",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Deterministic ICD-9-CM diagnosis-domain mapping."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diag_3."
        ),
        permitted_use=(
            "Conditional feature; not authorized for primary model "
            "entry without governance resolution."
        ),
    ),

    FeatureSpecification(
        feature_name="any_diabetes_diagnosis",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=DIAGNOSIS_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that any diagnosis slot maps to "
            "the DIABETES domain."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diagnosis sources."
        ),
        permitted_use=(
            "Conditional feature; retain for governed analysis but "
            "exclude from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_circulatory_diagnosis",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=DIAGNOSIS_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that any diagnosis slot maps to "
            "the CIRCULATORY domain."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diagnosis sources."
        ),
        permitted_use=(
            "Conditional feature; retain for governed analysis but "
            "exclude from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_respiratory_diagnosis",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=DIAGNOSIS_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that any diagnosis slot maps to "
            "the RESPIRATORY domain."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diagnosis sources."
        ),
        permitted_use=(
            "Conditional feature; retain for governed analysis but "
            "exclude from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_genitourinary_diagnosis",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=DIAGNOSIS_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that any diagnosis slot maps to "
            "the GENITOURINARY domain."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diagnosis sources."
        ),
        permitted_use=(
            "Conditional feature; retain for governed analysis but "
            "exclude from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_injury_poisoning_diagnosis",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=DIAGNOSIS_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that any diagnosis slot maps to "
            "the INJURY_POISONING domain."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diagnosis sources."
        ),
        permitted_use=(
            "Conditional feature; retain for governed analysis but "
            "exclude from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="distinct_diagnosis_domain_count",
        feature_class=FEATURE_CLASS_DIAGNOSIS,
        source_columns=DIAGNOSIS_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Count of distinct known diagnosis domains across "
            "diag_1, diag_2, and diag_3."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diagnosis sources."
        ),
        permitted_use=(
            "Conditional feature; retain for governed analysis but "
            "exclude from primary model entry."
        ),
    ),

    # --------------------------------------------------------
    # D6.15E — GLYCEMIC FEATURES
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="a1c_result_category",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("A1Cresult",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Normalize A1C result to NOT_RECORDED, NORMAL, "
            "ABNORMAL, MARKEDLY_ELEVATED, or UNKNOWN."
        ),
        prediction_time_rationale=(
            "A1Cresult is D4-CONDITIONAL because the retrospective "
            "source does not provide result timestamps."
        ),
        permitted_use=(
            "Conditional; not authorized for primary model entry "
            "without prediction-time resolution."
        ),
    ),

    FeatureSpecification(
        feature_name="max_glucose_result_category",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("max_glu_serum",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Normalize maximum glucose result to governed "
            "categorical representation."
        ),
        prediction_time_rationale=(
            "max_glu_serum is D4-CONDITIONAL because result "
            "timing relative to prediction is unavailable."
        ),
        permitted_use=(
            "Conditional; not authorized for primary model entry "
            "without prediction-time resolution."
        ),
    ),

    FeatureSpecification(
        feature_name="a1c_tested",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("A1Cresult",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that an A1C result is recorded."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL A1Cresult."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="max_glucose_tested",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("max_glu_serum",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that a maximum glucose result "
            "is recorded."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL max_glu_serum."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_glycemic_test_recorded",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=(
            "A1Cresult",
            "max_glu_serum",
        ),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that either governed glycemic "
            "result field is recorded."
        ),
        prediction_time_rationale=(
            "Derived entirely from D4-CONDITIONAL laboratory "
            "result sources."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="a1c_abnormal",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("A1Cresult",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator for A1C >7 or >8."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL A1Cresult."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="a1c_markedly_elevated",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("A1Cresult",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator for A1C >8."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL A1Cresult."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="max_glucose_abnormal",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("max_glu_serum",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator for recorded glucose >200 or >300."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL max_glu_serum."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="max_glucose_markedly_elevated",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=("max_glu_serum",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator for recorded glucose >300."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL max_glu_serum."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_glycemic_abnormality",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=(
            "A1Cresult",
            "max_glu_serum",
        ),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator for any governed abnormal glycemic "
            "result."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL glycemic sources."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_marked_glycemic_abnormality",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=(
            "A1Cresult",
            "max_glu_serum",
        ),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator for any markedly elevated governed "
            "glycemic result."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL glycemic sources."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="glycemic_abnormality_count",
        feature_class=FEATURE_CLASS_GLYCEMIC,
        source_columns=(
            "A1Cresult",
            "max_glu_serum",
        ),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Count of abnormal governed glycemic result domains."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL glycemic sources."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    # --------------------------------------------------------
    # D6.15F — MEDICATION FEATURES
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="diabetes_medication_intensity",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=MEDICATION_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Count of medication fields in Steady, Up, or Down state."
        ),
        prediction_time_rationale=(
            "Medication states are D4-CONDITIONAL because exact "
            "prediction-time availability is not established."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_diabetes_medication_exposure",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=MEDICATION_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that at least one diabetes medication "
            "field records Steady, Up, or Down."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL medication sources."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="insulin_exposure",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=("insulin",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary insulin exposure indicator."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL insulin state."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="metformin_exposure",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=("metformin",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary metformin exposure indicator."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL metformin state."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="any_directional_medication_change",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=MEDICATION_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator that at least one medication field "
            "records Up or Down."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL medication states."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="directional_medication_change_count",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=MEDICATION_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Count of medication fields recording Up or Down."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL medication states."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="diabetes_medication_prescribed",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=("diabetesMed",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator: diabetesMed == Yes."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL diabetesMed."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    FeatureSpecification(
        feature_name="diabetes_medication_changed",
        feature_class=FEATURE_CLASS_MEDICATION,
        source_columns=("change",),
        disposition=D6_CONDITIONAL,
        transformation=(
            "Binary indicator: change == Ch."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL treatment-change source."
        ),
        permitted_use=(
            "Conditional feature; excluded from primary model entry."
        ),
    ),

    # --------------------------------------------------------
    # D6.15G — TREATMENT STRUCTURE
    # --------------------------------------------------------

    FeatureSpecification(
        feature_name="diabetes_treatment_structure",
        feature_class=FEATURE_CLASS_TREATMENT_STRUCTURE,
        source_columns=MEDICATION_COLUMNS,
        disposition=D6_CONDITIONAL,
        transformation=(
            "Deterministic treatment-structure classification: "
            "no recorded medication, insulin only, non-insulin "
            "monotherapy, insulin plus other, or multiple "
            "non-insulin medications."
        ),
        prediction_time_rationale=(
            "Derived from D4-CONDITIONAL medication-state sources."
        ),
        permitted_use=(
            "Conditional feature; retained for governed analysis "
            "but excluded from primary model entry."
        ),
    ),
)



# ============================================================
# D6.16 — FEATURE SPECIFICATION VALIDATION
# ============================================================

def validate_feature_specifications() -> dict[str, Any]:
    """
    Validate the initial D6 feature specification registry.
    """

    names = [
        specification.feature_name
        for specification
        in FEATURE_SPECIFICATIONS
    ]

    duplicate_names = (
        len(names)
        - len(set(names))
    )

    allowed_dispositions = {
        D6_CANDIDATE,
        D6_CONDITIONAL,
        D6_BLOCKED,
        D6_GOVERNANCE_ONLY,
        D6_TARGET_ONLY,
    }

    invalid_dispositions = [
        specification.feature_name
        for specification
        in FEATURE_SPECIFICATIONS
        if specification.disposition
        not in allowed_dispositions
    ]

    source_columns = {
        source_column
        for specification
        in FEATURE_SPECIFICATIONS
        for source_column
        in specification.source_columns
    }

    prohibited_sources = (
        source_columns
        & (
            HARD_BLOCKED_RAW_FEATURES
            | IDENTIFIER_COLUMNS
            | OUTCOME_COLUMNS
        )
    )

    governed_source_universe = (
        D4_APPROVED_SOURCE_FEATURES
        | D4_CONDITIONAL_SOURCE_FEATURES
    )

    unknown_governance_sources = (
        source_columns
        - governed_source_universe
        - HARD_BLOCKED_RAW_FEATURES
        - IDENTIFIER_COLUMNS
        - OUTCOME_COLUMNS
    )

    candidate_features_with_conditional_sources = [
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

    checks = {
        "feature_names_unique":
            duplicate_names == 0,

        "all_dispositions_valid":
            len(
                invalid_dispositions
            ) == 0,

        "no_hard_blocked_raw_sources":
            len(
                prohibited_sources
            ) == 0,

        "no_identifier_sources":
            len(
                source_columns
                & IDENTIFIER_COLUMNS
            ) == 0,

        "no_outcome_sources":
            len(
                source_columns
                & OUTCOME_COLUMNS
            ) == 0,

        "all_sources_have_d4_governance_disposition":
            len(unknown_governance_sources) == 0,

        "candidate_features_use_only_d4_approved_sources":
            len(candidate_features_with_conditional_sources) == 0,
    }

    return {
        "feature_count":
            len(
                FEATURE_SPECIFICATIONS
            ),

        "duplicate_feature_names":
            duplicate_names,

        "invalid_dispositions":
            invalid_dispositions,

        "prohibited_sources":
            sorted(
                prohibited_sources
            ),

        "unknown_governance_sources":
            sorted(
                unknown_governance_sources
            ),

        "candidate_features_with_conditional_sources":
            sorted(
                candidate_features_with_conditional_sources
            ),

        **checks,

        "validation_status":
            (
                "PASS"
                if all(
                    checks.values()
                )
                else "FAIL"
            ),
    }


# ============================================================
# D6.17 — LOAD D3 GOVERNED COHORT
# ============================================================

def load_d6_source_cohort() -> pd.DataFrame:
    """
    Load the D3 governed cohort and validate the minimum D6
    source contract.
    """

    if not GOVERNED_COHORT_PATH.exists():
        raise FileNotFoundError(
            "D3 governed modeling cohort not found: "
            f"{GOVERNED_COHORT_PATH}"
        )

    cohort = pd.read_parquet(
        GOVERNED_COHORT_PATH
    )

    missing_columns = (
        REQUIRED_D6_COLUMNS
        - set(
            cohort.columns
        )
    )

    if missing_columns:
        raise ValueError(
            "D6 source cohort is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if cohort.empty:
        raise ValueError(
            "D6 source cohort is empty."
        )

    if cohort[
        "encounter_id"
    ].duplicated().any():
        raise ValueError(
            "D6 source cohort contains duplicate encounter IDs."
        )

    if cohort[
        GROUP_COLUMN
    ].isna().any():
        raise ValueError(
            "D6 source cohort contains missing patient IDs."
        )

    return cohort


# ============================================================
# D6.18 — FROZEN D5 ASSIGNMENT INTEGRITY VERIFICATION
# ============================================================

def calculate_file_sha256(
    file_path: Path,
) -> str:
    """
    Calculate the SHA-256 checksum of a file without modifying it.
    """

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file_handle:
        for block in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            sha256.update(block)

    return sha256.hexdigest().upper()


def verify_frozen_split_assignment_checksum() -> str:
    """
    Verify that D6 is consuming the exact D5 split assignment
    frozen and approved at the D5 lifecycle gate.
    """

    if not FROZEN_SPLIT_ASSIGNMENT_PATH.exists():
        raise FileNotFoundError(
            "Frozen D5 patient split assignment not found: "
            f"{FROZEN_SPLIT_ASSIGNMENT_PATH}"
        )

    observed_checksum = calculate_file_sha256(
        FROZEN_SPLIT_ASSIGNMENT_PATH
    )

    if observed_checksum != EXPECTED_D5_ASSIGNMENT_SHA256:
        raise RuntimeError(
            "Frozen D5 split assignment checksum mismatch. "
            "D6 execution has been stopped to prevent use of "
            "an altered or non-authoritative patient partition. "
            f"Expected: {EXPECTED_D5_ASSIGNMENT_SHA256}; "
            f"Observed: {observed_checksum}"
        )

    return observed_checksum


# ============================================================
# D6.19 — LOAD FROZEN D5 SPLIT ASSIGNMENT
# ============================================================

def load_frozen_split_assignment() -> pd.DataFrame:
    """
    Load the authoritative D5 patient split assignment.

    D6 must consume this persisted assignment rather than
    generating a new split.
    """

    if not FROZEN_SPLIT_ASSIGNMENT_PATH.exists():
        raise FileNotFoundError(
            "Frozen D5 patient split assignment not found: "
            f"{FROZEN_SPLIT_ASSIGNMENT_PATH}"
        )

    verify_frozen_split_assignment_checksum()

    assignment = pd.read_csv(
        FROZEN_SPLIT_ASSIGNMENT_PATH
    )

    required_columns = {
        GROUP_COLUMN,
        "split",
    }

    missing_columns = (
        required_columns
        - set(
            assignment.columns
        )
    )

    if missing_columns:
        raise ValueError(
            "Frozen D5 assignment is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if assignment[
        GROUP_COLUMN
    ].duplicated().any():
        raise ValueError(
            "Frozen D5 assignment contains duplicate patients."
        )

    if assignment[
        "split"
    ].isna().any():
        raise ValueError(
            "Frozen D5 assignment contains missing split labels."
        )

    observed_labels = set(
        assignment[
            "split"
        ].unique()
    )

    required_labels = {
        TRAIN_LABEL,
        VALIDATION_LABEL,
        TEST_LABEL,
    }

    if observed_labels != required_labels:
        raise ValueError(
            "Frozen D5 assignment contains unexpected "
            f"split labels: {sorted(observed_labels)}"
        )

    return assignment


# ============================================================
# D6.20 — ATTACH FROZEN PARTITION MEMBERSHIP
# ============================================================

def attach_frozen_partition(
    cohort: pd.DataFrame,
    assignment: pd.DataFrame,
) -> pd.DataFrame:
    """
    Attach the authoritative D5 patient partition to the D3
    governed encounter-level cohort.
    """

    partitioned = cohort.merge(
        assignment[
            [
                GROUP_COLUMN,
                "split",
            ]
        ],
        on=GROUP_COLUMN,
        how="left",
        validate="many_to_one",
    )

    if partitioned[
        "split"
    ].isna().any():
        raise RuntimeError(
            "One or more D3 encounters do not have a frozen "
            "D5 partition assignment."
        )

    if len(partitioned) != len(cohort):
        raise RuntimeError(
            "Encounter count changed while attaching the "
            "frozen D5 partition."
        )

    return partitioned


# ============================================================
# D6.21 — DEVELOPMENT DATA ACCESSOR
# ============================================================

def get_development_data(
    partitioned_cohort: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return train + validation data only.

    This accessor intentionally excludes the locked test
    partition from D6 development analysis.
    """

    development = (
        partitioned_cohort.loc[
            partitioned_cohort[
                "split"
            ].isin(
                FEATURE_ENGINEERING_CONTRACT
                .development_partitions
            )
        ]
        .copy()
    )

    if TEST_LABEL in set(
        development[
            "split"
        ].unique()
    ):
        raise RuntimeError(
            "Locked test contamination detected in "
            "D6 development data."
        )

    return development


# ============================================================
# D6.22 — LOCKED TEST ACCESS PROTECTION
# ============================================================

def validate_locked_test_protection(
    development_data: pd.DataFrame,
) -> dict[str, Any]:
    """
    Verify that the D6 development frame contains no locked-test
    encounters.
    """

    test_encounters = int(
        (
            development_data[
                "split"
            ]
            == TEST_LABEL
        ).sum()
    )

    test_patients = int(
        development_data.loc[
            development_data[
                "split"
            ]
            == TEST_LABEL,
            GROUP_COLUMN,
        ].nunique()
    )

    checks = {
        "no_locked_test_encounters":
            test_encounters == 0,

        "no_locked_test_patients":
            test_patients == 0,

        "contract_prohibits_locked_test_development_use":
            (
                FEATURE_ENGINEERING_CONTRACT
                .locked_test_development_use_permitted
                is False
            ),

        "contract_prohibits_locked_test_feature_selection":
            (
                FEATURE_ENGINEERING_CONTRACT
                .feature_selection_using_locked_test_permitted
                is False
            ),
    }

    return {
        "locked_test_encounters_in_development":
            test_encounters,

        "locked_test_patients_in_development":
            test_patients,

        **checks,

        "validation_status":
            (
                "PASS"
                if all(
                    checks.values()
                )
                else "FAIL"
            ),
    }


# ============================================================
# D6.23 — BUILD D6 DEVELOPMENT FOUNDATION
# ============================================================

def build_d6_development_foundation():
    """
    Build the governed D6 development foundation.

    No engineered clinical features are created yet.
    This function validates the D6 contract and safely exposes
    train + validation data while protecting locked test data.
    """

    specification_validation = (
        validate_feature_specifications()
    )

    if (
        specification_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 feature specification validation failed."
        )

    cohort = (
        load_d6_source_cohort()
    )

    assignment = (
        load_frozen_split_assignment()
    )

    partitioned_cohort = (
        attach_frozen_partition(
            cohort,
            assignment,
        )
    )

    development_data = (
        get_development_data(
            partitioned_cohort
        )
    )

    locked_test_validation = (
        validate_locked_test_protection(
            development_data
        )
    )

    if (
        locked_test_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 locked-test protection failed."
        )

    return (
        cohort,
        assignment,
        partitioned_cohort,
        development_data,
        specification_validation,
        locked_test_validation,
    )

# ============================================================
# D6.24 — PRIOR UTILIZATION FEATURE ENGINEERING
# ============================================================

def engineer_prior_utilization_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Engineer deterministic prior-utilization features.

    Source variables:
    - number_outpatient
    - number_emergency
    - number_inpatient

    No fitting, imputation, scaling, encoding, or outcome
    information is used.

    Governance note:
    All three source utilization variables were D4-APPROVED.
    These deterministic transformations therefore remain eligible
    as D6 candidate features, subject to downstream preprocessing
    and modeling governance.
    """

    required_columns = {
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Prior-utilization engineering is missing "
            f"required columns: {sorted(missing_columns)}"
        )

    engineered = df.copy()

    # --------------------------------------------------------
    # D6.24A — PRIOR OUTPATIENT USE
    # --------------------------------------------------------

    engineered[
        "prior_outpatient_use"
    ] = (
        engineered[
            "number_outpatient"
        ] > 0
    ).astype("int8")

    # --------------------------------------------------------
    # D6.24B — PRIOR EMERGENCY USE
    # --------------------------------------------------------

    engineered[
        "prior_emergency_use"
    ] = (
        engineered[
            "number_emergency"
        ] > 0
    ).astype("int8")

    # --------------------------------------------------------
    # D6.24C — PRIOR INPATIENT USE
    # --------------------------------------------------------

    engineered[
        "prior_inpatient_use"
    ] = (
        engineered[
            "number_inpatient"
        ] > 0
    ).astype("int8")

    # --------------------------------------------------------
    # D6.24D — PRIOR UTILIZATION INTENSITY
    # --------------------------------------------------------

    engineered[
        "prior_utilization_intensity"
    ] = (
        engineered[
            "number_outpatient"
        ]
        + engineered[
            "number_emergency"
        ]
        + engineered[
            "number_inpatient"
        ]
    )

    # --------------------------------------------------------
    # D6.24E — PRIOR UTILIZATION DOMAIN COUNT
    # --------------------------------------------------------

    engineered[
        "prior_utilization_domain_count"
    ] = (
        engineered[
            [
                "number_outpatient",
                "number_emergency",
                "number_inpatient",
            ]
        ]
        .gt(0)
        .sum(axis=1)
        .astype("int8")
    )

    return engineered


# ============================================================
# D6.25 — PRIOR UTILIZATION TRANSFORMATION VALIDATION
# ============================================================

def validate_prior_utilization_features(
    source_df: pd.DataFrame,
    engineered_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate structural and mathematical integrity of the
    engineered prior-utilization feature family.
    """

    expected_features = {
        "prior_outpatient_use",
        "prior_emergency_use",
        "prior_inpatient_use",
        "prior_utilization_intensity",
        "prior_utilization_domain_count",
    }

    missing_engineered_features = (
        expected_features
        - set(engineered_df.columns)
    )

    row_count_preserved = (
        len(source_df)
        == len(engineered_df)
    )

    encounter_order_preserved = (
        source_df[
            "encounter_id"
        ]
        .reset_index(drop=True)
        .equals(
            engineered_df[
                "encounter_id"
            ]
            .reset_index(drop=True)
        )
    )

    outpatient_correct = bool(
        (
            engineered_df[
                "prior_outpatient_use"
            ]
            ==
            (
                source_df[
                    "number_outpatient"
                ] > 0
            ).astype("int8")
        ).all()
    )

    emergency_correct = bool(
        (
            engineered_df[
                "prior_emergency_use"
            ]
            ==
            (
                source_df[
                    "number_emergency"
                ] > 0
            ).astype("int8")
        ).all()
    )

    inpatient_correct = bool(
        (
            engineered_df[
                "prior_inpatient_use"
            ]
            ==
            (
                source_df[
                    "number_inpatient"
                ] > 0
            ).astype("int8")
        ).all()
    )

    expected_intensity = (
        source_df[
            "number_outpatient"
        ]
        + source_df[
            "number_emergency"
        ]
        + source_df[
            "number_inpatient"
        ]
    )

    intensity_correct = bool(
        (
            engineered_df[
                "prior_utilization_intensity"
            ]
            == expected_intensity
        ).all()
    )

    expected_domain_count = (
        source_df[
            [
                "number_outpatient",
                "number_emergency",
                "number_inpatient",
            ]
        ]
        .gt(0)
        .sum(axis=1)
        .astype("int8")
    )

    domain_count_correct = bool(
        (
            engineered_df[
                "prior_utilization_domain_count"
            ]
            == expected_domain_count
        ).all()
    )

    binary_features_valid = bool(
        all(
            set(
                engineered_df[
                    feature
                ].unique()
            ).issubset(
                {0, 1}
            )
            for feature in (
                "prior_outpatient_use",
                "prior_emergency_use",
                "prior_inpatient_use",
            )
        )
    )

    domain_count_range_valid = bool(
        engineered_df[
            "prior_utilization_domain_count"
        ]
        .between(
            0,
            3,
        )
        .all()
    )

    intensity_nonnegative = bool(
        (
            engineered_df[
                "prior_utilization_intensity"
            ] >= 0
        ).all()
    )

    checks = {
        "all_expected_features_created":
            len(
                missing_engineered_features
            ) == 0,

        "row_count_preserved":
            row_count_preserved,

        "encounter_order_preserved":
            encounter_order_preserved,

        "outpatient_indicator_correct":
            outpatient_correct,

        "emergency_indicator_correct":
            emergency_correct,

        "inpatient_indicator_correct":
            inpatient_correct,

        "utilization_intensity_correct":
            intensity_correct,

        "utilization_domain_count_correct":
            domain_count_correct,

        "binary_feature_domains_valid":
            binary_features_valid,

        "domain_count_range_valid":
            domain_count_range_valid,

        "utilization_intensity_nonnegative":
            intensity_nonnegative,
    }

    return {
        "engineered_feature_count":
            len(expected_features),

        "missing_engineered_features":
            sorted(
                missing_engineered_features
            ),

        **checks,

        "validation_status":
            (
                "PASS"
                if all(
                    checks.values()
                )
                else "FAIL"
            ),
    }


# ============================================================
# D6.26 — BUILD PRIOR UTILIZATION DEVELOPMENT FEATURES
# ============================================================

def build_prior_utilization_development_features():
    """
    Build the D6 development foundation and engineer the first
    governed clinical feature family.

    Locked test remains excluded.
    """

    (
        cohort,
        assignment,
        partitioned_cohort,
        development_data,
        specification_validation,
        locked_test_validation,
    ) = build_d6_development_foundation()

    engineered_development = (
        engineer_prior_utilization_features(
            development_data
        )
    )

    transformation_validation = (
        validate_prior_utilization_features(
            development_data,
            engineered_development,
        )
    )

    if (
        transformation_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 prior-utilization feature validation failed."
        )

    return (
        engineered_development,
        transformation_validation,
    )

# ============================================================
# D6.28 — ICD-9-CM DIAGNOSIS DOMAIN MAPPING
# ============================================================

def map_icd9_diagnosis_domain(
    value: Any,
) -> str:
    """
    Map a raw ICD-9-CM diagnosis value to a governed,
    clinically interpretable diagnosis domain.

    The mapping is deterministic and does not use outcome data.

    Diabetes codes (250.xx) receive their own domain because
    diabetes is the index disease context for this project.

    Supplementary V/E codes and unknown/unparseable values are
    retained explicitly rather than silently coerced.
    """

    if pd.isna(value):
        return "UNKNOWN"

    code = str(value).strip().upper()

    if code in {
        "",
        "?",
        "NAN",
        "NONE",
    }:
        return "UNKNOWN"

    # --------------------------------------------------------
    # Supplementary ICD-9-CM codes
    # --------------------------------------------------------

    if code.startswith("V"):
        return "SUPPLEMENTARY_V"

    if code.startswith("E"):
        return "EXTERNAL_CAUSE_E"

    # --------------------------------------------------------
    # Numeric ICD-9-CM codes
    # --------------------------------------------------------

    try:
        numeric_code = float(code)

    except (TypeError, ValueError):
        return "UNMAPPED"

    # Diabetes mellitus receives a dedicated domain.
    if 250 <= numeric_code < 251:
        return "DIABETES"

    if 1 <= numeric_code <= 139:
        return "INFECTIOUS_PARASITIC"

    if 140 <= numeric_code <= 239:
        return "NEOPLASMS"

    if 240 <= numeric_code <= 279:
        return "ENDOCRINE_METABOLIC"

    if 280 <= numeric_code <= 289:
        return "BLOOD"

    if 290 <= numeric_code <= 319:
        return "MENTAL"

    if 320 <= numeric_code <= 389:
        return "NERVOUS_SENSE"

    if 390 <= numeric_code <= 459:
        return "CIRCULATORY"

    if 460 <= numeric_code <= 519:
        return "RESPIRATORY"

    if 520 <= numeric_code <= 579:
        return "DIGESTIVE"

    if 580 <= numeric_code <= 629:
        return "GENITOURINARY"

    if 630 <= numeric_code <= 679:
        return "PREGNANCY_CHILDBIRTH"

    if 680 <= numeric_code <= 709:
        return "SKIN_SUBCUTANEOUS"

    if 710 <= numeric_code <= 739:
        return "MUSCULOSKELETAL"

    if 740 <= numeric_code <= 759:
        return "CONGENITAL"

    if 760 <= numeric_code <= 779:
        return "PERINATAL"

    if 780 <= numeric_code <= 799:
        return "SYMPTOMS_SIGNS"

    if 800 <= numeric_code <= 999:
        return "INJURY_POISONING"

    return "UNMAPPED"


# ============================================================
# D6.29 — DIAGNOSIS FEATURE ENGINEERING
# ============================================================

def engineer_diagnosis_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Engineer deterministic diagnosis-domain features from
    diag_1, diag_2, and diag_3.

    Raw diagnosis codes are not themselves authorized as direct
    model inputs by this transformation.
    """

    missing_columns = (
        set(DIAGNOSIS_COLUMNS)
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Diagnosis engineering is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    engineered = df.copy()

    # --------------------------------------------------------
    # D6.29A — DOMAIN REPRESENTATION FOR EACH DIAGNOSIS SLOT
    # --------------------------------------------------------

    for column in DIAGNOSIS_COLUMNS:

        engineered[
            f"{column}_domain"
        ] = (
            engineered[column]
            .map(
                map_icd9_diagnosis_domain
            )
        )

    domain_columns = [
        "diag_1_domain",
        "diag_2_domain",
        "diag_3_domain",
    ]

    # --------------------------------------------------------
    # D6.29B — ENCOUNTER-LEVEL CLINICAL DOMAIN INDICATORS
    # --------------------------------------------------------

    def any_domain(
        domain: str,
    ) -> pd.Series:

        return (
            engineered[
                domain_columns
            ]
            .eq(domain)
            .any(axis=1)
            .astype("int8")
        )

    engineered[
        "any_diabetes_diagnosis"
    ] = any_domain(
        "DIABETES"
    )

    engineered[
        "any_circulatory_diagnosis"
    ] = any_domain(
        "CIRCULATORY"
    )

    engineered[
        "any_respiratory_diagnosis"
    ] = any_domain(
        "RESPIRATORY"
    )

    engineered[
        "any_genitourinary_diagnosis"
    ] = any_domain(
        "GENITOURINARY"
    )

    engineered[
        "any_injury_poisoning_diagnosis"
    ] = any_domain(
        "INJURY_POISONING"
    )

    # --------------------------------------------------------
    # D6.29C — DISTINCT KNOWN DIAGNOSIS DOMAIN COUNT
    # --------------------------------------------------------

    def count_distinct_known_domains(
        row: pd.Series,
    ) -> int:

        excluded_domains = {
            "UNKNOWN",
            "UNMAPPED",
        }

        observed_domains = {
            value
            for value in row
            if value not in excluded_domains
        }

        return len(
            observed_domains
        )

    engineered[
        "distinct_diagnosis_domain_count"
    ] = (
        engineered[
            domain_columns
        ]
        .apply(
            count_distinct_known_domains,
            axis=1,
        )
        .astype("int8")
    )

    return engineered


# ============================================================
# D6.30 — DIAGNOSIS TRANSFORMATION VALIDATION
# ============================================================

def validate_diagnosis_features(
    source_df: pd.DataFrame,
    engineered_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate diagnosis-domain feature engineering.
    """

    domain_columns = {
        "diag_1_domain",
        "diag_2_domain",
        "diag_3_domain",
    }

    indicator_columns = {
        "any_diabetes_diagnosis",
        "any_circulatory_diagnosis",
        "any_respiratory_diagnosis",
        "any_genitourinary_diagnosis",
        "any_injury_poisoning_diagnosis",
    }

    expected_features = (
        domain_columns
        | indicator_columns
        | {
            "distinct_diagnosis_domain_count",
        }
    )

    missing_features = (
        expected_features
        - set(engineered_df.columns)
    )

    row_count_preserved = (
        len(source_df)
        == len(engineered_df)
    )

    encounter_order_preserved = (
        source_df[
            "encounter_id"
        ]
        .reset_index(drop=True)
        .equals(
            engineered_df[
                "encounter_id"
            ]
            .reset_index(drop=True)
        )
    )

    domain_values_nonmissing = bool(
        engineered_df[
            list(domain_columns)
        ]
        .notna()
        .all()
        .all()
    )

    indicators_binary = bool(
        all(
            set(
                engineered_df[
                    column
                ].unique()
            ).issubset(
                {0, 1}
            )
            for column
            in indicator_columns
        )
    )

    distinct_domain_range_valid = bool(
        engineered_df[
            "distinct_diagnosis_domain_count"
        ]
        .between(
            0,
            3,
        )
        .all()
    )

    # Explicit mapping sanity checks.
    mapping_sanity_checks = {
        "250.8":
            "DIABETES",

        "250.02":
            "DIABETES",

        "428":
            "CIRCULATORY",

        "486":
            "RESPIRATORY",

        "599":
            "GENITOURINARY",

        "820":
            "INJURY_POISONING",

        "V57":
            "SUPPLEMENTARY_V",

        "?":
            "UNKNOWN",
    }

    mapping_sanity_pass = bool(
        all(
            map_icd9_diagnosis_domain(
                raw_code
            )
            == expected_domain
            for raw_code, expected_domain
            in mapping_sanity_checks.items()
        )
    )

    checks = {
        "all_expected_features_created":
            len(
                missing_features
            ) == 0,

        "row_count_preserved":
            row_count_preserved,

        "encounter_order_preserved":
            encounter_order_preserved,

        "domain_values_nonmissing":
            domain_values_nonmissing,

        "indicator_features_binary":
            indicators_binary,

        "distinct_domain_count_range_valid":
            distinct_domain_range_valid,

        "mapping_sanity_checks_pass":
            mapping_sanity_pass,
    }

    return {
        "engineered_feature_count":
            len(expected_features),

        "missing_engineered_features":
            sorted(
                missing_features
            ),

        **checks,

        "validation_status":
            (
                "PASS"
                if all(
                    checks.values()
                )
                else "FAIL"
            ),
    }


# ============================================================
# D6.31 — BUILD DIAGNOSIS DEVELOPMENT FEATURES
# ============================================================

def build_diagnosis_development_features():
    """
    Build governed diagnosis features using development
    partitions only.

    Locked test remains excluded from D6 development analysis.
    """

    (
        cohort,
        assignment,
        partitioned_cohort,
        development_data,
        specification_validation,
        locked_test_validation,
    ) = build_d6_development_foundation()

    engineered_development = (
        engineer_diagnosis_features(
            development_data
        )
    )

    transformation_validation = (
        validate_diagnosis_features(
            development_data,
            engineered_development,
        )
    )

    if (
        transformation_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 diagnosis feature validation failed."
        )

    return (
        engineered_development,
        transformation_validation,
    )

# ============================================================
# D6.33 — GLYCEMIC RESULT NORMALIZATION
# ============================================================

def normalize_a1c_result(
    value: Any,
) -> str:
    """
    Normalize A1Cresult into a deterministic governed category.

    Source semantics:
    - Norm = recorded normal result
    - >7   = abnormal result
    - >8   = markedly elevated result
    - missing = no recorded result in the source field
    """

    if pd.isna(value):
        return "NOT_RECORDED"

    value = str(value).strip()

    mapping = {
        "Norm": "NORMAL",
        ">7": "ABNORMAL",
        ">8": "MARKEDLY_ELEVATED",
    }

    return mapping.get(
        value,
        "UNKNOWN",
    )


def normalize_max_glucose_result(
    value: Any,
) -> str:
    """
    Normalize max_glu_serum into a deterministic governed category.

    Source semantics:
    - Norm = recorded normal result
    - >200 = abnormal result
    - >300 = markedly elevated result
    - missing = no recorded result in the source field
    """

    if pd.isna(value):
        return "NOT_RECORDED"

    value = str(value).strip()

    mapping = {
        "Norm": "NORMAL",
        ">200": "ABNORMAL",
        ">300": "MARKEDLY_ELEVATED",
    }

    return mapping.get(
        value,
        "UNKNOWN",
    )


# ============================================================
# D6.34 — GLYCEMIC FEATURE ENGINEERING
# ============================================================

def engineer_glycemic_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Engineer deterministic glycemic-result features.

    IMPORTANT:
    Missing laboratory-result fields are represented as
    NOT_RECORDED rather than interpreted as normal.

    These source variables remain subject to D4/D6
    prediction-time governance because the retrospective
    dataset does not provide result timestamps.
    """

    required_columns = {
        "A1Cresult",
        "max_glu_serum",
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Glycemic engineering is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    engineered = df.copy()

    # --------------------------------------------------------
    # D6.34A — NORMALIZED RESULT CATEGORIES
    # --------------------------------------------------------

    engineered[
        "a1c_result_category"
    ] = (
        engineered[
            "A1Cresult"
        ]
        .map(
            normalize_a1c_result
        )
    )

    engineered[
        "max_glucose_result_category"
    ] = (
        engineered[
            "max_glu_serum"
        ]
        .map(
            normalize_max_glucose_result
        )
    )

    # --------------------------------------------------------
    # D6.34B — TEST / RESULT RECORDED INDICATORS
    # --------------------------------------------------------

    engineered[
        "a1c_tested"
    ] = (
        engineered[
            "a1c_result_category"
        ]
        .ne(
            "NOT_RECORDED"
        )
        .astype("int8")
    )

    engineered[
        "max_glucose_tested"
    ] = (
        engineered[
            "max_glucose_result_category"
        ]
        .ne(
            "NOT_RECORDED"
        )
        .astype("int8")
    )

    engineered[
        "any_glycemic_test_recorded"
    ] = (
        (
            engineered[
                "a1c_tested"
            ] == 1
        )
        |
        (
            engineered[
                "max_glucose_tested"
            ] == 1
        )
    ).astype("int8")

    # --------------------------------------------------------
    # D6.34C — ABNORMALITY INDICATORS
    # --------------------------------------------------------

    abnormal_categories = {
        "ABNORMAL",
        "MARKEDLY_ELEVATED",
    }

    engineered[
        "a1c_abnormal"
    ] = (
        engineered[
            "a1c_result_category"
        ]
        .isin(
            abnormal_categories
        )
        .astype("int8")
    )

    engineered[
        "a1c_markedly_elevated"
    ] = (
        engineered[
            "a1c_result_category"
        ]
        .eq(
            "MARKEDLY_ELEVATED"
        )
        .astype("int8")
    )

    engineered[
        "max_glucose_abnormal"
    ] = (
        engineered[
            "max_glucose_result_category"
        ]
        .isin(
            abnormal_categories
        )
        .astype("int8")
    )

    engineered[
        "max_glucose_markedly_elevated"
    ] = (
        engineered[
            "max_glucose_result_category"
        ]
        .eq(
            "MARKEDLY_ELEVATED"
        )
        .astype("int8")
    )

    # --------------------------------------------------------
    # D6.34D — COMBINED GLYCEMIC FEATURES
    # --------------------------------------------------------

    engineered[
        "any_glycemic_abnormality"
    ] = (
        (
            engineered[
                "a1c_abnormal"
            ] == 1
        )
        |
        (
            engineered[
                "max_glucose_abnormal"
            ] == 1
        )
    ).astype("int8")

    engineered[
        "any_marked_glycemic_abnormality"
    ] = (
        (
            engineered[
                "a1c_markedly_elevated"
            ] == 1
        )
        |
        (
            engineered[
                "max_glucose_markedly_elevated"
            ] == 1
        )
    ).astype("int8")

    engineered[
        "glycemic_abnormality_count"
    ] = (
        engineered[
            "a1c_abnormal"
        ]
        + engineered[
            "max_glucose_abnormal"
        ]
    ).astype("int8")

    return engineered


# ============================================================
# D6.35 — GLYCEMIC TRANSFORMATION VALIDATION
# ============================================================

def validate_glycemic_features(
    source_df: pd.DataFrame,
    engineered_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate structural and semantic integrity of the
    deterministic glycemic feature family.
    """

    expected_features = {
        "a1c_result_category",
        "max_glucose_result_category",
        "a1c_tested",
        "max_glucose_tested",
        "any_glycemic_test_recorded",
        "a1c_abnormal",
        "a1c_markedly_elevated",
        "max_glucose_abnormal",
        "max_glucose_markedly_elevated",
        "any_glycemic_abnormality",
        "any_marked_glycemic_abnormality",
        "glycemic_abnormality_count",
    }

    missing_features = (
        expected_features
        - set(engineered_df.columns)
    )

    binary_features = {
        "a1c_tested",
        "max_glucose_tested",
        "any_glycemic_test_recorded",
        "a1c_abnormal",
        "a1c_markedly_elevated",
        "max_glucose_abnormal",
        "max_glucose_markedly_elevated",
        "any_glycemic_abnormality",
        "any_marked_glycemic_abnormality",
    }

    binary_domains_valid = bool(
        all(
            set(
                engineered_df[
                    feature
                ].unique()
            ).issubset(
                {0, 1}
            )
            for feature
            in binary_features
        )
    )

    a1c_recorded_expected = int(
        source_df[
            "A1Cresult"
        ].notna().sum()
    )

    glucose_recorded_expected = int(
        source_df[
            "max_glu_serum"
        ].notna().sum()
    )

    checks = {
        "all_expected_features_created":
            len(
                missing_features
            ) == 0,

        "row_count_preserved":
            len(source_df)
            == len(engineered_df),

        "encounter_order_preserved":
            source_df[
                "encounter_id"
            ]
            .reset_index(drop=True)
            .equals(
                engineered_df[
                    "encounter_id"
                ]
                .reset_index(drop=True)
            ),

        "binary_feature_domains_valid":
            binary_domains_valid,

        "a1c_recorded_count_preserved":
            int(
                engineered_df[
                    "a1c_tested"
                ].sum()
            )
            == a1c_recorded_expected,

        "glucose_recorded_count_preserved":
            int(
                engineered_df[
                    "max_glucose_tested"
                ].sum()
            )
            == glucose_recorded_expected,

        "glycemic_abnormality_count_range_valid":
            bool(
                engineered_df[
                    "glycemic_abnormality_count"
                ]
                .between(
                    0,
                    2,
                )
                .all()
            ),

        "normal_a1c_not_abnormal":
            bool(
                (
                    engineered_df.loc[
                        engineered_df[
                            "a1c_result_category"
                        ]
                        == "NORMAL",
                        "a1c_abnormal",
                    ]
                    == 0
                ).all()
            ),

        "normal_glucose_not_abnormal":
            bool(
                (
                    engineered_df.loc[
                        engineered_df[
                            "max_glucose_result_category"
                        ]
                        == "NORMAL",
                        "max_glucose_abnormal",
                    ]
                    == 0
                ).all()
            ),

        "missing_a1c_not_interpreted_as_normal":
            bool(
                (
                    engineered_df.loc[
                        source_df[
                            "A1Cresult"
                        ].isna(),
                        "a1c_result_category",
                    ]
                    == "NOT_RECORDED"
                ).all()
            ),

        "missing_glucose_not_interpreted_as_normal":
            bool(
                (
                    engineered_df.loc[
                        source_df[
                            "max_glu_serum"
                        ].isna(),
                        "max_glucose_result_category",
                    ]
                    == "NOT_RECORDED"
                ).all()
            ),
    }

    return {
        "engineered_feature_count":
            len(expected_features),

        "missing_engineered_features":
            sorted(
                missing_features
            ),

        **checks,

        "validation_status":
            (
                "PASS"
                if all(
                    checks.values()
                )
                else "FAIL"
            ),
    }


# ============================================================
# D6.36 — BUILD GLYCEMIC DEVELOPMENT FEATURES
# ============================================================

def build_glycemic_development_features():
    """
    Build governed glycemic features on development data only.

    Locked test remains excluded.
    """

    (
        cohort,
        assignment,
        partitioned_cohort,
        development_data,
        specification_validation,
        locked_test_validation,
    ) = build_d6_development_foundation()

    engineered_development = (
        engineer_glycemic_features(
            development_data
        )
    )

    transformation_validation = (
        validate_glycemic_features(
            development_data,
            engineered_development,
        )
    )

    if (
        transformation_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 glycemic feature validation failed."
        )

    return (
        engineered_development,
        transformation_validation,
    )

# ============================================================
# D6.37 — MEDICATION STATE GOVERNANCE CONSTANTS
# ============================================================

MEDICATION_EXPOSURE_STATES = frozenset(
    {
        "Steady",
        "Up",
        "Down",
    }
)

MEDICATION_DIRECTIONAL_CHANGE_STATES = frozenset(
    {
        "Up",
        "Down",
    }
)


# ============================================================
# D6.38 — MEDICATION & TREATMENT FEATURE ENGINEERING
# ============================================================

def engineer_medication_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Engineer deterministic medication and treatment-structure
    features from the governed diabetes medication fields.

    Exposure:
        Steady, Up, or Down.

    Directional medication change:
        Up or Down.

    IMPORTANT:
    These medication source variables remain D4-CONDITIONAL
    because the retrospective dataset does not establish the
    exact prediction-time availability of each medication state.
    """

    required_columns = (
        set(MEDICATION_COLUMNS)
        | {
            "change",
            "diabetesMed",
        }
    )

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Medication engineering is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    engineered = df.copy()

    # --------------------------------------------------------
    # D6.38A — MEDICATION EXPOSURE MATRIX
    # --------------------------------------------------------

    exposure_matrix = (
        engineered[
            list(MEDICATION_COLUMNS)
        ]
        .isin(
            MEDICATION_EXPOSURE_STATES
        )
    )

    # Number of diabetes-medication fields showing exposure.
    engineered[
        "diabetes_medication_intensity"
    ] = (
        exposure_matrix
        .sum(axis=1)
        .astype("int8")
    )

    engineered[
        "any_diabetes_medication_exposure"
    ] = (
        engineered[
            "diabetes_medication_intensity"
        ]
        .gt(0)
        .astype("int8")
    )

    # --------------------------------------------------------
    # D6.38B — SPECIFIC MEDICATION EXPOSURE
    # --------------------------------------------------------

    engineered[
        "insulin_exposure"
    ] = (
        engineered[
            "insulin"
        ]
        .isin(
            MEDICATION_EXPOSURE_STATES
        )
        .astype("int8")
    )

    engineered[
        "metformin_exposure"
    ] = (
        engineered[
            "metformin"
        ]
        .isin(
            MEDICATION_EXPOSURE_STATES
        )
        .astype("int8")
    )

    # --------------------------------------------------------
    # D6.38C — DIRECTIONAL MEDICATION CHANGE
    # --------------------------------------------------------

    directional_change_matrix = (
        engineered[
            list(MEDICATION_COLUMNS)
        ]
        .isin(
            MEDICATION_DIRECTIONAL_CHANGE_STATES
        )
    )

    engineered[
        "any_directional_medication_change"
    ] = (
        directional_change_matrix
        .any(axis=1)
        .astype("int8")
    )

    engineered[
        "directional_medication_change_count"
    ] = (
        directional_change_matrix
        .sum(axis=1)
        .astype("int8")
    )

    # --------------------------------------------------------
    # D6.38D — SOURCE-LEVEL TREATMENT INDICATORS
    # --------------------------------------------------------

    engineered[
        "diabetes_medication_prescribed"
    ] = (
        engineered[
            "diabetesMed"
        ]
        .eq("Yes")
        .astype("int8")
    )

    engineered[
        "diabetes_medication_changed"
    ] = (
        engineered[
            "change"
        ]
        .eq("Ch")
        .astype("int8")
    )

    # --------------------------------------------------------
    # D6.38E — TREATMENT STRUCTURE
    # --------------------------------------------------------

    engineered[
        "diabetes_treatment_structure"
    ] = np.select(
        [
            engineered[
                "diabetes_medication_intensity"
            ].eq(0),

            (
                engineered[
                    "diabetes_medication_intensity"
                ].eq(1)
                &
                engineered[
                    "insulin_exposure"
                ].eq(1)
            ),

            (
                engineered[
                    "diabetes_medication_intensity"
                ].eq(1)
                &
                engineered[
                    "insulin_exposure"
                ].eq(0)
            ),

            (
                engineered[
                    "diabetes_medication_intensity"
                ].gt(1)
                &
                engineered[
                    "insulin_exposure"
                ].eq(1)
            ),

            (
                engineered[
                    "diabetes_medication_intensity"
                ].gt(1)
                &
                engineered[
                    "insulin_exposure"
                ].eq(0)
            ),
        ],
        [
            "NO_RECORDED_DIABETES_MEDICATION",
            "INSULIN_ONLY",
            "NON_INSULIN_MONOTHERAPY",
            "INSULIN_PLUS_OTHER",
            "MULTIPLE_NON_INSULIN",
        ],
        default="UNCLASSIFIED",
    )

    return engineered


# ============================================================
# D6.39 — MEDICATION TRANSFORMATION VALIDATION
# ============================================================

def validate_medication_features(
    source_df: pd.DataFrame,
    engineered_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate deterministic medication and treatment-structure
    engineering.
    """

    expected_features = {
        "diabetes_medication_intensity",
        "any_diabetes_medication_exposure",
        "insulin_exposure",
        "metformin_exposure",
        "any_directional_medication_change",
        "directional_medication_change_count",
        "diabetes_medication_prescribed",
        "diabetes_medication_changed",
        "diabetes_treatment_structure",
    }

    missing_features = (
        expected_features
        - set(engineered_df.columns)
    )

    binary_features = {
        "any_diabetes_medication_exposure",
        "insulin_exposure",
        "metformin_exposure",
        "any_directional_medication_change",
        "diabetes_medication_prescribed",
        "diabetes_medication_changed",
    }

    binary_domains_valid = bool(
        all(
            set(
                engineered_df[
                    feature
                ].unique()
            ).issubset(
                {0, 1}
            )
            for feature
            in binary_features
        )
    )

    expected_exposure_matrix = (
        source_df[
            list(MEDICATION_COLUMNS)
        ]
        .isin(
            MEDICATION_EXPOSURE_STATES
        )
    )

    expected_intensity = (
        expected_exposure_matrix
        .sum(axis=1)
        .astype("int8")
    )

    expected_directional_matrix = (
        source_df[
            list(MEDICATION_COLUMNS)
        ]
        .isin(
            MEDICATION_DIRECTIONAL_CHANGE_STATES
        )
    )

    expected_directional_count = (
        expected_directional_matrix
        .sum(axis=1)
        .astype("int8")
    )

    allowed_treatment_structures = {
        "NO_RECORDED_DIABETES_MEDICATION",
        "INSULIN_ONLY",
        "NON_INSULIN_MONOTHERAPY",
        "INSULIN_PLUS_OTHER",
        "MULTIPLE_NON_INSULIN",
    }

    checks = {
        "all_expected_features_created":
            len(
                missing_features
            ) == 0,

        "row_count_preserved":
            len(source_df)
            == len(engineered_df),

        "encounter_order_preserved":
            source_df[
                "encounter_id"
            ]
            .reset_index(drop=True)
            .equals(
                engineered_df[
                    "encounter_id"
                ]
                .reset_index(drop=True)
            ),

        "binary_feature_domains_valid":
            binary_domains_valid,

        "medication_intensity_correct":
            bool(
                (
                    engineered_df[
                        "diabetes_medication_intensity"
                    ]
                    == expected_intensity
                ).all()
            ),

        "directional_change_count_correct":
            bool(
                (
                    engineered_df[
                        "directional_medication_change_count"
                    ]
                    == expected_directional_count
                ).all()
            ),

        "insulin_exposure_correct":
            bool(
                (
                    engineered_df[
                        "insulin_exposure"
                    ]
                    ==
                    source_df[
                        "insulin"
                    ]
                    .isin(
                        MEDICATION_EXPOSURE_STATES
                    )
                    .astype("int8")
                ).all()
            ),

        "metformin_exposure_correct":
            bool(
                (
                    engineered_df[
                        "metformin_exposure"
                    ]
                    ==
                    source_df[
                        "metformin"
                    ]
                    .isin(
                        MEDICATION_EXPOSURE_STATES
                    )
                    .astype("int8")
                ).all()
            ),

        "prescribed_indicator_matches_source":
            bool(
                (
                    engineered_df[
                        "diabetes_medication_prescribed"
                    ]
                    ==
                    source_df[
                        "diabetesMed"
                    ]
                    .eq("Yes")
                    .astype("int8")
                ).all()
            ),

        "change_indicator_matches_source":
            bool(
                (
                    engineered_df[
                        "diabetes_medication_changed"
                    ]
                    ==
                    source_df[
                        "change"
                    ]
                    .eq("Ch")
                    .astype("int8")
                ).all()
            ),

        "treatment_structure_domain_valid":
            set(
                engineered_df[
                    "diabetes_treatment_structure"
                ].unique()
            ).issubset(
                allowed_treatment_structures
            ),

        "medication_intensity_nonnegative":
            bool(
                (
                    engineered_df[
                        "diabetes_medication_intensity"
                    ]
                    >= 0
                ).all()
            ),

        "directional_change_count_nonnegative":
            bool(
                (
                    engineered_df[
                        "directional_medication_change_count"
                    ]
                    >= 0
                ).all()
            ),
    }

    return {
        "engineered_feature_count":
            len(expected_features),

        "missing_engineered_features":
            sorted(
                missing_features
            ),

        **checks,

        "validation_status":
            (
                "PASS"
                if all(
                    checks.values()
                )
                else "FAIL"
            ),
    }


# ============================================================
# D6.40 — BUILD MEDICATION DEVELOPMENT FEATURES
# ============================================================

def build_medication_development_features():
    """
    Build governed medication/treatment features using
    development partitions only.

    Locked test remains excluded.
    """

    (
        cohort,
        assignment,
        partitioned_cohort,
        development_data,
        specification_validation,
        locked_test_validation,
    ) = build_d6_development_foundation()

    engineered_development = (
        engineer_medication_features(
            development_data
        )
    )

    transformation_validation = (
        validate_medication_features(
            development_data,
            engineered_development,
        )
    )

    if (
        transformation_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D6 medication feature validation failed."
        )

    return (
        engineered_development,
        transformation_validation,
    )

# ============================================================
# D6.41 — GOVERNED FEATURE LISTS
# ============================================================

def get_governed_d6_feature_lists() -> dict[str, list[str]]:
    """
    Return the authoritative D6 feature lists derived directly
    from FEATURE_SPECIFICATIONS.

    The registry is the system of record. Feature lists must not
    be maintained independently because that could allow registry
    and modeling inputs to diverge.
    """

    validation = validate_feature_specifications()

    if validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D6 feature specification registry failed governance "
            "validation. Feature lists cannot be constructed."
        )

    candidate_features = [
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
        if specification.disposition == D6_CANDIDATE
    ]

    conditional_features = [
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
        if specification.disposition == D6_CONDITIONAL
    ]

    all_model_features = (
        candidate_features
        + conditional_features
    )

    if len(all_model_features) != len(set(all_model_features)):
        raise RuntimeError(
            "Duplicate feature names detected in governed D6 "
            "feature lists."
        )

    return {
        "candidate_features": candidate_features,
        "conditional_features": conditional_features,
        "all_registered_model_features": all_model_features,
    }


# ============================================================
# D6.42 — DIRECT GOVERNED SOURCE FEATURES
# ============================================================

DIRECT_GOVERNED_FEATURES = (
    "race",
    "gender",
    "age",
    "admission_type_id",
    "admission_source_id",
)


def validate_direct_governed_features(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate direct D4-approved demographic and admission-context
    features before they enter the combined D6 development matrix.
    """

    missing_columns = [
        column
        for column in DIRECT_GOVERNED_FEATURES
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing direct governed D6 source columns: "
            f"{missing_columns}"
        )

    candidate_registry = {
        specification.feature_name
        for specification in FEATURE_SPECIFICATIONS
        if specification.disposition == D6_CANDIDATE
    }

    unregistered_direct_features = sorted(
        set(DIRECT_GOVERNED_FEATURES)
        - candidate_registry
    )

    non_d4_approved_direct_features = sorted(
        set(DIRECT_GOVERNED_FEATURES)
        - D4_APPROVED_SOURCE_FEATURES
    )

    checks = {
        "all_direct_columns_present":
            len(missing_columns) == 0,

        "all_direct_features_registered_as_candidates":
            len(unregistered_direct_features) == 0,

        "all_direct_features_d4_approved":
            len(non_d4_approved_direct_features) == 0,
    }

    validation_status = (
        "PASS"
        if all(checks.values())
        else "FAIL"
    )

    return {
        "checks": checks,
        "missing_columns": missing_columns,
        "unregistered_direct_features":
            unregistered_direct_features,
        "non_d4_approved_direct_features":
            non_d4_approved_direct_features,
        "validation_status": validation_status,
    }


# ============================================================
# D6.43 — COMBINED DEVELOPMENT FEATURE ENGINEERING
# ============================================================

def build_combined_d6_development_features(
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Build the complete governed D6 development feature matrix.

    IMPORTANT
    ---------
    Development data contains TRAIN + VALIDATION only.

    The frozen TEST partition is not loaded into feature-design
    decisions and is not used to decide which transformations,
    features, or representations are retained.

    CONDITIONAL features are engineered and preserved for governed
    analysis, but remain excluded from the primary candidate model
    pathway unless formally resolved by later governance action.
    """

    # --------------------------------------------------------
    # Load governed D6 development foundation
    # --------------------------------------------------------

    (
        cohort,
        assignment,
        partitioned_cohort,
        development_df,
        specification_validation,
        locked_test_validation,
    ) = build_d6_development_foundation()

    if specification_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D6 feature specification validation failed."
        )

    if locked_test_validation["validation_status"] != "PASS":
        raise RuntimeError(
            "D6 locked-test protection validation failed."
        )

    original_row_count = len(development_df)
    original_encounter_order = (
        development_df["encounter_id"]
        .copy()
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Direct governed features
    # --------------------------------------------------------

    direct_audit = validate_direct_governed_features(
        development_df
    )

    if direct_audit["validation_status"] != "PASS":
        raise RuntimeError(
            "Direct governed feature validation failed."
        )

    # --------------------------------------------------------
    # Prior utilization
    # --------------------------------------------------------

    engineered_df = engineer_prior_utilization_features(
        development_df
    )

    prior_audit = validate_prior_utilization_features(
        development_df,
        engineered_df,
    )

    if prior_audit["validation_status"] != "PASS":
        raise RuntimeError(
            "Prior-utilization feature validation failed."
        )

    # --------------------------------------------------------
    # Diagnosis
    # --------------------------------------------------------

    diagnosis_source_df = engineered_df.copy()

    engineered_df = engineer_diagnosis_features(
        engineered_df
    )

    diagnosis_audit = validate_diagnosis_features(
        diagnosis_source_df,
        engineered_df,
    )

    if diagnosis_audit["validation_status"] != "PASS":
        raise RuntimeError(
            "Diagnosis feature validation failed."
        )

    # --------------------------------------------------------
    # Glycemic
    # --------------------------------------------------------

    glycemic_source_df = engineered_df.copy()

    engineered_df = engineer_glycemic_features(
        engineered_df
    )

    glycemic_audit = validate_glycemic_features(
        glycemic_source_df,
        engineered_df,
    )

    if glycemic_audit["validation_status"] != "PASS":
        raise RuntimeError(
            "Glycemic feature validation failed."
        )

    # --------------------------------------------------------
    # Medication / treatment structure
    # --------------------------------------------------------

    medication_source_df = engineered_df.copy()

    engineered_df = engineer_medication_features(
        engineered_df
    )

    medication_audit = validate_medication_features(
        medication_source_df,
        engineered_df,
    )

    if medication_audit["validation_status"] != "PASS":
        raise RuntimeError(
            "Medication feature validation failed."
        )

    # --------------------------------------------------------
    # Governed feature lists
    # --------------------------------------------------------

    feature_lists = get_governed_d6_feature_lists()

    candidate_features = (
        feature_lists["candidate_features"]
    )

    conditional_features = (
        feature_lists["conditional_features"]
    )

    registered_features = (
        feature_lists["all_registered_model_features"]
    )

    missing_engineered_features = sorted(
        set(registered_features)
        - set(engineered_df.columns)
    )

    if missing_engineered_features:
        raise RuntimeError(
            "Registered D6 features are missing from the combined "
            "engineered dataframe: "
            f"{missing_engineered_features}"
        )

# ============================================================
# D6.43A — GOVERNANCE & TRACEABILITY COLUMNS
# ============================================================

    governance_columns = [
        "encounter_id",
        GROUP_COLUMN,
        TARGET_COLUMN,
        "split",
   ]
    missing_governance_columns = [
        column
        for column in governance_columns
        if column not in engineered_df.columns
    ]

    if missing_governance_columns:
        raise RuntimeError(
            "Required governance columns missing from combined "
            "D6 dataframe: "
            f"{missing_governance_columns}"
        )

    # --------------------------------------------------------
    # Construct authoritative D6 matrix
    # --------------------------------------------------------

    output_columns = (
        governance_columns
        + candidate_features
        + conditional_features
    )

    combined_df = (
        engineered_df[
            output_columns
        ]
        .copy()
    )

    # --------------------------------------------------------
    # Structural integrity checks
    # --------------------------------------------------------

    final_encounter_order = (
        combined_df["encounter_id"]
        .copy()
        .reset_index(drop=True)
    )

    row_count_preserved = (
        len(combined_df)
        == original_row_count
    )

    encounter_order_preserved = (
        original_encounter_order.equals(
            final_encounter_order
        )
    )

    duplicate_encounter_ids = int(
        combined_df["encounter_id"]
        .duplicated()
        .sum()
    )

    candidate_conditional_overlap = sorted(
        set(candidate_features)
        & set(conditional_features)
    )

    prohibited_model_features = sorted(
        (
            set(candidate_features)
            | set(conditional_features)
        )
        & (
            HARD_BLOCKED_RAW_FEATURES
            | IDENTIFIER_COLUMNS
            | OUTCOME_COLUMNS
        )
    )

    candidate_features_with_conditional_lineage = [
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

    checks = {
        "feature_specification_pass":
            specification_validation["validation_status"] == "PASS",

        "locked_test_protection_pass":
            locked_test_validation["validation_status"] == "PASS",

        "direct_features_pass":
            direct_audit["validation_status"] == "PASS",

        "prior_utilization_pass":
            prior_audit["validation_status"] == "PASS",

        "diagnosis_pass":
            diagnosis_audit["validation_status"] == "PASS",

        "glycemic_pass":
            glycemic_audit["validation_status"] == "PASS",

        "medication_pass":
            medication_audit["validation_status"] == "PASS",

        "row_count_preserved":
            row_count_preserved,

        "encounter_order_preserved":
            encounter_order_preserved,

        "encounter_ids_unique":
            duplicate_encounter_ids == 0,

        "candidate_conditional_sets_disjoint":
            len(candidate_conditional_overlap) == 0,

        "no_prohibited_model_features":
            len(prohibited_model_features) == 0,

        "candidate_features_have_no_conditional_lineage":
            len(
                candidate_features_with_conditional_lineage
            ) == 0,

        "registered_feature_count_matches_matrix":
            len(registered_features) == 40,

        "candidate_feature_count_matches_registry":
            len(candidate_features) == 10,

        "conditional_feature_count_matches_registry":
            len(conditional_features) == 30,
    }

    validation_status = (
        "PASS"
        if all(checks.values())
        else "FAIL"
    )

    audit = {
        "development_encounters":
            int(len(combined_df)),

        "candidate_feature_count":
            int(len(candidate_features)),

        "conditional_feature_count":
            int(len(conditional_features)),

        "registered_feature_count":
            int(len(registered_features)),

        "candidate_features":
            candidate_features,

        "conditional_features":
            conditional_features,

        "candidate_conditional_overlap":
            candidate_conditional_overlap,

        "prohibited_model_features":
            prohibited_model_features,

        "candidate_features_with_conditional_lineage":
            candidate_features_with_conditional_lineage,

        "duplicate_encounter_ids":
            duplicate_encounter_ids,

        "checks":
            checks,

        "validation_status":
            validation_status,
    }

    if validation_status != "PASS":
        raise RuntimeError(
            "Combined D6 development feature matrix failed "
            f"governance validation: {audit}"
        )

    return combined_df, audit


# ============================================================
# D6.44 — PRIMARY CANDIDATE DEVELOPMENT MATRIX
# ============================================================

def build_primary_candidate_development_matrix(
) -> tuple[pd.DataFrame, pd.Series, dict[str, Any]]:
    """
    Return the governed primary development feature matrix X,
    target y, and D6 audit.

    Only D6-CANDIDATE features are exposed as model inputs.

    CONDITIONAL features, identifiers, governance columns,
    outcome representations, and D4-blocked variables are not
    included in X.
    """

    combined_df, audit = (
        build_combined_d6_development_features()
    )

    feature_lists = get_governed_d6_feature_lists()

    candidate_features = (
        feature_lists["candidate_features"]
    )

    X = combined_df[
        candidate_features
    ].copy()

    y = combined_df[
        TARGET_COLUMN
    ].copy()

    prohibited_in_X = sorted(
        set(X.columns)
        & (
            HARD_BLOCKED_RAW_FEATURES
            | IDENTIFIER_COLUMNS
            | OUTCOME_COLUMNS
            | set(
                feature_lists[
                    "conditional_features"
                ]
            )
        )
    )

    if prohibited_in_X:
        raise RuntimeError(
            "Primary D6 candidate matrix contains prohibited "
            f"features: {prohibited_in_X}"
        )

    if len(X) != len(y):
        raise RuntimeError(
            "Primary D6 X/y row-count mismatch."
        )

    primary_audit = {
        **audit,
        "primary_X_rows": int(len(X)),
        "primary_X_columns": int(X.shape[1]),
        "target_rows": int(len(y)),
        "prohibited_features_in_primary_X":
            prohibited_in_X,
        "primary_matrix_validation_status":
            "PASS",
    }

    return X, y, primary_audit

# ============================================================
# D6.45 — COMMAND-LINE FOUNDATION AUDIT
# ============================================================

if __name__ == "__main__":

    (
        cohort,
        assignment,
        partitioned_cohort,
        development_data,
        specification_validation,
        locked_test_validation,
    ) = build_d6_development_foundation()

    print(
        "=" * 72
    )
    print(
        "D6 — GOVERNED FEATURE ENGINEERING FOUNDATION"
    )
    print(
        "=" * 72
    )

    print()
    print(
        "FEATURE ENGINEERING CONTRACT"
    )
    print(
        "-" * 72
    )

    print(
        f"prediction_point: "
        f"{FEATURE_ENGINEERING_CONTRACT.prediction_point}"
    )

    print(
        f"grouping_key: "
        f"{FEATURE_ENGINEERING_CONTRACT.grouping_key}"
    )

    print(
        f"target: "
        f"{FEATURE_ENGINEERING_CONTRACT.target}"
    )

    print(
        f"development_partitions: "
        f"{FEATURE_ENGINEERING_CONTRACT.development_partitions}"
    )

    print(
        f"locked_test_partition: "
        f"{FEATURE_ENGINEERING_CONTRACT.locked_test_partition}"
    )

    print(
        f"locked_test_development_use_permitted: "
        f"{FEATURE_ENGINEERING_CONTRACT.locked_test_development_use_permitted}"
    )

    print()
    print(
        "SOURCE & PARTITION COUNTS"
    )
    print(
        "-" * 72
    )

    print(
        f"source_encounters: "
        f"{len(cohort):,}"
    )

    print(
        f"source_patients: "
        f"{cohort[GROUP_COLUMN].nunique():,}"
    )

    print(
        f"frozen_assignment_patients: "
        f"{len(assignment):,}"
    )

    print(
        f"development_encounters: "
        f"{len(development_data):,}"
    )

    print(
        f"development_patients: "
        f"{development_data[GROUP_COLUMN].nunique():,}"
    )

    print()
    print(
        "PARTITION COUNTS"
    )
    print(
        "-" * 72
    )

    partition_counts = (
        partitioned_cohort[
            "split"
        ]
        .value_counts()
        .reindex(
            [
                TRAIN_LABEL,
                VALIDATION_LABEL,
                TEST_LABEL,
            ]
        )
    )

    print(
        partition_counts.to_string()
    )

    print()
    print(
        "INITIAL FEATURE SPECIFICATION REGISTRY"
    )
    print(
        "-" * 72
    )

    print(
        f"registered_features: "
        f"{specification_validation['feature_count']}"
    )

    print(
        f"duplicate_feature_names: "
        f"{specification_validation['duplicate_feature_names']}"
    )

    print(
        f"prohibited_sources: "
        f"{specification_validation['prohibited_sources']}"
    )

    print(
        f"specification_validation_status: "
        f"{specification_validation['validation_status']}"
    )

    print()
    print(
        "LOCKED TEST PROTECTION"
    )
    print(
        "-" * 72
    )

    print(
        f"locked_test_encounters_in_development: "
        f"{locked_test_validation['locked_test_encounters_in_development']}"
    )

    print(
        f"locked_test_patients_in_development: "
        f"{locked_test_validation['locked_test_patients_in_development']}"
    )

    print(
        f"locked_test_validation_status: "
        f"{locked_test_validation['validation_status']}"
    )

    print()
    print(
        "=" * 72
    )
    print(
        "D6 governed feature engineering foundation: PASS"
    )
    print(
        "Locked test: PROTECTED FROM DEVELOPMENT ANALYSIS"
    )
    print(
        "Preprocessing fitting: NOT PERMITTED IN D6"
    )
    print(
        "Model training: NOT PERMITTED IN D6"
    )
    print(
        "=" * 72
    )