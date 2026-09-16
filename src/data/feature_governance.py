# ============================================================
# D4 — LEAKAGE & FEATURE GOVERNANCE
# ============================================================
"""
Govern feature eligibility for the Diabetes Readmission
Clinical AI system.

D4 establishes the prediction-time contract and the governance
rules that determine whether a variable may legitimately enter
model development.

Core principle:
    A feature is eligible only if its value is legitimately
    available at or before the defined prediction timestamp.

No model training occurs in D4.
"""

# ============================================================
# D4.1 — IMPORTS
# ============================================================

from dataclasses import dataclass, asdict
from typing import Any

import pandas as pd

from src.data.validation import load_raw_dataset
from src.data.cohort import (
    SOURCE_TARGET_COLUMN,
    DERIVED_TARGET_COLUMN,
    PATIENT_ID_COLUMN,
    ENCOUNTER_ID_COLUMN,
    build_governed_modeling_cohort,
)


# ============================================================
# D4.2 — GOVERNANCE DISPOSITIONS
# ============================================================

APPROVED = "APPROVED"
CONDITIONAL = "CONDITIONAL"
BLOCKED = "BLOCKED"
IDENTIFIER_ONLY = "IDENTIFIER/GOVERNANCE-ONLY"
TARGET_ONLY = "TARGET/OUTCOME"

VALID_GOVERNANCE_DISPOSITIONS = frozenset(
    {
        APPROVED,
        CONDITIONAL,
        BLOCKED,
        IDENTIFIER_ONLY,
        TARGET_ONLY,
    }
)


# ============================================================
# D4.3 — LEAKAGE TAXONOMY
# ============================================================

LEAKAGE_TAXONOMY = {
    "TARGET_LEAKAGE": (
        "Variable directly contains, derives from, or reveals "
        "the prediction outcome."
    ),
    "POST_PREDICTION_LEAKAGE": (
        "Variable is generated or finalized after the defined "
        "prediction timestamp."
    ),
    "TEMPORAL_LEAKAGE": (
        "Variable uses information from the future relative to "
        "the prediction timestamp."
    ),
    "AGGREGATION_LEAKAGE": (
        "Variable summarizes information across a period that "
        "extends beyond the prediction timestamp."
    ),
    "IDENTIFIER_LEAKAGE": (
        "Identifier may enable memorization, linkage, or "
        "patient/encounter-specific shortcut learning."
    ),
    "PROXY_LEAKAGE": (
        "Variable may indirectly encode the target or a "
        "post-prediction event strongly enough to create an "
        "invalid predictive shortcut."
    ),
    "SEMANTIC_AMBIGUITY": (
        "The dataset does not establish with sufficient "
        "certainty when or how the variable became available."
    ),
}


# ============================================================
# D4.4 — CLINICAL DECISION POINT
# ============================================================

@dataclass(frozen=True)
class ClinicalDecisionPoint:
    """
    Formal intended use and prediction-time definition.
    """

    population: str
    setting: str
    primary_users: tuple[str, ...]
    decision: str
    prediction_timestamp: str
    prediction_horizon: str
    outcome: str
    intended_action: str


CLINICAL_DECISION_POINT = ClinicalDecisionPoint(
    population=(
        "Eligible adult inpatient encounters involving patients "
        "with diabetes represented in the governed cohort."
    ),
    setting=(
        "Acute-care inpatient hospitalization."
    ),
    primary_users=(
        "Discharge planning team",
        "Care management team",
        "Treating clinicians",
    ),
    decision=(
        "Identify patients who may warrant enhanced "
        "readmission-prevention planning before discharge."
    ),
    prediction_timestamp=(
        "Before discharge, at the point when the model output "
        "would be used to support discharge-planning decisions."
    ),
    prediction_horizon=(
        "Readmission occurring within 30 days after discharge."
    ),
    outcome=(
        "Binary 30-day readmission outcome: "
        "readmitted_30d = 1 when readmitted == '<30'; "
        "otherwise 0."
    ),
    intended_action=(
        "Support prioritization for clinician-reviewed "
        "readmission-prevention interventions. The model does "
        "not autonomously determine discharge or treatment."
    ),
)


# ============================================================
# D4.5 — PREDICTION-TIME CONTRACT
# ============================================================

PREDICTION_TIME_CONTRACT = {
    "core_rule": (
        "A modeling feature must represent information that is "
        "legitimately available at or before the defined "
        "prediction timestamp."
    ),

    "historical_information": (
        "Information from prior encounters may be eligible when "
        "it can be established that it occurred before the "
        "current prediction timestamp."
    ),

    "current_encounter_information": (
        "Current-encounter variables require evidence that the "
        "value would already be known at the prediction "
        "timestamp and does not summarize information generated "
        "after that point."
    ),

    "retrospective_totals": (
        "Final encounter-level totals must not be assumed to be "
        "prediction-time-safe merely because they appear in the "
        "source dataset."
    ),

    "outcome_information": (
        "The source outcome and all deterministic or indirect "
        "representations of the outcome are prohibited as "
        "modeling features."
    ),

    "identifiers": (
        "Patient and encounter identifiers are retained for "
        "governance, traceability, patient-level splitting, and "
        "audit purposes only. They are not modeling features."
    ),

    "ambiguous_timing": (
        "When the availability timestamp cannot be established "
        "with sufficient confidence, the feature must not be "
        "automatically approved. It is classified as "
        "CONDITIONAL or BLOCKED pending evidence."
    ),

    "locked_test": (
        "No feature-governance decision may be informed by "
        "performance on the locked test partition."
    ),
}


# ============================================================
# D4.6 — FEATURE GOVERNANCE RECORD
# ============================================================

@dataclass(frozen=True)
class FeatureGovernanceRecord:
    """
    Auditable governance record for one source variable.
    """

    feature: str
    source_dtype: str
    governance_disposition: str
    feature_role: str
    prediction_time_status: str
    leakage_risk: str
    rationale: str
    permitted_use: str


# ============================================================
# D4.7 — SOURCE FEATURE INVENTORY
# ============================================================

def build_source_feature_inventory(
    governed_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Inventory every column available after D3.

    This function does NOT approve features. It creates the
    source inventory that will undergo feature-by-feature
    governance assessment.
    """

    records = []

    for position, column in enumerate(
        governed_df.columns,
        start=1,
    ):
        records.append(
            {
                "source_position": position,
                "feature": column,
                "source_dtype": str(
                    governed_df[column].dtype
                ),
                "missing_count": int(
                    governed_df[column].isna().sum()
                ),
                "missing_pct": round(
                    float(
                        governed_df[column]
                        .isna()
                        .mean()
                        * 100
                    ),
                    4,
                ),
                "unique_values": int(
                    governed_df[column]
                    .nunique(dropna=True)
                ),
            }
        )

    return pd.DataFrame(records)


# ============================================================
# D4.8 — NON-MODELING FIELD GOVERNANCE
# ============================================================

def govern_reserved_fields(
    inventory: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply deterministic governance to fields whose roles are
    already established independently of predictive modeling.

    Remaining clinical/source variables are intentionally left
    UNASSESSED until the formal feature-by-feature review.
    """

    governed = inventory.copy()

    governed["governance_disposition"] = "UNASSESSED"
    governed["feature_role"] = "UNASSESSED"
    governed["prediction_time_status"] = "UNASSESSED"
    governed["leakage_risk"] = "UNASSESSED"
    governed["rationale"] = "Pending D4 feature-level assessment."
    governed["permitted_use"] = "Not yet authorized for modeling."

    # --------------------------------------------------------
    # Patient identifier
    # --------------------------------------------------------

    patient_mask = (
        governed["feature"]
        == PATIENT_ID_COLUMN
    )

    governed.loc[
        patient_mask,
        "governance_disposition",
    ] = IDENTIFIER_ONLY

    governed.loc[
        patient_mask,
        "feature_role",
    ] = "Patient identifier"

    governed.loc[
        patient_mask,
        "prediction_time_status",
    ] = "AVAILABLE BUT PROHIBITED AS MODEL INPUT"

    governed.loc[
        patient_mask,
        "leakage_risk",
    ] = "IDENTIFIER_LEAKAGE"

    governed.loc[
        patient_mask,
        "rationale",
    ] = (
        "Required for patient-level splitting, traceability, "
        "and audit; prohibited as a predictive feature."
    )

    governed.loc[
        patient_mask,
        "permitted_use",
    ] = (
        "Patient-level splitting, governance, audit, and "
        "traceability only."
    )

    # --------------------------------------------------------
    # Encounter identifier
    # --------------------------------------------------------

    encounter_mask = (
        governed["feature"]
        == ENCOUNTER_ID_COLUMN
    )

    governed.loc[
        encounter_mask,
        "governance_disposition",
    ] = IDENTIFIER_ONLY

    governed.loc[
        encounter_mask,
        "feature_role",
    ] = "Encounter identifier"

    governed.loc[
        encounter_mask,
        "prediction_time_status",
    ] = "AVAILABLE BUT PROHIBITED AS MODEL INPUT"

    governed.loc[
        encounter_mask,
        "leakage_risk",
    ] = "IDENTIFIER_LEAKAGE"

    governed.loc[
        encounter_mask,
        "rationale",
    ] = (
        "Required for encounter traceability and audit; "
        "prohibited as a predictive feature."
    )

    governed.loc[
        encounter_mask,
        "permitted_use",
    ] = (
        "Governance, integrity checking, audit, and "
        "traceability only."
    )

    # --------------------------------------------------------
    # Raw source outcome
    # --------------------------------------------------------

    source_target_mask = (
        governed["feature"]
        == SOURCE_TARGET_COLUMN
    )

    governed.loc[
        source_target_mask,
        "governance_disposition",
    ] = TARGET_ONLY

    governed.loc[
        source_target_mask,
        "feature_role",
    ] = "Source outcome"

    governed.loc[
        source_target_mask,
        "prediction_time_status",
    ] = "POST-OUTCOME"

    governed.loc[
        source_target_mask,
        "leakage_risk",
    ] = "TARGET_LEAKAGE"

    governed.loc[
        source_target_mask,
        "rationale",
    ] = (
        "Source readmission outcome directly reveals the "
        "prediction target."
    )

    governed.loc[
        source_target_mask,
        "permitted_use",
    ] = "Outcome engineering and audit only."

    # --------------------------------------------------------
    # Engineered binary outcome
    # --------------------------------------------------------

    derived_target_mask = (
        governed["feature"]
        == DERIVED_TARGET_COLUMN
    )

    governed.loc[
        derived_target_mask,
        "governance_disposition",
    ] = TARGET_ONLY

    governed.loc[
        derived_target_mask,
        "feature_role",
    ] = "Engineered outcome"

    governed.loc[
        derived_target_mask,
        "prediction_time_status",
    ] = "POST-OUTCOME"

    governed.loc[
        derived_target_mask,
        "leakage_risk",
    ] = "TARGET_LEAKAGE"

    governed.loc[
        derived_target_mask,
        "rationale",
    ] = (
        "Formal binary prediction target; never eligible as "
        "a model input."
    )

    governed.loc[
        derived_target_mask,
        "permitted_use",
    ] = (
        "Supervised learning label and evaluation only."
    )

    return governed


# ============================================================
# D4.9 — FOUNDATIONAL GOVERNANCE VALIDATION
# ============================================================

def validate_foundational_feature_governance(
    governed_inventory: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate the D4 foundational governance state before
    feature-by-feature clinical assessment begins.
    """

    required_fields = {
        PATIENT_ID_COLUMN,
        ENCOUNTER_ID_COLUMN,
        SOURCE_TARGET_COLUMN,
        DERIVED_TARGET_COLUMN,
    }

    observed_fields = set(
        governed_inventory["feature"]
    )

    missing_required_fields = sorted(
        required_fields
        - observed_fields
    )

    identifier_rows = governed_inventory[
        governed_inventory[
            "feature"
        ].isin(
            {
                PATIENT_ID_COLUMN,
                ENCOUNTER_ID_COLUMN,
            }
        )
    ]

    target_rows = governed_inventory[
        governed_inventory[
            "feature"
        ].isin(
            {
                SOURCE_TARGET_COLUMN,
                DERIVED_TARGET_COLUMN,
            }
        )
    ]

    unassessed_count = int(
        (
            governed_inventory[
                "governance_disposition"
            ]
            == "UNASSESSED"
        ).sum()
    )

    checks = {
        "required_reserved_fields_present":
            len(missing_required_fields) == 0,

        "identifiers_governance_only":
            (
                len(identifier_rows) == 2
                and (
                    identifier_rows[
                        "governance_disposition"
                    ]
                    == IDENTIFIER_ONLY
                ).all()
            ),

        "targets_outcome_only":
            (
                len(target_rows) == 2
                and (
                    target_rows[
                        "governance_disposition"
                    ]
                    == TARGET_ONLY
                ).all()
            ),

        "clinical_features_not_prematurely_approved":
            (
                governed_inventory[
                    "governance_disposition"
                ]
                .isin(
                    {
                        APPROVED,
                        CONDITIONAL,
                        BLOCKED,
                    }
                )
                .sum()
                == 0
            ),
    }

    return {
        "total_inventory_fields":
            int(len(governed_inventory)),

        "reserved_fields_governed":
            int(
                (
                    governed_inventory[
                        "governance_disposition"
                    ]
                    != "UNASSESSED"
                ).sum()
            ),

        "unassessed_fields":
            unassessed_count,

        "missing_required_fields":
            missing_required_fields,

        "validation_checks":
            checks,

        "validation_status":
            (
                "PASS"
                if all(checks.values())
                else "FAIL"
            ),
    }


# ============================================================
# D4.10 — BUILD FOUNDATIONAL D4 STATE
# ============================================================

def build_foundational_feature_governance():
    """
    Reconstruct the governed D3 cohort and establish the D4
    source inventory plus deterministic reserved-field
    governance.
    """

    raw_df = load_raw_dataset()

    governed_df, d3_validation = (
        build_governed_modeling_cohort(
            raw_df
        )
    )

    if d3_validation[
        "validation_status"
    ] != "PASS":
        raise RuntimeError(
            "D3 governed cohort validation failed. "
            "D4 cannot proceed."
        )

    inventory = (
        build_source_feature_inventory(
            governed_df
        )
    )

    governed_inventory = (
        govern_reserved_fields(
            inventory
        )
    )

    validation = (
        validate_foundational_feature_governance(
            governed_inventory
        )
    )

    if validation[
        "validation_status"
    ] != "PASS":
        raise RuntimeError(
            "D4 foundational governance validation failed."
        )

    return (
        governed_df,
        governed_inventory,
        validation,
    )


# ============================================================
# D4.12 — SOURCE FEATURE GOVERNANCE POLICY
# ============================================================

# ------------------------------------------------------------
# D4.12A — APPROVED BASELINE FEATURES
# ------------------------------------------------------------
#
# These variables represent demographic, admission-context, or
# prior-utilization information that can reasonably precede the
# defined discharge-planning prediction point.
#
# Approval here means eligible for later preprocessing/feature
# engineering. It does NOT mean the raw representation must be
# used directly.

APPROVED_SOURCE_FEATURES = frozenset(
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


# ------------------------------------------------------------
# D4.12B — CONDITIONAL FEATURES
# ------------------------------------------------------------
#
# These variables may contain clinically useful information
# available before discharge, but the retrospective dataset does
# not provide sufficient timestamp granularity to prove that the
# final recorded value was available at the intended prediction
# moment.
#
# They therefore require governed reconstruction, transformation,
# or explicit prediction-time justification before modeling.

CONDITIONAL_SOURCE_FEATURES = frozenset(
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


# ------------------------------------------------------------
# D4.12C — BLOCKED RETROSPECTIVE / END-OF-ENCOUNTER FEATURES
# ------------------------------------------------------------
#
# These fields represent discharge-state information or
# cumulative encounter totals whose final values can incorporate
# information generated throughout the hospitalization.
#
# Without timestamp-safe reconstruction, they are blocked from
# the primary model.

BLOCKED_SOURCE_FEATURES = frozenset(
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
# D4.13 — FEATURE-LEVEL GOVERNANCE APPLICATION
# ============================================================

def apply_feature_level_governance(
    governed_inventory: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply the formal D4 governance policy to all remaining
    source features.

    Reserved identifiers and outcomes retain their previously
    assigned deterministic governance dispositions.
    """

    governed = governed_inventory.copy()

    # --------------------------------------------------------
    # Approved features
    # --------------------------------------------------------

    approved_mask = (
        governed["feature"]
        .isin(APPROVED_SOURCE_FEATURES)
    )

    governed.loc[
        approved_mask,
        "governance_disposition",
    ] = APPROVED

    governed.loc[
        approved_mask,
        "feature_role",
    ] = "Prediction-time candidate"

    governed.loc[
        approved_mask,
        "prediction_time_status",
    ] = "AVAILABLE AT OR BEFORE PREDICTION"

    governed.loc[
        approved_mask,
        "leakage_risk",
    ] = "LOW"

    governed.loc[
        approved_mask,
        "rationale",
    ] = (
        "Represents demographic, admission-context, or prior "
        "utilization information considered available before "
        "the discharge-planning prediction point."
    )

    governed.loc[
        approved_mask,
        "permitted_use",
    ] = (
        "Eligible for governed preprocessing and feature "
        "engineering."
    )

    # --------------------------------------------------------
    # Conditional features
    # --------------------------------------------------------

    conditional_mask = (
        governed["feature"]
        .isin(CONDITIONAL_SOURCE_FEATURES)
    )

    governed.loc[
        conditional_mask,
        "governance_disposition",
    ] = CONDITIONAL

    governed.loc[
        conditional_mask,
        "feature_role",
    ] = "Conditionally eligible clinical/source feature"

    governed.loc[
        conditional_mask,
        "prediction_time_status",
    ] = "TIMING NOT FULLY ESTABLISHED"

    governed.loc[
        conditional_mask,
        "leakage_risk",
    ] = "SEMANTIC_AMBIGUITY"

    governed.loc[
        conditional_mask,
        "rationale",
    ] = (
        "Potentially available before discharge, but the "
        "retrospective dataset does not establish sufficient "
        "timestamp granularity to prove availability of the "
        "final recorded value at the intended prediction time."
    )

    governed.loc[
        conditional_mask,
        "permitted_use",
    ] = (
        "Requires governed transformation, reconstruction, or "
        "explicit prediction-time justification before model "
        "entry."
    )

    # --------------------------------------------------------
    # Blocked features
    # --------------------------------------------------------

    blocked_mask = (
        governed["feature"]
        .isin(BLOCKED_SOURCE_FEATURES)
    )

    governed.loc[
        blocked_mask,
        "governance_disposition",
    ] = BLOCKED

    governed.loc[
        blocked_mask,
        "feature_role",
    ] = "Retrospective/end-of-encounter field"

    governed.loc[
        blocked_mask,
        "prediction_time_status",
    ] = "NOT PROVEN SAFE AT PREDICTION TIME"

    governed.loc[
        blocked_mask,
        "leakage_risk",
    ] = "POST_PREDICTION_OR_AGGREGATION_LEAKAGE"

    governed.loc[
        blocked_mask,
        "rationale",
    ] = (
        "Final recorded value may depend on information "
        "accumulated through the hospitalization or finalized "
        "at discharge; timestamp-safe availability is not "
        "established."
    )

    governed.loc[
        blocked_mask,
        "permitted_use",
    ] = (
        "Excluded from the primary model unless a future "
        "timestamp-safe version is explicitly reconstructed "
        "and separately governed."
    )

    return governed


# ============================================================
# D4.14 — COMPLETE FEATURE GOVERNANCE VALIDATION
# ============================================================

def validate_complete_feature_governance(
    governed_inventory: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate that every source field has received exactly one
    formal D4 governance disposition.
    """

    disposition_counts = (
        governed_inventory[
            "governance_disposition"
        ]
        .value_counts()
        .to_dict()
    )

    unassessed = governed_inventory[
        governed_inventory[
            "governance_disposition"
        ]
        == "UNASSESSED"
    ]

    invalid = governed_inventory[
        ~governed_inventory[
            "governance_disposition"
        ].isin(
            VALID_GOVERNANCE_DISPOSITIONS
        )
    ]

    classified_source_features = (
        APPROVED_SOURCE_FEATURES
        | CONDITIONAL_SOURCE_FEATURES
        | BLOCKED_SOURCE_FEATURES
    )

    overlap_checks = {
        "approved_conditional_disjoint":
            APPROVED_SOURCE_FEATURES.isdisjoint(
                CONDITIONAL_SOURCE_FEATURES
            ),

        "approved_blocked_disjoint":
            APPROVED_SOURCE_FEATURES.isdisjoint(
                BLOCKED_SOURCE_FEATURES
            ),

        "conditional_blocked_disjoint":
            CONDITIONAL_SOURCE_FEATURES.isdisjoint(
                BLOCKED_SOURCE_FEATURES
            ),
    }

    expected_non_reserved_count = (
        len(governed_inventory) - 4
    )

    checks = {
        "no_unassessed_features":
            len(unassessed) == 0,

        "no_invalid_dispositions":
            len(invalid) == 0,

        "all_non_reserved_features_classified":
            len(classified_source_features)
            == expected_non_reserved_count,

        "feature_policy_sets_disjoint":
            all(overlap_checks.values()),

        "all_inventory_fields_governed":
            sum(disposition_counts.values())
            == len(governed_inventory),
    }

    return {
        "total_fields":
            int(len(governed_inventory)),

        "approved_features":
            int(
                disposition_counts.get(
                    APPROVED,
                    0,
                )
            ),

        "conditional_features":
            int(
                disposition_counts.get(
                    CONDITIONAL,
                    0,
                )
            ),

        "blocked_features":
            int(
                disposition_counts.get(
                    BLOCKED,
                    0,
                )
            ),

        "identifier_only_fields":
            int(
                disposition_counts.get(
                    IDENTIFIER_ONLY,
                    0,
                )
            ),

        "target_only_fields":
            int(
                disposition_counts.get(
                    TARGET_ONLY,
                    0,
                )
            ),

        "unassessed_features":
            int(len(unassessed)),

        "validation_checks":
            checks,

        "validation_status":
            (
                "PASS"
                if all(checks.values())
                else "FAIL"
            ),
    }


# ============================================================
# D4.15 — BUILD COMPLETE FEATURE GOVERNANCE STATE
# ============================================================

def build_complete_feature_governance():
    """
    Build the complete D4 feature-governance state.
    """

    (
        governed_df,
        foundational_inventory,
        foundational_validation,
    ) = build_foundational_feature_governance()

    if foundational_validation[
        "validation_status"
    ] != "PASS":
        raise RuntimeError(
            "Foundational D4 governance failed."
        )

    governed_inventory = (
        apply_feature_level_governance(
            foundational_inventory
        )
    )

    validation = (
        validate_complete_feature_governance(
            governed_inventory
        )
    )

    if validation[
        "validation_status"
    ] != "PASS":
        raise RuntimeError(
            "Complete D4 feature governance validation failed."
        )

    return (
        governed_df,
        governed_inventory,
        validation,
    )

# ============================================================
# D4.16 — COMMAND-LINE VALIDATION
# ============================================================

if __name__ == "__main__":

    (
        governed_df,
        governed_inventory,
        validation,
    ) = build_complete_feature_governance()

    print("=" * 70)
    print(
        "D4 — LEAKAGE & FEATURE GOVERNANCE"
    )
    print("=" * 70)

    # ========================================================
    # D4.16A — CLINICAL DECISION POINT
    # ========================================================

    print()
    print(
        "D4.4 — CLINICAL DECISION POINT"
    )
    print("-" * 70)

    for key, value in asdict(
        CLINICAL_DECISION_POINT
    ).items():
        print(f"{key}: {value}")

    # ========================================================
    # D4.16B — PREDICTION-TIME CONTRACT
    # ========================================================

    print()
    print(
        "D4.5 — PREDICTION-TIME CONTRACT"
    )
    print("-" * 70)

    for key, value in (
        PREDICTION_TIME_CONTRACT.items()
    ):
        print(f"{key}: {value}")

    # ========================================================
    # D4.16C — SOURCE FEATURE INVENTORY
    # ========================================================

    print()
    print(
        "D4.7 — SOURCE FEATURE INVENTORY"
    )
    print("-" * 70)

    print(
        f"total_fields: "
        f"{len(governed_inventory)}"
    )

    print(
        f"source_encounters: "
        f"{len(governed_df)}"
    )

    # ========================================================
    # D4.16D — COMPLETE GOVERNANCE SUMMARY
    # ========================================================

    print()
    print(
        "D4.14 — COMPLETE FEATURE GOVERNANCE"
    )
    print("-" * 70)

    print(
        f"APPROVED: "
        f"{validation['approved_features']}"
    )

    print(
        f"CONDITIONAL: "
        f"{validation['conditional_features']}"
    )

    print(
        f"BLOCKED: "
        f"{validation['blocked_features']}"
    )

    print(
        f"IDENTIFIER/GOVERNANCE-ONLY: "
        f"{validation['identifier_only_fields']}"
    )

    print(
        f"TARGET/OUTCOME: "
        f"{validation['target_only_fields']}"
    )

    print(
        f"UNASSESSED: "
        f"{validation['unassessed_features']}"
    )

    print(
        f"validation_status: "
        f"{validation['validation_status']}"
    )

    # ========================================================
    # D4.16E — VALIDATION CHECKS
    # ========================================================

    print()
    print(
        "VALIDATION CHECKS"
    )
    print("-" * 70)

    for key, value in (
        validation[
            "validation_checks"
        ].items()
    ):
        print(f"{key}: {value}")

    # ========================================================
    # D4.16F — FEATURE GOVERNANCE REGISTER
    # ========================================================

    print()
    print(
        "D4 — FEATURE GOVERNANCE REGISTER"
    )
    print("-" * 70)

    display_columns = [
        "source_position",
        "feature",
        "governance_disposition",
        "prediction_time_status",
        "leakage_risk",
    ]

    print(
        governed_inventory[
            display_columns
        ].to_string(index=False)
    )

    # ========================================================
    # D4.16G — FINAL D4 VALIDATION RESULT
    # ========================================================

    print()
    print("=" * 70)
    print(
        "D4 complete feature governance: "
        f"{validation['validation_status']}"
    )
    print("=" * 70)

    print(
        "All 51 source/governance fields have received "
        "a formal D4 disposition."
    )

    print(
        "No model training has occurred."
    )

    print(
        "Conditional features remain unauthorized for direct "
        "model entry pending governed transformation or "
        "prediction-time justification."
    )

    print(
        "Blocked features remain excluded from the primary "
        "model unless timestamp-safe versions are explicitly "
        "reconstructed and separately governed."
    )

    print(
        "Locked-test evaluation has not occurred."
    )

    print("=" * 70)