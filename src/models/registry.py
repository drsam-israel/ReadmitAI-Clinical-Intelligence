# ============================================================
# D13 — MODEL REGISTRY & ARTIFACT FREEZE
# ============================================================
# Purpose:
#   Register the exact development-stage clinical AI candidate
#   that exited D12 and establish an immutable artifact boundary
#   before the one-time D14 locked-TEST evaluation.
#
# Governance principle:
#   D13 does not develop, retrain, retune, recalibrate, refit,
#   reinterpret, or evaluate the model. It establishes identity,
#   provenance, integrity, traceability, and change control for
#   the frozen candidate system.
# ============================================================

from __future__ import annotations

import json
from typing import Any, Final


# ============================================================
# D13.00 — REGISTRY & FREEZE GOVERNANCE CONTRACT
# ============================================================

D13_STAGE_ID: Final[str] = "D13"

D13_STAGE_NAME: Final[str] = (
    "Model Registry & Artifact Freeze"
)

D13_SOURCE_LIFECYCLE_STAGE: Final[str] = "D12"

D13_SOURCE_GIT_COMMIT: Final[str] = "4e995f2"

D13_NEXT_LIFECYCLE_STAGE: Final[str] = (
    "D14_LOCKED_TEST_EVALUATION"
)

D13_EVALUATION_PARTITION: Final[str] = "NONE"

D13_LOCKED_TEST_EVALUATION_STAGE: Final[str] = "D14"


# ============================================================
# D13.01 — FROZEN SYSTEM IDENTITY
# ============================================================

D13_EXPECTED_MODEL_NAME: Final[str] = "xgboost"

D13_EXPECTED_MODEL_SHA256: Final[str] = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16A519DF016990FAC065AF3249BDA88085"
)

D13_EXPECTED_D7_PREPROCESSOR_SHA256: Final[str] = (
    "076878C0BD7C9B80897F3AA06157719A1E311165299549D83213C789CA1ECEAC"
)

D13_EXPECTED_D7_SCHEMA_SHA256: Final[str] = (
    "69E0E7F19C64350A6995830E875C1303E5D14F55FD7CDA4A7D845CCDE7B756ED"
)

D13_EXPECTED_DEVELOPMENT_THRESHOLD: Final[float] = 0.12

D13_EXPECTED_TRANSFORMED_FEATURE_COUNT: Final[int] = 49

D13_EXPECTED_SOURCE_FEATURE_COUNT: Final[int] = 10

D13_EXPECTED_D8_MODEL_METADATA_SHA256: Final[str] = (
    "5838A6C77F05BB183F90B9AA4B0ED9F0AE5B0FBF2E3E1B1326A79A3A67A1AC76"
)


# ============================================================
# D13.02 — REGISTRY PURPOSE
# ============================================================

D13_REGISTRY_PURPOSE: Final[str] = (
    "Create a traceable and integrity-verifiable registry record "
    "for the exact frozen development-stage clinical AI candidate "
    "that completed D12, before any locked-TEST evaluation occurs."
)


# ============================================================
# D13.03 — PERMITTED ACTIVITIES
# ============================================================

D13_PERMITTED_ACTIVITIES: Final[tuple[str, ...]] = (
    "read_frozen_model_artifact",
    "read_frozen_preprocessor_artifact",
    "read_frozen_transformed_feature_schema",
    "verify_artifact_checksums",
    "verify_artifact_existence",
    "verify_cross_stage_identity",
    "capture_model_metadata",
    "capture_preprocessing_metadata",
    "capture_feature_schema_metadata",
    "capture_operating_threshold_metadata",
    "capture_software_environment_metadata",
    "capture_lifecycle_provenance",
    "capture_governance_evidence_references",
    "generate_model_registry_record",
    "generate_artifact_inventory",
    "generate_freeze_manifest",
    "generate_change_control_record",
    "generate_registry_gate_decision",
)


# ============================================================
# D13.04 — PROHIBITED ACTIVITIES
# ============================================================

D13_PROHIBITED_ACTIVITIES: Final[tuple[str, ...]] = (
    "model_retraining",
    "hyperparameter_retuning",
    "preprocessor_refitting",
    "feature_reengineering",
    "feature_selection_change",
    "threshold_retuning",
    "probability_recalibration",
    "subgroup_specific_thresholding",
    "locked_test_access",
    "locked_test_evaluation",
    "validation_driven_model_change",
    "automatic_model_mitigation",
    "autonomous_clinical_decision_making",
    "deployment_authorization",
)


# ============================================================
# D13.05 — FREEZE PRINCIPLES
# ============================================================

D13_FREEZE_PRINCIPLES: Final[tuple[str, ...]] = (
    (
        "The D13 registered candidate must be the exact model system "
        "that exited D12."
    ),
    (
        "Artifact identity must be established using cryptographic "
        "checksums rather than filenames alone."
    ),
    (
        "The model, preprocessing artifact, transformed feature schema, "
        "feature contract, and development operating threshold must be "
        "traceable as one governed candidate system."
    ),
    (
        "D13 must not access or evaluate the locked TEST partition."
    ),
    (
        "No artifact may be silently replaced, regenerated, refitted, "
        "or modified during registration."
    ),
    (
        "Any post-freeze change to a registered component invalidates "
        "the existing candidate identity and requires explicit "
        "change control."
    ),
    (
        "D13 progression to D14 authorizes locked-TEST evaluation only; "
        "it does not authorize clinical deployment."
    ),
)


# ============================================================
# D13.06 — REQUIRED REGISTRY COMPONENTS
# ============================================================

D13_REQUIRED_REGISTRY_COMPONENTS: Final[tuple[str, ...]] = (
    "selected_model",
    "model_artifact",
    "model_sha256",
    "preprocessor_artifact",
    "preprocessor_sha256",
    "transformed_feature_schema",
    "transformed_feature_schema_sha256",
    "source_feature_contract",
    "development_operating_threshold",
    "model_development_metadata",
    "software_environment",
    "lifecycle_provenance",
    "governance_evidence_traceability",
    "artifact_integrity_record",
    "change_control_status",
)


# ============================================================
# D13.07 — STATIC REGISTRY BOUNDARY
# ============================================================

def build_d13_static_registry_boundary() -> dict[str, Any]:
    """
    Build the static governance boundary for D13.

    This function declares what D13 is allowed to register and verify.
    It does not load, mutate, regenerate, refit, score, or evaluate
    any model or dataset.
    """

    return {
        "stage_id":
            D13_STAGE_ID,

        "stage_name":
            D13_STAGE_NAME,

        "source_lifecycle_stage":
            D13_SOURCE_LIFECYCLE_STAGE,

        "source_git_commit":
            D13_SOURCE_GIT_COMMIT,

        "next_lifecycle_stage":
            D13_NEXT_LIFECYCLE_STAGE,

        "evaluation_partition":
            D13_EVALUATION_PARTITION,

        "locked_test_evaluation_stage":
            D13_LOCKED_TEST_EVALUATION_STAGE,

        "registry_purpose":
            D13_REGISTRY_PURPOSE,

        "model_name":
            D13_EXPECTED_MODEL_NAME,

        "expected_model_sha256":
            D13_EXPECTED_MODEL_SHA256,

        "expected_d7_preprocessor_sha256":
            D13_EXPECTED_D7_PREPROCESSOR_SHA256,

        "expected_d7_schema_sha256":
            D13_EXPECTED_D7_SCHEMA_SHA256,

        "development_threshold":
            D13_EXPECTED_DEVELOPMENT_THRESHOLD,

        "transformed_feature_count":
            D13_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "source_feature_count":
            D13_EXPECTED_SOURCE_FEATURE_COUNT,

        "permitted_activities":
            D13_PERMITTED_ACTIVITIES,

        "prohibited_activities":
            D13_PROHIBITED_ACTIVITIES,

        "freeze_principles":
            D13_FREEZE_PRINCIPLES,

        "required_registry_components":
            D13_REQUIRED_REGISTRY_COMPONENTS,

        "model_retrained":
            False,

        "preprocessor_refitted":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "locked_test_evaluated":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D13.08 — STATIC BOUNDARY VALIDATION
# ============================================================

def validate_d13_static_registry_boundary(
    boundary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the D13 static governance contract before any artifact
    registration or integrity verification is allowed to proceed.
    """

    if boundary is None:
        boundary = build_d13_static_registry_boundary()

    checks = {
        "stage_is_d13":
            boundary["stage_id"] == "D13",

        "source_stage_is_d12":
            boundary["source_lifecycle_stage"] == "D12",

        "source_commit_is_d12_freeze":
            boundary["source_git_commit"] == "4e995f2",

        "next_stage_is_d14":
            boundary["next_lifecycle_stage"]
            == "D14_LOCKED_TEST_EVALUATION",

        "no_evaluation_partition":
            boundary["evaluation_partition"] == "NONE",

        "locked_test_reserved_for_d14":
            boundary["locked_test_evaluation_stage"] == "D14",

        "model_name_is_xgboost":
            boundary["model_name"] == "xgboost",

        "model_sha_is_frozen":
            boundary["expected_model_sha256"]
            == D13_EXPECTED_MODEL_SHA256,

        "preprocessor_sha_is_frozen":
            boundary["expected_d7_preprocessor_sha256"]
            == D13_EXPECTED_D7_PREPROCESSOR_SHA256,

        "schema_sha_is_frozen":
            boundary["expected_d7_schema_sha256"]
            == D13_EXPECTED_D7_SCHEMA_SHA256,

        "development_threshold_is_frozen":
            boundary["development_threshold"]
            == D13_EXPECTED_DEVELOPMENT_THRESHOLD,

        "transformed_feature_count_is_49":
            boundary["transformed_feature_count"] == 49,

        "source_feature_count_is_10":
            boundary["source_feature_count"] == 10,

        "locked_test_access_prohibited":
            "locked_test_access"
            in boundary["prohibited_activities"],

        "locked_test_evaluation_prohibited":
            "locked_test_evaluation"
            in boundary["prohibited_activities"],

        "model_retraining_prohibited":
            "model_retraining"
            in boundary["prohibited_activities"],

        "preprocessor_refitting_prohibited":
            "preprocessor_refitting"
            in boundary["prohibited_activities"],

        "threshold_retuning_prohibited":
            "threshold_retuning"
            in boundary["prohibited_activities"],

        "deployment_authorization_prohibited":
            "deployment_authorization"
            in boundary["prohibited_activities"],

        "model_not_retrained":
            boundary["model_retrained"] is False,

        "preprocessor_not_refitted":
            boundary["preprocessor_refitted"] is False,

        "threshold_not_retuned":
            boundary["threshold_retuned"] is False,

        "locked_test_not_accessed":
            boundary["locked_test_accessed"] is False,

        "locked_test_not_evaluated":
            boundary["locked_test_evaluated"] is False,

        "deployment_not_authorized":
            boundary["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "stage_id":
            D13_STAGE_ID,

        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "source_git_commit":
            boundary["source_git_commit"],

        "model_name":
            boundary["model_name"],

        "expected_model_sha256":
            boundary["expected_model_sha256"],

        "expected_d7_preprocessor_sha256":
            boundary["expected_d7_preprocessor_sha256"],

        "expected_d7_schema_sha256":
            boundary["expected_d7_schema_sha256"],

        "development_threshold":
            boundary["development_threshold"],

        "locked_test_accessed":
            boundary["locked_test_accessed"],

        "locked_test_evaluated":
            boundary["locked_test_evaluated"],

        "deployment_authorized":
            boundary["deployment_authorized"],
    }

# ============================================================
# D13.10 — FROZEN ARTIFACT IDENTITY VERIFICATION
# ============================================================

import hashlib
from pathlib import Path

from src.features import preprocessing as d7
from src.models import development as d8


def _d13_sha256(path: Path) -> str:
    """
    Calculate SHA-256 for an existing artifact using read-only access.

    This helper does not modify, deserialize, regenerate, or rewrite
    the artifact.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest().upper()


def build_d13_frozen_artifact_identity() -> dict[str, Any]:
    """
    Verify the physical identity of the frozen model system inherited
    from D7 and D8.

    This function performs read-only filesystem inspection and SHA-256
    calculation. It does not load data, transform encounters, generate
    predictions, refit preprocessing, retrain the model, or access TEST.
    """

    model_path = Path(
        d8.D8_SELECTED_MODEL_ARTIFACT_PATH
    )

    preprocessor_path = Path(
        d7.D7_PREPROCESSOR_PATH
    )

    schema_path = Path(
        d7.D7_TRANSFORMED_SCHEMA_PATH
    )

    artifact_paths = {
        "model":
            model_path,

        "preprocessor":
            preprocessor_path,

        "transformed_feature_schema":
            schema_path,
    }

    missing_artifacts = [
        name
        for name, path in artifact_paths.items()
        if not path.is_file()
    ]

    if missing_artifacts:
        raise FileNotFoundError(
            "D13 cannot establish the frozen candidate identity "
            "because required artifacts are missing: "
            f"{missing_artifacts}"
        )

    # Capture metadata before checksum calculation.
    before_metadata = {
        name: {
            "size_bytes":
                path.stat().st_size,

            "mtime_ns":
                path.stat().st_mtime_ns,
        }
        for name, path in artifact_paths.items()
    }

    model_sha256 = _d13_sha256(
        model_path
    )

    preprocessor_sha256 = _d13_sha256(
        preprocessor_path
    )

    schema_sha256 = _d13_sha256(
        schema_path
    )

    # Capture metadata again to demonstrate that D13's integrity
    # verification did not rewrite the frozen artifacts.
    after_metadata = {
        name: {
            "size_bytes":
                path.stat().st_size,

            "mtime_ns":
                path.stat().st_mtime_ns,
        }
        for name, path in artifact_paths.items()
    }

    return {
        "model_artifact_path":
            str(model_path),

        "model_artifact_exists":
            model_path.is_file(),

        "model_sha256":
            model_sha256,

        "expected_model_sha256":
            D13_EXPECTED_MODEL_SHA256,

        "model_sha256_matches":
            model_sha256
            == D13_EXPECTED_MODEL_SHA256,

        "preprocessor_artifact_path":
            str(preprocessor_path),

        "preprocessor_artifact_exists":
            preprocessor_path.is_file(),

        "preprocessor_sha256":
            preprocessor_sha256,

        "expected_preprocessor_sha256":
            D13_EXPECTED_D7_PREPROCESSOR_SHA256,

        "preprocessor_sha256_matches":
            preprocessor_sha256
            == D13_EXPECTED_D7_PREPROCESSOR_SHA256,

        "schema_artifact_path":
            str(schema_path),

        "schema_artifact_exists":
            schema_path.is_file(),

        "schema_sha256":
            schema_sha256,

        "expected_schema_sha256":
            D13_EXPECTED_D7_SCHEMA_SHA256,

        "schema_sha256_matches":
            schema_sha256
            == D13_EXPECTED_D7_SCHEMA_SHA256,

        "before_metadata":
            before_metadata,

        "after_metadata":
            after_metadata,

        "artifact_sizes_unchanged":
            all(
                before_metadata[name]["size_bytes"]
                == after_metadata[name]["size_bytes"]
                for name in artifact_paths
            ),

        "artifact_mtimes_unchanged":
            all(
                before_metadata[name]["mtime_ns"]
                == after_metadata[name]["mtime_ns"]
                for name in artifact_paths
            ),

        "model_loaded":
            False,

        "model_retrained":
            False,

        "preprocessor_loaded":
            False,

        "preprocessor_refitted":
            False,

        "predictions_generated":
            False,

        "threshold_retuned":
            False,

        "locked_test_accessed":
            False,

        "locked_test_evaluated":
            False,

        "deployment_authorized":
            False,
    }


# ============================================================
# D13.11 — FROZEN ARTIFACT IDENTITY VALIDATION
# ============================================================

def validate_d13_frozen_artifact_identity(
    identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate that the physical artifacts currently on disk are exactly
    the frozen artifacts expected by the D13 registry contract.
    """

    if identity is None:
        identity = build_d13_frozen_artifact_identity()

    checks = {
        "model_artifact_exists":
            identity["model_artifact_exists"],

        "preprocessor_artifact_exists":
            identity["preprocessor_artifact_exists"],

        "schema_artifact_exists":
            identity["schema_artifact_exists"],

        "model_sha256_matches":
            identity["model_sha256_matches"],

        "preprocessor_sha256_matches":
            identity["preprocessor_sha256_matches"],

        "schema_sha256_matches":
            identity["schema_sha256_matches"],

        "artifact_sizes_unchanged":
            identity["artifact_sizes_unchanged"],

        "artifact_mtimes_unchanged":
            identity["artifact_mtimes_unchanged"],

        "model_not_loaded":
            identity["model_loaded"] is False,

        "model_not_retrained":
            identity["model_retrained"] is False,

        "preprocessor_not_loaded":
            identity["preprocessor_loaded"] is False,

        "preprocessor_not_refitted":
            identity["preprocessor_refitted"] is False,

        "predictions_not_generated":
            identity["predictions_generated"] is False,

        "threshold_not_retuned":
            identity["threshold_retuned"] is False,

        "locked_test_not_accessed":
            identity["locked_test_accessed"] is False,

        "locked_test_not_evaluated":
            identity["locked_test_evaluated"] is False,

        "deployment_not_authorized":
            identity["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **identity,

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "validation_status":
            "PASS"
            if not failed_checks
            else "FAIL",
    }


# ============================================================
# D13.12 — EXECUTABLE ARTIFACT IDENTITY CHECK
# ============================================================

def print_d13_frozen_artifact_identity() -> None:
    """
    Print the governed D13 frozen-artifact integrity result.
    """

    result = validate_d13_frozen_artifact_identity()

    print("=" * 72)
    print("D13 FROZEN ARTIFACT IDENTITY VERIFICATION")
    print("=" * 72)

    for key in (
        "validation_status",
        "model_artifact_path",
        "model_sha256",
        "model_sha256_matches",
        "preprocessor_artifact_path",
        "preprocessor_sha256",
        "preprocessor_sha256_matches",
        "schema_artifact_path",
        "schema_sha256",
        "schema_sha256_matches",
        "artifact_sizes_unchanged",
        "artifact_mtimes_unchanged",
        "model_loaded",
        "preprocessor_loaded",
        "predictions_generated",
        "locked_test_accessed",
        "locked_test_evaluated",
        "deployment_authorized",
        "failed_checks",
    ):
        print(f"{key}: {result[key]}")


# ============================================================
# D13.09 — EXECUTABLE STATIC CONTRACT CHECK
# ============================================================

def print_d13_static_registry_boundary() -> None:
    """
    Print a concise executable validation of the D13 static
    registry and artifact-freeze governance boundary.
    """

    result = validate_d13_static_registry_boundary()

    print("=" * 72)
    print("D13 MODEL REGISTRY & ARTIFACT FREEZE — STATIC BOUNDARY")
    print("=" * 72)

    for key in (
        "validation_status",
        "source_git_commit",
        "model_name",
        "expected_model_sha256",
        "expected_d7_preprocessor_sha256",
        "expected_d7_schema_sha256",
        "development_threshold",
        "locked_test_accessed",
        "locked_test_evaluated",
        "deployment_authorized",
        "failed_checks",
    ):
        print(f"{key}: {result[key]}")



# ============================================================
# D13.13 — REGISTERED CLINICAL-AI CANDIDATE IDENTITY
# ============================================================

D13_REGISTRY_ID: Final[str] = "DIABETES_READMISSION_XGB_D13_V1"
D13_MODEL_VERSION: Final[str] = "1.0.0"
D13_CANDIDATE_STATUS: Final[str] = (
    "FROZEN_DEVELOPMENT_CANDIDATE_PENDING_D14_LOCKED_TEST"
)


def build_d13_registered_candidate_identity() -> dict[str, Any]:
    """Bind frozen components into one governed candidate identity."""
    static_validation = validate_d13_static_registry_boundary()
    artifact_validation = validate_d13_frozen_artifact_identity()

    if static_validation["validation_status"] != "PASS":
        raise RuntimeError("D13 static registry boundary failed validation.")
    if artifact_validation["validation_status"] != "PASS":
        raise RuntimeError("D13 frozen artifact identity verification failed.")

    metadata_path = Path(d8.D8_SELECTED_MODEL_METADATA_PATH)
    if not metadata_path.is_file():
        raise FileNotFoundError("D8 selected-model metadata artifact is missing.")

    before = {
        "size_bytes": metadata_path.stat().st_size,
        "mtime_ns": metadata_path.stat().st_mtime_ns,
    }
    metadata_sha256 = _d13_sha256(metadata_path)
    after = {
        "size_bytes": metadata_path.stat().st_size,
        "mtime_ns": metadata_path.stat().st_mtime_ns,
    }

    identity_material = "|".join(
        (
            D13_REGISTRY_ID,
            D13_MODEL_VERSION,
            D13_SOURCE_LIFECYCLE_STAGE,
            D13_SOURCE_GIT_COMMIT,
            artifact_validation["model_sha256"],
            metadata_sha256,
            artifact_validation["preprocessor_sha256"],
            artifact_validation["schema_sha256"],
            str(D13_EXPECTED_DEVELOPMENT_THRESHOLD),
            str(D13_EXPECTED_SOURCE_FEATURE_COUNT),
            str(D13_EXPECTED_TRANSFORMED_FEATURE_COUNT),
        )
    )
    candidate_system_sha256 = hashlib.sha256(
        identity_material.encode("utf-8")
    ).hexdigest().upper()

    return {
        "registry_id": D13_REGISTRY_ID,
        "model_version": D13_MODEL_VERSION,
        "candidate_status": D13_CANDIDATE_STATUS,
        "model_name": D13_EXPECTED_MODEL_NAME,
        "source_lifecycle_stage": D13_SOURCE_LIFECYCLE_STAGE,
        "source_git_commit": D13_SOURCE_GIT_COMMIT,
        "model_artifact_path": artifact_validation["model_artifact_path"],
        "model_sha256": artifact_validation["model_sha256"],
        "model_sha256_verified": artifact_validation["model_sha256_matches"],
        "model_metadata_path": str(metadata_path),
        "model_metadata_sha256": metadata_sha256,
        "expected_model_metadata_sha256": D13_EXPECTED_D8_MODEL_METADATA_SHA256,
        "model_metadata_sha256_verified":
            metadata_sha256 == D13_EXPECTED_D8_MODEL_METADATA_SHA256,
        "model_metadata_size_unchanged":
            before["size_bytes"] == after["size_bytes"],
        "model_metadata_mtime_unchanged":
            before["mtime_ns"] == after["mtime_ns"],
        "preprocessor_artifact_path": artifact_validation["preprocessor_artifact_path"],
        "preprocessor_sha256": artifact_validation["preprocessor_sha256"],
        "preprocessor_sha256_verified": artifact_validation["preprocessor_sha256_matches"],
        "transformed_feature_schema_path": artifact_validation["schema_artifact_path"],
        "transformed_feature_schema_sha256": artifact_validation["schema_sha256"],
        "transformed_feature_schema_sha256_verified":
            artifact_validation["schema_sha256_matches"],
        "source_feature_count": D13_EXPECTED_SOURCE_FEATURE_COUNT,
        "transformed_feature_count": D13_EXPECTED_TRANSFORMED_FEATURE_COUNT,
        "development_operating_threshold": D13_EXPECTED_DEVELOPMENT_THRESHOLD,
        "candidate_system_sha256": candidate_system_sha256,
        "identity_material": identity_material,
        "model_loaded": False,
        "model_retrained": False,
        "preprocessor_loaded": False,
        "preprocessor_refitted": False,
        "predictions_generated": False,
        "threshold_retuned": False,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }


# ============================================================
# D13.14 — REGISTERED CANDIDATE IDENTITY VALIDATION
# ============================================================

def validate_d13_registered_candidate_identity(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the governed identity of the registered D13 candidate."""
    if candidate is None:
        candidate = build_d13_registered_candidate_identity()

    checks = {
        "registry_id_defined": candidate["registry_id"] == D13_REGISTRY_ID,
        "model_version_defined": candidate["model_version"] == D13_MODEL_VERSION,
        "candidate_pending_d14": candidate["candidate_status"] == D13_CANDIDATE_STATUS,
        "source_stage_is_d12": candidate["source_lifecycle_stage"] == "D12",
        "source_commit_matches_d12_freeze":
            candidate["source_git_commit"] == D13_SOURCE_GIT_COMMIT,
        "model_identity_verified": candidate["model_sha256_verified"],
        "model_metadata_identity_verified": candidate["model_metadata_sha256_verified"],
        "preprocessor_identity_verified": candidate["preprocessor_sha256_verified"],
        "schema_identity_verified":
            candidate["transformed_feature_schema_sha256_verified"],
        "model_metadata_size_unchanged": candidate["model_metadata_size_unchanged"],
        "model_metadata_mtime_unchanged": candidate["model_metadata_mtime_unchanged"],
        "source_feature_count_is_10":
            candidate["source_feature_count"] == D13_EXPECTED_SOURCE_FEATURE_COUNT,
        "transformed_feature_count_is_49":
            candidate["transformed_feature_count"] == D13_EXPECTED_TRANSFORMED_FEATURE_COUNT,
        "development_threshold_is_frozen":
            candidate["development_operating_threshold"] == D13_EXPECTED_DEVELOPMENT_THRESHOLD,
        "candidate_system_sha256_present":
            len(candidate["candidate_system_sha256"]) == 64,
        "model_not_loaded": candidate["model_loaded"] is False,
        "model_not_retrained": candidate["model_retrained"] is False,
        "preprocessor_not_loaded": candidate["preprocessor_loaded"] is False,
        "preprocessor_not_refitted": candidate["preprocessor_refitted"] is False,
        "predictions_not_generated": candidate["predictions_generated"] is False,
        "threshold_not_retuned": candidate["threshold_retuned"] is False,
        "locked_test_not_accessed": candidate["locked_test_accessed"] is False,
        "locked_test_not_evaluated": candidate["locked_test_evaluated"] is False,
        "deployment_not_authorized": candidate["deployment_authorized"] is False,
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    return {
        **candidate,
        "checks": checks,
        "failed_checks": failed_checks,
        "validation_status": "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D13.15 — EXECUTABLE REGISTERED CANDIDATE CHECK
# ============================================================

def print_d13_registered_candidate_identity() -> None:
    """Print the governed D13 registered-candidate identity."""
    result = validate_d13_registered_candidate_identity()
    print("=" * 72)
    print("D13 REGISTERED CLINICAL-AI CANDIDATE IDENTITY")
    print("=" * 72)
    for key in (
        "validation_status",
        "registry_id",
        "model_version",
        "candidate_status",
        "source_lifecycle_stage",
        "source_git_commit",
        "model_sha256",
        "model_metadata_sha256",
        "preprocessor_sha256",
        "transformed_feature_schema_sha256",
        "source_feature_count",
        "transformed_feature_count",
        "development_operating_threshold",
        "candidate_system_sha256",
        "model_retrained",
        "preprocessor_refitted",
        "predictions_generated",
        "threshold_retuned",
        "locked_test_accessed",
        "locked_test_evaluated",
        "deployment_authorized",
        "failed_checks",
    ):
        print(f"{key}: {result[key]}")


# ============================================================
# D13.16 — AUTHORITATIVE SOURCE FEATURE CONTRACT
# ============================================================

def build_d13_source_feature_contract() -> dict[str, Any]:
    """
    Capture the authoritative ordered D7 source-feature contract.

    The contract is consumed directly from the frozen D7 preprocessing
    interface. D13 does not redefine, reorder, engineer, or transform
    the features.
    """

    primary_features = tuple(d7.PRIMARY_CANDIDATE_FEATURES)
    categorical_features = tuple(d7.CATEGORICAL_FEATURES)
    numeric_features = tuple(d7.NUMERIC_FEATURES)

    contract_payload = {
        "primary_candidate_features": list(primary_features),
        "categorical_features": list(categorical_features),
        "numeric_features": list(numeric_features),
        "expected_raw_feature_count":
            int(d7.EXPECTED_D7_RAW_FEATURE_COUNT),
        "expected_transformed_feature_count":
            int(d7.EXPECTED_D7_TRANSFORMED_FEATURE_COUNT),
    }

    canonical_contract_json = json.dumps(
        contract_payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    source_feature_contract_sha256 = hashlib.sha256(
        canonical_contract_json.encode("utf-8")
    ).hexdigest().upper()

    return {
        **contract_payload,
        "canonical_contract_json":
            canonical_contract_json,
        "source_feature_contract_sha256":
            source_feature_contract_sha256,
        "source_interface":
            "src.features.preprocessing",
        "source_definition":
            "PRIMARY_CANDIDATE_FEATURES",
        "feature_order_preserved":
            True,
        "feature_contract_redefined":
            False,
        "feature_engineering_performed":
            False,
        "locked_test_accessed":
            False,
    }


def validate_d13_source_feature_contract(
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the authoritative D7 source-feature contract for D13.
    """

    if contract is None:
        contract = build_d13_source_feature_contract()

    primary_features = contract["primary_candidate_features"]
    categorical_features = contract["categorical_features"]
    numeric_features = contract["numeric_features"]

    checks = {
        "raw_feature_count_matches_d7":
            len(primary_features)
            == int(d7.EXPECTED_D7_RAW_FEATURE_COUNT)
            == D13_EXPECTED_SOURCE_FEATURE_COUNT,

        "transformed_feature_count_matches_d7":
            contract["expected_transformed_feature_count"]
            == int(d7.EXPECTED_D7_TRANSFORMED_FEATURE_COUNT)
            == D13_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "categorical_numeric_partition_complete":
            len(categorical_features) + len(numeric_features)
            == len(primary_features),

        "categorical_features_preserve_primary_order":
            categorical_features
            == [
                feature
                for feature in primary_features
                if feature in set(categorical_features)
            ],

        "numeric_features_preserve_primary_order":
            numeric_features
            == [
                feature
                for feature in primary_features
                if feature in set(numeric_features)
            ],

        "categorical_numeric_disjoint":
            set(categorical_features).isdisjoint(
                set(numeric_features)
            ),

        "categorical_numeric_union_matches_primary":
            set(categorical_features).union(
                set(numeric_features)
            )
            == set(primary_features),

        "source_feature_names_unique":
            len(primary_features)
            == len(set(primary_features)),

        "feature_order_preserved":
            contract["feature_order_preserved"] is True,

        "feature_contract_not_redefined":
            contract["feature_contract_redefined"] is False,

        "feature_engineering_not_performed":
            contract["feature_engineering_performed"] is False,

        "contract_sha256_present":
            len(contract["source_feature_contract_sha256"]) == 64,

        "locked_test_not_accessed":
            contract["locked_test_accessed"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **contract,
        "checks":
            checks,
        "failed_checks":
            failed_checks,
        "validation_status":
            "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D13.17 — FINAL REGISTERED SYSTEM FINGERPRINT
# ============================================================

def build_d13_final_registered_candidate_identity() -> dict[str, Any]:
    """
    Bind the authoritative ordered source-feature contract into the
    final D13 registered candidate-system identity.

    This supersedes the earlier intermediate candidate fingerprint
    produced before the explicit feature-contract hash was available.
    """

    candidate = validate_d13_registered_candidate_identity()
    feature_contract = validate_d13_source_feature_contract()

    if candidate["validation_status"] != "PASS":
        raise RuntimeError(
            "D13 final registration blocked because the registered "
            "candidate identity failed validation."
        )

    if feature_contract["validation_status"] != "PASS":
        raise RuntimeError(
            "D13 final registration blocked because the authoritative "
            "source-feature contract failed validation."
        )

    intermediate_candidate_system_sha256 = (
        candidate["candidate_system_sha256"]
    )

    final_identity_material = "|".join(
        (
            D13_REGISTRY_ID,
            D13_MODEL_VERSION,
            D13_SOURCE_LIFECYCLE_STAGE,
            D13_SOURCE_GIT_COMMIT,
            candidate["model_sha256"],
            candidate["model_metadata_sha256"],
            candidate["preprocessor_sha256"],
            candidate["transformed_feature_schema_sha256"],
            feature_contract["source_feature_contract_sha256"],
            str(candidate["development_operating_threshold"]),
            str(candidate["source_feature_count"]),
            str(candidate["transformed_feature_count"]),
        )
    )

    final_candidate_system_sha256 = hashlib.sha256(
        final_identity_material.encode("utf-8")
    ).hexdigest().upper()

    return {
        **candidate,
        "source_feature_contract":
            feature_contract["primary_candidate_features"],
        "categorical_features":
            feature_contract["categorical_features"],
        "numeric_features":
            feature_contract["numeric_features"],
        "source_feature_contract_sha256":
            feature_contract["source_feature_contract_sha256"],
        "source_feature_contract_validation_status":
            feature_contract["validation_status"],
        "intermediate_candidate_system_sha256":
            intermediate_candidate_system_sha256,
        "candidate_system_sha256":
            final_candidate_system_sha256,
        "final_identity_material":
            final_identity_material,
        "feature_contract_bound_to_system_identity":
            True,
        "locked_test_accessed":
            False,
        "locked_test_evaluated":
            False,
        "deployment_authorized":
            False,
    }


def validate_d13_final_registered_candidate_identity(
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Validate the final D13 candidate identity after binding the
    authoritative ordered source-feature contract.
    """

    if candidate is None:
        candidate = build_d13_final_registered_candidate_identity()

    checks = {
        "base_candidate_validation_passed":
            candidate["validation_status"] == "PASS",

        "feature_contract_validation_passed":
            candidate["source_feature_contract_validation_status"]
            == "PASS",

        "feature_contract_bound":
            candidate["feature_contract_bound_to_system_identity"]
            is True,

        "source_feature_count_is_10":
            len(candidate["source_feature_contract"])
            == D13_EXPECTED_SOURCE_FEATURE_COUNT,

        "categorical_feature_count_is_5":
            len(candidate["categorical_features"]) == 5,

        "numeric_feature_count_is_5":
            len(candidate["numeric_features"]) == 5,

        "source_feature_contract_sha256_present":
            len(candidate["source_feature_contract_sha256"]) == 64,

        "final_candidate_system_sha256_present":
            len(candidate["candidate_system_sha256"]) == 64,

        "final_fingerprint_differs_from_intermediate":
            candidate["candidate_system_sha256"]
            != candidate["intermediate_candidate_system_sha256"],

        "model_sha256_still_frozen":
            candidate["model_sha256"]
            == D13_EXPECTED_MODEL_SHA256,

        "model_metadata_sha256_still_frozen":
            candidate["model_metadata_sha256"]
            == D13_EXPECTED_D8_MODEL_METADATA_SHA256,

        "preprocessor_sha256_still_frozen":
            candidate["preprocessor_sha256"]
            == D13_EXPECTED_D7_PREPROCESSOR_SHA256,

        "schema_sha256_still_frozen":
            candidate["transformed_feature_schema_sha256"]
            == D13_EXPECTED_D7_SCHEMA_SHA256,

        "threshold_still_frozen":
            candidate["development_operating_threshold"]
            == D13_EXPECTED_DEVELOPMENT_THRESHOLD,

        "model_not_retrained":
            candidate["model_retrained"] is False,

        "preprocessor_not_refitted":
            candidate["preprocessor_refitted"] is False,

        "predictions_not_generated":
            candidate["predictions_generated"] is False,

        "threshold_not_retuned":
            candidate["threshold_retuned"] is False,

        "locked_test_not_accessed":
            candidate["locked_test_accessed"] is False,

        "locked_test_not_evaluated":
            candidate["locked_test_evaluated"] is False,

        "deployment_not_authorized":
            candidate["deployment_authorized"] is False,
    }

    failed_checks = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    return {
        **candidate,
        "final_checks":
            checks,
        "final_failed_checks":
            failed_checks,
        "final_validation_status":
            "PASS" if not failed_checks else "FAIL",
    }


# ============================================================
# D13.18 — EXECUTABLE FINAL REGISTRY IDENTITY CHECK
# ============================================================

def print_d13_final_registered_candidate_identity() -> None:
    """
    Print the final D13 candidate identity with the authoritative
    source-feature contract cryptographically bound.
    """

    result = validate_d13_final_registered_candidate_identity()

    print("=" * 72)
    print("D13 FINAL REGISTERED CLINICAL-AI SYSTEM IDENTITY")
    print("=" * 72)

    for key in (
        "final_validation_status",
        "registry_id",
        "model_version",
        "candidate_status",
        "source_git_commit",
        "source_feature_contract",
        "categorical_features",
        "numeric_features",
        "source_feature_contract_sha256",
        "model_sha256",
        "model_metadata_sha256",
        "preprocessor_sha256",
        "transformed_feature_schema_sha256",
        "development_operating_threshold",
        "intermediate_candidate_system_sha256",
        "candidate_system_sha256",
        "feature_contract_bound_to_system_identity",
        "model_retrained",
        "preprocessor_refitted",
        "predictions_generated",
        "threshold_retuned",
        "locked_test_accessed",
        "locked_test_evaluated",
        "deployment_authorized",
        "final_failed_checks",
    ):
        print(f"{key}: {result[key]}")


# ============================================================
# D13.19 — SOFTWARE ENVIRONMENT PROVENANCE
# ============================================================

D13_VERIFIED_SOFTWARE_ENVIRONMENT: Final[dict[str, str]] = {
    "python": "3.13.15",
    "platform": "Windows-10-10.0.19045-SP0",
    "numpy": "2.5.3",
    "pandas": "3.0.5",
    "scikit_learn": "1.9.1",
    "xgboost": "3.4.1",
    "joblib": "1.6.0",
    "shap": "0.52.0",
    "git": "2.55.0.windows.3",
}


def build_d13_software_environment_provenance() -> dict[str, Any]:
    """Build deterministic, evidence-derived software provenance."""
    canonical_json = json.dumps(
        D13_VERIFIED_SOFTWARE_ENVIRONMENT,
        sort_keys=True,
        separators=(",", ":"),
    )
    fingerprint = hashlib.sha256(
        canonical_json.encode("utf-8")
    ).hexdigest().upper()
    return {
        "software_environment": dict(D13_VERIFIED_SOFTWARE_ENVIRONMENT),
        "canonical_environment_json": canonical_json,
        "software_environment_sha256": fingerprint,
        "environment_record_source": "verified_project_terminal",
        "candidate_system_identity_changed": False,
        "locked_test_accessed": False,
    }


def validate_d13_software_environment_provenance(
    record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if record is None:
        record = build_d13_software_environment_provenance()
    required = {
        "python", "platform", "numpy", "pandas", "scikit_learn",
        "xgboost", "joblib", "shap", "git",
    }
    checks = {
        "all_required_components_present":
            set(record["software_environment"]) == required,
        "environment_sha256_present":
            len(record["software_environment_sha256"]) == 64,
        "candidate_identity_not_changed":
            record["candidate_system_identity_changed"] is False,
        "locked_test_not_accessed":
            record["locked_test_accessed"] is False,
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        **record,
        "checks": checks,
        "failed_checks": failed,
        "validation_status": "PASS" if not failed else "FAIL",
    }


# ============================================================
# D13.20 — LIFECYCLE PROVENANCE & ARTIFACT INVENTORY
# ============================================================

def build_d13_registry_evidence_bundle() -> dict[str, Any]:
    """Assemble the read-only D13 registry evidence bundle."""
    system = validate_d13_final_registered_candidate_identity()
    environment = validate_d13_software_environment_provenance()

    if system["final_validation_status"] != "PASS":
        raise RuntimeError("Final D13 system identity failed validation.")
    if environment["validation_status"] != "PASS":
        raise RuntimeError("D13 software provenance failed validation.")

    artifact_inventory = [
        {
            "component": "selected_model",
            "path": system["model_artifact_path"],
            "sha256": system["model_sha256"],
            "frozen": True,
        },
        {
            "component": "model_metadata",
            "path": system["model_metadata_path"],
            "sha256": system["model_metadata_sha256"],
            "frozen": True,
        },
        {
            "component": "preprocessor",
            "path": system["preprocessor_artifact_path"],
            "sha256": system["preprocessor_sha256"],
            "frozen": True,
        },
        {
            "component": "transformed_feature_schema",
            "path": system["transformed_feature_schema_path"],
            "sha256": system["transformed_feature_schema_sha256"],
            "frozen": True,
        },
        {
            "component": "source_feature_contract",
            "path": "authoritative:D7.PRIMARY_CANDIDATE_FEATURES",
            "sha256": system["source_feature_contract_sha256"],
            "frozen": True,
        },
    ]

    lifecycle_provenance = {
        "D7": "governed_preprocessing",
        "D8": "model_development_and_selection",
        "D9": "clinical_utility_and_threshold_governance",
        "D10": "fairness_and_subgroup_evaluation",
        "D11": "robustness_and_transportability",
        "D12": "explainability_and_model_interpretation_governance",
        "D13": "model_registry_and_artifact_freeze",
        "D13_source_git_commit": D13_SOURCE_GIT_COMMIT,
        "next_stage": D13_NEXT_LIFECYCLE_STAGE,
    }

    change_control = {
        "registered_candidate_mutated": False,
        "model_retrained": False,
        "preprocessor_refitted": False,
        "feature_contract_changed": False,
        "threshold_retuned": False,
        "probability_recalibrated": False,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
        "post_freeze_change_requires_new_identity": True,
    }

    return {
        "registry_id": system["registry_id"],
        "model_version": system["model_version"],
        "candidate_status": system["candidate_status"],
        "candidate_system_sha256": system["candidate_system_sha256"],
        "source_feature_contract_sha256":
            system["source_feature_contract_sha256"],
        "development_operating_threshold":
            system["development_operating_threshold"],
        "artifact_inventory": artifact_inventory,
        "software_environment":
            environment["software_environment"],
        "software_environment_sha256":
            environment["software_environment_sha256"],
        "lifecycle_provenance": lifecycle_provenance,
        "change_control_status": change_control,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }


def validate_d13_registry_evidence_bundle(
    bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if bundle is None:
        bundle = build_d13_registry_evidence_bundle()

    inventory = bundle["artifact_inventory"]
    change = bundle["change_control_status"]

    checks = {
        "registry_id_present": bool(bundle["registry_id"]),
        "model_version_present": bool(bundle["model_version"]),
        "candidate_system_sha256_present":
            len(bundle["candidate_system_sha256"]) == 64,
        "source_feature_contract_sha256_present":
            len(bundle["source_feature_contract_sha256"]) == 64,
        "artifact_inventory_complete":
            {x["component"] for x in inventory}
            == {
                "selected_model",
                "model_metadata",
                "preprocessor",
                "transformed_feature_schema",
                "source_feature_contract",
            },
        "all_inventory_components_frozen":
            all(x["frozen"] is True for x in inventory),
        "software_environment_sha256_present":
            len(bundle["software_environment_sha256"]) == 64,
        "lifecycle_reaches_d13":
            bundle["lifecycle_provenance"]["D13"]
            == "model_registry_and_artifact_freeze",
        "next_stage_is_d14":
            bundle["lifecycle_provenance"]["next_stage"]
            == "D14_LOCKED_TEST_EVALUATION",
        "candidate_not_mutated":
            change["registered_candidate_mutated"] is False,
        "change_control_required":
            change["post_freeze_change_requires_new_identity"] is True,
        "locked_test_not_accessed":
            bundle["locked_test_accessed"] is False,
        "locked_test_not_evaluated":
            bundle["locked_test_evaluated"] is False,
        "deployment_not_authorized":
            bundle["deployment_authorized"] is False,
    }

    failed = [k for k, v in checks.items() if not v]
    return {
        **bundle,
        "checks": checks,
        "failed_checks": failed,
        "validation_status": "PASS" if not failed else "FAIL",
    }


# ============================================================
# D13.21 — FORMAL REGISTRY RECORD & FREEZE MANIFEST
# ============================================================

def build_d13_formal_registry_record() -> dict[str, Any]:
    """Build the canonical in-memory D13 registry record."""
    bundle = validate_d13_registry_evidence_bundle()
    if bundle["validation_status"] != "PASS":
        raise RuntimeError("D13 registry evidence bundle failed validation.")

    return {
        "stage_id": D13_STAGE_ID,
        "stage_name": D13_STAGE_NAME,
        "registry_id": bundle["registry_id"],
        "model_version": bundle["model_version"],
        "candidate_status": bundle["candidate_status"],
        "candidate_system_sha256": bundle["candidate_system_sha256"],
        "source_feature_contract_sha256":
            bundle["source_feature_contract_sha256"],
        "development_operating_threshold":
            bundle["development_operating_threshold"],
        "artifact_inventory": bundle["artifact_inventory"],
        "software_environment": bundle["software_environment"],
        "software_environment_sha256":
            bundle["software_environment_sha256"],
        "lifecycle_provenance": bundle["lifecycle_provenance"],
        "change_control_status": bundle["change_control_status"],
        "evaluation_partition": D13_EVALUATION_PARTITION,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }


def build_d13_freeze_manifest() -> dict[str, Any]:
    """Build a deterministic freeze manifest without writing artifacts."""
    record = build_d13_formal_registry_record()
    canonical_record_json = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    manifest_sha256 = hashlib.sha256(
        canonical_record_json.encode("utf-8")
    ).hexdigest().upper()
    return {
        "registry_record": record,
        "canonical_registry_record_json": canonical_record_json,
        "freeze_manifest_sha256": manifest_sha256,
        "freeze_status": "FROZEN_PENDING_D14_LOCKED_TEST",
        "post_freeze_change_requires_new_identity": True,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }


# ============================================================
# D13.22 — REGISTRY GATE DECISION
# ============================================================

def build_d13_registry_gate_decision() -> dict[str, Any]:
    """Issue the D13 governance gate for progression to D14 only."""
    bundle = validate_d13_registry_evidence_bundle()
    manifest = build_d13_freeze_manifest()

    failed_checks = list(bundle["failed_checks"])
    manifest_valid = len(manifest["freeze_manifest_sha256"]) == 64
    if not manifest_valid:
        failed_checks.append("freeze_manifest_sha256_invalid")

    passed = not failed_checks

    return {
        "stage_id": D13_STAGE_ID,
        "validation_status": "PASS" if passed else "FAIL",
        "registry_id": bundle["registry_id"],
        "candidate_system_sha256": bundle["candidate_system_sha256"],
        "freeze_manifest_sha256": manifest["freeze_manifest_sha256"],
        "gate_disposition":
            "PASS_PROGRESS_TO_D14_LOCKED_TEST_EVALUATION"
            if passed
            else "FAIL_REMAIN_IN_D13",
        "progression_to_d14_authorized": passed,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
        "failed_checks": failed_checks,
    }


# ============================================================
# D13.23 — EXECUTABLE REGISTRY EVIDENCE & GATE CHECK
# ============================================================

def print_d13_registry_evidence_and_gate() -> None:
    """Print the final D13 registry evidence and governance gate."""
    environment = validate_d13_software_environment_provenance()
    bundle = validate_d13_registry_evidence_bundle()
    manifest = build_d13_freeze_manifest()
    gate = build_d13_registry_gate_decision()

    print("=" * 72)
    print("D13 SOFTWARE ENVIRONMENT PROVENANCE")
    print("=" * 72)
    print(f"validation_status: {environment['validation_status']}")
    print(f"software_environment: {environment['software_environment']}")
    print(
        "software_environment_sha256: "
        f"{environment['software_environment_sha256']}"
    )
    print(f"failed_checks: {environment['failed_checks']}")
    print()

    print("=" * 72)
    print("D13 FORMAL REGISTRY & FREEZE EVIDENCE")
    print("=" * 72)
    print(f"validation_status: {bundle['validation_status']}")
    print(f"registry_id: {bundle['registry_id']}")
    print(f"candidate_system_sha256: {bundle['candidate_system_sha256']}")
    print(
        "source_feature_contract_sha256: "
        f"{bundle['source_feature_contract_sha256']}"
    )
    print(f"artifact_inventory_count: {len(bundle['artifact_inventory'])}")
    print(
        "software_environment_sha256: "
        f"{bundle['software_environment_sha256']}"
    )
    print(f"freeze_manifest_sha256: {manifest['freeze_manifest_sha256']}")
    print(f"failed_checks: {bundle['failed_checks']}")
    print()

    print("=" * 72)
    print("D13 REGISTRY & ARTIFACT FREEZE — GATE DECISION")
    print("=" * 72)
    for key in (
        "validation_status",
        "registry_id",
        "candidate_system_sha256",
        "freeze_manifest_sha256",
        "gate_disposition",
        "progression_to_d14_authorized",
        "locked_test_accessed",
        "locked_test_evaluated",
        "deployment_authorized",
        "failed_checks",
    ):
        print(f"{key}: {gate[key]}")


if __name__ == "__main__":
    print_d13_static_registry_boundary()
    print()
    print_d13_frozen_artifact_identity()
    print()
    print_d13_registered_candidate_identity()
    print()
    print_d13_final_registered_candidate_identity()
    print()
    print_d13_registry_evidence_and_gate()
