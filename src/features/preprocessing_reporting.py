# ============================================================
# D7 — GOVERNED PREPROCESSING EVIDENCE & REPORTING
# ============================================================
"""
Generate the auditable evidence package for D7 Governed
Preprocessing.

This module converts the fitted D7 preprocessing state into
version-controlled governance evidence.

The fitted binary itself remains a local/runtime artifact.
Its checksum, schema, learned state, governance controls, and
reproducibility evidence are recorded here.

D7 does NOT:
- train predictive models;
- tune hyperparameters;
- select clinical thresholds;
- access the locked test partition;
- authorize clinical deployment.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.features.preprocessing import (
    PROJECT_ROOT,
    D6_DEVELOPMENT_ARTIFACT,
    EXPECTED_D6_DEVELOPMENT_SHA256,
    PRIMARY_CANDIDATE_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    SOURCE_UNKNOWN_CATEGORY_VALUES,
    CANONICAL_UNKNOWN_CATEGORY,
    D7_PREPROCESSING_CONTRACT,
    D7_PREPROCESSOR_PATH,
    D7_TRANSFORMED_SCHEMA_PATH,
    EXPECTED_D7_RAW_FEATURE_COUNT,
    EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
    EXPECTED_D7_TRAIN_ENCOUNTERS,
    EXPECTED_D7_VALIDATION_ENCOUNTERS,
    TRAIN_LABEL,
    VALIDATION_LABEL,
    LOCKED_TEST_LABEL,
    calculate_file_sha256,
    build_persisted_d7_primary_preprocessor,
)


# ============================================================
# D7.R01 — EVIDENCE OUTPUT PATHS
# ============================================================

D7_MANIFEST_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "manifests"
    / "D7_preprocessing_manifest.yaml"
)

D7_CONTRACT_REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "governance"
    / "D7_preprocessing_contract.md"
)

D7_GATE_DECISION_PATH = (
    PROJECT_ROOT
    / "reports"
    / "governance"
    / "D7_preprocessing_gate_decision.md"
)

D7_SUMMARY_TABLE_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D7_preprocessing_summary.csv"
)

D7_FEATURE_REGISTRY_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D7_transformed_feature_registry.csv"
)

D7_UNKNOWN_AUDIT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D7_unknown_category_audit.csv"
)

D7_LEARNED_STATE_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D7_learned_preprocessing_state.csv"
)


# ============================================================
# D7.R02 — PREPARE EVIDENCE DIRECTORIES
# ============================================================

def prepare_d7_evidence_directories() -> None:
    """
    Create all version-controlled D7 evidence directories.
    """

    for path in (
        D7_MANIFEST_PATH,
        D7_CONTRACT_REPORT_PATH,
        D7_GATE_DECISION_PATH,
        D7_SUMMARY_TABLE_PATH,
        D7_FEATURE_REGISTRY_PATH,
        D7_UNKNOWN_AUDIT_PATH,
        D7_LEARNED_STATE_PATH,
    ):
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# D7.R03 — BUILD PREPROCESSING SUMMARY
# ============================================================

def build_d7_preprocessing_summary(
    workflow: dict[str, Any],
) -> pd.DataFrame:
    """
    Build a compact quantitative D7 governance summary.
    """

    fitted_bundle = workflow["fitted_bundle"]
    persistence = workflow["persistence_result"]
    validation = workflow[
        "persistence_validation"
    ]

    boundary = fitted_bundle[
        "boundary_validation"
    ]

    preprocessing = fitted_bundle[
        "preprocessing_validation"
    ]

    records = [
        {
            "control":
                "raw_primary_feature_count",
            "value":
                EXPECTED_D7_RAW_FEATURE_COUNT,
        },
        {
            "control":
                "transformed_feature_count",
            "value":
                persistence[
                    "transformed_feature_count"
                ],
        },
        {
            "control":
                "train_encounters",
            "value":
                persistence[
                    "train_encounters"
                ],
        },
        {
            "control":
                "validation_encounters",
            "value":
                persistence[
                    "validation_encounters"
                ],
        },
        {
            "control":
                "patient_overlap_count",
            "value":
                boundary[
                    "patient_overlap_count"
                ],
        },
        {
            "control":
                "encounter_overlap_count",
            "value":
                boundary[
                    "encounter_overlap_count"
                ],
        },
        {
            "control":
                "train_missing_after_transform",
            "value":
                preprocessing[
                    "train_missing_values"
                ],
        },
        {
            "control":
                "validation_missing_after_transform",
            "value":
                preprocessing[
                    "validation_missing_values"
                ],
        },
        {
            "control":
                "train_nonfinite_after_transform",
            "value":
                preprocessing[
                    "train_nonfinite_values"
                ],
        },
        {
            "control":
                "validation_nonfinite_after_transform",
            "value":
                preprocessing[
                    "validation_nonfinite_values"
                ],
        },
        {
            "control":
                "train_reproduction_exact",
            "value":
                validation[
                    "train_reproduction_exact"
                ],
        },
        {
            "control":
                "validation_reproduction_exact",
            "value":
                validation[
                    "validation_reproduction_exact"
                ],
        },
        {
            "control":
                "preprocessor_checksum_verified",
            "value":
                validation[
                    "preprocessor_checksum_verified"
                ],
        },
        {
            "control":
                "schema_checksum_verified",
            "value":
                validation[
                    "schema_checksum_verified"
                ],
        },
        {
            "control":
                "fit_partition",
            "value":
                TRAIN_LABEL,
        },
        {
            "control":
                "validation_contributed_to_fit",
            "value":
                False,
        },
        {
            "control":
                "locked_test_accessed",
            "value":
                False,
        },
        {
            "control":
                "overall_validation_status",
            "value":
                validation[
                    "validation_status"
                ],
        },
    ]

    return pd.DataFrame(records)


# ============================================================
# D7.R04 — BUILD TRANSFORMED FEATURE REGISTRY
# ============================================================

def build_d7_transformed_feature_registry(
    workflow: dict[str, Any],
) -> pd.DataFrame:
    """
    Register every final model-ready D7 feature in authoritative
    transformed order.
    """

    fitted_bundle = workflow["fitted_bundle"]

    feature_names = fitted_bundle[
        "transformed_feature_names"
    ]

    records = []

    for position, transformed_name in enumerate(
        feature_names,
        start=1,
    ):
        if transformed_name.startswith(
            "categorical__"
        ):
            pathway = "categorical"

            raw_component = (
                transformed_name
                .replace(
                    "categorical__",
                    "",
                    1,
                )
            )

            source_feature = next(
                (
                    feature
                    for feature
                    in CATEGORICAL_FEATURES
                    if raw_component.startswith(
                        f"{feature}_"
                    )
                ),
                None,
            )

            transformation = (
                "source-unknown normalization + "
                "TRAIN-fitted imputation + "
                "TRAIN-fitted one-hot encoding"
            )

        elif transformed_name.startswith(
            "numeric__"
        ):
            pathway = "numeric"

            source_feature = (
                transformed_name
                .replace(
                    "numeric__",
                    "",
                    1,
                )
            )

            transformation = (
                "TRAIN-fitted median imputation"
            )

        else:
            pathway = "unknown"
            source_feature = None
            transformation = "UNRESOLVED"

        records.append(
            {
                "transformed_position":
                    position,

                "transformed_feature":
                    transformed_name,

                "source_feature":
                    source_feature,

                "pathway":
                    pathway,

                "transformation":
                    transformation,

                "d6_governance_status":
                    "CANDIDATE",

                "authorized_for_primary_model":
                    True,
            }
        )

    return pd.DataFrame(records)


# ============================================================
# D7.R05 — BUILD UNKNOWN-CATEGORY AUDIT
# ============================================================

def build_d7_unknown_category_audit(
    workflow: dict[str, Any],
) -> pd.DataFrame:
    """
    Preserve source-unknown prevalence and canonicalization evidence.
    """

    fitted_bundle = workflow["fitted_bundle"]

    audit = (
        fitted_bundle[
            "unknown_category_audit"
        ]
        .copy()
    )

    audit[
        "canonical_replacement"
    ] = CANONICAL_UNKNOWN_CATEGORY

    audit[
        "governance_policy"
    ] = (
        "Preserve explicit source unknowns as a "
        "transparent model category; do not infer "
        "demographic membership."
    )

    return audit


# ============================================================
# D7.R06 — BUILD LEARNED PREPROCESSING STATE
# ============================================================

def build_d7_learned_preprocessing_state(
    workflow: dict[str, Any],
) -> pd.DataFrame:
    """
    Record parameters learned exclusively from TRAIN.
    """

    preprocessor = (
        workflow[
            "fitted_bundle"
        ][
            "preprocessor"
        ]
    )

    categorical_pipeline = (
        preprocessor
        .named_transformers_[
            "categorical"
        ]
    )

    categorical_imputer = (
        categorical_pipeline
        .named_steps[
            "imputer"
        ]
    )

    encoder = (
        categorical_pipeline
        .named_steps[
            "encoder"
        ]
    )

    numeric_pipeline = (
        preprocessor
        .named_transformers_[
            "numeric"
        ]
    )

    numeric_imputer = (
        numeric_pipeline
        .named_steps[
            "imputer"
        ]
    )

    records = []

    for (
        feature,
        imputation_value,
        categories,
    ) in zip(
        CATEGORICAL_FEATURES,
        categorical_imputer.statistics_,
        encoder.categories_,
    ):
        records.append(
            {
                "source_feature":
                    feature,

                "pathway":
                    "categorical",

                "learned_parameter":
                    "imputation_value",

                "learned_value":
                    str(imputation_value),

                "fit_partition":
                    TRAIN_LABEL,
            }
        )

        records.append(
            {
                "source_feature":
                    feature,

                "pathway":
                    "categorical",

                "learned_parameter":
                    "encoder_categories",

                "learned_value":
                    " | ".join(
                        str(value)
                        for value
                        in categories
                    ),

                "fit_partition":
                    TRAIN_LABEL,
            }
        )

    for (
        feature,
        median_value,
    ) in zip(
        NUMERIC_FEATURES,
        numeric_imputer.statistics_,
    ):
        records.append(
            {
                "source_feature":
                    feature,

                "pathway":
                    "numeric",

                "learned_parameter":
                    "median_imputation_value",

                "learned_value":
                    str(median_value),

                "fit_partition":
                    TRAIN_LABEL,
            }
        )

    return pd.DataFrame(records)


# ============================================================
# D7.R07 — BUILD MACHINE-READABLE MANIFEST
# ============================================================

def build_d7_preprocessing_manifest(
    workflow: dict[str, Any],
) -> dict[str, Any]:
    """
    Build the machine-readable D7 governance manifest.
    """

    fitted_bundle = workflow["fitted_bundle"]
    persistence = workflow["persistence_result"]
    validation = workflow[
        "persistence_validation"
    ]

    train_normalization = (
        fitted_bundle[
            "train_normalization_validation"
        ]
    )

    validation_normalization = (
        fitted_bundle[
            "validation_normalization_validation"
        ]
    )

    manifest = {
        "stage":
            "D7",

        "stage_name":
            "Governed Preprocessing Pipeline",

        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "status":
            "PASS",

        "upstream_dependency": {
            "stage":
                "D6",

            "artifact":
                str(
                    D6_DEVELOPMENT_ARTIFACT
                    .relative_to(
                        PROJECT_ROOT
                    )
                ),

            "expected_sha256":
                EXPECTED_D6_DEVELOPMENT_SHA256,
        },

        "development_boundary": {
            "train_encounters":
                EXPECTED_D7_TRAIN_ENCOUNTERS,

            "validation_encounters":
                EXPECTED_D7_VALIDATION_ENCOUNTERS,

            "fit_partition":
                TRAIN_LABEL,

            "validation_fit_permitted":
                False,

            "locked_test_label":
                LOCKED_TEST_LABEL,

            "locked_test_accessed":
                False,
        },

        "feature_contract": {
            "raw_primary_feature_count":
                EXPECTED_D7_RAW_FEATURE_COUNT,

            "raw_primary_features":
                list(
                    PRIMARY_CANDIDATE_FEATURES
                ),

            "categorical_features":
                list(
                    CATEGORICAL_FEATURES
                ),

            "numeric_features":
                list(
                    NUMERIC_FEATURES
                ),

            "transformed_feature_count":
                EXPECTED_D7_TRANSFORMED_FEATURE_COUNT,
        },

        "unknown_category_governance": {
            "canonical_unknown_category":
                CANONICAL_UNKNOWN_CATEGORY,

            "source_unknown_values": {
                feature:
                    sorted(
                        list(values)
                    )
                for feature, values
                in SOURCE_UNKNOWN_CATEGORY_VALUES.items()
            },

            "train_canonical_unknown_counts":
                train_normalization[
                    "canonical_unknown_counts"
                ],

            "validation_canonical_unknown_counts":
                validation_normalization[
                    "canonical_unknown_counts"
                ],

            "policy":
                (
                    "Explicit source unknown demographic "
                    "values are preserved as a canonical "
                    "unknown category rather than imputed "
                    "into an observed demographic group."
                ),
        },

        "persisted_artifacts": {
            "preprocessor": {
                "path":
                    str(
                        D7_PREPROCESSOR_PATH
                        .relative_to(
                            PROJECT_ROOT
                        )
                    ),

                "sha256":
                    persistence[
                        "preprocessor_sha256"
                    ],

                "git_policy":
                    "runtime artifact; ignored",
            },

            "transformed_schema": {
                "path":
                    str(
                        D7_TRANSFORMED_SCHEMA_PATH
                        .relative_to(
                            PROJECT_ROOT
                        )
                    ),

                "sha256":
                    persistence[
                        "schema_sha256"
                    ],

                "git_policy":
                    "runtime artifact; ignored",
            },
        },

        "reproducibility": {
            "preprocessor_checksum_verified":
                validation[
                    "preprocessor_checksum_verified"
                ],

            "schema_checksum_verified":
                validation[
                    "schema_checksum_verified"
                ],

            "train_reproduction_exact":
                validation[
                    "train_reproduction_exact"
                ],

            "validation_reproduction_exact":
                validation[
                    "validation_reproduction_exact"
                ],

            "schema_matches_original":
                validation[
                    "schema_matches_original"
                ],
        },

        "gate": {
            "d7_preprocessing":
                "PASS",

            "authorized_next_stage":
                "D8 Model Development & Selection",

            "model_training_completed":
                False,

            "locked_test_evaluation_authorized":
                False,

            "clinical_deployment_authorized":
                False,
        },
    }

    return manifest


# ============================================================
# D7.R08 — WRITE GOVERNANCE CONTRACT
# ============================================================

def write_d7_preprocessing_contract(
) -> None:
    """
    Write the human-readable D7 preprocessing contract.
    """

    content = f"""# D7 — Governed Preprocessing Contract

## Purpose

D7 converts the frozen D6 primary candidate feature set into a
reproducible model-ready representation while preserving leakage,
partition, feature-authorization, and locked-test controls.

## Prediction Point

{D7_PREPROCESSING_CONTRACT.prediction_point}

## Authorized Raw Model Inputs

Exactly {EXPECTED_D7_RAW_FEATURE_COUNT} D6-CANDIDATE features are
authorized for the primary modeling pathway:

{chr(10).join(f"- {feature}" for feature in PRIMARY_CANDIDATE_FEATURES)}

## Categorical Pathway

Categorical features:

{chr(10).join(f"- {feature}" for feature in CATEGORICAL_FEATURES)}

Controls:

- Explicit source-specific unknown markers are normalized to
  `{CANONICAL_UNKNOWN_CATEGORY}`.
- Unknown demographic membership is preserved rather than inferred.
- Native missing values are handled using the governed categorical
  imputation policy.
- Imputation state is learned from TRAIN only.
- One-hot vocabulary is learned from TRAIN only.
- Genuinely unseen later categories are handled without refitting.

## Numeric Pathway

Numeric features:

{chr(10).join(f"- {feature}" for feature in NUMERIC_FEATURES)}

Controls:

- Median imputation is fitted on TRAIN only.
- No D7 scaling is applied.
- Model-specific scaling, if justified, must be governed downstream.

## Development Boundary

- TRAIN: FIT + TRANSFORM
- VALIDATION: TRANSFORM ONLY
- LOCKED TEST: NOT ACCESSED

Validation must never contribute to fitted preprocessing state.

## Prohibited D7 Activities

D7 does not:

- redesign D6 feature authorization;
- promote D6-CONDITIONAL features;
- use identifiers or outcomes as model inputs;
- train predictive models;
- tune hyperparameters;
- select operating thresholds;
- access the locked test partition;
- authorize clinical deployment.

## Persistence & Reproducibility

The fitted preprocessing transformer and authoritative transformed
schema are persisted locally as runtime artifacts.

Their SHA-256 checksums and learned-state evidence are recorded in
the D7 manifest and evidence tables.

A persisted transformer must reproduce the original TRAIN and
VALIDATION transformations exactly before D7 may pass.

## Governance Principle

Unknown sensitive demographic values must remain explicitly unknown.
They must not be silently reassigned to an observed demographic
group through modal imputation.

"""

    D7_CONTRACT_REPORT_PATH.write_text(
        content,
        encoding="utf-8",
    )


# ============================================================
# D7.R09 — WRITE FORMAL GATE DECISION
# ============================================================

def write_d7_gate_decision(
    workflow: dict[str, Any],
) -> None:
    """
    Write the formal D7 stage-gate decision.
    """

    persistence = workflow["persistence_result"]
    validation = workflow[
        "persistence_validation"
    ]

    content = f"""# D7 — Preprocessing Gate Decision

## Decision

**PASS — AUTHORIZED TO PROCEED TO D8 MODEL DEVELOPMENT & SELECTION**

## Evidence Reviewed

- Frozen D6 development artifact checksum verified.
- TRAIN and VALIDATION patient boundaries preserved.
- Locked test partition remained inaccessible.
- Exactly {EXPECTED_D7_RAW_FEATURE_COUNT} authorized raw features
  entered preprocessing.
- Final transformed schema contains
  {EXPECTED_D7_TRANSFORMED_FEATURE_COUNT} model-ready features.
- Explicit source-coded demographic unknowns were preserved as
  `{CANONICAL_UNKNOWN_CATEGORY}`.
- No raw `race=?` or `gender=Unknown/Invalid` dummy variables remain.
- TRAIN-only preprocessing fit was enforced.
- VALIDATION contributed no fitted state.
- Missing and non-finite transformed values were absent.
- Persisted TRAIN transformation reproduced exactly:
  {validation["train_reproduction_exact"]}.
- Persisted VALIDATION transformation reproduced exactly:
  {validation["validation_reproduction_exact"]}.
- Preprocessor checksum verification:
  {validation["preprocessor_checksum_verified"]}.
- Schema checksum verification:
  {validation["schema_checksum_verified"]}.

## Persisted Artifact Integrity

Preprocessor SHA-256:

`{persistence["preprocessor_sha256"]}`

Transformed schema SHA-256:

`{persistence["schema_sha256"]}`

## Authorization

D7 authorizes progression to:

**D8 — Model Development & Selection**

This gate does **not** authorize:

- locked-test evaluation;
- autonomous clinical decision-making;
- production deployment;
- clinical use;
- final model approval.

Those decisions require completion of the downstream clinical,
fairness, robustness, explainability, registry, locked-test,
deployment, and governance stages.

## Final D7 Status

**PASS**

"""

    D7_GATE_DECISION_PATH.write_text(
        content,
        encoding="utf-8",
    )


# ============================================================
# D7.R10 — WRITE COMPLETE D7 EVIDENCE PACKAGE
# ============================================================

def write_d7_evidence_package(
) -> dict[str, Any]:
    """
    Build, validate, persist, and document the complete D7
    preprocessing evidence package.
    """

    prepare_d7_evidence_directories()

    workflow = (
        build_persisted_d7_primary_preprocessor()
    )

    summary = (
        build_d7_preprocessing_summary(
            workflow
        )
    )

    feature_registry = (
        build_d7_transformed_feature_registry(
            workflow
        )
    )

    unknown_audit = (
        build_d7_unknown_category_audit(
            workflow
        )
    )

    learned_state = (
        build_d7_learned_preprocessing_state(
            workflow
        )
    )

    manifest = (
        build_d7_preprocessing_manifest(
            workflow
        )
    )

    summary.to_csv(
        D7_SUMMARY_TABLE_PATH,
        index=False,
    )

    feature_registry.to_csv(
        D7_FEATURE_REGISTRY_PATH,
        index=False,
    )

    unknown_audit.to_csv(
        D7_UNKNOWN_AUDIT_PATH,
        index=False,
    )

    learned_state.to_csv(
        D7_LEARNED_STATE_PATH,
        index=False,
    )

    with D7_MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as file_handle:
        yaml.safe_dump(
            manifest,
            file_handle,
            sort_keys=False,
            allow_unicode=True,
        )

    write_d7_preprocessing_contract()

    write_d7_gate_decision(
        workflow
    )

    generated_artifacts = {
        "manifest":
            str(D7_MANIFEST_PATH),

        "contract":
            str(D7_CONTRACT_REPORT_PATH),

        "gate_decision":
            str(D7_GATE_DECISION_PATH),

        "summary":
            str(D7_SUMMARY_TABLE_PATH),

        "feature_registry":
            str(D7_FEATURE_REGISTRY_PATH),

        "unknown_category_audit":
            str(D7_UNKNOWN_AUDIT_PATH),

        "learned_preprocessing_state":
            str(D7_LEARNED_STATE_PATH),
    }

    return {
        "workflow":
            workflow,

        "generated_artifacts":
            generated_artifacts,

        "manifest":
            manifest,

        "validation_status":
            "PASS",
    }


# ============================================================
# D7.R11 — COMMAND-LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":
    result = write_d7_evidence_package()

    print(
        "D7 evidence package status:",
        result["validation_status"],
    )

    print(
        "Generated artifacts:"
    )

    for name, path in (
        result[
            "generated_artifacts"
        ].items()
    ):
        print(
            f"  {name}: {path}"
        )