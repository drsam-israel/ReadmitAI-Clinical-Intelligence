# ============================================================
# D5 — GOVERNED SPLIT PERSISTENCE & EVIDENCE REPORTING
# ============================================================
"""
Persist and document the governed D5 patient-level split.

Outputs:
1. Patient-level split assignment
2. Encounter-level split summary
3. Patient-overlap audit
4. Split governance contract
5. Split gate decision
6. Machine-readable manifest with checksums

No model training occurs in D5.
"""

# ============================================================
# D5.R1 — IMPORTS
# ============================================================

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

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
    build_governed_patient_split,
)


# ============================================================
# D5.R2 — PROJECT & OUTPUT PATHS
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

SPLITS_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "splits"
)

TABLES_DIR = (
    PROJECT_ROOT
    / "reports"
    / "tables"
)

GOVERNANCE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "governance"
)

MANIFESTS_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "manifests"
)

PATIENT_ASSIGNMENT_PATH = (
    SPLITS_DIR
    / "D5_patient_split_assignment.csv"
)

SPLIT_SUMMARY_PATH = (
    TABLES_DIR
    / "D5_split_summary.csv"
)

OVERLAP_AUDIT_PATH = (
    TABLES_DIR
    / "D5_patient_overlap_audit.csv"
)

SPLIT_CONTRACT_PATH = (
    GOVERNANCE_DIR
    / "D5_split_governance_contract.md"
)

GATE_DECISION_PATH = (
    GOVERNANCE_DIR
    / "D5_split_gate_decision.md"
)

MANIFEST_PATH = (
    MANIFESTS_DIR
    / "D5_split_manifest.yaml"
)


# ============================================================
# D5.R3 — OUTPUT DIRECTORY PREPARATION
# ============================================================

def ensure_output_directories() -> None:
    """
    Ensure all D5 evidence directories exist.
    """

    for directory in (
        SPLITS_DIR,
        TABLES_DIR,
        GOVERNANCE_DIR,
        MANIFESTS_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# D5.R4 — FILE CHECKSUM
# ============================================================

def calculate_sha256(
    path: Path,
) -> str:
    """
    Calculate SHA-256 checksum for a persisted artifact.
    """

    digest = sha256()

    with path.open("rb") as file_handle:
        for chunk in iter(
            lambda: file_handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest().upper()


# ============================================================
# D5.R5 — PERSIST PATIENT ASSIGNMENT
# ============================================================

def persist_patient_assignment(
    patient_assignment: pd.DataFrame,
) -> None:
    """
    Persist the authoritative patient-to-split mapping.

    This artifact becomes the source of truth for downstream
    partition membership.
    """

    columns = [
        GROUP_COLUMN,
        "patient_positive",
        "encounter_count",
        "positive_encounter_count",
        "split",
    ]

    assignment = (
        patient_assignment[
            columns
        ]
        .sort_values(
            GROUP_COLUMN
        )
        .reset_index(drop=True)
    )

    assignment.to_csv(
        PATIENT_ASSIGNMENT_PATH,
        index=False,
    )


# ============================================================
# D5.R6 — PATIENT OVERLAP EVIDENCE
# ============================================================

def build_overlap_audit_table(
    split_validation: dict[str, Any],
) -> pd.DataFrame:
    """
    Build a persistent patient-overlap audit table.
    """

    records = [
        {
            "audit_control":
                "multi_split_patients",
            "observed_value":
                split_validation[
                    "multi_split_patients"
                ],
            "required_value":
                0,
            "status":
                "PASS"
                if split_validation[
                    "multi_split_patients"
                ] == 0
                else "FAIL",
        },
        {
            "audit_control":
                "train_validation_overlap",
            "observed_value":
                split_validation[
                    "train_validation_overlap"
                ],
            "required_value":
                0,
            "status":
                "PASS"
                if split_validation[
                    "train_validation_overlap"
                ] == 0
                else "FAIL",
        },
        {
            "audit_control":
                "train_test_overlap",
            "observed_value":
                split_validation[
                    "train_test_overlap"
                ],
            "required_value":
                0,
            "status":
                "PASS"
                if split_validation[
                    "train_test_overlap"
                ] == 0
                else "FAIL",
        },
        {
            "audit_control":
                "validation_test_overlap",
            "observed_value":
                split_validation[
                    "validation_test_overlap"
                ],
            "required_value":
                0,
            "status":
                "PASS"
                if split_validation[
                    "validation_test_overlap"
                ] == 0
                else "FAIL",
        },
    ]

    return pd.DataFrame(
        records
    )


# ============================================================
# D5.R7 — SPLIT GOVERNANCE CONTRACT DOCUMENT
# ============================================================

def build_split_contract_document() -> str:
    """
    Build the formal human-readable D5 split contract.
    """

    return f"""# D5 Governed Patient-Level Split Contract

## Project

Diabetes Readmission Clinical AI

## Purpose

This contract defines the governed development partitions used
throughout subsequent model-development stages.

The split unit is the patient rather than the encounter because
multiple encounters may belong to the same patient.

## Split Unit

**Grouping key:** `{GROUP_COLUMN}`

A patient may belong to one and only one partition.

Patient overlap across train, validation, and locked test is
prohibited.

## Outcome

**Target:** `{TARGET_COLUMN}`

The patient-level outcome representation used for split balancing
is not a predictive feature.

## Partition Policy

**Training:** {TRAIN_FRACTION:.0%}

Used for fitting preprocessing transformations and models.

**Validation:** {VALIDATION_FRACTION:.0%}

{SPLIT_GOVERNANCE_CONTRACT.validation_permitted_use}

**Locked test:** {TEST_FRACTION:.0%}

{SPLIT_GOVERNANCE_CONTRACT.locked_test_permitted_use}

## Reproducibility

**Random seed:** {RANDOM_SEED}

{SPLIT_GOVERNANCE_CONTRACT.reproducibility_rule}

The persisted patient assignment becomes the authoritative
downstream source of partition membership.

Downstream stages must load the persisted assignment rather than
silently generating a new split.

## Leakage Control

No patient may appear in more than one partition.

The locked test partition must not influence:

- feature engineering decisions;
- preprocessing decisions;
- model selection;
- hyperparameter selection;
- calibration decisions;
- threshold selection;
- clinical utility optimization.

## Governance Status

The locked test partition is **CREATED BUT PROTECTED**.

Creation of the locked test partition does not authorize its use
for model-development decisions.
"""


# ============================================================
# D5.R8 — GATE DECISION DOCUMENT
# ============================================================

def build_gate_decision_document(
    split_validation: dict[str, Any],
    reproducibility_validation: dict[str, Any],
    split_summary: pd.DataFrame,
) -> str:
    """
    Build the formal D5 lifecycle gate decision.
    """

    split_status = (
        split_validation[
            "validation_status"
        ]
    )

    reproducibility_status = (
        reproducibility_validation[
            "validation_status"
        ]
    )

    gate = (
        "PASS"
        if (
            split_status == "PASS"
            and reproducibility_status == "PASS"
        )
        else "FAIL"
    )

    summary_lines = []

    for row in (
        split_summary
        .itertuples(index=False)
    ):
        summary_lines.append(
            f"- **{row.split}:** "
            f"{int(row.encounters):,} encounters; "
            f"{int(row.patients):,} patients; "
            f"{int(row.positive_encounters):,} positive encounters; "
            f"{row.readmission_rate:.4%} readmission rate"
        )

    summary_text = "\n".join(
        summary_lines
    )

    return f"""# D5 Governed Patient-Level Split Gate Decision

## Gate

**{gate}**

## Source Cohort

- Encounters: {split_validation["source_encounters"]:,}
- Unique patients: {split_validation["source_patients"]:,}

## Partition Results

{summary_text}

## Patient Leakage Audit

- Multi-split patients: {split_validation["multi_split_patients"]}
- Train-validation overlap: {split_validation["train_validation_overlap"]}
- Train-test overlap: {split_validation["train_test_overlap"]}
- Validation-test overlap: {split_validation["validation_test_overlap"]}

## Reproducibility

Same governed cohort + same algorithm + seed `{RANDOM_SEED}`
reproduces the same patient assignment:

**{reproducibility_validation["same_seed_same_assignment"]}**

## Gate Basis

D5 may close only when:

- every source patient receives one split assignment;
- every source encounter is preserved;
- all three required partitions exist;
- patient overlap is zero;
- no split assignment is missing;
- patient assignments are unique;
- deterministic regeneration succeeds;
- the patient assignment is persisted as a governed artifact.

## Decision

D5 lifecycle gate: **{gate}**

The train and validation partitions may proceed to downstream
development stages subject to existing D4 feature-governance
controls.

The test partition remains **LOCKED**.

## Clinical Deployment

**NOT APPROVED**

Successful data splitting does not establish model performance or
clinical deployment readiness.
"""


# ============================================================
# D5.R9 — BUILD MACHINE-READABLE MANIFEST
# ============================================================

def build_manifest(
    split_validation: dict[str, Any],
    reproducibility_validation: dict[str, Any],
    assignment_checksum: str,
) -> dict[str, Any]:
    """
    Build the machine-readable D5 split manifest.
    """

    return {
        "stage":
            "D5",

        "name":
            "Governed Patient-Level Splitting",

        "project":
            "Diabetes Readmission Clinical AI",

        "generated_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "gate_decision":
            "PASS",

        "clinical_deployment_status":
            "NOT APPROVED",

        "grouping_key":
            GROUP_COLUMN,

        "target":
            TARGET_COLUMN,

        "random_seed":
            RANDOM_SEED,

        "split_fractions": {
            "train":
                TRAIN_FRACTION,
            "validation":
                VALIDATION_FRACTION,
            "test":
                TEST_FRACTION,
        },

        "source_counts": {
            "encounters":
                split_validation[
                    "source_encounters"
                ],
            "patients":
                split_validation[
                    "source_patients"
                ],
        },

        "patient_overlap": {
            "multi_split_patients":
                split_validation[
                    "multi_split_patients"
                ],
            "train_validation":
                split_validation[
                    "train_validation_overlap"
                ],
            "train_test":
                split_validation[
                    "train_test_overlap"
                ],
            "validation_test":
                split_validation[
                    "validation_test_overlap"
                ],
        },

        "reproducibility": {
            "same_seed_same_assignment":
                reproducibility_validation[
                    "same_seed_same_assignment"
                ],
        },

        "locked_test": {
            "status":
                "LOCKED",
            "development_use_permitted":
                False,
        },

        "authoritative_assignment": {
            "path":
                "artifacts/splits/"
                "D5_patient_split_assignment.csv",
            "sha256":
                assignment_checksum,
        },

        "generated_files": [
            "artifacts/splits/"
            "D5_patient_split_assignment.csv",

            "reports/tables/"
            "D5_split_summary.csv",

            "reports/tables/"
            "D5_patient_overlap_audit.csv",

            "reports/governance/"
            "D5_split_governance_contract.md",

            "reports/governance/"
            "D5_split_gate_decision.md",
        ],
    }


# ============================================================
# D5.R10 — GENERATE COMPLETE D5 EVIDENCE PACKAGE
# ============================================================

def generate_d5_evidence_package() -> dict[str, Any]:
    """
    Generate and persist the complete D5 evidence package.
    """

    ensure_output_directories()

    (
        cohort,
        patient_frame,
        patient_assignment,
        split_cohort,
        split_summary,
        split_validation,
        reproducibility_validation,
    ) = build_governed_patient_split()

    if (
        split_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D5 split validation failed. "
            "Evidence package will not be finalized."
        )

    if (
        reproducibility_validation[
            "validation_status"
        ]
        != "PASS"
    ):
        raise RuntimeError(
            "D5 reproducibility validation failed. "
            "Evidence package will not be finalized."
        )

    # --------------------------------------------------------
    # Persist authoritative patient assignment
    # --------------------------------------------------------

    persist_patient_assignment(
        patient_assignment
    )

    assignment_checksum = (
        calculate_sha256(
            PATIENT_ASSIGNMENT_PATH
        )
    )

    # --------------------------------------------------------
    # Persist split summary
    # --------------------------------------------------------

    split_summary.to_csv(
        SPLIT_SUMMARY_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Persist patient-overlap audit
    # --------------------------------------------------------

    overlap_audit = (
        build_overlap_audit_table(
            split_validation
        )
    )

    overlap_audit.to_csv(
        OVERLAP_AUDIT_PATH,
        index=False,
    )

    # --------------------------------------------------------
    # Persist split governance contract
    # --------------------------------------------------------

    SPLIT_CONTRACT_PATH.write_text(
        build_split_contract_document(),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Persist lifecycle gate decision
    # --------------------------------------------------------

    GATE_DECISION_PATH.write_text(
        build_gate_decision_document(
            split_validation,
            reproducibility_validation,
            split_summary,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Persist machine-readable manifest
    # --------------------------------------------------------

    manifest = build_manifest(
        split_validation,
        reproducibility_validation,
        assignment_checksum,
    )

    MANIFEST_PATH.write_text(
        yaml.safe_dump(
            manifest,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    return {
        "status":
            "SUCCESS",

        "gate_decision":
            "PASS",

        "source_encounters":
            split_validation[
                "source_encounters"
            ],

        "source_patients":
            split_validation[
                "source_patients"
            ],

        "assignment_checksum":
            assignment_checksum,

        "split_summary":
            split_summary,

        "patient_overlap":
            {
                "multi_split_patients":
                    split_validation[
                        "multi_split_patients"
                    ],
                "train_validation":
                    split_validation[
                        "train_validation_overlap"
                    ],
                "train_test":
                    split_validation[
                        "train_test_overlap"
                    ],
                "validation_test":
                    split_validation[
                        "validation_test_overlap"
                    ],
            },

        "generated_files": {
            "patient_assignment":
                str(
                    PATIENT_ASSIGNMENT_PATH
                ),

            "split_summary":
                str(
                    SPLIT_SUMMARY_PATH
                ),

            "overlap_audit":
                str(
                    OVERLAP_AUDIT_PATH
                ),

            "split_contract":
                str(
                    SPLIT_CONTRACT_PATH
                ),

            "gate_decision":
                str(
                    GATE_DECISION_PATH
                ),

            "manifest":
                str(
                    MANIFEST_PATH
                ),
        },
    }


# ============================================================
# D5.R11 — COMMAND-LINE EXECUTION
# ============================================================

if __name__ == "__main__":

    result = (
        generate_d5_evidence_package()
    )

    print(
        "=" * 72
    )
    print(
        "D5 — GOVERNED PATIENT-LEVEL SPLIT EVIDENCE PACKAGE"
    )
    print(
        "=" * 72
    )

    print(
        f"status: "
        f"{result['status']}"
    )

    print(
        f"gate_decision: "
        f"{result['gate_decision']}"
    )

    print(
        f"source_encounters: "
        f"{result['source_encounters']:,}"
    )

    print(
        f"source_patients: "
        f"{result['source_patients']:,}"
    )

    print()
    print(
        "SPLIT SUMMARY"
    )
    print(
        "-" * 72
    )

    print(
        result[
            "split_summary"
        ].to_string(
            index=False
        )
    )

    print()
    print(
        "PATIENT OVERLAP"
    )
    print(
        "-" * 72
    )

    for key, value in (
        result[
            "patient_overlap"
        ].items()
    ):
        print(
            f"{key}: {value}"
        )

    print()
    print(
        "AUTHORITATIVE ASSIGNMENT CHECKSUM"
    )
    print(
        "-" * 72
    )

    print(
        result[
            "assignment_checksum"
        ]
    )

    print()
    print(
        "GENERATED FILES"
    )
    print(
        "-" * 72
    )

    for name, path in (
        result[
            "generated_files"
        ].items()
    ):
        print(
            f"{name}: {path}"
        )

    print()
    print(
        "=" * 72
    )
    print(
        "D5 evidence generation: SUCCESS"
    )
    print(
        "Locked test partition: FROZEN AND PROTECTED"
    )
    print(
        "Clinical deployment: NOT APPROVED"
    )
    print(
        "=" * 72
    )