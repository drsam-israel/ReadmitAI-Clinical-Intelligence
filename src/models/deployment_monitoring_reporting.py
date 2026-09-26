# ============================================================
# D15 — DEPLOYMENT & MONITORING DESIGN
# FORMAL EVIDENCE & GOVERNANCE REPORTING
# ============================================================
#
# Purpose
# -------
# Generate the reproducible evidence package for D15 from the
# authoritative, already-validated D15 runtime controls.
#
# This module does NOT:
# - retrain the model
# - refit preprocessing
# - retune the operating threshold
# - recalibrate the model
# - modify D13 candidate identity
# - modify D14 locked-test results
# - authorize production deployment
#
# D15 reporting converts validated engineering and governance
# controls into persistent, auditable evidence.
# ============================================================


from __future__ import annotations

from pathlib import Path
from typing import Final

import src.models.deployment_monitoring as d15


# ============================================================
# D15-R01.01 — REPORTING STAGE IDENTITY
# ============================================================

D15_REPORTING_STAGE_ID: Final[str] = "D15"

D15_REPORTING_STAGE_NAME: Final[str] = (
    "DEPLOYMENT_AND_MONITORING_DESIGN"
)

D15_REPORTING_CLASSIFICATION: Final[str] = (
    "PRE_DEPLOYMENT_ARCHITECTURE_AND_MONITORING_DESIGN"
)

D15_REPORTING_IMPLEMENTATION_STATUS: Final[str] = (
    "RESEARCH_VALIDATION_PROTOTYPE_ONLY"
)

D15_REPORTING_PRODUCTION_STATUS: Final[str] = (
    "NOT_AUTHORIZED_FOR_PRODUCTION"
)

D15_REPORTING_SOURCE_STAGE: Final[str] = "D14"

D15_REPORTING_SOURCE_COMMIT: Final[str] = "1e003ee"

D15_REPORTING_NEXT_STAGE: Final[str] = "D16"


# ============================================================
# D15-R01.02 — PROJECT ROOT
# ============================================================

D15_REPORTING_MODULE_PATH: Final[Path] = (
    Path(__file__).resolve()
)

D15_PROJECT_ROOT: Final[Path] = (
    D15_REPORTING_MODULE_PATH.parents[2]
)


# ============================================================
# D15-R01.03 — EVIDENCE DIRECTORIES
# ============================================================

D15_MANIFEST_DIR: Final[Path] = (
    D15_PROJECT_ROOT
    / "artifacts"
    / "manifests"
)

D15_GOVERNANCE_REPORT_DIR: Final[Path] = (
    D15_PROJECT_ROOT
    / "reports"
    / "governance"
)

D15_TABLE_REPORT_DIR: Final[Path] = (
    D15_PROJECT_ROOT
    / "reports"
    / "tables"
)


# ============================================================
# D15-R01.04 — AUTHORITATIVE EVIDENCE ARTIFACT REGISTRY
# ============================================================

D15_EVIDENCE_ARTIFACT_REGISTRY: Final[dict[str, Path]] = {

    # --------------------------------------------------------
    # Manifest
    # --------------------------------------------------------

    "manifest": (
        D15_MANIFEST_DIR
        / "D15_deployment_monitoring_manifest.yaml"
    ),

    # --------------------------------------------------------
    # Governance documents
    # --------------------------------------------------------

    "governance_contract": (
        D15_GOVERNANCE_REPORT_DIR
        / "D15_deployment_monitoring_contract.md"
    ),

    "architecture_design": (
        D15_GOVERNANCE_REPORT_DIR
        / "D15_deployment_architecture_design.md"
    ),

    "monitoring_plan": (
        D15_GOVERNANCE_REPORT_DIR
        / "D15_monitoring_and_drift_control_plan.md"
    ),

    "operational_governance": (
        D15_GOVERNANCE_REPORT_DIR
        / "D15_incident_change_rollback_continuity_plan.md"
    ),

    "deployment_readiness_assessment": (
        D15_GOVERNANCE_REPORT_DIR
        / "D15_deployment_readiness_assessment.md"
    ),

    "gate_decision": (
        D15_GOVERNANCE_REPORT_DIR
        / "D15_deployment_monitoring_gate_decision.md"
    ),

    # --------------------------------------------------------
    # Structured evidence tables
    # --------------------------------------------------------

    "architecture_controls": (
        D15_TABLE_REPORT_DIR
        / "D15_architecture_controls.csv"
    ),

    "monitoring_control_catalogue": (
        D15_TABLE_REPORT_DIR
        / "D15_monitoring_control_catalogue.csv"
    ),

    "quantitative_reference_bands": (
        D15_TABLE_REPORT_DIR
        / "D15_quantitative_reference_bands.csv"
    ),

    "bootstrap_discrimination_uncertainty": (
        D15_TABLE_REPORT_DIR
        / "D15_bootstrap_discrimination_uncertainty.csv"
    ),

    "known_risk_slice_references": (
        D15_TABLE_REPORT_DIR
        / "D15_known_risk_slice_references.csv"
    ),

    "escalation_trigger_catalogue": (
        D15_TABLE_REPORT_DIR
        / "D15_escalation_trigger_catalogue.csv"
    ),

    "residual_risk_traceability": (
        D15_TABLE_REPORT_DIR
        / "D15_residual_risk_traceability.csv"
    ),

    "operational_control_evidence": (
        D15_TABLE_REPORT_DIR
        / "D15_operational_control_evidence.csv"
    ),
}


# ============================================================
# D15-R01.05 — REQUIRED EVIDENCE ARTIFACT KEYS
# ============================================================

D15_REQUIRED_EVIDENCE_ARTIFACT_KEYS: Final[tuple[str, ...]] = (
    "manifest",
    "governance_contract",
    "architecture_design",
    "monitoring_plan",
    "operational_governance",
    "deployment_readiness_assessment",
    "gate_decision",
    "architecture_controls",
    "monitoring_control_catalogue",
    "quantitative_reference_bands",
    "bootstrap_discrimination_uncertainty",
    "known_risk_slice_references",
    "escalation_trigger_catalogue",
    "residual_risk_traceability",
    "operational_control_evidence",
)


# ============================================================
# D15-R01.06 — EVIDENCE PACKAGE GOVERNANCE PRINCIPLES
# ============================================================

D15_EVIDENCE_PACKAGE_GOVERNANCE: Final[dict[str, object]] = {

    "evidence_generation_only": True,

    "runtime_logic_reimplementation_prohibited": True,

    "model_retraining_prohibited": True,

    "preprocessor_refit_prohibited": True,

    "threshold_retuning_prohibited": True,

    "model_recalibration_prohibited": True,

    "locked_test_driven_redesign_prohibited": True,

    "candidate_identity_modification_prohibited": True,

    "automatic_model_change_prohibited": True,

    "automatic_threshold_change_prohibited": True,

    "automatic_production_authorization_prohibited": True,

    "external_validation_established": False,

    "prospective_validation_established": False,

    "clinical_effectiveness_established": False,

    "production_deployment_authorized": False,

    "human_clinical_oversight_required": True,

    "advisory_use_only": True,
}


# ============================================================
# D15-R01.07 — VALIDATE REPORTING CONTRACT
# ============================================================

def validate_d15_reporting_contract() -> dict[str, object]:
    """
    Validate the D15 formal evidence-package contract.

    This validation confirms that the reporting layer remains
    aligned with the frozen D15 runtime and does not introduce
    unsupported deployment or clinical-effectiveness claims.
    """

    registry_keys = set(
        D15_EVIDENCE_ARTIFACT_REGISTRY.keys()
    )

    required_keys = set(
        D15_REQUIRED_EVIDENCE_ARTIFACT_KEYS
    )

    checks = {

        "stage_identity_is_d15": (
            D15_REPORTING_STAGE_ID == "D15"
        ),

        "source_stage_is_d14": (
            D15_REPORTING_SOURCE_STAGE == "D14"
        ),

        "source_commit_is_frozen_d14_commit": (
            D15_REPORTING_SOURCE_COMMIT == "1e003ee"
        ),

        "next_stage_is_d16": (
            D15_REPORTING_NEXT_STAGE == "D16"
        ),

        "artifact_registry_complete": (
            registry_keys == required_keys
        ),

        "artifact_registry_has_15_artifacts": (
            len(D15_EVIDENCE_ARTIFACT_REGISTRY) == 15
        ),

        "all_artifact_paths_are_project_scoped": all(
            D15_PROJECT_ROOT in path.parents
            for path
            in D15_EVIDENCE_ARTIFACT_REGISTRY.values()
        ),

        "reporting_prohibits_retraining": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "model_retraining_prohibited"
            ]
            is True
        ),

        "reporting_prohibits_preprocessor_refit": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "preprocessor_refit_prohibited"
            ]
            is True
        ),

        "reporting_prohibits_threshold_retuning": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "threshold_retuning_prohibited"
            ]
            is True
        ),

        "reporting_prohibits_recalibration": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "model_recalibration_prohibited"
            ]
            is True
        ),

        "reporting_prohibits_locked_test_redesign": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "locked_test_driven_redesign_prohibited"
            ]
            is True
        ),

        "external_validation_not_established": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "external_validation_established"
            ]
            is False
        ),

        "clinical_effectiveness_not_established": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "clinical_effectiveness_established"
            ]
            is False
        ),

        "production_deployment_not_authorized": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "production_deployment_authorized"
            ]
            is False
        ),

        "runtime_also_prohibits_production_deployment": (
            d15.D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
            is False
        ),

        "human_oversight_required": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "human_clinical_oversight_required"
            ]
            is True
        ),

        "advisory_use_only": (
            D15_EVIDENCE_PACKAGE_GOVERNANCE[
                "advisory_use_only"
            ]
            is True
        ),
    }

    overall_pass = all(checks.values())

    return {
        "stage_id": D15_REPORTING_STAGE_ID,
        "stage_name": D15_REPORTING_STAGE_NAME,
        "source_stage": D15_REPORTING_SOURCE_STAGE,
        "source_commit": D15_REPORTING_SOURCE_COMMIT,
        "next_stage": D15_REPORTING_NEXT_STAGE,
        "artifact_count": len(
            D15_EVIDENCE_ARTIFACT_REGISTRY
        ),
        "checks": checks,
        "overall_pass": overall_pass,
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R01.08 — PRINT REPORTING CONTRACT EVIDENCE
# ============================================================

def print_d15_reporting_contract() -> None:
    """
    Print deterministic evidence for the D15 reporting contract.
    """

    evidence = validate_d15_reporting_contract()

    print("=" * 112)

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "FORMAL EVIDENCE PACKAGE CONTRACT"
    )

    print("=" * 112)

    print()

    print(
        f"Stage:                         "
        f"{evidence['stage_id']}"
    )

    print(
        f"Source lifecycle stage:        "
        f"{evidence['source_stage']}"
    )

    print(
        f"Source Git commit:             "
        f"{evidence['source_commit']}"
    )

    print(
        f"Next lifecycle stage:          "
        f"{evidence['next_stage']}"
    )

    print(
        f"Registered evidence artifacts: "
        f"{evidence['artifact_count']}"
    )

    print()

    print(
        "Governance validation"
    )

    print("-" * 112)

    for check_name, passed in evidence["checks"].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print("-" * 112)

    print(
        f"REPORTING CONTRACT STATUS:      "
        f"{'PASS' if evidence['overall_pass'] else 'FAIL'}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print("=" * 112)

# ============================================================
# D15-R02 — ARCHITECTURE & FROZEN-SYSTEM EVIDENCE EXTRACTION
# ============================================================
#
# Purpose
# -------
# Extract persistent reporting evidence directly from the
# authoritative D15 runtime without recreating runtime logic.
#
# The reporting layer must preserve:
# - D13 registered candidate identity
# - D7 frozen preprocessing identity
# - D8 frozen model identity
# - D9 frozen operating threshold
# - D15 architecture and inference contract
# - advisory-only human decision authority
# ============================================================


# ============================================================
# D15-R02.01 — BUILD FROZEN-SYSTEM IDENTITY EVIDENCE
# ============================================================

def build_d15_frozen_system_identity_evidence() -> dict[str, object]:
    """
    Build reporting evidence for the frozen clinical-AI
    candidate consumed by D15.

    No artifact is modified or refitted.
    """

    artifact_snapshot = (
        d15.snapshot_d15_frozen_artifacts()
    )

    artifact_validation = (
        d15.validate_d15_frozen_artifact_identity(
            snapshot=artifact_snapshot
        )
    )

    return {

        "registry_id": (
            d15.D15_EXPECTED_REGISTRY_ID
        ),

        "model_version": (
            d15.D15_EXPECTED_MODEL_VERSION
        ),

        "candidate_system_sha256": (
            d15.D15_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "operating_threshold": (
            d15.D15_FROZEN_OPERATING_THRESHOLD
        ),

        "d7_preprocessor_expected_sha256": (
            d15.D15_EXPECTED_D7_PREPROCESSOR_SHA256
        ),

        "d7_schema_expected_sha256": (
            d15.D15_EXPECTED_D7_SCHEMA_SHA256
        ),

        "d8_model_expected_sha256": (
            d15.D15_EXPECTED_D8_MODEL_SHA256
        ),

        "d8_metadata_expected_sha256": (
            d15.D15_EXPECTED_D8_METADATA_SHA256
        ),

        "artifact_snapshot": artifact_snapshot,

        "artifact_validation": artifact_validation,

        "production_deployment_authorized": (
            d15.D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
        ),
    }


# ============================================================
# D15-R02.02 — BUILD ARCHITECTURE EVIDENCE
# ============================================================

def build_d15_architecture_evidence() -> dict[str, object]:
    """
    Extract the authoritative D15 deployment architecture and
    controlled-inference design evidence.
    """

    architecture_validation = (
        d15.validate_d15_deployment_architecture()
    )

    return {

        "architecture_layers": (
            d15.D15_ARCHITECTURE_LAYERS
        ),

        "inference_flow": (
            d15.D15_INFERENCE_FLOW
        ),

        "required_raw_source_features": (
            d15.D15_REQUIRED_INFERENCE_SOURCE_FEATURES
        ),

        "expected_engineered_primary_features": (
            d15.D15_EXPECTED_ENGINEERED_PRIMARY_FEATURES
        ),

        "expected_primary_feature_count": (
            d15.D15_EXPECTED_PRIMARY_FEATURE_COUNT
        ),

        "expected_transformed_feature_count": (
            d15.D15_EXPECTED_TRANSFORMED_FEATURE_COUNT
        ),

        "output_classification": (
            d15.D15_OUTPUT_CLASSIFICATION
        ),

        "allowed_advisory_flags": (
            d15.D15_ALLOWED_ADVISORY_FLAGS
        ),

        "output_disclaimer": (
            d15.D15_OUTPUT_DISCLAIMER
        ),

        "architecture_validation": (
            architecture_validation
        ),

        "production_deployment_authorized": (
            d15.D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
        ),
    }


# ============================================================
# D15-R02.03 — VALIDATE EXTRACTED ARCHITECTURE EVIDENCE
# ============================================================

def validate_d15_reporting_architecture_evidence() -> dict[str, object]:
    """
    Validate that D15 reporting evidence is derived from the
    authoritative frozen runtime contract.
    """

    frozen = (
        build_d15_frozen_system_identity_evidence()
    )

    architecture = (
        build_d15_architecture_evidence()
    )

    artifact_validation = (
        frozen["artifact_validation"]
    )

    architecture_validation = (
        architecture["architecture_validation"]
    )

    checks = {

        "registry_identity_preserved": (
            frozen["registry_id"]
            == "DIABETES_READMISSION_XGB_D13_V1"
        ),

        "model_version_preserved": (
            frozen["model_version"]
            == "1.0.0"
        ),

        "candidate_system_hash_preserved": (
            frozen["candidate_system_sha256"]
            == d15.D15_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "operating_threshold_preserved": (
            frozen["operating_threshold"]
            == 0.12
        ),

        "frozen_artifact_validation_passes": (
            artifact_validation["overall_pass"]
            is True
        ),

        "architecture_validation_passes": (
            architecture_validation["overall_pass"]
            is True
        ),

        "architecture_has_12_layers": (
            len(
                architecture["architecture_layers"]
            )
            == 12
        ),

        "raw_input_contract_has_8_features": (
            len(
                architecture[
                    "required_raw_source_features"
                ]
            )
            == 8
        ),

        "engineered_primary_contract_has_10_features": (
            len(
                architecture[
                    "expected_engineered_primary_features"
                ]
            )
            == 10
        ),

        "primary_feature_count_is_10": (
            architecture[
                "expected_primary_feature_count"
            ]
            == 10
        ),

        "transformed_feature_count_is_49": (
            architecture[
                "expected_transformed_feature_count"
            ]
            == 49
        ),

        "output_is_clinical_decision_support_advisory": (
            architecture[
                "output_classification"
            ]
            == "CLINICAL_DECISION_SUPPORT_ADVISORY"
        ),

        "human_review_priority_flag_exists": (
            "PRIORITIZE_FOR_HUMAN_REVIEW"
            in architecture["allowed_advisory_flags"]
        ),

        "no_priority_flag_exists": (
            "NO_MODEL_PRIORITY_FLAG"
            in architecture["allowed_advisory_flags"]
        ),

        "reporting_does_not_authorize_production": (
            frozen[
                "production_deployment_authorized"
            ]
            is False
            and architecture[
                "production_deployment_authorized"
            ]
            is False
        ),
    }

    return {
        "frozen_system": frozen,
        "architecture": architecture,
        "checks": checks,
        "overall_pass": all(checks.values()),
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R02.04 — BUILD ARCHITECTURE CONTROL ROWS
# ============================================================

def build_d15_architecture_control_rows() -> list[dict[str, object]]:
    """
    Convert the authoritative architecture into structured
    reporting rows for the later architecture-controls CSV.
    """

    evidence = (
        validate_d15_reporting_architecture_evidence()
    )

    architecture = evidence["architecture"]

    rows: list[dict[str, object]] = []

    for position, layer in enumerate(
        architecture["architecture_layers"],
        start=1,
    ):

        rows.append(
            {
                "control_type": "ARCHITECTURE_LAYER",
                "sequence": position,
                "control_name": layer,
                "frozen_or_governed": True,
                "production_authorization": False,
            }
        )

    for position, step in enumerate(
        architecture["inference_flow"],
        start=1,
    ):

        rows.append(
            {
                "control_type": "INFERENCE_FLOW",
                "sequence": position,
                "control_name": step,
                "frozen_or_governed": True,
                "production_authorization": False,
            }
        )

    return rows


# ============================================================
# D15-R02.05 — PRINT ARCHITECTURE REPORTING EVIDENCE
# ============================================================

def print_d15_reporting_architecture_evidence() -> None:
    """
    Print deterministic D15 architecture and frozen-system
    reporting evidence.
    """

    evidence = (
        validate_d15_reporting_architecture_evidence()
    )

    frozen = evidence["frozen_system"]
    architecture = evidence["architecture"]

    print("=" * 112)

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "ARCHITECTURE & FROZEN-SYSTEM REPORTING EVIDENCE"
    )

    print("=" * 112)

    print()

    print(
        f"Registry ID:                    "
        f"{frozen['registry_id']}"
    )

    print(
        f"Model version:                  "
        f"{frozen['model_version']}"
    )

    print(
        f"Candidate system SHA256:        "
        f"{frozen['candidate_system_sha256']}"
    )

    print(
        f"Frozen operating threshold:     "
        f"{frozen['operating_threshold']}"
    )

    print(
        f"Architecture layers:            "
        f"{len(architecture['architecture_layers'])}"
    )

    print(
        f"Raw source features:            "
        f"{len(architecture['required_raw_source_features'])}"
    )

    print(
        f"Engineered primary features:    "
        f"{architecture['expected_primary_feature_count']}"
    )

    print(
        f"Transformed features:           "
        f"{architecture['expected_transformed_feature_count']}"
    )

    print(
        f"Output classification:          "
        f"{architecture['output_classification']}"
    )

    print()

    print(
        "Governance validation"
    )

    print("-" * 112)

    for check_name, passed in evidence["checks"].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print("-" * 112)

    print(
        f"ARCHITECTURE REPORTING STATUS:   "
        f"{'PASS' if evidence['overall_pass'] else 'FAIL'}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print("=" * 112)

# ============================================================
# D15-R03 — MONITORING & QUANTITATIVE SURVEILLANCE EVIDENCE
# ============================================================


# ============================================================
# D15-R03.01 — BUILD MONITORING GOVERNANCE EVIDENCE
# ============================================================

def build_d15_monitoring_governance_evidence() -> dict[str, object]:
    """
    Extract the authoritative D15 monitoring-control framework.
    """

    validation = (
        d15.validate_d15_monitoring_control_catalogue()
    )

    return {
        "control_catalogue": (
            d15.D15_MONITORING_CONTROL_CATALOGUE
        ),
        "immediate_domains": (
            d15.D15_IMMEDIATE_MONITORING_DOMAINS
        ),
        "outcome_dependent_domains": (
            d15.D15_OUTCOME_DEPENDENT_MONITORING_DOMAINS
        ),
        "threshold_governance": (
            d15.D15_THRESHOLD_GOVERNANCE
        ),
        "validation": validation,
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R03.02 — BUILD QUANTITATIVE REFERENCE EVIDENCE
# ============================================================

def build_d15_quantitative_reference_evidence() -> dict[str, object]:
    """
    Extract D14-derived internal historical surveillance
    references.

    These are NOT production acceptance targets.
    """

    validation = (
        d15.validate_d15_quantitative_monitoring_limit_foundation()
    )

    rate_bands = (
        d15.build_d15_internal_rate_reference_bands()
    )

    return {
        "rate_reference_bands": rate_bands,
        "known_risk_slice_references": (
            d15.D15_D14_KNOWN_RISK_SLICE_REFERENCES
        ),
        "sample_sufficiency": (
            d15.D15_MONITORING_SAMPLE_SUFFICIENCY
        ),
        "limit_governance": (
            d15.D15_QUANTITATIVE_LIMIT_GOVERNANCE
        ),
        "discrimination_limit_governance": (
            d15.D15_DISCRIMINATION_LIMIT_GOVERNANCE
        ),
        "validation": validation,
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R03.03 — BUILD ESCALATION EVIDENCE
# ============================================================

def build_d15_escalation_reporting_evidence() -> dict[str, object]:
    """
    Extract the authoritative monitoring escalation catalogue.
    """

    return {
        "states": d15.D15_MONITORING_STATES,
        "actions": d15.D15_MONITORING_ACTIONS,
        "escalation_levels": d15.D15_ESCALATION_LEVELS,
        "trigger_catalogue": (
            d15.D15_ESCALATION_TRIGGER_CATALOGUE
        ),
        "uncalibrated_evidence_dependent_triggers": (
            d15.D15_UNCALIBRATED_EVIDENCE_DEPENDENT_TRIGGERS
        ),
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R03.04 — VALIDATE MONITORING REPORTING EVIDENCE
# ============================================================

def validate_d15_monitoring_reporting_evidence() -> dict[str, object]:
    """
    Validate monitoring, quantitative-reference and escalation
    evidence before persistence.
    """

    monitoring = (
        build_d15_monitoring_governance_evidence()
    )

    quantitative = (
        build_d15_quantitative_reference_evidence()
    )

    escalation = (
        build_d15_escalation_reporting_evidence()
    )

    controls = monitoring["control_catalogue"]
    rate_bands = quantitative["rate_reference_bands"]
    risk_slices = quantitative["known_risk_slice_references"]
    triggers = escalation["trigger_catalogue"]

    checks = {
        "monitoring_catalogue_validation_passes": (
            monitoring["validation"]["overall_pass"] is True
        ),

        "quantitative_foundation_validation_passes": (
            quantitative["validation"]["overall_pass"] is True
        ),

        "monitoring_catalogue_has_17_controls": (
            len(controls) == 17
        ),

        "six_internal_rate_reference_bands_exist": (
            len(rate_bands) == 6
        ),

        "five_known_risk_slice_references_exist": (
            len(risk_slices) == 5
        ),

        "seventeen_escalation_triggers_exist": (
            len(triggers) == 17
        ),

        "reference_bands_are_not_production_targets": all(
            band.get("production_acceptance_limit") is False
            and band.get("clinical_acceptability_limit") is False
            and band.get("reference_classification")
           == "INTERNAL_HISTORICAL_SURVEILLANCE_REFERENCE"
           for band in rate_bands.values()
        ),

        "reference_governance_prohibits_target_interpretation": (
            quantitative["limit_governance"][
            "reference_is_production_target"
       ]
           is False
          and quantitative["limit_governance"][
          "reference_is_clinical_acceptability_threshold"
       ]
         is False
         and quantitative["limit_governance"][
        "reference_establishes_external_validity"
       ]
        is False
        and quantitative["limit_governance"][
        "reference_establishes_clinical_effectiveness"
      ]
        is False
       ),

        "known_risk_slices_are_not_acceptable_targets": all(
            record.get("acceptable_target") is False
            for record in risk_slices.values()
        ),

        "outcome_monitoring_requires_matured_outcomes": (
            len(
                monitoring["outcome_dependent_domains"]
            ) > 0
        ),

        "immediate_monitoring_exists": (
            len(monitoring["immediate_domains"]) > 0
        ),

        "sample_sufficiency_contract_exists": (
            len(
                quantitative["sample_sufficiency"]
            ) > 0
        ),

        "uncalibrated_triggers_do_not_default_normal": (
            len(
                escalation[
                    "uncalibrated_evidence_dependent_triggers"
                ]
            ) > 0
        ),

        "production_deployment_remains_unauthorized": (
            monitoring["production_deployment_authorized"] is False
            and quantitative[
                "production_deployment_authorized"
            ] is False
            and escalation[
                "production_deployment_authorized"
            ] is False
        ),
    }

    return {
        "monitoring": monitoring,
        "quantitative": quantitative,
        "escalation": escalation,
        "checks": checks,
        "overall_pass": all(checks.values()),
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R03.05 — PRINT MONITORING REPORTING EVIDENCE
# ============================================================

def print_d15_monitoring_reporting_evidence() -> None:
    """
    Print deterministic monitoring/reporting evidence.
    """

    evidence = (
        validate_d15_monitoring_reporting_evidence()
    )

    monitoring = evidence["monitoring"]
    quantitative = evidence["quantitative"]
    escalation = evidence["escalation"]

    print("=" * 112)
    print("D15 — DEPLOYMENT & MONITORING DESIGN")
    print("MONITORING & QUANTITATIVE SURVEILLANCE REPORTING EVIDENCE")
    print("=" * 112)
    print()

    print(
        f"Monitoring controls:            "
        f"{len(monitoring['control_catalogue'])}"
    )

    print(
        f"Immediate monitoring domains:   "
        f"{len(monitoring['immediate_domains'])}"
    )

    print(
        f"Outcome-dependent domains:      "
        f"{len(monitoring['outcome_dependent_domains'])}"
    )

    print(
        f"Internal rate references:       "
        f"{len(quantitative['rate_reference_bands'])}"
    )

    print(
        f"Known-risk slice references:    "
        f"{len(quantitative['known_risk_slice_references'])}"
    )

    print(
        f"Escalation triggers:            "
        f"{len(escalation['trigger_catalogue'])}"
    )

    print()
    print("Governance validation")
    print("-" * 112)

    for check_name, passed in evidence["checks"].items():
        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()
    print("-" * 112)

    print(
        f"MONITORING REPORTING STATUS:     "
        f"{'PASS' if evidence['overall_pass'] else 'FAIL'}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print("=" * 112)

# ============================================================
# D15-R04 — FORMAL BOOTSTRAP UNCERTAINTY & MATERIALITY EVIDENCE
# ============================================================
#
# Purpose
# -------
# Generate the formal D15 discrimination-uncertainty evidence
# using the authoritative D15 bootstrap implementation.
#
# The bootstrap operates on the frozen D14 locked-test
# outcome/prediction pairs.
#
# It does NOT:
# - refit the model
# - refit preprocessing
# - retune the threshold
# - recalibrate the model
# - modify D14 results
# - establish external validity
# - establish clinical effectiveness
# - authorize production deployment
#
# Statistical signal and clinical materiality remain distinct.
# ============================================================


# ============================================================
# D15-R04.01 — FORMAL BOOTSTRAP CONFIGURATION
# ============================================================

D15_REPORTING_BOOTSTRAP_REPLICATES: Final[int] = (
    d15.D15_BOOTSTRAP_REPLICATES
)

D15_REPORTING_BOOTSTRAP_CONFIDENCE_LEVEL: Final[float] = (
    d15.D15_BOOTSTRAP_CONFIDENCE_LEVEL
)

D15_REPORTING_BOOTSTRAP_RANDOM_SEED: Final[int] = (
    d15.D15_BOOTSTRAP_RANDOM_SEED
)


# ============================================================
# D15-R04.02 — FORMAL BOOTSTRAP GOVERNANCE CONTRACT
# ============================================================

D15_REPORTING_BOOTSTRAP_GOVERNANCE: Final[
    dict[str, object]
] = {
    "source": (
        "D14_FROZEN_LOCKED_TEST_PREDICTION_OUTCOME_PAIRS"
    ),
    "method": "STRATIFIED_PERCENTILE_BOOTSTRAP",
    "replicates": D15_REPORTING_BOOTSTRAP_REPLICATES,
    "confidence_level": (
        D15_REPORTING_BOOTSTRAP_CONFIDENCE_LEVEL
    ),
    "random_seed": D15_REPORTING_BOOTSTRAP_RANDOM_SEED,

    "model_refit_permitted": False,
    "preprocessor_refit_permitted": False,
    "threshold_retuning_permitted": False,
    "recalibration_permitted": False,
    "locked_test_redesign_permitted": False,

    "statistical_signal_equals_clinical_materiality": False,
    "single_window_signal_establishes_persistent_drift": False,
    "human_materiality_review_required": True,

    "external_validation_established": False,
    "clinical_effectiveness_established": False,
    "production_deployment_authorized": False,
}


# ============================================================
# D15-R04.03 — GENERATE FORMAL BOOTSTRAP EVIDENCE
# ============================================================

def build_d15_formal_bootstrap_reporting_evidence(
    *,
    n_bootstrap: int = D15_REPORTING_BOOTSTRAP_REPLICATES,
) -> dict[str, object]:
    """
    Generate formal bootstrap uncertainty evidence through the
    authoritative D15 runtime implementation.

    The authoritative runtime already:
    - loads frozen D14 prediction/outcome pairs
    - calculates stratified percentile bootstrap uncertainty
    - validates D14 point-estimate reproduction
    - validates bootstrap reproducibility
    - validates materiality/persistence governance

    The reporting layer consumes that evidence without
    reimplementing the statistical procedure.
    """

    runtime_evidence = (
        d15.build_d15_bootstrap_materiality_evidence(
            n_bootstrap=n_bootstrap
        )
    )

    bootstrap = (
        runtime_evidence["bootstrap"]
    )

    point_validation = (
        runtime_evidence["point_validation"]
    )

    reproducibility = (
        runtime_evidence["reproducibility"]
    )

    return {
        "configuration": {
            "n_bootstrap": n_bootstrap,
            "confidence_level": (
                D15_REPORTING_BOOTSTRAP_CONFIDENCE_LEVEL
            ),
            "random_seed": (
                D15_REPORTING_BOOTSTRAP_RANDOM_SEED
            ),
        },

        "governance": (
            D15_REPORTING_BOOTSTRAP_GOVERNANCE
        ),

        "runtime_evidence": runtime_evidence,

        "bootstrap_evidence": bootstrap,

        "point_estimate_validation": (
            point_validation
        ),

        "reproducibility_validation": (
            reproducibility
        ),

        "runtime_validation_status": (
            runtime_evidence["validation_status"]
        ),

        "runtime_overall_pass": (
            runtime_evidence["overall_pass"]
        ),

        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R04.04 — VALIDATE FORMAL BOOTSTRAP REPORTING EVIDENCE
# ============================================================

def validate_d15_formal_bootstrap_reporting_evidence(
    evidence: dict[str, object],
) -> dict[str, object]:
    """
    Validate formal bootstrap reporting evidence without
    independently recreating the authoritative runtime
    statistical procedure.
    """

    configuration = evidence["configuration"]

    governance = evidence["governance"]

    bootstrap = evidence["bootstrap_evidence"]

    point_validation = (
        evidence["point_estimate_validation"]
    )

    reproducibility = (
        evidence["reproducibility_validation"]
    )

    checks = {

        "formal_run_uses_2000_replicates": (
            configuration["n_bootstrap"] == 2000
        ),

        "confidence_level_is_95_percent": (
            configuration["confidence_level"] == 0.95
        ),

        "random_seed_is_42": (
            configuration["random_seed"] == 42
        ),

        "runtime_bootstrap_replicates_are_2000": (
            d15.D15_BOOTSTRAP_REPLICATES == 2000
        ),

        "runtime_confidence_level_is_95_percent": (
            d15.D15_BOOTSTRAP_CONFIDENCE_LEVEL == 0.95
        ),

        "runtime_random_seed_is_42": (
            d15.D15_BOOTSTRAP_RANDOM_SEED == 42
        ),

        "point_estimate_validation_passes": (
            point_validation["overall_pass"] is True
        ),

        "bootstrap_reproducibility_validation_passes": (
            reproducibility["overall_pass"] is True
        ),

        "authoritative_runtime_evidence_passes": (
            evidence["runtime_overall_pass"] is True
            and evidence["runtime_validation_status"] == "PASS"
        ),

        "bootstrap_evidence_exists": (
            isinstance(bootstrap, dict)
            and len(bootstrap) > 0
        ),

        "bootstrap_method_is_stratified_percentile": (
            bootstrap["method"]
            == "STRATIFIED_PERCENTILE_BOOTSTRAP"
        ),

        "bootstrap_contains_pr_auc": (
            isinstance(
                bootstrap.get("pr_auc"),
                dict,
            )
        ),

        "bootstrap_contains_roc_auc": (
            isinstance(
                bootstrap.get("roc_auc"),
                dict,
            )
        ),

        "no_invalid_bootstrap_replicates": (
            bootstrap[
                "invalid_bootstrap_replicates"
            ]
            == 0
        ),

        "model_not_retrained": (
            bootstrap["model_retrained"] is False
        ),

        "model_not_retuned": (
            bootstrap["model_retuned"] is False
        ),

        "threshold_not_retuned": (
            bootstrap["threshold_retuned"] is False
        ),

        "model_not_recalibrated": (
            bootstrap["model_recalibrated"] is False
        ),

        "locked_test_redesign_prohibited": (
            governance[
                "locked_test_redesign_permitted"
            ]
            is False
        ),

        "statistical_signal_not_clinical_materiality": (
            governance[
                "statistical_signal_equals_clinical_materiality"
            ]
            is False
        ),

        "single_window_not_persistent_drift": (
            governance[
                "single_window_signal_establishes_persistent_drift"
            ]
            is False
        ),

        "human_materiality_review_required": (
            governance[
                "human_materiality_review_required"
            ]
            is True
        ),

        "external_validation_not_established": (
            governance[
                "external_validation_established"
            ]
            is False
        ),

        "clinical_effectiveness_not_established": (
            governance[
                "clinical_effectiveness_established"
            ]
            is False
        ),

        "production_deployment_not_authorized": (
            governance[
                "production_deployment_authorized"
            ]
            is False
            and evidence[
                "production_deployment_authorized"
            ]
            is False
        ),
    }

    return {
        "checks": checks,
        "overall_pass": all(checks.values()),
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R04.05 — EXTRACT DISCRIMINATION METRIC RECORD
# ============================================================

def extract_d15_bootstrap_metric_record(
    bootstrap_evidence: dict[str, object],
    metric_name: str,
) -> dict[str, object]:
    """
    Extract one discrimination metric from the authoritative
    bootstrap evidence.

    Supported governed metrics:
    - pr_auc
    - roc_auc
    """

    normalized_name = (
        metric_name
        .strip()
        .lower()
        .replace("-", "_")
    )

    aliases = {
        "pr_auc": "pr_auc",
        "prauc": "pr_auc",
        "average_precision": "pr_auc",

        "roc_auc": "roc_auc",
        "rocauc": "roc_auc",
    }

    authoritative_key = aliases.get(
        normalized_name
    )

    if authoritative_key is None:
        raise KeyError(
            f"Unsupported bootstrap metric: {metric_name}"
        )

    record = bootstrap_evidence.get(
        authoritative_key
    )

    if not isinstance(record, dict):
        raise KeyError(
            "Authoritative bootstrap evidence does not "
            f"contain metric: {authoritative_key}"
        )

    return record


# ============================================================
# D15-R04.06 — BUILD STRUCTURED BOOTSTRAP REPORTING ROWS
# ============================================================

def build_d15_bootstrap_reporting_rows(
    evidence: dict[str, object],
) -> list[dict[str, object]]:
    """
    Convert authoritative PR-AUC and ROC-AUC bootstrap evidence
    into structured rows for the later persistent CSV artifact.
    """

    bootstrap = evidence["bootstrap_evidence"]

    rows: list[dict[str, object]] = []

    for metric_name in (
        "pr_auc",
        "roc_auc",
    ):

        metric = (
            extract_d15_bootstrap_metric_record(
                bootstrap,
                metric_name,
            )
        )

        rows.append(
            {
                "metric": metric_name,
                "method": bootstrap["method"],
                "bootstrap_replicates": (
                    bootstrap[
                        "bootstrap_replicates"
                    ]
                ),
                "random_seed": (
                    bootstrap["random_seed"]
                ),
                "confidence_level": (
                    bootstrap[
                        "confidence_level"
                    ]
                ),
                "point_estimate": (
                    metric["point_estimate"]
                ),
                "bootstrap_mean": (
                    metric["bootstrap_mean"]
                ),
                "bootstrap_std": (
                    metric["bootstrap_std"]
                ),
                "lower_bound": (
                    metric["lower_bound"]
                ),
                "upper_bound": (
                    metric["upper_bound"]
                ),
                "reference_classification": (
                    "INTERNAL_HISTORICAL_"
                    "SURVEILLANCE_REFERENCE"
                ),
                "production_acceptance_limit": False,
                "clinical_acceptability_limit": False,
                "external_validation_established": False,
                "clinical_effectiveness_established": False,
                "production_deployment_authorized": False,
            }
        )

    return rows


# ============================================================
# D15-R04.07 — PRINT FORMAL BOOTSTRAP EVIDENCE
# ============================================================

def print_d15_formal_bootstrap_reporting_evidence(
    *,
    n_bootstrap: int = D15_REPORTING_BOOTSTRAP_REPLICATES,
) -> None:
    """
    Execute and print the formal D15 bootstrap reporting run.
    """

    evidence = (
        build_d15_formal_bootstrap_reporting_evidence(
            n_bootstrap=n_bootstrap
        )
    )

    validation = (
        validate_d15_formal_bootstrap_reporting_evidence(
            evidence
        )
    )

    bootstrap = evidence["bootstrap_evidence"]

    pr_auc = (
        extract_d15_bootstrap_metric_record(
            bootstrap,
            "pr_auc",
        )
    )

    roc_auc = (
        extract_d15_bootstrap_metric_record(
            bootstrap,
            "roc_auc",
        )
    )

    print("=" * 112)

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "FORMAL BOOTSTRAP DISCRIMINATION & MATERIALITY EVIDENCE"
    )

    print("=" * 112)

    print()

    print(
        f"Bootstrap method:               "
        f"{bootstrap['method']}"
    )

    print(
        f"Bootstrap replicates:           "
        f"{bootstrap['bootstrap_replicates']}"
    )

    print(
        f"Confidence level:               "
        f"{bootstrap['confidence_level']}"
    )

    print(
        f"Random seed:                    "
        f"{bootstrap['random_seed']}"
    )

    print(
        "Reference source:               "
        "D14 frozen locked-test prediction/outcome pairs"
    )

    print()

    print(
        "Discrimination uncertainty"
    )

    print("-" * 112)

    print(
        f"PR-AUC point estimate:          "
        f"{pr_auc['point_estimate']:.12f}"
    )

    print(
        f"PR-AUC bootstrap mean:          "
        f"{pr_auc['bootstrap_mean']:.12f}"
    )

    print(
        f"PR-AUC bootstrap std:           "
        f"{pr_auc['bootstrap_std']:.12f}"
    )

    print(
        f"PR-AUC 95% interval:            "
        f"[{pr_auc['lower_bound']:.12f}, "
        f"{pr_auc['upper_bound']:.12f}]"
    )

    print()

    print(
        f"ROC-AUC point estimate:         "
        f"{roc_auc['point_estimate']:.12f}"
    )

    print(
        f"ROC-AUC bootstrap mean:         "
        f"{roc_auc['bootstrap_mean']:.12f}"
    )

    print(
        f"ROC-AUC bootstrap std:          "
        f"{roc_auc['bootstrap_std']:.12f}"
    )

    print(
        f"ROC-AUC 95% interval:           "
        f"[{roc_auc['lower_bound']:.12f}, "
        f"{roc_auc['upper_bound']:.12f}]"
    )

    print()

    print(
        f"Invalid bootstrap replicates:   "
        f"{bootstrap['invalid_bootstrap_replicates']}"
    )

    print()

    print(
        "Governance validation"
    )

    print("-" * 112)

    for check_name, passed in validation["checks"].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print("-" * 112)

    print(
        f"FORMAL BOOTSTRAP STATUS:         "
        f"{'PASS' if validation['overall_pass'] else 'FAIL'}"
    )

    print(
        "STATISTICAL SIGNAL = CLINICAL MATERIALITY: "
        "False"
    )

    print(
        "SINGLE WINDOW = PERSISTENT DRIFT:          "
        "False"
    )

    print(
        "EXTERNAL VALIDATION ESTABLISHED:           "
        "False"
    )

    print(
        "CLINICAL EFFECTIVENESS ESTABLISHED:        "
        "False"
    )

    print(
        "PRODUCTION DEPLOYMENT AUTHORIZED:          "
        "False"
    )

    print("=" * 112)

# ============================================================
# D15-R05 — OPERATIONAL GOVERNANCE & RESIDUAL-RISK TRACEABILITY
# ============================================================
#
# Purpose
# -------
# Convert the authoritative D15 incident, change-control,
# rollback, business-continuity and D14 residual-risk handoff
# structures into formal reporting evidence.
#
# Important distinction:
# D15 defines and validates the operational governance design.
# It does NOT claim that live enterprise incident-management
# or rollback infrastructure has been deployed.
# ============================================================


# ============================================================
# D15-R05.01 — BUILD OPERATIONAL GOVERNANCE EVIDENCE
# ============================================================

def build_d15_operational_governance_evidence() -> dict[str, object]:
    """
    Extract authoritative operational-governance controls from
    the validated D15 runtime.
    """

    validation = (
        d15.validate_d15_incident_change_rollback_continuity_controls()
    )

    return {
        "incident_severity_model": (
            d15.D15_INCIDENT_SEVERITY_MODEL
        ),

        "required_incident_fields": (
            d15.D15_REQUIRED_INCIDENT_FIELDS
        ),

        "change_classification": (
            d15.D15_CHANGE_CLASSIFICATION
        ),

        "model_affecting_change_types": (
            d15.D15_MODEL_AFFECTING_CHANGE_TYPES
        ),

        "monitoring_change_control_boundary": (
            d15.D15_MONITORING_CHANGE_CONTROL_BOUNDARY
        ),

        "rollback_triggers": (
            d15.D15_ROLLBACK_TRIGGERS
        ),

        "rollback_governance": (
            d15.D15_ROLLBACK_GOVERNANCE
        ),

        "business_continuity_control": (
            d15.D15_BUSINESS_CONTINUITY_CONTROL
        ),

        "incident_management_implemented": (
            d15.D15_INCIDENT_MANAGEMENT_IMPLEMENTED
        ),

        "rollback_implemented": (
            d15.D15_ROLLBACK_IMPLEMENTED
        ),

        "validation": validation,

        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R05.02 — BUILD RESIDUAL-RISK TRACEABILITY EVIDENCE
# ============================================================

def build_d15_residual_risk_traceability_evidence() -> dict[str, object]:
    """
    Build the authoritative D14-to-D15 residual-risk handoff.

    All seven D14 residual risks must remain visible and
    unresolved unless a later authorized governance process
    formally changes their disposition.
    """

    handoff = list(
        d15.D15_D14_RESIDUAL_RISK_HANDOFF
    )

    required_risks = tuple(
        d15.D15_REQUIRED_D14_RESIDUAL_RISKS
    )

    reference_signals = (
        d15.D15_RESIDUAL_RISK_REFERENCE_SIGNALS
    )

    return {
        "principle": (
            d15.D15_RESIDUAL_RISK_PRINCIPLE
        ),

        "required_risk_ids": required_risks,

        "handoff": handoff,

        "reference_signals": reference_signals,

        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R05.03 — BUILD RESIDUAL-RISK REPORTING ROWS
# ============================================================

def build_d15_residual_risk_reporting_rows() -> list[dict[str, object]]:
    """
    Convert D14-to-D15 residual-risk handoff into structured
    rows for the persistent traceability CSV.
    """

    evidence = (
        build_d15_residual_risk_traceability_evidence()
    )

    reference_signals = evidence["reference_signals"]

    rows: list[dict[str, object]] = []

    for record in evidence["handoff"]:

        risk_id = record["risk_id"]

        signal = reference_signals[risk_id]

        rows.append(
            {
                "risk_id": risk_id,

                "risk_domain": (
                    record["risk_domain"]
                ),

                "d15_control_domain": (
                    record["d15_control_domain"]
                ),

                "handoff_status": (
                    record["status"]
                ),

                "reference_risk_name": (
                    signal["risk_name"]
                ),

                "reference_evidence": repr(
                    signal["reference_evidence"]
                ),

                "resolved_in_d15": False,

                "requires_explicit_governance_decision": True,

                "production_deployment_authorized": False,
            }
        )

    return rows


# ============================================================
# D15-R05.04 — BUILD OPERATIONAL CONTROL REPORTING ROWS
# ============================================================

def build_d15_operational_control_reporting_rows() -> list[
    dict[str, object]
]:
    """
    Convert the operational-governance design into structured
    evidence rows.
    """

    evidence = (
        build_d15_operational_governance_evidence()
    )

    rows: list[dict[str, object]] = []

    # --------------------------------------------------------
    # Incident severity controls
    # --------------------------------------------------------

    for severity, specification in (
        evidence["incident_severity_model"].items()
    ):

        rows.append(
            {
                "control_domain": "INCIDENT_MANAGEMENT",
                "control_id": severity,
                "control_classification": (
                    specification["classification"]
                ),
                "control_requirement": (
                    specification["required_action"]
                ),
                "implementation_status": (
                    "DESIGNED_AND_VALIDATED_NOT_LIVE_IMPLEMENTED"
                ),
                "production_deployment_authorized": False,
            }
        )

    # --------------------------------------------------------
    # Change classifications
    # --------------------------------------------------------

    for change_class, specification in (
        evidence["change_classification"].items()
    ):

        rows.append(
            {
                "control_domain": "CHANGE_CONTROL",
                "control_id": change_class,
                "control_classification": (
                    "GOVERNED_CHANGE_CLASS"
                ),
                "control_requirement": repr(
                    specification
                ),
                "implementation_status": (
                    "DESIGNED_AND_VALIDATED"
                ),
                "production_deployment_authorized": False,
            }
        )

    # --------------------------------------------------------
    # Rollback triggers
    # --------------------------------------------------------

    for trigger in evidence["rollback_triggers"]:

        rows.append(
            {
                "control_domain": "ROLLBACK",
                "control_id": trigger,
                "control_classification": (
                    "ROLLBACK_TRIGGER"
                ),
                "control_requirement": (
                    "FORMAL_ROLLBACK_OR_AI_SERVICE_"
                    "SUSPENSION_DECISION_REQUIRED"
                ),
                "implementation_status": (
                    "DESIGNED_AND_VALIDATED_NOT_LIVE_IMPLEMENTED"
                ),
                "production_deployment_authorized": False,
            }
        )

    # --------------------------------------------------------
    # Business continuity
    # --------------------------------------------------------

    continuity = (
        evidence["business_continuity_control"]
    )

    rows.append(
        {
            "control_domain": "BUSINESS_CONTINUITY",
            "control_id": "CLINICAL_WORKFLOW_CONTINUITY",
            "control_classification": (
                "SAFE_FALLBACK"
            ),
            "control_requirement": (
                continuity["fallback_workflow"]
            ),
            "implementation_status": (
                "DESIGNED_AND_VALIDATED"
            ),
            "production_deployment_authorized": False,
        }
    )

    return rows


# ============================================================
# D15-R05.05 — VALIDATE OPERATIONAL & RISK EVIDENCE
# ============================================================

def validate_d15_operational_risk_reporting_evidence() -> dict[str, object]:
    """
    Validate D15 operational-governance design and D14 residual
    risk traceability.
    """

    operational = (
        build_d15_operational_governance_evidence()
    )

    residual = (
        build_d15_residual_risk_traceability_evidence()
    )

    handoff = residual["handoff"]

    required_risks = set(
        residual["required_risk_ids"]
    )

    handoff_ids = {
        record["risk_id"]
        for record in handoff
    }

    checks = {

        "runtime_operational_validation_passes": (
            operational["validation"]["overall_pass"] is True
        ),

        "four_incident_severity_levels_exist": (
            set(
                operational[
                    "incident_severity_model"
                ].keys()
            )
            == {
                "SEV1",
                "SEV2",
                "SEV3",
                "SEV4",
            }
        ),

        "required_incident_contract_exists": (
            len(
                operational[
                    "required_incident_fields"
                ]
            )
            == 20
        ),

        "four_change_classifications_exist": (
            len(
                operational[
                    "change_classification"
                ]
            )
            == 4
        ),

        "model_affecting_change_types_exist": (
            len(
                operational[
                    "model_affecting_change_types"
                ]
            )
            > 0
        ),

        "automatic_model_change_prohibited": (
            operational[
                "monitoring_change_control_boundary"
            ][
                "automatic_model_change_permitted"
            ]
            is False
        ),

        "silent_test_driven_redesign_prohibited": (
            operational[
                "monitoring_change_control_boundary"
            ][
                "test_driven_silent_redesign_permitted"
            ]
            is False
        ),

        "seven_rollback_triggers_exist": (
            len(
                operational["rollback_triggers"]
            )
            == 7
        ),

        "rollback_requires_authorized_target": (
            operational[
                "rollback_governance"
            ][
                "rollback_target_must_be_authorized"
            ]
            is True
        ),

        "rollback_requires_integrity_verification": (
            operational[
                "rollback_governance"
            ][
                "rollback_target_integrity_must_be_verified"
            ]
            is True
        ),

        "rollback_cannot_generate_replacement_ai_prediction": (
            operational[
                "rollback_governance"
            ][
                "fallback_may_generate_replacement_ai_prediction"
            ]
            is False
        ),

        "clinical_workflow_continues_without_ai": (
            operational[
                "business_continuity_control"
            ][
                "clinical_workflow_must_continue_without_ai"
            ]
            is True
        ),

        "ai_unavailability_does_not_block_care": (
            operational[
                "business_continuity_control"
            ][
                "ai_unavailability_blocks_clinical_care"
            ]
            is False
        ),

        "clinical_team_retains_decision_authority": (
            operational[
                "business_continuity_control"
            ][
                "clinical_team_retains_decision_authority"
            ]
            is True
        ),

        "no_synthetic_fallback_ai_score": (
            operational[
                "business_continuity_control"
            ][
                "fallback_generates_synthetic_ai_score"
            ]
            is False
        ),

        "incident_management_not_falsely_claimed_live": (
            operational[
                "incident_management_implemented"
            ]
            is False
        ),

        "rollback_not_falsely_claimed_live": (
            operational[
                "rollback_implemented"
            ]
            is False
        ),

        "exactly_seven_d14_residual_risks_required": (
            len(required_risks) == 7
        ),

        "exactly_seven_d14_residual_risks_handed_off": (
            len(handoff) == 7
        ),

        "all_required_risks_are_handed_off": (
            handoff_ids == required_risks
        ),

        "all_residual_risks_remain_unresolved": all(
            record["status"]
            == "UNRESOLVED_CARRY_FORWARD"
            for record in handoff
        ),

        "all_residual_risks_have_d15_control_domains": all(
            bool(
                record["d15_control_domain"]
            )
            for record in handoff
        ),

        "all_residual_risks_have_reference_signals": (
            set(
                residual[
                    "reference_signals"
                ].keys()
            )
            == required_risks
        ),

        "production_deployment_remains_unauthorized": (
            operational[
                "production_deployment_authorized"
            ]
            is False
            and residual[
                "production_deployment_authorized"
            ]
            is False
        ),
    }

    return {
        "operational": operational,
        "residual_risk": residual,
        "checks": checks,
        "overall_pass": all(checks.values()),
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R05.06 — PRINT OPERATIONAL & RISK EVIDENCE
# ============================================================

def print_d15_operational_risk_reporting_evidence() -> None:
    """
    Print deterministic operational-governance and residual-risk
    reporting evidence.
    """

    evidence = (
        validate_d15_operational_risk_reporting_evidence()
    )

    operational = evidence["operational"]
    residual = evidence["residual_risk"]

    print("=" * 112)

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "OPERATIONAL GOVERNANCE & RESIDUAL-RISK TRACEABILITY"
    )

    print("=" * 112)

    print()

    print(
        f"Incident severity levels:       "
        f"{len(operational['incident_severity_model'])}"
    )

    print(
        f"Required incident fields:       "
        f"{len(operational['required_incident_fields'])}"
    )

    print(
        f"Change classifications:         "
        f"{len(operational['change_classification'])}"
    )

    print(
        f"Rollback triggers:              "
        f"{len(operational['rollback_triggers'])}"
    )

    print(
        f"D14 residual risks required:    "
        f"{len(residual['required_risk_ids'])}"
    )

    print(
        f"D14 residual risks handed off:  "
        f"{len(residual['handoff'])}"
    )

    print(
        f"Live incident system claimed:   "
        f"{operational['incident_management_implemented']}"
    )

    print(
        f"Live rollback system claimed:   "
        f"{operational['rollback_implemented']}"
    )

    print()

    print(
        "Residual-risk handoff"
    )

    print("-" * 112)

    for record in residual["handoff"]:

        print(
            f"{record['risk_id']:<16}"
            f"{record['risk_domain']:<42}"
            f"{record['status']}"
        )

    print()

    print(
        "Governance validation"
    )

    print("-" * 112)

    for check_name, passed in evidence["checks"].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print("-" * 112)

    print(
        f"OPERATIONAL/RISK REPORTING STATUS: "
        f"{'PASS' if evidence['overall_pass'] else 'FAIL'}"
    )

    print(
        "ALL D14 RESIDUAL RISKS RESOLVED:    "
        "False"
    )

    print(
        "LIVE INCIDENT MANAGEMENT IMPLEMENTED: "
        "False"
    )

    print(
        "LIVE ROLLBACK IMPLEMENTED:            "
        "False"
    )

    print(
        "PRODUCTION DEPLOYMENT AUTHORIZED:      "
        "False"
    )

    print("=" * 112)

# ============================================================
# D15-R06 — PERSISTENT EVIDENCE PACKAGE GENERATOR
# ============================================================
#
# Purpose
# -------
# Materialize the validated D15 reporting evidence into the
# permanent governance and structured-evidence package
# registered in D15-R01.
#
# Evidence package:
# - 1 manifest
# - 6 governance/design documents
# - 1 final gate decision
# - 7 structured evidence tables
#
# Total: 15 artifacts
#
# This generator does NOT authorize production deployment.
# ============================================================


# ============================================================
# D15-R06.01 — REPORTING IMPORTS
# ============================================================

import csv
import hashlib
import json
from datetime import datetime, timezone


# ============================================================
# D15-R06.02 — FILE & SERIALIZATION HELPERS
# ============================================================

def _d15_ensure_evidence_directories() -> None:
    """
    Create D15 reporting directories if they do not already
    exist.
    """

    D15_MANIFEST_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    D15_GOVERNANCE_REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    D15_TABLE_REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def _d15_write_text(
    path: Path,
    text: str,
) -> None:
    """
    Write deterministic UTF-8 text.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        text.rstrip() + "\n",
        encoding="utf-8",
    )


def _d15_write_csv(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    """
    Write structured reporting rows to CSV.
    """

    if not rows:
        raise ValueError(
            f"Cannot write empty D15 CSV: {path}"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(
        rows[0].keys()
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:

            normalized_row = {}

            for key in fieldnames:

                value = row.get(key)

                if isinstance(
                    value,
                    (tuple, list, dict),
                ):
                    value = json.dumps(
                        value,
                        ensure_ascii=False,
                        sort_keys=True,
                        default=str,
                    )

                normalized_row[key] = value

            writer.writerow(
                normalized_row
            )


def _d15_sha256_file(
    path: Path,
) -> str:
    """
    Calculate SHA256 for one persisted D15 artifact.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:

        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest().upper()


def _d15_relative_path(
    path: Path,
) -> str:
    """
    Return project-relative artifact path.
    """

    return str(
        path.relative_to(
            D15_PROJECT_ROOT
        )
    ).replace("\\", "/")


# ============================================================
# D15-R06.03 — BUILD ARCHITECTURE CONTROL TABLE
# ============================================================

def build_d15_architecture_control_table_rows() -> list[
    dict[str, object]
]:
    """
    Build structured architecture-control evidence.
    """

    architecture = (
        build_d15_architecture_evidence()
    )

    rows = (
        build_d15_architecture_control_rows()
    )

    enriched_rows: list[
        dict[str, object]
    ] = []

    for row in rows:

        enriched = dict(row)

        enriched.update(
            {
                "registry_id": (
                    d15.D15_EXPECTED_REGISTRY_ID
                ),
                "model_version": (
                    d15.D15_EXPECTED_MODEL_VERSION
                ),
                "operating_threshold": (
                    d15.D15_FROZEN_OPERATING_THRESHOLD
                ),
                "output_classification": (
                    architecture[
                        "output_classification"
                    ]
                ),
                "human_oversight_required": True,
                "production_deployment_authorized": False,
            }
        )

        enriched_rows.append(
            enriched
        )

    return enriched_rows


# ============================================================
# D15-R06.04 — BUILD MONITORING CONTROL TABLE
# ============================================================

def build_d15_monitoring_control_table_rows() -> list[
    dict[str, object]
]:
    """
    Serialize all 17 authoritative monitoring controls.
    """

    rows: list[
        dict[str, object]
    ] = []

    for control in (
        d15.D15_MONITORING_CONTROL_CATALOGUE
    ):

        rows.append(
            {
                "control_id": (
                    control["control_id"]
                ),
                "domain": (
                    control["domain"]
                ),
                "control_name": (
                    control["control_name"]
                ),
                "signal": (
                    control["signal"]
                ),
                "reference_type": (
                    control["reference_type"]
                ),
                "cadence": (
                    control["cadence"]
                ),
                "d14_risk_ids": (
                    control["d14_risk_ids"]
                ),
                "governance_action": (
                    control["governance_action"]
                ),
                "production_deployment_authorized": False,
            }
        )

    return rows


# ============================================================
# D15-R06.05 — BUILD QUANTITATIVE REFERENCE TABLE
# ============================================================

def build_d15_quantitative_reference_table_rows() -> list[
    dict[str, object]
]:
    """
    Serialize the six D14-derived internal historical
    surveillance reference bands.
    """

    bands = (
        d15.build_d15_internal_rate_reference_bands()
    )

    rows: list[
        dict[str, object]
    ] = []

    for metric_name, record in bands.items():

        rows.append(
            {
                "metric": metric_name,
                "events": record["events"],
                "denominator": record["denominator"],
                "observed_rate": (
                    record["observed_rate"]
                ),
                "confidence_level": (
                    record["confidence_level"]
                ),
                "lower_bound": (
                    record["lower_bound"]
                ),
                "upper_bound": (
                    record["upper_bound"]
                ),
                "reference_classification": (
                    record[
                        "reference_classification"
                    ]
                ),
                "production_acceptance_limit": (
                    record[
                        "production_acceptance_limit"
                    ]
                ),
                "clinical_acceptability_limit": (
                    record[
                        "clinical_acceptability_limit"
                    ]
                ),
                "external_validation_established": False,
                "clinical_effectiveness_established": False,
                "production_deployment_authorized": False,
            }
        )

    return rows


# ============================================================
# D15-R06.06 — BUILD KNOWN-RISK SLICE TABLE
# ============================================================

def build_d15_known_risk_slice_table_rows() -> list[
    dict[str, object]
]:
    """
    Serialize all five known-risk historical slice references.
    """

    rows: list[
        dict[str, object]
    ] = []

    for slice_name, record in (
        d15.D15_D14_KNOWN_RISK_SLICE_REFERENCES.items()
    ):

        row = {
            "slice_name": slice_name,
        }

        row.update(
            dict(record)
        )

        row[
            "reference_classification"
        ] = (
            "KNOWN_HISTORICAL_RISK_REFERENCE"
        )

        row[
            "production_deployment_authorized"
        ] = False

        rows.append(
            row
        )

    return rows


# ============================================================
# D15-R06.07 — BUILD ESCALATION TRIGGER TABLE
# ============================================================

def build_d15_escalation_trigger_table_rows() -> list[
    dict[str, object]
]:
    """
    Serialize all 17 authoritative escalation triggers.
    """

    rows: list[
        dict[str, object]
    ] = []

    for trigger in (
        d15.D15_ESCALATION_TRIGGER_CATALOGUE
    ):

        row = dict(trigger)

        row[
            "production_deployment_authorized"
        ] = False

        rows.append(
            row
        )

    return rows


# ============================================================
# D15-R06.08 — BUILD GOVERNANCE CONTRACT DOCUMENT
# ============================================================

def build_d15_governance_contract_document() -> str:
    """
    Build formal D15 governance contract.
    """

    return f"""
# D15 — Deployment & Monitoring Design
## Governance Contract

### 1. Lifecycle Identity

- Stage: D15 — Deployment & Monitoring Design
- Source lifecycle stage: D14
- Source Git commit: {D15_REPORTING_SOURCE_COMMIT}
- Next lifecycle stage: D16
- Candidate registry ID: {d15.D15_EXPECTED_REGISTRY_ID}
- Candidate model version: {d15.D15_EXPECTED_MODEL_VERSION}
- Candidate system SHA256: {d15.D15_EXPECTED_CANDIDATE_SYSTEM_SHA256}
- Frozen operating threshold: {d15.D15_FROZEN_OPERATING_THRESHOLD}

### 2. D15 Classification

D15 is a pre-deployment architecture, monitoring, operational-governance,
and evidence-design stage for a research/validation clinical decision-support
prototype.

D15 completion does not constitute production deployment authorization.

### 3. Intended Use

The system is designed only to support clinician-reviewed prioritization of
patients for readmission-prevention review.

The model is advisory. It does not autonomously determine discharge,
treatment, care eligibility, or clinical intervention.

### 4. Frozen-System Controls

The following remain frozen during D15:

- D7 preprocessing
- D8 selected development model
- D9 operating threshold
- D13 registered candidate identity
- D14 locked-test results

D15 prohibits silent retraining, refitting, threshold retuning,
recalibration, or locked-test-driven redesign.

### 5. Human Oversight

Human clinical review is required.

Clinical teams retain final decision authority.

AI output must not replace clinician judgment.

### 6. Validation Boundaries

- Internal locked-test validation completed: TRUE
- External validation established: FALSE
- Prospective validation established: FALSE
- Clinical effectiveness established: FALSE
- Production deployment authorized: FALSE

### 7. Residual Risk

All seven D14 residual risks remain unresolved and are carried forward into
D15 monitoring, operational governance, validation-readiness, and escalation
controls.

### 8. Governance Principle

Engineering readiness, monitoring readiness, and governance-design
completion must not be interpreted as evidence of external validity,
clinical effectiveness, or authorization for production clinical use.
"""


# ============================================================
# D15-R06.09 — BUILD ARCHITECTURE DOCUMENT
# ============================================================

def build_d15_architecture_document() -> str:
    """
    Build formal architecture-design document.
    """

    architecture = (
        build_d15_architecture_evidence()
    )

    layers = "\n".join(
        f"{index}. {layer}"
        for index, layer in enumerate(
            architecture[
                "architecture_layers"
            ],
            start=1,
        )
    )

    source_features = "\n".join(
        f"- {feature}"
        for feature in architecture[
            "required_raw_source_features"
        ]
    )

    return f"""
# D15 — Controlled Deployment Architecture Design

## 1. Architecture Purpose

The architecture defines a controlled clinical-AI inference pathway for the
frozen D13 candidate without authorizing production deployment.

## 2. Controlled Architecture Layers

{layers}

## 3. Governed Raw Input Contract

The controlled inference boundary accepts exactly eight governed source
features:

{source_features}

## 4. Feature Transformation Contract

- Raw governed inputs: 8
- Engineered primary features: 10
- Frozen transformed features: 49
- Frozen preprocessing: D7
- Frozen model: D8
- Frozen operating threshold: {d15.D15_FROZEN_OPERATING_THRESHOLD}

## 5. Output Contract

Output classification:

**{architecture["output_classification"]}**

Allowed advisory states:

- PRIORITIZE_FOR_HUMAN_REVIEW
- NO_MODEL_PRIORITY_FLAG

The output is advisory and requires human clinical interpretation.

## 6. Safety Boundary

The architecture does not permit autonomous discharge, treatment,
eligibility, or care decisions.

## 7. Deployment Status

Production deployment authorized: **FALSE**
"""


# ============================================================
# D15-R06.10 — BUILD MONITORING PLAN DOCUMENT
# ============================================================

def build_d15_monitoring_plan_document() -> str:
    """
    Build formal monitoring and drift-control plan.
    """

    return f"""
# D15 — Monitoring & Drift Control Plan

## 1. Monitoring Objective

The monitoring framework is designed to detect structural, statistical,
performance, subgroup, explainability, workflow, and governance signals
without automatically modifying the model.

## 2. Monitoring Coverage

- Monitoring controls: {len(d15.D15_MONITORING_CONTROL_CATALOGUE)}
- Immediate monitoring domains: {len(d15.D15_IMMEDIATE_MONITORING_DOMAINS)}
- Outcome-dependent monitoring domains: {len(d15.D15_OUTCOME_DEPENDENT_MONITORING_DOMAINS)}
- Escalation triggers: {len(d15.D15_ESCALATION_TRIGGER_CATALOGUE)}

## 3. Quantitative Reference Principle

D14 locked-test rate estimates and uncertainty intervals are classified as
internal historical surveillance references.

They are not:

- production acceptance limits;
- clinical acceptability thresholds;
- external-validation criteria;
- evidence of clinical effectiveness; or
- automatic model-change triggers.

## 4. Statistical Signal Governance

A statistical signal does not automatically establish clinical materiality.

A single monitoring window does not establish persistent drift.

Persistent or material signals require authorized investigation and
governance review.

## 5. Outcome Maturity

Outcome-dependent performance controls are not assessable until sufficient
matured outcome evidence is available.

Insufficient evidence must not default to NORMAL.

## 6. Automated Change Prohibition

Monitoring does not automatically:

- retrain the model;
- recalibrate the model;
- change the operating threshold;
- alter preprocessing;
- introduce subgroup-specific thresholds; or
- authorize production deployment.

## 7. Deployment Status

Production deployment authorized: **FALSE**
"""


# ============================================================
# D15-R06.11 — BUILD OPERATIONAL GOVERNANCE DOCUMENT
# ============================================================

def build_d15_operational_governance_document() -> str:
    """
    Build incident/change/rollback/business-continuity plan.
    """

    continuity = (
        d15.D15_BUSINESS_CONTINUITY_CONTROL
    )

    return f"""
# D15 — Incident, Change, Rollback & Business Continuity Plan

## 1. Incident Governance

D15 defines four incident severity classes:

- SEV1 — Critical
- SEV2 — High
- SEV3 — Moderate
- SEV4 — Low

The incident record contract contains
{len(d15.D15_REQUIRED_INCIDENT_FIELDS)} required fields.

Live enterprise incident-management implementation claimed: **FALSE**

## 2. Change Control

Model-affecting changes require separate controlled change authorization,
revalidation, and version governance.

Automatic model changes are prohibited.

Silent locked-test-driven redesign is prohibited.

## 3. Rollback

D15 defines {len(d15.D15_ROLLBACK_TRIGGERS)} rollback triggers.

A rollback target must be:

- identifiable;
- authorized;
- integrity verified; and
- auditable.

Live enterprise rollback implementation claimed: **FALSE**

## 4. Business Continuity

AI service failure must not block normal clinical care.

Safe fallback workflow:

**{continuity["fallback_workflow"]}**

No synthetic or improvised replacement AI score may be generated during
fallback.

Clinical teams retain decision authority.

## 5. Service Restoration

Service restoration requires integrity validation, incident resolution, and
governance clearance when material.

## 6. Deployment Status

Production deployment authorized: **FALSE**
"""


# ============================================================
# D15-R06.12 — BUILD DEPLOYMENT READINESS ASSESSMENT
# ============================================================

def build_d15_deployment_readiness_assessment_document(
    bootstrap_evidence: dict[str, object],
) -> str:
    """
    Build formal deployment-readiness assessment.
    """

    bootstrap = (
        bootstrap_evidence[
            "bootstrap_evidence"
        ]
    )

    pr_auc = bootstrap["pr_auc"]
    roc_auc = bootstrap["roc_auc"]

    return f"""
# D15 — Deployment Readiness Assessment

## Executive Assessment

The frozen candidate has completed internal locked-test evaluation and D15
deployment/monitoring engineering design.

This does **not** establish production clinical deployment readiness.

## 1. Frozen Candidate

- Registry ID: {d15.D15_EXPECTED_REGISTRY_ID}
- Model version: {d15.D15_EXPECTED_MODEL_VERSION}
- Candidate system SHA256: {d15.D15_EXPECTED_CANDIDATE_SYSTEM_SHA256}
- Operating threshold: {d15.D15_FROZEN_OPERATING_THRESHOLD}

## 2. Internal Locked-Test Evidence

PR-AUC:

- Point estimate: {pr_auc["point_estimate"]:.12f}
- 95% bootstrap interval: [{pr_auc["lower_bound"]:.12f}, {pr_auc["upper_bound"]:.12f}]

ROC-AUC:

- Point estimate: {roc_auc["point_estimate"]:.12f}
- 95% bootstrap interval: [{roc_auc["lower_bound"]:.12f}, {roc_auc["upper_bound"]:.12f}]

Formal bootstrap replicates: {bootstrap["bootstrap_replicates"]}

These intervals characterize internal statistical uncertainty. They are not
production acceptance criteria.

## 3. Readiness Evidence Completed

- Frozen-system identity verification
- Controlled inference architecture
- Input and feature-contract design
- Monitoring-control catalogue
- Quantitative surveillance foundation
- Statistical uncertainty characterization
- Escalation framework
- Incident-management design
- Change-control design
- Rollback design
- Business-continuity design
- D14 residual-risk traceability

## 4. Material Unresolved Risks

Seven D14 residual risks remain unresolved:

1. Utilization-dependent model behavior
2. Explainability utilization dominance
3. Subgroup operating heterogeneity
4. Admission-context heterogeneity
5. Limited model discrimination
6. External transportability not established
7. Clinical effectiveness not established

## 5. Missing Deployment Evidence

The current evidence does not establish:

- external validation;
- prospective validation;
- real-world clinical effectiveness;
- live production monitoring performance;
- live incident-management implementation;
- live rollback implementation; or
- production clinical safety authorization.

## 6. Readiness Disposition

D15 engineering and governance design: **COMPLETED**

Research/validation prototype: **SUPPORTED**

Production deployment authorization: **NOT GRANTED**

External validation: **NOT ESTABLISHED**

Clinical effectiveness: **NOT ESTABLISHED**
"""


# ============================================================
# D15-R06.13 — BUILD FINAL GATE DECISION
# ============================================================

def build_d15_gate_decision_document() -> str:
    """
    Build formal D15 lifecycle gate decision.
    """

    return """
# D15 — Deployment & Monitoring Design Gate Decision

## Gate Decision

**CONDITIONAL PASS — PROGRESS TO D16 WITH DOCUMENTED RESIDUAL RISKS**

## Basis

D15 has established and validated:

- controlled inference architecture;
- frozen-system integrity controls;
- monitoring and drift-control design;
- quantitative surveillance references;
- statistical uncertainty evidence;
- escalation governance;
- incident-management design;
- controlled change governance;
- rollback governance;
- business continuity; and
- residual-risk traceability.

## Conditions

All seven D14 residual risks remain unresolved and must remain visible in
subsequent portfolio, validation, governance, and deployment-readiness
documentation.

D15 completion must not be interpreted as evidence of external validity,
prospective clinical effectiveness, or production clinical authorization.

## Authorized Next Lifecycle Action

Proceed to:

**D16 — Portfolio, Submission & Interview Evidence Package**

## Clinical Deployment Decision

**PRODUCTION DEPLOYMENT NOT AUTHORIZED**

## External Validation

**NOT ESTABLISHED**

## Clinical Effectiveness

**NOT ESTABLISHED**

## Live Incident/Rollback Infrastructure

**NOT ESTABLISHED AS IMPLEMENTED PRODUCTION CAPABILITY**
"""


# ============================================================
# D15-R06.14 — BUILD MANIFEST CONTENT
# ============================================================

def build_d15_manifest_document(
    *,
    artifact_records: list[dict[str, object]],
    bootstrap_evidence: dict[str, object],
    generated_at_utc: str,
) -> str:
    """
    Build YAML-compatible D15 evidence manifest without adding a
    third-party YAML dependency.
    """

    bootstrap = (
        bootstrap_evidence[
            "bootstrap_evidence"
        ]
    )

    lines = [
        "stage_id: D15",
        "stage_name: DEPLOYMENT_AND_MONITORING_DESIGN",
        f"generated_at_utc: {generated_at_utc}",
        f"source_stage: {D15_REPORTING_SOURCE_STAGE}",
        f"source_git_commit: {D15_REPORTING_SOURCE_COMMIT}",
        f"next_stage: {D15_REPORTING_NEXT_STAGE}",
        f"registry_id: {d15.D15_EXPECTED_REGISTRY_ID}",
        f"model_version: {d15.D15_EXPECTED_MODEL_VERSION}",
        (
            "candidate_system_sha256: "
            f"{d15.D15_EXPECTED_CANDIDATE_SYSTEM_SHA256}"
        ),
        (
            "frozen_operating_threshold: "
            f"{d15.D15_FROZEN_OPERATING_THRESHOLD}"
        ),
        (
            "bootstrap_replicates: "
            f"{bootstrap['bootstrap_replicates']}"
        ),
        (
            "bootstrap_confidence_level: "
            f"{bootstrap['confidence_level']}"
        ),
        (
            "bootstrap_random_seed: "
            f"{bootstrap['random_seed']}"
        ),
        (
            "external_validation_established: false"
        ),
        (
            "clinical_effectiveness_established: false"
        ),
        (
            "production_deployment_authorized: false"
        ),
        (
            "residual_risk_count: 7"
        ),
        (
            "gate_decision: "
            "CONDITIONAL_PASS_PROGRESS_TO_D16_"
            "WITH_DOCUMENTED_RESIDUAL_RISKS"
        ),
        "artifacts:",
    ]

    for record in artifact_records:

        lines.extend(
            [
                (
                    f"  - artifact_key: "
                    f"{record['artifact_key']}"
                ),
                (
                    f"    path: "
                    f"{record['path']}"
                ),
                (
                    f"    sha256: "
                    f"{record['sha256']}"
                ),
                (
                    f"    size_bytes: "
                    f"{record['size_bytes']}"
                ),
            ]
        )

    return "\n".join(
        lines
    )


# ============================================================
# D15-R06.15 — GENERATE COMPLETE D15 EVIDENCE PACKAGE
# ============================================================

def generate_d15_evidence_package() -> dict[str, object]:
    """
    Generate all 15 registered D15 evidence artifacts.

    The formal 2,000-replicate bootstrap is calculated once and
    reused throughout the evidence package.
    """

    _d15_ensure_evidence_directories()

    # --------------------------------------------------------
    # Validate upstream reporting layers first
    # --------------------------------------------------------

    r01 = (
        validate_d15_reporting_contract()
    )

    r02 = (
        validate_d15_reporting_architecture_evidence()
    )

    r03 = (
        validate_d15_monitoring_reporting_evidence()
    )

    r05 = (
        validate_d15_operational_risk_reporting_evidence()
    )

    if not all(
        (
            r01["overall_pass"],
            r02["overall_pass"],
            r03["overall_pass"],
            r05["overall_pass"],
        )
    ):
        raise RuntimeError(
            "D15 evidence generation blocked because one or "
            "more prerequisite reporting gates failed."
        )

    # --------------------------------------------------------
    # Formal bootstrap — exactly once
    # --------------------------------------------------------

    bootstrap_evidence = (
        build_d15_formal_bootstrap_reporting_evidence(
            n_bootstrap=(
                D15_REPORTING_BOOTSTRAP_REPLICATES
            )
        )
    )

    r04 = (
        validate_d15_formal_bootstrap_reporting_evidence(
            bootstrap_evidence
        )
    )

    if not r04["overall_pass"]:
        raise RuntimeError(
            "D15 evidence generation blocked because the "
            "formal bootstrap reporting gate failed."
        )

    # --------------------------------------------------------
    # Generate structured tables
    # --------------------------------------------------------

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "architecture_controls"
        ],
        build_d15_architecture_control_table_rows(),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "monitoring_control_catalogue"
        ],
        build_d15_monitoring_control_table_rows(),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "quantitative_reference_bands"
        ],
        build_d15_quantitative_reference_table_rows(),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "bootstrap_discrimination_uncertainty"
        ],
        build_d15_bootstrap_reporting_rows(
            bootstrap_evidence
        ),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "known_risk_slice_references"
        ],
        build_d15_known_risk_slice_table_rows(),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "escalation_trigger_catalogue"
        ],
        build_d15_escalation_trigger_table_rows(),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "residual_risk_traceability"
        ],
        build_d15_residual_risk_reporting_rows(),
    )

    _d15_write_csv(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "operational_control_evidence"
        ],
        build_d15_operational_control_reporting_rows(),
    )

    # --------------------------------------------------------
    # Generate governance documents
    # --------------------------------------------------------

    _d15_write_text(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "governance_contract"
        ],
        build_d15_governance_contract_document(),
    )

    _d15_write_text(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "architecture_design"
        ],
        build_d15_architecture_document(),
    )

    _d15_write_text(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "monitoring_plan"
        ],
        build_d15_monitoring_plan_document(),
    )

    _d15_write_text(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "operational_governance"
        ],
        build_d15_operational_governance_document(),
    )

    _d15_write_text(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "deployment_readiness_assessment"
        ],
        build_d15_deployment_readiness_assessment_document(
            bootstrap_evidence
        ),
    )

    _d15_write_text(
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "gate_decision"
        ],
        build_d15_gate_decision_document(),
    )

    # --------------------------------------------------------
    # Build checksums for all non-manifest artifacts
    # --------------------------------------------------------

    artifact_records: list[
        dict[str, object]
    ] = []

    for artifact_key, path in (
        D15_EVIDENCE_ARTIFACT_REGISTRY.items()
    ):

        if artifact_key == "manifest":
            continue

        if not path.exists():
            raise FileNotFoundError(
                f"Expected D15 artifact missing: {path}"
            )

        artifact_records.append(
            {
                "artifact_key": artifact_key,
                "path": _d15_relative_path(
                    path
                ),
                "sha256": _d15_sha256_file(
                    path
                ),
                "size_bytes": (
                    path.stat().st_size
                ),
            }
        )

    # --------------------------------------------------------
    # Generate manifest last
    # --------------------------------------------------------

    generated_at_utc = (
        datetime.now(
            timezone.utc
        )
        .replace(
            microsecond=0
        )
        .isoformat()
        .replace(
            "+00:00",
            "Z",
        )
    )

    manifest_path = (
        D15_EVIDENCE_ARTIFACT_REGISTRY[
            "manifest"
        ]
    )

    _d15_write_text(
        manifest_path,
        build_d15_manifest_document(
            artifact_records=artifact_records,
            bootstrap_evidence=bootstrap_evidence,
            generated_at_utc=generated_at_utc,
        ),
    )

    # --------------------------------------------------------
    # Final existence validation
    # --------------------------------------------------------

    missing = [
        key
        for key, path in (
            D15_EVIDENCE_ARTIFACT_REGISTRY.items()
        )
        if not path.exists()
    ]

    if missing:
        raise RuntimeError(
            "D15 evidence package incomplete. Missing: "
            + ", ".join(
                missing
            )
        )

    return {
        "stage": "D15",
        "artifact_count": len(
            D15_EVIDENCE_ARTIFACT_REGISTRY
        ),
        "all_artifacts_exist": True,
        "manifest_path": str(
            manifest_path
        ),
        "manifest_sha256": (
            _d15_sha256_file(
                manifest_path
            )
        ),
        "formal_bootstrap": (
            bootstrap_evidence[
                "bootstrap_evidence"
            ]
        ),
        "r01_pass": r01["overall_pass"],
        "r02_pass": r02["overall_pass"],
        "r03_pass": r03["overall_pass"],
        "r04_pass": r04["overall_pass"],
        "r05_pass": r05["overall_pass"],
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R06.16 — PRINT EVIDENCE PACKAGE GENERATION RESULT
# ============================================================

def print_d15_evidence_package_generation() -> None:
    """
    Generate and print the complete D15 evidence package.
    """

    result = (
        generate_d15_evidence_package()
    )

    print("=" * 112)

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "FORMAL EVIDENCE PACKAGE GENERATION"
    )

    print("=" * 112)

    print()

    print(
        f"Registered artifacts:           "
        f"{result['artifact_count']}"
    )

    print(
        f"All artifacts exist:            "
        f"{result['all_artifacts_exist']}"
    )

    print(
        f"R01 reporting contract:         "
        f"{'PASS' if result['r01_pass'] else 'FAIL'}"
    )

    print(
        f"R02 architecture evidence:      "
        f"{'PASS' if result['r02_pass'] else 'FAIL'}"
    )

    print(
        f"R03 monitoring evidence:        "
        f"{'PASS' if result['r03_pass'] else 'FAIL'}"
    )

    print(
        f"R04 bootstrap evidence:         "
        f"{'PASS' if result['r04_pass'] else 'FAIL'}"
    )

    print(
        f"R05 operational/risk evidence:  "
        f"{'PASS' if result['r05_pass'] else 'FAIL'}"
    )

    print()

    print(
        f"Manifest:                       "
        f"{result['manifest_path']}"
    )

    print(
        f"Manifest SHA256:                "
        f"{result['manifest_sha256']}"
    )

    print()

    print(
        "EVIDENCE PACKAGE STATUS:        PASS"
    )

    print(
        "PRODUCTION DEPLOYMENT AUTHORIZED: "
        "False"
    )

    print("=" * 112)

# ============================================================
# D15-R07 — PERSISTED EVIDENCE PACKAGE INTEGRITY VALIDATION
# ============================================================
#
# Purpose
# -------
# Validate the materialized D15 evidence package after
# generation.
#
# This layer verifies:
# - registry completeness;
# - artifact existence;
# - non-empty artifacts;
# - manifest coverage;
# - persisted SHA256 integrity;
# - persisted size integrity;
# - critical lifecycle/governance statements;
# - structured-table row counts;
# - residual-risk preservation;
# - production deployment remains unauthorized.
#
# The manifest intentionally records the 14 non-manifest
# artifacts and does not recursively hash itself.
# ============================================================


# ============================================================
# D15-R07.01 — MANIFEST PARSING
# ============================================================

def _parse_d15_persisted_manifest() -> dict[str, object]:
    """
    Parse the deterministic D15 YAML-compatible manifest using
    the controlled schema produced by R06.

    No external YAML dependency is required.
    """

    manifest_path = (
        D15_EVIDENCE_ARTIFACT_REGISTRY["manifest"]
    )

    if not manifest_path.exists():
        raise FileNotFoundError(
            f"D15 manifest not found: {manifest_path}"
        )

    lines = manifest_path.read_text(
        encoding="utf-8"
    ).splitlines()

    metadata: dict[str, str] = {}
    artifacts: list[dict[str, str]] = []

    current_artifact: dict[str, str] | None = None
    in_artifacts = False

    for line in lines:

        if line == "artifacts:":
            in_artifacts = True
            continue

        if not in_artifacts:

            if ": " in line:
                key, value = line.split(
                    ": ",
                    1,
                )

                metadata[key.strip()] = (
                    value.strip()
                )

            continue

        stripped = line.strip()

        if stripped.startswith(
            "- artifact_key:"
        ):

            if current_artifact is not None:
                artifacts.append(
                    current_artifact
                )

            current_artifact = {
                "artifact_key": (
                    stripped.split(
                        ":",
                        1,
                    )[1].strip()
                )
            }

            continue

        if (
            current_artifact is not None
            and ": " in stripped
        ):

            key, value = stripped.split(
                ": ",
                1,
            )

            current_artifact[
                key.strip()
            ] = value.strip()

    if current_artifact is not None:
        artifacts.append(
            current_artifact
        )

    return {
        "metadata": metadata,
        "artifacts": artifacts,
    }


# ============================================================
# D15-R07.02 — CSV ROW COUNT
# ============================================================

def _count_d15_csv_data_rows(
    path: Path,
) -> int:
    """
    Count persisted CSV data rows excluding the header.
    """

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle
        )

        return sum(
            1
            for _ in reader
        )


# ============================================================
# D15-R07.03 — VALIDATE PERSISTED PACKAGE
# ============================================================

def validate_d15_persisted_evidence_package() -> dict[str, object]:
    """
    Validate the complete persisted D15 evidence package
    against the authoritative reporting registry and manifest.
    """

    parsed = (
        _parse_d15_persisted_manifest()
    )

    metadata = parsed["metadata"]
    manifest_artifacts = (
        parsed["artifacts"]
    )

    registry = (
        D15_EVIDENCE_ARTIFACT_REGISTRY
    )

    required_keys = set(
        D15_REQUIRED_EVIDENCE_ARTIFACT_KEYS
    )

    registry_keys = set(
        registry.keys()
    )

    non_manifest_registry_keys = (
        registry_keys - {"manifest"}
    )

    manifest_keys = {
        record["artifact_key"]
        for record in manifest_artifacts
    }

    # --------------------------------------------------------
    # Physical artifact integrity
    # --------------------------------------------------------

    all_registered_exist = all(
        path.exists()
        for path in registry.values()
    )

    all_registered_nonempty = all(
        path.exists()
        and path.stat().st_size > 0
        for path in registry.values()
    )

    # --------------------------------------------------------
    # Manifest integrity against physical artifacts
    # --------------------------------------------------------

    manifest_hashes_match = True
    manifest_sizes_match = True
    manifest_paths_match = True

    for record in manifest_artifacts:

        artifact_key = (
            record["artifact_key"]
        )

        if artifact_key not in registry:
            manifest_hashes_match = False
            manifest_sizes_match = False
            manifest_paths_match = False
            continue

        path = registry[
            artifact_key
        ]

        expected_relative_path = (
            _d15_relative_path(
                path
            )
        )

        if record.get(
            "path"
        ) != expected_relative_path:
            manifest_paths_match = False

        if record.get(
            "sha256"
        ) != _d15_sha256_file(
            path
        ):
            manifest_hashes_match = False

        if int(
            record.get(
                "size_bytes",
                "-1",
            )
        ) != path.stat().st_size:
            manifest_sizes_match = False

    # --------------------------------------------------------
    # Critical governance documents
    # --------------------------------------------------------

    gate_text = registry[
        "gate_decision"
    ].read_text(
        encoding="utf-8"
    )

    readiness_text = registry[
        "deployment_readiness_assessment"
    ].read_text(
        encoding="utf-8"
    )

    contract_text = registry[
        "governance_contract"
    ].read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Structured evidence row counts
    # --------------------------------------------------------

    csv_row_counts = {
        "architecture_controls": (
            _count_d15_csv_data_rows(
                registry[
                    "architecture_controls"
                ]
            )
        ),

        "monitoring_control_catalogue": (
            _count_d15_csv_data_rows(
                registry[
                    "monitoring_control_catalogue"
                ]
            )
        ),

        "quantitative_reference_bands": (
            _count_d15_csv_data_rows(
                registry[
                    "quantitative_reference_bands"
                ]
            )
        ),

        "bootstrap_discrimination_uncertainty": (
            _count_d15_csv_data_rows(
                registry[
                    "bootstrap_discrimination_uncertainty"
                ]
            )
        ),

        "known_risk_slice_references": (
            _count_d15_csv_data_rows(
                registry[
                    "known_risk_slice_references"
                ]
            )
        ),

        "escalation_trigger_catalogue": (
            _count_d15_csv_data_rows(
                registry[
                    "escalation_trigger_catalogue"
                ]
            )
        ),

        "residual_risk_traceability": (
            _count_d15_csv_data_rows(
                registry[
                    "residual_risk_traceability"
                ]
            )
        ),

        "operational_control_evidence": (
            _count_d15_csv_data_rows(
                registry[
                    "operational_control_evidence"
                ]
            )
        ),
    }

    # --------------------------------------------------------
    # Residual-risk persisted content
    # --------------------------------------------------------

    residual_risk_path = registry[
        "residual_risk_traceability"
    ]

    with residual_risk_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:

        residual_rows = list(
            csv.DictReader(
                handle
            )
        )

    persisted_risk_ids = {
        row["risk_id"]
        for row in residual_rows
    }

    all_persisted_risks_unresolved = all(
        row["handoff_status"]
        == "UNRESOLVED_CARRY_FORWARD"
        for row in residual_rows
    )

    # --------------------------------------------------------
    # Validation checks
    # --------------------------------------------------------

    checks = {

        "registry_contains_15_artifacts": (
            len(registry) == 15
        ),

        "required_key_contract_contains_15_artifacts": (
            len(required_keys) == 15
        ),

        "registry_matches_required_key_contract": (
            registry_keys == required_keys
        ),

        "all_registered_artifacts_exist": (
            all_registered_exist
        ),

        "all_registered_artifacts_are_nonempty": (
            all_registered_nonempty
        ),

        "manifest_contains_14_non_manifest_artifacts": (
            len(manifest_artifacts) == 14
        ),

        "manifest_keys_match_non_manifest_registry": (
            manifest_keys
            == non_manifest_registry_keys
        ),

        "manifest_paths_match_registry": (
            manifest_paths_match
        ),

        "manifest_hashes_match_persisted_artifacts": (
            manifest_hashes_match
        ),

        "manifest_sizes_match_persisted_artifacts": (
            manifest_sizes_match
        ),

        "manifest_stage_is_d15": (
            metadata.get(
                "stage_id"
            )
            == "D15"
        ),

        "manifest_source_stage_is_d14": (
            metadata.get(
                "source_stage"
            )
            == "D14"
        ),

        "manifest_source_commit_is_frozen_d14_commit": (
            metadata.get(
                "source_git_commit"
            )
            == D15_REPORTING_SOURCE_COMMIT
        ),

        "manifest_next_stage_is_d16": (
            metadata.get(
                "next_stage"
            )
            == "D16"
        ),

        "manifest_registry_id_matches_frozen_candidate": (
            metadata.get(
                "registry_id"
            )
            == d15.D15_EXPECTED_REGISTRY_ID
        ),

        "manifest_model_version_matches_frozen_candidate": (
            metadata.get(
                "model_version"
            )
            == d15.D15_EXPECTED_MODEL_VERSION
        ),

        "manifest_candidate_hash_matches_frozen_candidate": (
            metadata.get(
                "candidate_system_sha256"
            )
            == d15.D15_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),

        "manifest_threshold_is_012": (
            metadata.get(
                "frozen_operating_threshold"
            )
            == "0.12"
        ),

        "manifest_bootstrap_replicates_are_2000": (
            metadata.get(
                "bootstrap_replicates"
            )
            == "2000"
        ),

        "manifest_bootstrap_confidence_is_95_percent": (
            metadata.get(
                "bootstrap_confidence_level"
            )
            == "0.95"
        ),

        "manifest_bootstrap_seed_is_42": (
            metadata.get(
                "bootstrap_random_seed"
            )
            == "42"
        ),

        "manifest_residual_risk_count_is_7": (
            metadata.get(
                "residual_risk_count"
            )
            == "7"
        ),

        "manifest_external_validation_not_established": (
            metadata.get(
                "external_validation_established"
            )
            == "false"
        ),

        "manifest_clinical_effectiveness_not_established": (
            metadata.get(
                "clinical_effectiveness_established"
            )
            == "false"
        ),

        "manifest_production_deployment_not_authorized": (
            metadata.get(
                "production_deployment_authorized"
            )
            == "false"
        ),

        "manifest_gate_decision_is_conditional_pass": (
            metadata.get(
                "gate_decision"
            )
            == (
                "CONDITIONAL_PASS_PROGRESS_TO_D16_"
                "WITH_DOCUMENTED_RESIDUAL_RISKS"
            )
        ),

        "architecture_table_has_19_rows": (
            csv_row_counts[
                "architecture_controls"
            ]
            == 19
        ),

        "monitoring_catalogue_has_17_rows": (
            csv_row_counts[
                "monitoring_control_catalogue"
            ]
            == 17
        ),

        "quantitative_reference_table_has_6_rows": (
            csv_row_counts[
                "quantitative_reference_bands"
            ]
            == 6
        ),

        "bootstrap_table_has_2_metric_rows": (
            csv_row_counts[
                "bootstrap_discrimination_uncertainty"
            ]
            == 2
        ),

        "known_risk_slice_table_has_5_rows": (
            csv_row_counts[
                "known_risk_slice_references"
            ]
            == 5
        ),

        "escalation_catalogue_has_17_rows": (
            csv_row_counts[
                "escalation_trigger_catalogue"
            ]
            == 17
        ),

        "residual_risk_table_has_7_rows": (
            csv_row_counts[
                "residual_risk_traceability"
            ]
            == 7
        ),

        "operational_control_table_has_16_rows": (
            csv_row_counts[
                "operational_control_evidence"
            ]
            == 16
        ),

        "persisted_risk_ids_match_required_d14_risks": (
            persisted_risk_ids
            == set(
                d15.D15_REQUIRED_D14_RESIDUAL_RISKS
            )
        ),

        "all_persisted_residual_risks_remain_unresolved": (
            all_persisted_risks_unresolved
        ),

        "gate_preserves_conditional_pass": (
            (
                "CONDITIONAL PASS"
                in gate_text
            )
            and (
                "PROGRESS TO D16 WITH DOCUMENTED "
                "RESIDUAL RISKS"
                in gate_text
            )
        ),

        "gate_prohibits_production_deployment": (
            "PRODUCTION DEPLOYMENT NOT AUTHORIZED"
            in gate_text
        ),

        "gate_preserves_external_validation_boundary": (
            "## External Validation"
            in gate_text
            and "**NOT ESTABLISHED**"
            in gate_text
        ),

        "gate_preserves_clinical_effectiveness_boundary": (
            "## Clinical Effectiveness"
            in gate_text
            and "**NOT ESTABLISHED**"
            in gate_text
        ),

        "readiness_document_preserves_production_boundary": (
            "Production deployment authorization: **NOT GRANTED**"
            in readiness_text
        ),

        "contract_preserves_advisory_human_oversight": (
            "The model is advisory."
            in contract_text
            and (
                "Human clinical review is required."
                in contract_text
            )
        ),

        "production_deployment_remains_unauthorized": True,
    }

    return {
        "manifest": parsed,
        "csv_row_counts": csv_row_counts,
        "checks": checks,
        "overall_pass": all(
            checks.values()
        ),
        "manifest_sha256": (
            _d15_sha256_file(
                registry["manifest"]
            )
        ),
        "production_deployment_authorized": False,
    }


# ============================================================
# D15-R07.04 — PRINT PERSISTED PACKAGE VALIDATION
# ============================================================

def print_d15_persisted_evidence_validation() -> None:
    """
    Print deterministic persisted-package integrity evidence.
    """

    result = (
        validate_d15_persisted_evidence_package()
    )

    print("=" * 112)

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "PERSISTED EVIDENCE PACKAGE INTEGRITY VALIDATION"
    )

    print("=" * 112)

    print()

    print(
        f"Registered artifacts:           "
        f"{len(D15_EVIDENCE_ARTIFACT_REGISTRY)}"
    )

    print(
        f"Manifest child artifacts:       "
        f"{len(result['manifest']['artifacts'])}"
    )

    print()

    print(
        "Persisted structured-evidence rows"
    )

    print("-" * 112)

    for key, count in (
        result["csv_row_counts"].items()
    ):

        print(
            f"{key:<48}"
            f"{count}"
        )

    print()

    print(
        "Integrity & governance validation"
    )

    print("-" * 112)

    for check_name, passed in (
        result["checks"].items()
    ):

        print(
            f"{check_name:<82}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print("-" * 112)

    print(
        "PERSISTED EVIDENCE STATUS:       "
        f"{'PASS' if result['overall_pass'] else 'FAIL'}"
    )

    print(
        f"MANIFEST SHA256:                 "
        f"{result['manifest_sha256']}"
    )

    print(
        "PRODUCTION DEPLOYMENT AUTHORIZED: "
        "False"
    )

    print("=" * 112)