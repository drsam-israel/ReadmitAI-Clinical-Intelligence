# ============================================================
# D15 — DEPLOYMENT & MONITORING DESIGN
# ============================================================
#
# D15.00 — DEPLOYMENT & MONITORING GOVERNANCE CONTRACT
#
# Purpose:
# Establish the governance boundary for designing a controlled
# deployment and monitoring architecture around the frozen D14
# clinical AI candidate.
#
# IMPORTANT:
# D15 does NOT authorize production deployment.
#
# The candidate remains:
#
#   - internally validated on the locked TEST partition;
#   - not externally validated;
#   - not prospectively validated;
#   - not proven clinically effective;
#   - not authorized for production deployment.
#
# D15 may design deployment controls, monitoring specifications,
# human-oversight requirements, rollback controls, incident
# management, and deployment-readiness evidence.
#
# D15 must NOT modify the frozen candidate using locked TEST
# evidence.
# ============================================================


from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


# ============================================================
# D15.01 — LIFECYCLE IDENTITY
# ============================================================


D15_STAGE_ID = "D15"

D15_STAGE_NAME = (
    "Deployment & Monitoring Design"
)

D15_SOURCE_LIFECYCLE_STAGE = "D14"

D15_SOURCE_GIT_COMMIT = "1e003ee"

D15_NEXT_LIFECYCLE_STAGE = (
    "D16_PORTFOLIO_SUBMISSION_AND_INTERVIEW_EVIDENCE_PACKAGE"
)


# ============================================================
# D15.02 — FROZEN REGISTERED CANDIDATE IDENTITY
# ============================================================


D15_EXPECTED_REGISTRY_ID = (
    "DIABETES_READMISSION_XGB_D13_V1"
)

D15_EXPECTED_CANDIDATE_SYSTEM_SHA256 = (
    "9349A52C715517666540C0D5B1EDB148"
    "D48709C0FC2CC77BE9B53F10FE373679"
)

D15_EXPECTED_MODEL_VERSION = "1.0.0"

D15_FROZEN_OPERATING_THRESHOLD = 0.12

D15_THRESHOLD_CLASSIFICATION = (
    "FROZEN_DEVELOPMENT_STAGE_OPERATING_THRESHOLD"
)


# ============================================================
# D15.03 — D14 HANDOFF STATUS
# ============================================================


D15_D14_FINAL_DISPOSITION = (
    "CONDITIONAL_PASS_PROGRESS_TO_D15_"
    "WITH_DOCUMENTED_RESIDUAL_RISKS"
)

D15_INTERNAL_LOCKED_TEST_VALIDATION_COMPLETED = True

D15_EXTERNAL_VALIDATION_ESTABLISHED = False

D15_PROSPECTIVE_VALIDATION_ESTABLISHED = False

D15_CLINICAL_EFFECTIVENESS_ESTABLISHED = False

D15_PRODUCTION_DEPLOYMENT_AUTHORIZED = False


# ============================================================
# D15.04 — D15 DESIGN CLASSIFICATION
# ============================================================


D15_DESIGN_CLASSIFICATION = (
    "PRE_DEPLOYMENT_ARCHITECTURE_AND_MONITORING_DESIGN"
)

D15_IMPLEMENTATION_CLASSIFICATION = (
    "RESEARCH_VALIDATION_PROTOTYPE_ONLY"
)

D15_PRODUCTION_STATUS = (
    "NOT_AUTHORIZED_FOR_PRODUCTION"
)


# ============================================================
# D15.05 — INTENDED CLINICAL DECISION-SUPPORT BOUNDARY
# ============================================================


D15_PRIMARY_USERS = (
    "discharge_planning_team",
    "care_management_team",
    "treating_clinicians",
)

D15_INTENDED_USE = (
    "Support clinician-reviewed prioritization of patients "
    "for readmission-prevention assessment and interventions "
    "before discharge."
)

D15_PROHIBITED_AUTONOMOUS_USE = (
    "The model must not autonomously determine discharge, "
    "treatment, admission, denial of care, or allocation of "
    "clinical resources without qualified human review."
)

D15_HUMAN_OVERSIGHT_REQUIRED = True

D15_HUMAN_OVERRIDE_REQUIRED = True

D15_MODEL_OUTPUT_IS_ADVISORY = True


# ============================================================
# D15.06 — FROZEN SYSTEM COMPONENTS
# ============================================================


D15_FROZEN_COMPONENTS = (
    "D7_PRIMARY_PREPROCESSOR",
    "D7_TRANSFORMED_FEATURE_SCHEMA",
    "D8_SELECTED_XGBOOST_MODEL",
    "D9_OPERATING_THRESHOLD_0_12",
    "D13_REGISTERED_CANDIDATE_IDENTITY",
    "D14_LOCKED_TEST_EVIDENCE",
)

D15_FROZEN_COMPONENT_MODIFICATION_ALLOWED = False


# ============================================================
# D15.07 — PROHIBITED D15 ACTIVITIES
# ============================================================


D15_PROHIBITED_ACTIVITIES = (
    "RETRAIN_MODEL_USING_LOCKED_TEST",
    "RETUNE_MODEL_USING_LOCKED_TEST",
    "RECALIBRATE_MODEL_USING_LOCKED_TEST",
    "CHANGE_FEATURE_SET_USING_LOCKED_TEST",
    "CHANGE_PREPROCESSING_USING_LOCKED_TEST",
    "CHANGE_THRESHOLD_USING_LOCKED_TEST",
    "CREATE_SUBGROUP_THRESHOLDS_FROM_LOCKED_TEST",
    "SELECT_NEW_MODEL_USING_LOCKED_TEST",
    "REDESIGN_CANDIDATE_USING_LOCKED_TEST",
    "CLAIM_EXTERNAL_VALIDATION",
    "CLAIM_PROSPECTIVE_CLINICAL_EFFECTIVENESS",
    "CLAIM_PRODUCTION_DEPLOYMENT_READINESS",
    "AUTHORIZE_PRODUCTION_DEPLOYMENT",
    "ALLOW_AUTONOMOUS_CLINICAL_DECISION_MAKING",
)


# ============================================================
# D15.08 — REQUIRED DEPLOYMENT DESIGN DOMAINS
# ============================================================


D15_REQUIRED_DESIGN_DOMAINS = (
    "SYSTEM_ARCHITECTURE",
    "CLINICAL_WORKFLOW_INTEGRATION",
    "HUMAN_OVERSIGHT",
    "INPUT_DATA_VALIDATION",
    "INFERENCE_SAFETY",
    "OUTPUT_PRESENTATION",
    "AUDIT_LOGGING",
    "ACCESS_CONTROL",
    "MODEL_VERSION_CONTROL",
    "MONITORING",
    "DRIFT_DETECTION",
    "PERFORMANCE_SURVEILLANCE",
    "SUBGROUP_SURVEILLANCE",
    "INCIDENT_MANAGEMENT",
    "CHANGE_CONTROL",
    "ROLLBACK",
    "BUSINESS_CONTINUITY",
    "EXTERNAL_VALIDATION_READINESS",
)


# ============================================================
# D15.09 — REQUIRED MONITORING DOMAINS
# ============================================================


D15_REQUIRED_MONITORING_DOMAINS = (
    "DATA_QUALITY",
    "SCHEMA_INTEGRITY",
    "MISSINGNESS",
    "UNKNOWN_CATEGORY_RATE",
    "INPUT_DISTRIBUTION",
    "PREDICTION_DISTRIBUTION",
    "ALERT_RATE",
    "MODEL_DISCRIMINATION",
    "MODEL_CALIBRATION",
    "OPERATING_POINT_PERFORMANCE",
    "SUBGROUP_PERFORMANCE",
    "UTILIZATION_DEPENDENCE",
    "ADMISSION_CONTEXT_PERFORMANCE",
    "EXPLAINABILITY_STABILITY",
    "CLINICAL_OVERRIDE_RATE",
    "WORKFLOW_ADOPTION",
    "INCIDENTS",
)


# ============================================================
# D15.10 — D14 RESIDUAL-RISK HANDOFF
# ============================================================


D15_REQUIRED_D14_RESIDUAL_RISKS = (
    "D14-RISK-001",
    "D14-RISK-002",
    "D14-RISK-003",
    "D14-RISK-004",
    "D14-RISK-005",
    "D14-RISK-006",
    "D14-RISK-007",
)


D15_D14_RESIDUAL_RISK_HANDOFF = (
    {
        "risk_id": "D14-RISK-001",
        "risk_domain":
            "UTILIZATION_DEPENDENT_MODEL_BEHAVIOR",
        "d15_control_domain":
            "UTILIZATION_DEPENDENCE_MONITORING",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
    {
        "risk_id": "D14-RISK-002",
        "risk_domain":
            "EXPLAINABILITY_UTILIZATION_DOMINANCE",
        "d15_control_domain":
            "EXPLAINABILITY_STABILITY_MONITORING",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
    {
        "risk_id": "D14-RISK-003",
        "risk_domain":
            "SUBGROUP_OPERATING_HETEROGENEITY",
        "d15_control_domain":
            "SUBGROUP_PERFORMANCE_SURVEILLANCE",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
    {
        "risk_id": "D14-RISK-004",
        "risk_domain":
            "ADMISSION_CONTEXT_HETEROGENEITY",
        "d15_control_domain":
            "ADMISSION_CONTEXT_SURVEILLANCE",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
    {
        "risk_id": "D14-RISK-005",
        "risk_domain":
            "LIMITED_MODEL_DISCRIMINATION",
        "d15_control_domain":
            "PERFORMANCE_SURVEILLANCE",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
    {
        "risk_id": "D14-RISK-006",
        "risk_domain":
            "EXTERNAL_TRANSPORTABILITY",
        "d15_control_domain":
            "EXTERNAL_VALIDATION_READINESS",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
    {
        "risk_id": "D14-RISK-007",
        "risk_domain":
            "CLINICAL_EFFECTIVENESS",
        "d15_control_domain":
            "PROSPECTIVE_CLINICAL_VALIDATION",
        "status":
            "UNRESOLVED_CARRY_FORWARD",
    },
)


# ============================================================
# D15.11 — DEPLOYMENT READINESS PRINCIPLE
# ============================================================


D15_DEPLOYMENT_READINESS_PRINCIPLE = (
    "Successful technical implementation or monitoring design "
    "does not itself authorize production deployment."
)

D15_EXTERNAL_VALIDATION_PRINCIPLE = (
    "Internal locked-test performance must not be represented "
    "as external transportability."
)

D15_CLINICAL_EFFECTIVENESS_PRINCIPLE = (
    "Retrospective predictive performance must not be "
    "represented as prospective clinical effectiveness."
)

D15_RESIDUAL_RISK_PRINCIPLE = (
    "Residual risks inherited from D14 must remain visible, "
    "traceable, monitored, and subject to explicit governance "
    "decision before any deployment consideration."
)


# ============================================================
# D15.12 — PRE-IMPLEMENTATION STATE
# ============================================================


D15_SYSTEM_ARCHITECTURE_IMPLEMENTED = False

D15_CLINICAL_WORKFLOW_IMPLEMENTED = False

D15_MONITORING_IMPLEMENTED = False

D15_DRIFT_MONITORING_IMPLEMENTED = False

D15_INCIDENT_MANAGEMENT_IMPLEMENTED = False

D15_ROLLBACK_IMPLEMENTED = False

D15_EXTERNAL_VALIDATION_COMPLETED = False

D15_PROSPECTIVE_VALIDATION_COMPLETED = False

D15_PRODUCTION_DEPLOYMENT_COMPLETED = False

D15_PRODUCTION_DEPLOYMENT_AUTHORIZED = False


# ============================================================
# D15.13 — GOVERNANCE CONTRACT
# ============================================================


@dataclass(frozen=True)
class D15DeploymentMonitoringGovernanceContract:
    stage_id: str
    stage_name: str
    source_lifecycle_stage: str
    source_git_commit: str
    registry_id: str
    candidate_system_sha256: str
    model_version: str
    frozen_threshold: float
    d14_disposition: str
    design_classification: str
    implementation_classification: str
    human_oversight_required: bool
    human_override_required: bool
    model_output_is_advisory: bool
    external_validation_established: bool
    prospective_validation_established: bool
    clinical_effectiveness_established: bool
    production_deployment_authorized: bool
    frozen_component_modification_allowed: bool
    residual_risk_count: int
    next_lifecycle_stage: str


# ============================================================
# D15.14 — BUILD GOVERNANCE CONTRACT
# ============================================================


def build_d15_governance_contract(
) -> D15DeploymentMonitoringGovernanceContract:
    """
    Build the immutable D15 pre-implementation governance
    contract.
    """

    return D15DeploymentMonitoringGovernanceContract(
        stage_id=D15_STAGE_ID,
        stage_name=D15_STAGE_NAME,
        source_lifecycle_stage=(
            D15_SOURCE_LIFECYCLE_STAGE
        ),
        source_git_commit=(
            D15_SOURCE_GIT_COMMIT
        ),
        registry_id=(
            D15_EXPECTED_REGISTRY_ID
        ),
        candidate_system_sha256=(
            D15_EXPECTED_CANDIDATE_SYSTEM_SHA256
        ),
        model_version=(
            D15_EXPECTED_MODEL_VERSION
        ),
        frozen_threshold=(
            D15_FROZEN_OPERATING_THRESHOLD
        ),
        d14_disposition=(
            D15_D14_FINAL_DISPOSITION
        ),
        design_classification=(
            D15_DESIGN_CLASSIFICATION
        ),
        implementation_classification=(
            D15_IMPLEMENTATION_CLASSIFICATION
        ),
        human_oversight_required=(
            D15_HUMAN_OVERSIGHT_REQUIRED
        ),
        human_override_required=(
            D15_HUMAN_OVERRIDE_REQUIRED
        ),
        model_output_is_advisory=(
            D15_MODEL_OUTPUT_IS_ADVISORY
        ),
        external_validation_established=(
            D15_EXTERNAL_VALIDATION_ESTABLISHED
        ),
        prospective_validation_established=(
            D15_PROSPECTIVE_VALIDATION_ESTABLISHED
        ),
        clinical_effectiveness_established=(
            D15_CLINICAL_EFFECTIVENESS_ESTABLISHED
        ),
        production_deployment_authorized=(
            D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
        ),
        frozen_component_modification_allowed=(
            D15_FROZEN_COMPONENT_MODIFICATION_ALLOWED
        ),
        residual_risk_count=len(
            D15_D14_RESIDUAL_RISK_HANDOFF
        ),
        next_lifecycle_stage=(
            D15_NEXT_LIFECYCLE_STAGE
        ),
    )


# ============================================================
# D15.15 — VALIDATE GOVERNANCE CONTRACT
# ============================================================


def validate_d15_governance_contract(
    contract: (
        D15DeploymentMonitoringGovernanceContract
        | None
    ) = None,
) -> dict[str, Any]:
    """
    Fail-closed validation of the D15 pre-implementation
    governance contract.
    """

    if contract is None:
        contract = build_d15_governance_contract()

    residual_risk_ids = {
        item["risk_id"]
        for item in D15_D14_RESIDUAL_RISK_HANDOFF
    }

    checks = {
        "stage_identity_preserved":
            contract.stage_id
            == D15_STAGE_ID,

        "source_stage_is_d14":
            contract.source_lifecycle_stage
            == "D14",

        "source_commit_is_frozen_d14":
            contract.source_git_commit
            == "1e003ee",

        "registered_candidate_preserved":
            contract.registry_id
            == D15_EXPECTED_REGISTRY_ID,

        "candidate_hash_preserved":
            contract.candidate_system_sha256
            == D15_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "model_version_preserved":
            contract.model_version
            == D15_EXPECTED_MODEL_VERSION,

        "threshold_preserved":
            contract.frozen_threshold
            == D15_FROZEN_OPERATING_THRESHOLD,

        "d14_disposition_preserved":
            contract.d14_disposition
            == D15_D14_FINAL_DISPOSITION,

        "human_oversight_required":
            contract.human_oversight_required
            is True,

        "human_override_required":
            contract.human_override_required
            is True,

        "model_output_is_advisory":
            contract.model_output_is_advisory
            is True,

        "external_validation_not_claimed":
            contract.external_validation_established
            is False,

        "prospective_validation_not_claimed":
            contract.prospective_validation_established
            is False,

        "clinical_effectiveness_not_claimed":
            contract.clinical_effectiveness_established
            is False,

        "production_deployment_not_authorized":
            contract.production_deployment_authorized
            is False,

        "frozen_candidate_modification_prohibited":
            contract.frozen_component_modification_allowed
            is False,

        "seven_residual_risks_carried_forward":
            contract.residual_risk_count
            == 7,

        "all_expected_residual_risk_ids_present":
            residual_risk_ids
            == set(
                D15_REQUIRED_D14_RESIDUAL_RISKS
            ),

        "all_residual_risks_unresolved":
            all(
                item["status"]
                == "UNRESOLVED_CARRY_FORWARD"
                for item
                in D15_D14_RESIDUAL_RISK_HANDOFF
            ),

        "required_design_domains_declared":
            len(
                D15_REQUIRED_DESIGN_DOMAINS
            ) >= 18,

        "required_monitoring_domains_declared":
            len(
                D15_REQUIRED_MONITORING_DOMAINS
            ) >= 17,

        "production_not_completed":
            D15_PRODUCTION_DEPLOYMENT_COMPLETED
            is False,

        "next_stage_is_d16":
            contract.next_lifecycle_stage
            == D15_NEXT_LIFECYCLE_STAGE,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "validation_classification":
            "D15_PRE_IMPLEMENTATION_GOVERNANCE_GATE",

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            "PASS"
            if overall_pass
            else "FAIL",

        "residual_risk_count":
            len(
                D15_D14_RESIDUAL_RISK_HANDOFF
            ),

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_DEPLOYMENT_ARCHITECTURE_DESIGN"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_D15_GOVERNANCE_CONTRACT"
            ),
    }


# ============================================================
# D15.16 — BUILD PRE-IMPLEMENTATION EVIDENCE
# ============================================================


def build_d15_preimplementation_evidence(
) -> dict[str, Any]:
    """
    Build the governed evidence bundle establishing the D15
    design boundary before deployment architecture work begins.
    """

    contract = build_d15_governance_contract()

    validation = validate_d15_governance_contract(
        contract
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "stage_name":
            D15_STAGE_NAME,

        "source_lifecycle_stage":
            D15_SOURCE_LIFECYCLE_STAGE,

        "source_git_commit":
            D15_SOURCE_GIT_COMMIT,

        "registry_id":
            D15_EXPECTED_REGISTRY_ID,

        "candidate_system_sha256":
            D15_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "model_version":
            D15_EXPECTED_MODEL_VERSION,

        "frozen_threshold":
            D15_FROZEN_OPERATING_THRESHOLD,

        "d14_final_disposition":
            D15_D14_FINAL_DISPOSITION,

        "design_classification":
            D15_DESIGN_CLASSIFICATION,

        "implementation_classification":
            D15_IMPLEMENTATION_CLASSIFICATION,

        "intended_use":
            D15_INTENDED_USE,

        "prohibited_autonomous_use":
            D15_PROHIBITED_AUTONOMOUS_USE,

        "primary_users":
            list(
                D15_PRIMARY_USERS
            ),

        "frozen_components":
            list(
                D15_FROZEN_COMPONENTS
            ),

        "prohibited_activities":
            list(
                D15_PROHIBITED_ACTIVITIES
            ),

        "required_design_domains":
            list(
                D15_REQUIRED_DESIGN_DOMAINS
            ),

        "required_monitoring_domains":
            list(
                D15_REQUIRED_MONITORING_DOMAINS
            ),

        "residual_risk_handoff": [
            dict(item)
            for item
            in D15_D14_RESIDUAL_RISK_HANDOFF
        ],

        "contract": {
            field.name: getattr(
                contract,
                field.name,
            )
            for field in fields(
                contract
            )
        },

        "validation":
            validation,

        "external_validation_established":
            False,

        "prospective_validation_established":
            False,

        "clinical_effectiveness_established":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.17 — PRINT GOVERNANCE EVIDENCE
# ============================================================


def print_d15_preimplementation_evidence(
) -> None:
    """
    Print a human-readable D15 governance gate summary.
    """

    evidence = (
        build_d15_preimplementation_evidence()
    )

    validation = evidence[
        "validation"
    ]

    print(
        "=" * 108
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "PRE-IMPLEMENTATION GOVERNANCE CONTRACT"
    )

    print(
        "=" * 108
    )

    print()

    print(
        "Frozen candidate"
    )

    print(
        "-" * 108
    )

    print(
        f"Registry ID:                    "
        f"{evidence['registry_id']}"
    )

    print(
        f"Source D14 Git commit:          "
        f"{evidence['source_git_commit']}"
    )

    print(
        f"Model version:                  "
        f"{evidence['model_version']}"
    )

    print(
        f"Frozen threshold:               "
        f"{evidence['frozen_threshold']}"
    )

    print()

    print(
        "Validation boundary"
    )

    print(
        "-" * 108
    )

    print(
        f"Internal locked TEST complete:  "
        f"{D15_INTERNAL_LOCKED_TEST_VALIDATION_COMPLETED}"
    )

    print(
        f"External validation:            "
        f"{evidence['external_validation_established']}"
    )

    print(
        f"Prospective validation:         "
        f"{evidence['prospective_validation_established']}"
    )

    print(
        f"Clinical effectiveness:         "
        f"{evidence['clinical_effectiveness_established']}"
    )

    print(
        f"Production deployment:          "
        f"{evidence['production_deployment_authorized']}"
    )

    print()

    print(
        "Clinical decision-support boundary"
    )

    print(
        "-" * 108
    )

    print(
        f"Human oversight required:       "
        f"{D15_HUMAN_OVERSIGHT_REQUIRED}"
    )

    print(
        f"Human override required:        "
        f"{D15_HUMAN_OVERRIDE_REQUIRED}"
    )

    print(
        f"Model output advisory only:     "
        f"{D15_MODEL_OUTPUT_IS_ADVISORY}"
    )

    print()

    print(
        "D14 residual-risk handoff"
    )

    print(
        "-" * 108
    )

    for risk in evidence[
        "residual_risk_handoff"
    ]:
        print(
            f"{risk['risk_id']:<15}"
            f"{risk['risk_domain']:<42}"
            f"{risk['status']}"
        )

    print()

    print(
        "Governance checks"
    )

    print(
        "-" * 108
    )

    for (
        check_name,
        passed,
    ) in validation[
        "checks"
    ].items():
        print(
            f"{check_name:<72}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 108
    )

    print(
        f"PRE-IMPLEMENTATION STATUS:      "
        f"{validation['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:         "
        f"{validation['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{validation['production_deployment_authorized']}"
    )

    print(
        "=" * 108
    )


# ============================================================
# D15.18 — GOVERNANCE INTERPRETATION
# ============================================================

# D15 begins from a frozen D14 candidate. The purpose of this
# stage is not to improve the model using locked-test evidence.
#
# D15 instead designs the controlled technical and clinical
# operating environment in which the candidate could be
# evaluated further.
#
# The seven D14 residual risks remain active governance inputs.
#
# In particular:
#
#   D14-RISK-001
#       Utilization-dependent operating behavior must become
#       an explicit monitoring domain.
#
#   D14-RISK-002
#       Utilization-dominant attribution must be monitored for
#       stability and clinically reviewed.
#
#   D14-RISK-003
#       Subgroup operating heterogeneity requires ongoing
#       subgroup surveillance.
#
#   D14-RISK-004
#       Admission-context heterogeneity requires contextual
#       monitoring.
#
#   D14-RISK-005
#       Limited discrimination requires explicit performance
#       surveillance and prevents exaggerated clinical claims.
#
#   D14-RISK-006
#       External transportability remains unresolved and must
#       be addressed through external validation rather than
#       internal TEST reuse.
#
#   D14-RISK-007
#       Clinical effectiveness remains unresolved and requires
#       prospective workflow evaluation.
#
# No successful D15 engineering activity by itself converts
# these unresolved issues into deployment authorization.
# ============================================================

# ============================================================
# D15.20 — CONTROLLED DEPLOYMENT ARCHITECTURE
# ============================================================
#
# Purpose:
# Define the authoritative pre-production inference architecture
# for the frozen registered candidate.
#
# This is an architecture specification. It does NOT constitute
# production deployment authorization.
# ============================================================


# ============================================================
# D15.21 — ARCHITECTURE LAYERS
# ============================================================


D15_ARCHITECTURE_LAYERS = (
    {
        "layer_id": "D15-ARCH-01",
        "layer_name": "INPUT_CAPTURE",
        "purpose": (
            "Capture the governed source variables required "
            "for candidate inference."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-02",
        "layer_name": "INPUT_VALIDATION",
        "purpose": (
            "Validate schema, required fields, permitted "
            "values, missingness, type integrity, and "
            "inference eligibility before preprocessing."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-03",
        "layer_name": "GOVERNED_FEATURE_ENGINEERING",
        "purpose": (
            "Apply the authoritative deterministic D6 feature "
            "engineering logic required by the frozen system."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-04",
        "layer_name": "FROZEN_PREPROCESSING",
        "purpose": (
            "Transform governed source features using the "
            "persisted frozen D7 preprocessing artifact and "
            "transformed feature schema."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-05",
        "layer_name": "FROZEN_MODEL_INFERENCE",
        "purpose": (
            "Generate readmission probability using the "
            "registered frozen D8 XGBoost model."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-06",
        "layer_name": "FROZEN_OPERATING_POINT",
        "purpose": (
            "Apply the frozen 0.12 operating threshold without "
            "runtime optimization or subgroup-specific "
            "threshold adjustment."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-07",
        "layer_name": "ADVISORY_OUTPUT",
        "purpose": (
            "Present probability and advisory prioritization "
            "status to an authorized human reviewer."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-08",
        "layer_name": "EXPLANATION",
        "purpose": (
            "Provide model interpretation evidence without "
            "representing attribution as clinical causality."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-09",
        "layer_name": "AUDIT_LOGGING",
        "purpose": (
            "Record inference provenance, model identity, "
            "threshold identity, validation status, and "
            "human-review events."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-10",
        "layer_name": "MONITORING_TELEMETRY",
        "purpose": (
            "Emit governed telemetry for data quality, model "
            "behavior, subgroup behavior, residual risks, "
            "workflow adoption, and incidents."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-11",
        "layer_name": "HUMAN_OVERSIGHT",
        "purpose": (
            "Require qualified human interpretation, override "
            "capability, and accountability for downstream "
            "clinical action."
        ),
        "mutation_of_frozen_candidate": False,
    },
    {
        "layer_id": "D15-ARCH-12",
        "layer_name": "GOVERNANCE_CONTROL",
        "purpose": (
            "Provide escalation, incident management, change "
            "control, rollback, and deployment-governance "
            "decision mechanisms."
        ),
        "mutation_of_frozen_candidate": False,
    },
)


# ============================================================
# D15.22 — AUTHORITATIVE INFERENCE FLOW
# ============================================================


D15_INFERENCE_FLOW = (
    "INPUT_CAPTURE",
    "INPUT_VALIDATION",
    "GOVERNED_FEATURE_ENGINEERING",
    "FROZEN_PREPROCESSING",
    "FROZEN_MODEL_INFERENCE",
    "FROZEN_OPERATING_POINT",
    "ADVISORY_OUTPUT",
)


D15_PARALLEL_CONTROL_OUTPUTS = (
    "EXPLANATION",
    "AUDIT_LOGGING",
    "MONITORING_TELEMETRY",
)


D15_GOVERNANCE_CONTROL_FLOW = (
    "MONITORING_TELEMETRY",
    "HUMAN_OVERSIGHT",
    "GOVERNANCE_CONTROL",
)


# ============================================================
# D15.23 — INPUT CONTRACT
# ============================================================


D15_REQUIRED_INFERENCE_SOURCE_FEATURES = (
    "race",
    "gender",
    "age",
    "admission_type_id",
    "admission_source_id",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
)


D15_EXPECTED_ENGINEERED_PRIMARY_FEATURES = (
    "race",
    "gender",
    "age",
    "admission_type_id",
    "admission_source_id",
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
)


D15_EXPECTED_RAW_INFERENCE_FEATURE_COUNT = 8

D15_EXPECTED_PRIMARY_FEATURE_COUNT = 10

D15_EXPECTED_TRANSFORMED_FEATURE_COUNT = 49


# ============================================================
# D15.24 — INFERENCE SAFETY RULES
# ============================================================


D15_INFERENCE_SAFETY_RULES = (
    {
        "rule_id": "D15-SAFE-001",
        "rule_name": "REQUIRED_INPUTS_PRESENT",
        "action_on_failure": "BLOCK_INFERENCE",
    },
    {
        "rule_id": "D15-SAFE-002",
        "rule_name": "INPUT_TYPES_VALID",
        "action_on_failure": "BLOCK_INFERENCE",
    },
    {
        "rule_id": "D15-SAFE-003",
        "rule_name": "UTILIZATION_COUNTS_NONNEGATIVE",
        "action_on_failure": "BLOCK_INFERENCE",
    },
    {
        "rule_id": "D15-SAFE-004",
        "rule_name": "FROZEN_PREPROCESSOR_IDENTITY_VALID",
        "action_on_failure": "BLOCK_INFERENCE_AND_ESCALATE",
    },
    {
        "rule_id": "D15-SAFE-005",
        "rule_name": "FROZEN_SCHEMA_IDENTITY_VALID",
        "action_on_failure": "BLOCK_INFERENCE_AND_ESCALATE",
    },
    {
        "rule_id": "D15-SAFE-006",
        "rule_name": "FROZEN_MODEL_IDENTITY_VALID",
        "action_on_failure": "BLOCK_INFERENCE_AND_ESCALATE",
    },
    {
        "rule_id": "D15-SAFE-007",
        "rule_name": "TRANSFORMED_DIMENSION_VALID",
        "action_on_failure": "BLOCK_INFERENCE",
    },
    {
        "rule_id": "D15-SAFE-008",
        "rule_name": "TRANSFORMED_VALUES_FINITE",
        "action_on_failure": "BLOCK_INFERENCE",
    },
    {
        "rule_id": "D15-SAFE-009",
        "rule_name": "PROBABILITY_FINITE_AND_BOUNDED",
        "action_on_failure": "BLOCK_OUTPUT_AND_ESCALATE",
    },
    {
        "rule_id": "D15-SAFE-010",
        "rule_name": "FROZEN_THRESHOLD_PRESERVED",
        "action_on_failure": "BLOCK_OUTPUT_AND_ESCALATE",
    },
    {
        "rule_id": "D15-SAFE-011",
        "rule_name": "HUMAN_REVIEW_REQUIRED",
        "action_on_failure": "NO_CLINICAL_ACTION",
    },
    {
        "rule_id": "D15-SAFE-012",
        "rule_name": "AUDIT_EVENT_REQUIRED",
        "action_on_failure": "ESCALATE_LOGGING_FAILURE",
    },
)


# ============================================================
# D15.25 — OUTPUT CONTRACT
# ============================================================


D15_REQUIRED_OUTPUT_FIELDS = (
    "registry_id",
    "model_version",
    "candidate_system_sha256",
    "prediction_probability",
    "frozen_threshold",
    "advisory_flag",
    "output_classification",
    "human_review_required",
    "deployment_authorized",
)


D15_OUTPUT_CLASSIFICATION = (
    "CLINICAL_DECISION_SUPPORT_ADVISORY"
)


D15_ALLOWED_ADVISORY_FLAGS = (
    "PRIORITIZE_FOR_HUMAN_REVIEW",
    "NO_MODEL_PRIORITY_FLAG",
)


D15_OUTPUT_DISCLAIMER = (
    "This output is a research/validation clinical decision-"
    "support signal from an internally validated candidate. "
    "It is not an autonomous clinical decision, does not "
    "establish clinical effectiveness, and is not authorized "
    "for production deployment."
)


# ============================================================
# D15.26 — AUDIT EVENT CONTRACT
# ============================================================


D15_REQUIRED_AUDIT_FIELDS = (
    "event_timestamp_utc",
    "event_type",
    "registry_id",
    "model_version",
    "candidate_system_sha256",
    "preprocessor_sha256",
    "schema_sha256",
    "model_sha256",
    "frozen_threshold",
    "input_validation_status",
    "inference_status",
    "advisory_flag",
    "human_review_required",
    "deployment_authorized",
)


D15_AUDIT_EVENT_TYPES = (
    "INFERENCE_REQUESTED",
    "INFERENCE_BLOCKED",
    "INFERENCE_COMPLETED",
    "HUMAN_REVIEW_RECORDED",
    "HUMAN_OVERRIDE_RECORDED",
    "MONITORING_ALERT",
    "MODEL_INCIDENT",
    "ROLLBACK_EVENT",
)


# ============================================================
# D15.27 — HUMAN OVERSIGHT CONTRACT
# ============================================================


D15_HUMAN_REVIEW_OUTCOMES = (
    "REVIEWED_MODEL_PRIORITY_ACCEPTED",
    "REVIEWED_MODEL_PRIORITY_OVERRIDDEN",
    "REVIEWED_NO_MODEL_PRIORITY_ACCEPTED",
    "REVIEWED_NO_MODEL_PRIORITY_OVERRIDDEN",
    "REVIEW_INCOMPLETE",
)


D15_HUMAN_OVERRIDE_REASONS = (
    "CLINICAL_CONTEXT_NOT_CAPTURED",
    "DATA_QUALITY_CONCERN",
    "KNOWN_RECENT_EVENT_NOT_IN_MODEL_INPUT",
    "MODEL_OUTPUT_INCONSISTENT_WITH_CLINICAL_ASSESSMENT",
    "WORKFLOW_OR_RESOURCE_CONSTRAINT",
    "OTHER_DOCUMENTED_REASON",
)


# ============================================================
# D15.28 — VALIDATE ARCHITECTURE DESIGN
# ============================================================


def validate_d15_deployment_architecture(
) -> dict[str, Any]:
    """
    Validate the D15 controlled deployment architecture.

    This validates architecture completeness and governance
    boundaries. It does not authorize production deployment.
    """

    layer_names = tuple(
        item["layer_name"]
        for item in D15_ARCHITECTURE_LAYERS
    )

    layer_ids = tuple(
        item["layer_id"]
        for item in D15_ARCHITECTURE_LAYERS
    )

    safety_rule_ids = tuple(
        item["rule_id"]
        for item in D15_INFERENCE_SAFETY_RULES
    )

    checks = {
        "twelve_architecture_layers_declared":
            len(D15_ARCHITECTURE_LAYERS)
            == 12,

        "architecture_layer_ids_unique":
            len(layer_ids)
            == len(set(layer_ids)),

        "architecture_layer_names_unique":
            len(layer_names)
            == len(set(layer_names)),

        "all_inference_flow_layers_declared":
            set(D15_INFERENCE_FLOW).issubset(
                set(layer_names)
            ),

        "all_parallel_control_layers_declared":
            set(
                D15_PARALLEL_CONTROL_OUTPUTS
            ).issubset(
                set(layer_names)
            ),

        "all_governance_control_layers_declared":
            set(
                D15_GOVERNANCE_CONTROL_FLOW
            ).issubset(
                set(layer_names)
            ),

        "no_architecture_layer_mutates_candidate":
            all(
                item[
                    "mutation_of_frozen_candidate"
                ] is False
                for item
                in D15_ARCHITECTURE_LAYERS
            ),

        "eight_required_source_features":
            len(
                D15_REQUIRED_INFERENCE_SOURCE_FEATURES
            ) == 8,

        "ten_primary_features_expected":
            len(
                D15_EXPECTED_ENGINEERED_PRIMARY_FEATURES
            ) == 10,

        "transformed_dimension_is_49":
            D15_EXPECTED_TRANSFORMED_FEATURE_COUNT
            == 49,

        "twelve_inference_safety_rules":
            len(
                D15_INFERENCE_SAFETY_RULES
            ) == 12,

        "safety_rule_ids_unique":
            len(safety_rule_ids)
            == len(set(safety_rule_ids)),

        "artifact_identity_failures_block_inference":
            all(
                item["action_on_failure"]
                == "BLOCK_INFERENCE_AND_ESCALATE"
                for item
                in D15_INFERENCE_SAFETY_RULES
                if item["rule_name"] in {
                    "FROZEN_PREPROCESSOR_IDENTITY_VALID",
                    "FROZEN_SCHEMA_IDENTITY_VALID",
                    "FROZEN_MODEL_IDENTITY_VALID",
                }
            ),

        "human_review_required":
            D15_HUMAN_OVERSIGHT_REQUIRED
            is True,

        "human_override_required":
            D15_HUMAN_OVERRIDE_REQUIRED
            is True,

        "output_is_advisory":
            D15_MODEL_OUTPUT_IS_ADVISORY
            is True,

        "output_contract_contains_probability":
            "prediction_probability"
            in D15_REQUIRED_OUTPUT_FIELDS,

        "output_contract_contains_threshold":
            "frozen_threshold"
            in D15_REQUIRED_OUTPUT_FIELDS,

        "output_contract_contains_human_review":
            "human_review_required"
            in D15_REQUIRED_OUTPUT_FIELDS,

        "output_contract_contains_deployment_status":
            "deployment_authorized"
            in D15_REQUIRED_OUTPUT_FIELDS,

        "audit_contract_contains_candidate_identity":
            "candidate_system_sha256"
            in D15_REQUIRED_AUDIT_FIELDS,

        "audit_contract_contains_component_hashes":
            {
                "preprocessor_sha256",
                "schema_sha256",
                "model_sha256",
            }.issubset(
                set(
                    D15_REQUIRED_AUDIT_FIELDS
                )
            ),

        "human_override_events_supported":
            "HUMAN_OVERRIDE_RECORDED"
            in D15_AUDIT_EVENT_TYPES,

        "monitoring_alert_events_supported":
            "MONITORING_ALERT"
            in D15_AUDIT_EVENT_TYPES,

        "rollback_events_supported":
            "ROLLBACK_EVENT"
            in D15_AUDIT_EVENT_TYPES,

        "frozen_threshold_preserved":
            D15_FROZEN_OPERATING_THRESHOLD
            == 0.12,

        "production_deployment_not_authorized":
            D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "validation_classification":
            "D15_CONTROLLED_DEPLOYMENT_ARCHITECTURE_GATE",

        "architecture_layer_count":
            len(
                D15_ARCHITECTURE_LAYERS
            ),

        "source_feature_count":
            len(
                D15_REQUIRED_INFERENCE_SOURCE_FEATURES
            ),

        "primary_feature_count":
            len(
                D15_EXPECTED_ENGINEERED_PRIMARY_FEATURES
            ),

        "transformed_feature_count":
            D15_EXPECTED_TRANSFORMED_FEATURE_COUNT,

        "safety_rule_count":
            len(
                D15_INFERENCE_SAFETY_RULES
            ),

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_CONTROLLED_INFERENCE_SERVICE_IMPLEMENTATION"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_D15_ARCHITECTURE"
            ),
    }


# ============================================================
# D15.29 — PRINT ARCHITECTURE EVIDENCE
# ============================================================


def print_d15_deployment_architecture(
) -> None:
    """
    Print the D15 controlled deployment architecture and
    architecture-governance validation.
    """

    validation = (
        validate_d15_deployment_architecture()
    )

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "CONTROLLED DEPLOYMENT ARCHITECTURE"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Architecture flow"
    )

    print(
        "-" * 112
    )

    for index, layer in enumerate(
        D15_INFERENCE_FLOW,
        start=1,
    ):
        print(
            f"{index:02d}. {layer}"
        )

    print()

    print(
        "Parallel control outputs"
    )

    print(
        "-" * 112
    )

    for layer in (
        D15_PARALLEL_CONTROL_OUTPUTS
    ):
        print(
            f"- {layer}"
        )

    print()

    print(
        "Governance control path"
    )

    print(
        "-" * 112
    )

    print(
        " -> ".join(
            D15_GOVERNANCE_CONTROL_FLOW
        )
    )

    print()

    print(
        "Inference contract"
    )

    print(
        "-" * 112
    )

    print(
        f"Required source features:       "
        f"{validation['source_feature_count']}"
    )

    print(
        f"Governed primary features:      "
        f"{validation['primary_feature_count']}"
    )

    print(
        f"Transformed features:           "
        f"{validation['transformed_feature_count']}"
    )

    print(
        f"Frozen threshold:               "
        f"{D15_FROZEN_OPERATING_THRESHOLD}"
    )

    print(
        f"Output classification:          "
        f"{D15_OUTPUT_CLASSIFICATION}"
    )

    print(
        f"Human review required:          "
        f"{D15_HUMAN_OVERSIGHT_REQUIRED}"
    )

    print()

    print(
        "Architecture validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in validation[
        "checks"
    ].items():
        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"ARCHITECTURE STATUS:            "
        f"{validation['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:         "
        f"{validation['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{validation['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )


# ============================================================
# D15.29A — ARCHITECTURE INTERPRETATION
# ============================================================

# This architecture establishes a fail-closed inference path.
#
# The application layer will not be permitted to bypass:
#
#   input validation
#   -> governed feature engineering
#   -> frozen preprocessing
#   -> frozen model
#   -> frozen threshold
#   -> advisory output
#
# Artifact identity failures are blocking failures.
#
# Clinical users retain authority over downstream action.
#
# Audit logging and monitoring are architectural requirements,
# not optional application features.
#
# Production deployment remains unauthorized.
# ============================================================

# ============================================================
# D15.30 — CONTROLLED INFERENCE SERVICE
# ============================================================
#
# Purpose:
# Implement the reusable governed inference pathway for the
# frozen registered candidate.
#
# This service:
#
#   raw governed input
#       -> validation
#       -> authoritative D6 feature engineering
#       -> frozen D7 normalization/preprocessing
#       -> frozen D8 model inference
#       -> frozen D9 threshold
#       -> advisory output
#       -> audit event
#       -> monitoring telemetry
#
# IMPORTANT:
# This is a research/validation inference service.
# It does NOT authorize production deployment.
# ============================================================


from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import math

import joblib
import numpy as np
import pandas as pd

from src.features.engineering import (
    engineer_prior_utilization_features,
    get_governed_d6_feature_lists,
)

from src.features.preprocessing import (
    D7_PREPROCESSOR_PATH,
    D7_TRANSFORMED_SCHEMA_PATH,
    normalize_source_unknown_categories,
    load_persisted_primary_preprocessor,
    load_persisted_transformed_schema,
)

from src.models.development import (
    D8_EXPECTED_D7_PREPROCESSOR_SHA256,
    D8_EXPECTED_D7_SCHEMA_SHA256,
    D8_SELECTED_MODEL_ARTIFACT_PATH,
    D8_SELECTED_MODEL_METADATA_PATH,
)


# ============================================================
# D15.31 — FROZEN COMPONENT HASHES
# ============================================================


D15_EXPECTED_D7_PREPROCESSOR_SHA256 = (
    D8_EXPECTED_D7_PREPROCESSOR_SHA256
)

D15_EXPECTED_D7_SCHEMA_SHA256 = (
    D8_EXPECTED_D7_SCHEMA_SHA256
)

D15_EXPECTED_D8_MODEL_SHA256 = (
    "2FD02A54DF759EBAAF0D02D64D5ACE16"
    "A519DF016990FAC065AF3249BDA88085"
)

D15_EXPECTED_D8_METADATA_SHA256 = (
    "5838A6C77F05BB183F90B9AA4B0ED9F"
    "0AE5B0FBF2E3E1B1326A79A3A67A1AC76"
)


# ============================================================
# D15.32 — CONTROLLED INFERENCE EXCEPTION
# ============================================================


class D15InferenceBlockedError(RuntimeError):
    """
    Raised when a governed inference request fails a blocking
    safety or artifact-integrity control.
    """


# ============================================================
# D15.33 — FILE-INTEGRITY UTILITIES
# ============================================================


def calculate_d15_file_sha256(
    path: str | Path,
) -> str:
    """
    Calculate SHA256 for a persisted frozen artifact.
    """

    artifact_path = Path(path)

    if not artifact_path.exists():
        raise D15InferenceBlockedError(
            f"Required frozen artifact does not exist: "
            f"{artifact_path}"
        )

    digest = sha256()

    with artifact_path.open("rb") as file_handle:
        for chunk in iter(
            lambda: file_handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest().upper()


def snapshot_d15_frozen_artifacts(
) -> dict[str, Any]:
    """
    Snapshot the identity of all persisted artifacts consumed
    by the D15 controlled inference service.
    """

    return {
        "preprocessor_path":
            str(D7_PREPROCESSOR_PATH),

        "preprocessor_sha256":
            calculate_d15_file_sha256(
                D7_PREPROCESSOR_PATH
            ),

        "schema_path":
            str(D7_TRANSFORMED_SCHEMA_PATH),

        "schema_sha256":
            calculate_d15_file_sha256(
                D7_TRANSFORMED_SCHEMA_PATH
            ),

        "model_path":
            str(
                D8_SELECTED_MODEL_ARTIFACT_PATH
            ),

        "model_sha256":
            calculate_d15_file_sha256(
                D8_SELECTED_MODEL_ARTIFACT_PATH
            ),

        "metadata_path":
            str(
                D8_SELECTED_MODEL_METADATA_PATH
            ),

        "metadata_sha256":
            calculate_d15_file_sha256(
                D8_SELECTED_MODEL_METADATA_PATH
            ),
    }


def validate_d15_frozen_artifact_identity(
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Fail closed if any persisted component differs from the
    frozen candidate identity.
    """

    if snapshot is None:
        snapshot = snapshot_d15_frozen_artifacts()

    checks = {
        "preprocessor_sha256_valid":
            snapshot[
                "preprocessor_sha256"
            ]
            == D15_EXPECTED_D7_PREPROCESSOR_SHA256,

        "schema_sha256_valid":
            snapshot[
                "schema_sha256"
            ]
            == D15_EXPECTED_D7_SCHEMA_SHA256,

        "model_sha256_valid":
            snapshot[
                "model_sha256"
            ]
            == D15_EXPECTED_D8_MODEL_SHA256,

        "metadata_sha256_valid":
            snapshot[
                "metadata_sha256"
            ]
            == D15_EXPECTED_D8_METADATA_SHA256,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "snapshot":
            snapshot,
    }


# ============================================================
# D15.34 — RAW INPUT VALIDATION
# ============================================================


D15_NONNEGATIVE_UTILIZATION_COLUMNS = (
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
)


def validate_d15_inference_input(
    input_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate raw inference input before any model-system
    transformation is performed.

    The first implementation intentionally supports exactly one
    encounter per inference request.
    """

    checks: dict[str, bool] = {}

    checks[
        "input_is_dataframe"
    ] = isinstance(
        input_df,
        pd.DataFrame,
    )

    if not checks["input_is_dataframe"]:
        return {
            "checks": checks,
            "overall_pass": False,
            "validation_status": "FAIL",
        }

    checks[
        "exactly_one_encounter"
    ] = len(input_df) == 1

    required = set(
        D15_REQUIRED_INFERENCE_SOURCE_FEATURES
    )

    actual = set(
        input_df.columns
    )

    checks[
        "all_required_inputs_present"
    ] = required.issubset(
        actual
    )

    checks[
        "no_required_input_is_missing"
    ] = (
        input_df[
            list(
                D15_REQUIRED_INFERENCE_SOURCE_FEATURES
            )
        ].isna().sum().sum()
        == 0
        if required.issubset(actual)
        else False
    )

    utilization_numeric = True
    utilization_nonnegative = True
    utilization_integer_like = True

    if required.issubset(actual):
        for column in (
            D15_NONNEGATIVE_UTILIZATION_COLUMNS
        ):
            value = input_df.iloc[0][column]

            try:
                numeric_value = float(value)
            except (
                TypeError,
                ValueError,
            ):
                utilization_numeric = False
                utilization_nonnegative = False
                utilization_integer_like = False
                continue

            if not math.isfinite(
                numeric_value
            ):
                utilization_numeric = False
                utilization_nonnegative = False
                utilization_integer_like = False
                continue

            if numeric_value < 0:
                utilization_nonnegative = False

            if not numeric_value.is_integer():
                utilization_integer_like = False

    else:
        utilization_numeric = False
        utilization_nonnegative = False
        utilization_integer_like = False

    checks[
        "utilization_counts_numeric"
    ] = utilization_numeric

    checks[
        "utilization_counts_nonnegative"
    ] = utilization_nonnegative

    checks[
        "utilization_counts_integer_like"
    ] = utilization_integer_like

    overall_pass = all(
        checks.values()
    )

    return {
        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),
    }


# ============================================================
# D15.35 — GOVERNED FEATURE ENGINEERING
# ============================================================


def build_d15_governed_primary_features(
    input_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Apply the authoritative frozen D6 deterministic feature
    engineering logic.

    D6 remains the system of record for candidate-feature
    authorization. D15 consumes the authoritative
    ``candidate_features`` list and does not redefine feature
    governance locally.

    No feature-learning operation occurs here.
    """

    # --------------------------------------------------------
    # STEP 1 — Apply authoritative D6 deterministic engineering
    # --------------------------------------------------------

    engineered = (
        engineer_prior_utilization_features(
            input_df.copy()
        )
    )

    # --------------------------------------------------------
    # STEP 2 — Read authoritative D6 governed feature lists
    # --------------------------------------------------------

    governed_lists = (
        get_governed_d6_feature_lists()
    )

    required_governance_keys = {
        "candidate_features",
        "conditional_features",
        "all_registered_model_features",
    }

    actual_governance_keys = set(
        governed_lists.keys()
    )

    if not required_governance_keys.issubset(
        actual_governance_keys
    ):
        missing_keys = sorted(
            required_governance_keys
            - actual_governance_keys
        )

        raise D15InferenceBlockedError(
            "Authoritative D6 feature-governance interface "
            "is incomplete. Missing keys: "
            f"{missing_keys}"
        )

    candidate_features = list(
        governed_lists[
            "candidate_features"
        ]
    )

    conditional_features = list(
        governed_lists[
            "conditional_features"
        ]
    )

    all_registered_features = list(
        governed_lists[
            "all_registered_model_features"
        ]
    )

    # --------------------------------------------------------
    # STEP 3 — Verify frozen candidate-feature contract
    # --------------------------------------------------------

    expected_candidate_features = list(
        D15_EXPECTED_ENGINEERED_PRIMARY_FEATURES
    )

    if candidate_features != (
        expected_candidate_features
    ):
        raise D15InferenceBlockedError(
            "D6 governed candidate-feature contract differs "
            "from the frozen D15 inference contract. "
            f"Expected: {expected_candidate_features}. "
            f"Observed: {candidate_features}."
        )

    if len(candidate_features) != (
        D15_EXPECTED_PRIMARY_FEATURE_COUNT
    ):
        raise D15InferenceBlockedError(
            "D6 candidate-feature count differs from the "
            "frozen D15 contract. "
            f"Expected "
            f"{D15_EXPECTED_PRIMARY_FEATURE_COUNT}; "
            f"observed {len(candidate_features)}."
        )

    # --------------------------------------------------------
    # STEP 4 — Verify D6 registry reconciliation
    # --------------------------------------------------------

    expected_registered_features = (
        candidate_features
        + conditional_features
    )

    if all_registered_features != (
        expected_registered_features
    ):
        raise D15InferenceBlockedError(
            "D6 registered-feature inventory does not "
            "reconcile to candidate + conditional features."
        )

    if len(
        set(candidate_features)
    ) != len(
        candidate_features
    ):
        raise D15InferenceBlockedError(
            "Duplicate candidate features detected in the "
            "authoritative D6 governance contract."
        )

    candidate_conditional_overlap = (
        set(candidate_features)
        & set(conditional_features)
    )

    if candidate_conditional_overlap:
        raise D15InferenceBlockedError(
            "D6 candidate and conditional feature sets "
            "overlap unexpectedly: "
            f"{sorted(candidate_conditional_overlap)}"
        )

    # --------------------------------------------------------
    # STEP 5 — Verify engineered columns exist
    # --------------------------------------------------------

    missing_candidate_features = [
        feature
        for feature
        in candidate_features
        if feature
        not in engineered.columns
    ]

    if missing_candidate_features:
        raise D15InferenceBlockedError(
            "Authoritative D6 feature engineering did not "
            "produce required candidate features: "
            f"{missing_candidate_features}"
        )

    # --------------------------------------------------------
    # STEP 6 — Construct governed primary feature matrix
    # --------------------------------------------------------

    primary = engineered[
        candidate_features
    ].copy()

    expected_shape = (
        len(input_df),
        D15_EXPECTED_PRIMARY_FEATURE_COUNT,
    )

    if primary.shape != expected_shape:
        raise D15InferenceBlockedError(
            "Governed primary feature matrix has an "
            "unexpected shape. "
            f"Expected {expected_shape}; "
            f"observed {primary.shape}."
        )

    # --------------------------------------------------------
    # STEP 7 — Prevent conditional-feature contamination
    # --------------------------------------------------------

    conditional_features_present = [
        feature
        for feature
        in conditional_features
        if feature
        in primary.columns
    ]

    if conditional_features_present:
        raise D15InferenceBlockedError(
            "Conditional D6 features entered the primary "
            "D15 inference matrix: "
            f"{conditional_features_present}"
        )

    # --------------------------------------------------------
    # STEP 8 — Return governed feature evidence
    # --------------------------------------------------------

    return {
        "engineered_source":
            engineered,

        "primary_features":
            primary,

        "candidate_features":
            candidate_features,

        "conditional_features":
            conditional_features,

        "all_registered_model_features":
            all_registered_features,

        "governance_interface_keys":
            sorted(
                actual_governance_keys
            ),

        "candidate_feature_count":
            len(
                candidate_features
            ),

        "conditional_feature_count":
            len(
                conditional_features
            ),

        "registered_feature_count":
            len(
                all_registered_features
            ),

        "conditional_features_in_primary_matrix":
            conditional_features_present,

        "feature_engineering_learned_state":
            False,

        "authoritative_governance_source":
            "D6_GET_GOVERNED_FEATURE_LISTS",

        "feature_contract_status":
            "PASS",
    }
# ============================================================
# D15.36 — FROZEN PREPROCESSING
# ============================================================


def transform_d15_with_frozen_preprocessor(
    primary_features: pd.DataFrame,
) -> dict[str, Any]:
    """
    Normalize source unknown categories and transform using the
    persisted frozen D7 preprocessor.

    The preprocessor is loaded only. It is never fitted here.
    """

    normalized = (
        normalize_source_unknown_categories(
            primary_features.copy()
        )
    )

    preprocessor = (
        load_persisted_primary_preprocessor()
    )

    schema = (
        load_persisted_transformed_schema()
    )

    if len(schema) != (
        D15_EXPECTED_TRANSFORMED_FEATURE_COUNT
    ):
        raise D15InferenceBlockedError(
            "Frozen D7 transformed schema does not contain "
            f"{D15_EXPECTED_TRANSFORMED_FEATURE_COUNT} "
            "features."
        )

    transformed = (
        preprocessor.transform(
            normalized
        )
    )

    if hasattr(
        transformed,
        "toarray",
    ):
        transformed = (
            transformed.toarray()
        )

    transformed = np.asarray(
        transformed,
        dtype=float,
    )

    if transformed.shape != (
        len(primary_features),
        D15_EXPECTED_TRANSFORMED_FEATURE_COUNT,
    ):
        raise D15InferenceBlockedError(
            "Frozen preprocessing produced an unexpected "
            f"shape: {transformed.shape}"
        )

    if not np.isfinite(
        transformed
    ).all():
        raise D15InferenceBlockedError(
            "Frozen preprocessing produced non-finite values."
        )

    transformed_df = pd.DataFrame(
        transformed,
        columns=schema,
        index=primary_features.index,
    )

    return {
        "normalized_primary_features":
            normalized,

        "transformed_features":
            transformed_df,

        "transformed_schema":
            schema,

        "preprocessor":
            preprocessor,

        "preprocessor_refitted":
            False,

        "schema_modified":
            False,
    }


# ============================================================
# D15.37 — FROZEN MODEL INFERENCE
# ============================================================


def load_d15_frozen_model(
):
    """
    Load the persisted D8 model after artifact identity has been
    verified by the controlled inference service.
    """

    return joblib.load(
        D8_SELECTED_MODEL_ARTIFACT_PATH
    )


def generate_d15_frozen_probability(
    model: Any,
    transformed_features: pd.DataFrame,
) -> float:
    """
    Generate one probability from the frozen registered model.
    """

    probabilities = (
        model.predict_proba(
            transformed_features
        )[:, 1]
    )

    if len(probabilities) != 1:
        raise D15InferenceBlockedError(
            "Controlled single-encounter inference returned "
            "an unexpected prediction count."
        )

    probability = float(
        probabilities[0]
    )

    if not math.isfinite(
        probability
    ):
        raise D15InferenceBlockedError(
            "Frozen model returned a non-finite probability."
        )

    if not (
        0.0
        <= probability
        <= 1.0
    ):
        raise D15InferenceBlockedError(
            "Frozen model returned a probability outside "
            "[0, 1]."
        )

    return probability


# ============================================================
# D15.38 — AUDIT + MONITORING EVENT BUILDERS
# ============================================================


def build_d15_advisory_flag(
    probability: float,
) -> str:
    """
    Apply the frozen operating threshold.

    No threshold optimization occurs here.
    """

    if probability >= (
        D15_FROZEN_OPERATING_THRESHOLD
    ):
        return (
            "PRIORITIZE_FOR_HUMAN_REVIEW"
        )

    return (
        "NO_MODEL_PRIORITY_FLAG"
    )


def build_d15_audit_event(
    *,
    artifact_snapshot: dict[str, Any],
    probability: float,
    advisory_flag: str,
    input_validation_status: str,
) -> dict[str, Any]:
    """
    Build a structured audit event for successful inference.
    """

    return {
        "event_timestamp_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "event_type":
            "INFERENCE_COMPLETED",

        "registry_id":
            D15_EXPECTED_REGISTRY_ID,

        "model_version":
            D15_EXPECTED_MODEL_VERSION,

        "candidate_system_sha256":
            D15_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "preprocessor_sha256":
            artifact_snapshot[
                "preprocessor_sha256"
            ],

        "schema_sha256":
            artifact_snapshot[
                "schema_sha256"
            ],

        "model_sha256":
            artifact_snapshot[
                "model_sha256"
            ],

        "frozen_threshold":
            D15_FROZEN_OPERATING_THRESHOLD,

        "input_validation_status":
            input_validation_status,

        "inference_status":
            "COMPLETED",

        "advisory_flag":
            advisory_flag,

        "human_review_required":
            True,

        "deployment_authorized":
            False,

        "prediction_probability":
            probability,
    }


def build_d15_monitoring_telemetry(
    *,
    input_df: pd.DataFrame,
    primary_features: pd.DataFrame,
    probability: float,
    advisory_flag: str,
) -> dict[str, Any]:
    """
    Emit encounter-level monitoring telemetry required by the
    later D15 monitoring layer.

    No patient identifier is required for this prototype
    telemetry contract.
    """

    row = input_df.iloc[0]

    primary_row = (
        primary_features.iloc[0]
    )

    return {
        "telemetry_timestamp_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "registry_id":
            D15_EXPECTED_REGISTRY_ID,

        "model_version":
            D15_EXPECTED_MODEL_VERSION,

        "frozen_threshold":
            D15_FROZEN_OPERATING_THRESHOLD,

        "prediction_probability":
            probability,

        "advisory_flag":
            advisory_flag,

        "race":
            str(row["race"]),

        "gender":
            str(row["gender"]),

        "age":
            str(row["age"]),

        "admission_type_id":
            int(
                row["admission_type_id"]
            ),

        "admission_source_id":
            int(
                row["admission_source_id"]
            ),

        "number_outpatient":
            int(
                row["number_outpatient"]
            ),

        "number_emergency":
            int(
                row["number_emergency"]
            ),

        "number_inpatient":
            int(
                row["number_inpatient"]
            ),

        "prior_outpatient_use":
            int(
                primary_row[
                    "prior_outpatient_use"
                ]
            ),

        "prior_emergency_use":
            int(
                primary_row[
                    "prior_emergency_use"
                ]
            ),

        "prior_inpatient_use":
            int(
                primary_row[
                    "prior_inpatient_use"
                ]
            ),

        "prior_utilization_intensity":
            float(
                primary_row[
                    "prior_utilization_intensity"
                ]
            ),

        "prior_utilization_domain_count":
            int(
                primary_row[
                    "prior_utilization_domain_count"
                ]
            ),

        "human_review_required":
            True,

        "deployment_authorized":
            False,
    }


# ============================================================
# D15.39 — AUTHORITATIVE CONTROLLED INFERENCE SERVICE
# ============================================================


def run_d15_controlled_inference(
    input_record: (
        dict[str, Any]
        | pd.DataFrame
    ),
) -> dict[str, Any]:
    """
    Execute the complete governed D15 inference pathway.

    This is the authoritative backend interface intended for
    later prototype UI consumption.

    The function fails closed if:
      - raw input validation fails;
      - frozen artifact identity fails;
      - D6 feature contract changes;
      - D7 transformed schema changes;
      - transformed values are invalid;
      - model probability is invalid.

    The function does NOT:
      - fit preprocessing;
      - retrain the model;
      - recalibrate the model;
      - retune the model;
      - change the threshold;
      - create subgroup thresholds;
      - authorize production deployment.
    """

    if isinstance(
        input_record,
        dict,
    ):
        input_df = pd.DataFrame(
            [input_record]
        )

    elif isinstance(
        input_record,
        pd.DataFrame,
    ):
        input_df = (
            input_record.copy()
        )

    else:
        raise D15InferenceBlockedError(
            "Inference input must be a dictionary or "
            "pandas DataFrame."
        )

    # --------------------------------------------------------
    # STEP 1 — Raw input validation
    # --------------------------------------------------------

    input_validation = (
        validate_d15_inference_input(
            input_df
        )
    )

    if not input_validation[
        "overall_pass"
    ]:
        raise D15InferenceBlockedError(
            "Inference blocked by raw input validation: "
            f"{input_validation['checks']}"
        )

    # --------------------------------------------------------
    # STEP 2 — Frozen artifact identity
    # --------------------------------------------------------

    before_snapshot = (
        snapshot_d15_frozen_artifacts()
    )

    artifact_validation = (
        validate_d15_frozen_artifact_identity(
            before_snapshot
        )
    )

    if not artifact_validation[
        "overall_pass"
    ]:
        raise D15InferenceBlockedError(
            "Inference blocked because frozen artifact "
            "identity validation failed: "
            f"{artifact_validation['checks']}"
        )

    # --------------------------------------------------------
    # STEP 3 — Governed D6 feature engineering
    # --------------------------------------------------------

    feature_bundle = (
        build_d15_governed_primary_features(
            input_df
        )
    )

    primary_features = (
        feature_bundle[
            "primary_features"
        ]
    )

    # --------------------------------------------------------
    # STEP 4 — Frozen D7 preprocessing
    # --------------------------------------------------------

    preprocessing_bundle = (
        transform_d15_with_frozen_preprocessor(
            primary_features
        )
    )

    transformed_features = (
        preprocessing_bundle[
            "transformed_features"
        ]
    )

    # --------------------------------------------------------
    # STEP 5 — Frozen D8 model inference
    # --------------------------------------------------------

    model = (
        load_d15_frozen_model()
    )

    probability = (
        generate_d15_frozen_probability(
            model,
            transformed_features,
        )
    )

    # --------------------------------------------------------
    # STEP 6 — Frozen D9 operating threshold
    # --------------------------------------------------------

    advisory_flag = (
        build_d15_advisory_flag(
            probability
        )
    )

    # --------------------------------------------------------
    # STEP 7 — Verify artifacts were not rewritten
    # --------------------------------------------------------

    after_snapshot = (
        snapshot_d15_frozen_artifacts()
    )

    artifacts_unchanged = (
        before_snapshot
        == after_snapshot
    )

    if not artifacts_unchanged:
        raise D15InferenceBlockedError(
            "Frozen artifact identity changed during "
            "controlled inference."
        )

    # --------------------------------------------------------
    # STEP 8 — Audit event
    # --------------------------------------------------------

    audit_event = (
        build_d15_audit_event(
            artifact_snapshot=(
                after_snapshot
            ),
            probability=probability,
            advisory_flag=(
                advisory_flag
            ),
            input_validation_status=(
                input_validation[
                    "validation_status"
                ]
            ),
        )
    )

    # --------------------------------------------------------
    # STEP 9 — Monitoring telemetry
    # --------------------------------------------------------

    monitoring_telemetry = (
        build_d15_monitoring_telemetry(
            input_df=input_df,
            primary_features=(
                primary_features
            ),
            probability=probability,
            advisory_flag=(
                advisory_flag
            ),
        )
    )

    # --------------------------------------------------------
    # STEP 10 — Advisory output
    # --------------------------------------------------------

    advisory_output = {
        "registry_id":
            D15_EXPECTED_REGISTRY_ID,

        "model_version":
            D15_EXPECTED_MODEL_VERSION,

        "candidate_system_sha256":
            D15_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "prediction_probability":
            probability,

        "frozen_threshold":
            D15_FROZEN_OPERATING_THRESHOLD,

        "advisory_flag":
            advisory_flag,

        "output_classification":
            D15_OUTPUT_CLASSIFICATION,

        "human_review_required":
            True,

        "deployment_authorized":
            False,

        "disclaimer":
            D15_OUTPUT_DISCLAIMER,
    }

    # --------------------------------------------------------
    # STEP 11 — Final service validation
    # --------------------------------------------------------

    output_fields_present = (
        set(
            D15_REQUIRED_OUTPUT_FIELDS
        ).issubset(
            set(
                advisory_output.keys()
            )
        )
    )

    audit_fields_present = (
        set(
            D15_REQUIRED_AUDIT_FIELDS
        ).issubset(
            set(
                audit_event.keys()
            )
        )
    )

    service_checks = {
        "input_validation_passed":
            input_validation[
                "overall_pass"
            ],

        "frozen_artifact_identity_passed":
            artifact_validation[
                "overall_pass"
            ],

        "d6_feature_engineering_has_no_learned_state":
            feature_bundle[
                "feature_engineering_learned_state"
            ]
            is False,

        "primary_feature_count_is_10":
            primary_features.shape
            == (
                1,
                D15_EXPECTED_PRIMARY_FEATURE_COUNT,
            ),

        "preprocessor_not_refitted":
            preprocessing_bundle[
                "preprocessor_refitted"
            ]
            is False,

        "schema_not_modified":
            preprocessing_bundle[
                "schema_modified"
            ]
            is False,

        "transformed_feature_count_is_49":
            transformed_features.shape
            == (
                1,
                D15_EXPECTED_TRANSFORMED_FEATURE_COUNT,
            ),

        "probability_is_finite":
            math.isfinite(
                probability
            ),

        "probability_is_bounded":
            0.0
            <= probability
            <= 1.0,

        "threshold_is_frozen":
            D15_FROZEN_OPERATING_THRESHOLD
            == 0.12,

        "advisory_flag_valid":
            advisory_flag
            in D15_ALLOWED_ADVISORY_FLAGS,

        "required_output_fields_present":
            output_fields_present,

        "required_audit_fields_present":
            audit_fields_present,

        "frozen_artifacts_unchanged":
            artifacts_unchanged,

        "human_review_required":
            advisory_output[
                "human_review_required"
            ]
            is True,

        "deployment_not_authorized":
            advisory_output[
                "deployment_authorized"
            ]
            is False,
    }

    service_pass = all(
        service_checks.values()
    )

    if not service_pass:
        raise D15InferenceBlockedError(
            "Controlled inference failed final service "
            f"validation: {service_checks}"
        )

    return {
        "stage_id":
            D15_STAGE_ID,

        "service_classification":
            "CONTROLLED_RESEARCH_VALIDATION_INFERENCE",

        "advisory_output":
            advisory_output,

        "input_validation":
            input_validation,

        "artifact_validation":
            artifact_validation,

        "artifact_snapshot_before":
            before_snapshot,

        "artifact_snapshot_after":
            after_snapshot,

        "feature_engineering":
            {
                "candidate_features":
                    feature_bundle[
                        "candidate_features"
                    ],

                "feature_engineering_learned_state":
                    False,
            },

        "preprocessing":
            {
                "transformed_feature_count":
                    transformed_features.shape[1],

                "preprocessor_refitted":
                    False,

                "schema_modified":
                    False,
            },

        "audit_event":
            audit_event,

        "monitoring_telemetry":
            monitoring_telemetry,

        "service_validation":
            {
                "checks":
                    service_checks,

                "overall_pass":
                    service_pass,

                "validation_status":
                    "PASS",

                "next_controlled_action":
                    "D15_INFERENCE_SERVICE_TESTING",
            },

        "model_retrained":
            False,

        "model_retuned":
            False,

        "model_recalibrated":
            False,

        "threshold_retuned":
            False,

        "subgroup_threshold_created":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.39A — PRINT CONTROLLED INFERENCE EVIDENCE
# ============================================================


def print_d15_controlled_inference_evidence(
    input_record: (
        dict[str, Any]
        | pd.DataFrame
    ),
) -> None:
    """
    Execute and print one controlled inference evidence record.
    """

    evidence = (
        run_d15_controlled_inference(
            input_record
        )
    )

    output = evidence[
        "advisory_output"
    ]

    validation = evidence[
        "service_validation"
    ]

    artifact_snapshot = evidence[
        "artifact_snapshot_after"
    ]

    telemetry = evidence[
        "monitoring_telemetry"
    ]

    print(
        "=" * 112
    )

    print(
        "D15 — CONTROLLED INFERENCE SERVICE"
    )

    print(
        "RESEARCH / VALIDATION PROTOTYPE"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Frozen candidate"
    )

    print(
        "-" * 112
    )

    print(
        f"Registry ID:                    "
        f"{output['registry_id']}"
    )

    print(
        f"Model version:                  "
        f"{output['model_version']}"
    )

    print(
        f"Frozen threshold:               "
        f"{output['frozen_threshold']}"
    )

    print()

    print(
        "Frozen artifact identity"
    )

    print(
        "-" * 112
    )

    print(
        f"D7 preprocessor SHA256:         "
        f"{artifact_snapshot['preprocessor_sha256']}"
    )

    print(
        f"D7 schema SHA256:               "
        f"{artifact_snapshot['schema_sha256']}"
    )

    print(
        f"D8 model SHA256:                "
        f"{artifact_snapshot['model_sha256']}"
    )

    print(
        f"D8 metadata SHA256:             "
        f"{artifact_snapshot['metadata_sha256']}"
    )

    print()

    print(
        "Inference result"
    )

    print(
        "-" * 112
    )

    print(
        f"Probability:                     "
        f"{output['prediction_probability']:.12f}"
    )

    print(
        f"Advisory flag:                   "
        f"{output['advisory_flag']}"
    )

    print(
        f"Human review required:           "
        f"{output['human_review_required']}"
    )

    print(
        f"Prior utilization intensity:     "
        f"{telemetry['prior_utilization_intensity']}"
    )

    print(
        f"Prior utilization domains:       "
        f"{telemetry['prior_utilization_domain_count']}"
    )

    print()

    print(
        "Service validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in validation[
        "checks"
    ].items():
        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"INFERENCE SERVICE STATUS:        "
        f"{validation['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{validation['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )


# ============================================================
# D15.39B — SERVICE GOVERNANCE INTERPRETATION
# ============================================================

# This service is the single governed inference backend for the
# later research/validation user interface.
#
# The UI must not:
#
#   - reimplement D6 feature engineering;
#   - fit or alter D7 preprocessing;
#   - load an alternative model;
#   - change the 0.12 threshold;
#   - implement subgroup-specific thresholds;
#   - suppress audit or monitoring telemetry.
#
# The service output is advisory.
#
# A successful inference does not establish:
#
#   - external validation;
#   - prospective validation;
#   - clinical effectiveness;
#   - production deployment authorization.
#
# ============================================================

# ============================================================
# D15.50 — MONITORING & DRIFT CONTROL FRAMEWORK
# ============================================================
#
# Purpose:
# Establish the authoritative monitoring control catalogue for
# the frozen clinical decision-support candidate.
#
# D15 monitoring does NOT:
#
#   - retrain the model automatically;
#   - recalibrate the model automatically;
#   - change the frozen 0.12 threshold;
#   - introduce subgroup-specific thresholds;
#   - treat drift as proof of clinical harm;
#   - treat absence of drift as proof of clinical effectiveness;
#   - authorize production deployment.
#
# Monitoring signals trigger review and governance action.
# ============================================================


# ============================================================
# D15.51 — MONITORING CONTROL CATALOGUE
# ============================================================


D15_MONITORING_CONTROL_CATALOGUE = (
    {
        "control_id": "D15-MON-001",
        "domain": "DATA_QUALITY",
        "control_name": "REQUIRED_INPUT_COMPLETENESS",
        "signal": "required_input_missingness_rate",
        "reference_type": "STRUCTURAL_CONTRACT",
        "cadence": "CONTINUOUS_AND_WINDOWED",
        "d14_risk_ids": (),
        "governance_action":
            "BLOCK_INVALID_INFERENCE_AND_REVIEW_DATA_PIPELINE",
    },
    {
        "control_id": "D15-MON-002",
        "domain": "SCHEMA_INTEGRITY",
        "control_name": "INFERENCE_SCHEMA_CONFORMANCE",
        "signal": "schema_validation_failure_rate",
        "reference_type": "STRUCTURAL_CONTRACT",
        "cadence": "CONTINUOUS",
        "d14_risk_ids": (),
        "governance_action":
            "BLOCK_INVALID_INFERENCE_AND_ESCALATE_SCHEMA_CHANGE",
    },
    {
        "control_id": "D15-MON-003",
        "domain": "MISSINGNESS",
        "control_name": "INPUT_MISSINGNESS_SURVEILLANCE",
        "signal": "feature_missingness_profile",
        "reference_type": "EMPIRICAL_BASELINE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (),
        "governance_action":
            "REVIEW_DATA_QUALITY_AND_SOURCE_SYSTEM",
    },
    {
        "control_id": "D15-MON-004",
        "domain": "UNKNOWN_CATEGORY_RATE",
        "control_name": "UNKNOWN_CATEGORY_SURVEILLANCE",
        "signal": "unknown_category_rate_by_feature",
        "reference_type": "EMPIRICAL_BASELINE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-003",
            "D14-RISK-006",
        ),
        "governance_action":
            "REVIEW_REPRESENTATION_AND_TRANSPORTABILITY",
    },
    {
        "control_id": "D15-MON-005",
        "domain": "INPUT_DISTRIBUTION",
        "control_name": "INPUT_DISTRIBUTION_SHIFT",
        "signal": "feature_distribution_shift",
        "reference_type": "EMPIRICAL_BASELINE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-006",
        ),
        "governance_action":
            "REVIEW_POPULATION_SHIFT_AND_EXTERNAL_VALIDITY",
    },
    {
        "control_id": "D15-MON-006",
        "domain": "PREDICTION_DISTRIBUTION",
        "control_name": "PREDICTION_DISTRIBUTION_SHIFT",
        "signal": "prediction_probability_distribution",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-001",
            "D14-RISK-005",
            "D14-RISK-006",
        ),
        "governance_action":
            "REVIEW_MODEL_BEHAVIOR_AND_POPULATION_SHIFT",
    },
    {
        "control_id": "D15-MON-007",
        "domain": "ALERT_RATE",
        "control_name": "ALERT_RATE_SURVEILLANCE",
        "signal": "alert_rate",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-001",
            "D14-RISK-004",
            "D14-RISK-006",
        ),
        "governance_action":
            "REVIEW_WORKLOAD_AND_OPERATING_BEHAVIOR",
    },
    {
        "control_id": "D15-MON-008",
        "domain": "MODEL_DISCRIMINATION",
        "control_name": "DISCRIMINATION_SURVEILLANCE",
        "signal": "roc_auc_and_pr_auc",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "OUTCOME_MATURED_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-005",
            "D14-RISK-006",
        ),
        "governance_action":
            "ESCALATE_PERFORMANCE_DEGRADATION_REVIEW",
    },
    {
        "control_id": "D15-MON-009",
        "domain": "MODEL_CALIBRATION",
        "control_name": "CALIBRATION_SURVEILLANCE",
        "signal": "brier_logloss_calibration_profile",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "OUTCOME_MATURED_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-005",
            "D14-RISK-006",
        ),
        "governance_action":
            "ESCALATE_CALIBRATION_REVIEW",
    },
    {
        "control_id": "D15-MON-010",
        "domain": "OPERATING_POINT_PERFORMANCE",
        "control_name": "FROZEN_THRESHOLD_PERFORMANCE",
        "signal":
            "sensitivity_specificity_ppv_npv_f1_alert_rate",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "OUTCOME_MATURED_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-001",
            "D14-RISK-005",
            "D14-RISK-006",
        ),
        "governance_action":
            "ESCALATE_OPERATING_POINT_REVIEW",
    },
    {
        "control_id": "D15-MON-011",
        "domain": "SUBGROUP_PERFORMANCE",
        "control_name": "SUBGROUP_HETEROGENEITY_SURVEILLANCE",
        "signal":
            "race_gender_age_subgroup_performance",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "OUTCOME_MATURED_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-003",
            "D14-RISK-006",
        ),
        "governance_action":
            "ESCALATE_RESPONSIBLE_AI_REVIEW",
    },
    {
        "control_id": "D15-MON-012",
        "domain": "UTILIZATION_DEPENDENCE",
        "control_name": "UTILIZATION_DEPENDENCE_SURVEILLANCE",
        "signal":
            "performance_by_prior_utilization_structure",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "OUTCOME_MATURED_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-001",
            "D14-RISK-002",
        ),
        "governance_action":
            "ESCALATE_STRUCTURAL_MODEL_BEHAVIOR_REVIEW",
    },
    {
        "control_id": "D15-MON-013",
        "domain": "ADMISSION_CONTEXT_PERFORMANCE",
        "control_name": "ADMISSION_CONTEXT_SURVEILLANCE",
        "signal":
            "performance_by_admission_context",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "OUTCOME_MATURED_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-004",
            "D14-RISK-006",
        ),
        "governance_action":
            "ESCALATE_CONTEXT_SPECIFIC_PERFORMANCE_REVIEW",
    },
    {
        "control_id": "D15-MON-014",
        "domain": "EXPLAINABILITY_STABILITY",
        "control_name": "ATTRIBUTION_STABILITY_SURVEILLANCE",
        "signal":
            "source_family_attribution_distribution",
        "reference_type": "D14_LOCKED_TEST_REFERENCE",
        "cadence": "PERIODIC_MODEL_REVIEW",
        "d14_risk_ids": (
            "D14-RISK-002",
            "D14-RISK-006",
        ),
        "governance_action":
            "ESCALATE_EXPLAINABILITY_REVIEW",
    },
    {
        "control_id": "D15-MON-015",
        "domain": "CLINICAL_OVERRIDE_RATE",
        "control_name": "HUMAN_OVERRIDE_SURVEILLANCE",
        "signal":
            "human_override_rate_and_reason_distribution",
        "reference_type": "PROSPECTIVE_OPERATIONAL_BASELINE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-007",
        ),
        "governance_action":
            "REVIEW_HUMAN_MODEL_DISAGREEMENT",
    },
    {
        "control_id": "D15-MON-016",
        "domain": "WORKFLOW_ADOPTION",
        "control_name": "WORKFLOW_ADOPTION_SURVEILLANCE",
        "signal":
            "review_completion_and_response_metrics",
        "reference_type": "PROSPECTIVE_OPERATIONAL_BASELINE",
        "cadence": "MONITORING_WINDOW",
        "d14_risk_ids": (
            "D14-RISK-007",
        ),
        "governance_action":
            "REVIEW_WORKFLOW_INTEGRATION_AND_USABILITY",
    },
    {
        "control_id": "D15-MON-017",
        "domain": "INCIDENTS",
        "control_name": "MODEL_INCIDENT_SURVEILLANCE",
        "signal":
            "model_safety_and_governance_incident_events",
        "reference_type": "ZERO_TOLERANCE_EVENT_CONTROL",
        "cadence": "CONTINUOUS",
        "d14_risk_ids": (
            "D14-RISK-001",
            "D14-RISK-002",
            "D14-RISK-003",
            "D14-RISK-004",
            "D14-RISK-005",
            "D14-RISK-006",
            "D14-RISK-007",
        ),
        "governance_action":
            "ACTIVATE_INCIDENT_MANAGEMENT_AND_ESCALATION",
    },
)


# ============================================================
# D15.52 — MONITORING STATE MODEL
# ============================================================


D15_MONITORING_STATES = (
    "NORMAL",
    "WATCH",
    "ALERT",
    "CRITICAL",
    "NOT_ASSESSABLE",
)


D15_MONITORING_ACTIONS = {
    "NORMAL":
        "CONTINUE_GOVERNED_MONITORING",

    "WATCH":
        "INCREASE_REVIEW_AND_INVESTIGATE",

    "ALERT":
        "FORMAL_GOVERNANCE_REVIEW_REQUIRED",

    "CRITICAL":
        "CONSIDER_SUSPENSION_OR_ROLLBACK_PENDING_REVIEW",

    "NOT_ASSESSABLE":
        "DO_NOT_INFER_SAFETY_FROM_MISSING_EVIDENCE",
}


# ============================================================
# D15.53 — OUTCOME MATURITY CONTRACT
# ============================================================


D15_OUTCOME_DEPENDENT_MONITORING_DOMAINS = (
    "MODEL_DISCRIMINATION",
    "MODEL_CALIBRATION",
    "OPERATING_POINT_PERFORMANCE",
    "SUBGROUP_PERFORMANCE",
    "UTILIZATION_DEPENDENCE",
    "ADMISSION_CONTEXT_PERFORMANCE",
)


D15_IMMEDIATE_MONITORING_DOMAINS = (
    "DATA_QUALITY",
    "SCHEMA_INTEGRITY",
    "MISSINGNESS",
    "UNKNOWN_CATEGORY_RATE",
    "INPUT_DISTRIBUTION",
    "PREDICTION_DISTRIBUTION",
    "ALERT_RATE",
    "EXPLAINABILITY_STABILITY",
    "CLINICAL_OVERRIDE_RATE",
    "WORKFLOW_ADOPTION",
    "INCIDENTS",
)


# ============================================================
# D15.54 — D14 LOCKED-TEST REFERENCE BASELINE
# ============================================================
#
# These values are historical internal locked-test references.
#
# They are NOT:
#
#   - production targets;
#   - external validation benchmarks;
#   - clinical-effectiveness targets;
#   - authorization thresholds.
#
# They provide traceable internal reference values against
# which future monitoring observations may be compared.
# ============================================================


D15_D14_LOCKED_TEST_REFERENCE = {
    "encounter_count":
        15038,

    "positive_count":
        1707,

    "negative_count":
        13331,

    "prevalence":
        0.113512,

    "pr_auc":
        0.182040618234,

    "roc_auc":
        0.623405163566,

    "brier_score":
        0.098257477438,

    "log_loss":
        0.343252654445,

    "sensitivity":
        0.487404803749,

    "specificity":
        0.705423449104,

    "ppv":
        0.174826644253,

    "npv":
        0.914874987839,

    "f1":
        0.257346118157,

    "alert_count":
        4759,

    "alert_rate":
        0.316464955446,

    "alerts_per_100":
        31.6464955446,

    "frozen_threshold":
        0.12,
}


# ============================================================
# D15.55 — KNOWN RESIDUAL-RISK REFERENCE SIGNALS
# ============================================================


D15_RESIDUAL_RISK_REFERENCE_SIGNALS = {
    "D14-RISK-001": {
        "risk_name":
            "UTILIZATION_DEPENDENT_MODEL_BEHAVIOR",

        "reference_evidence": {
            "zero_utilization_alert_rate":
                0.0,

            "zero_utilization_sensitivity":
                0.0,

            "one_domain_alert_rate":
                0.6056,

            "one_domain_sensitivity":
                0.7467,

            "two_plus_domains_alert_rate":
                0.9254,

            "two_plus_domains_sensitivity":
                0.9789,

            "intensity_ge_3_alert_rate":
                0.8654,

            "intensity_ge_3_sensitivity":
                0.9619,
        },
    },

    "D14-RISK-002": {
        "risk_name":
            "EXPLAINABILITY_UTILIZATION_DOMINANCE",

        "reference_evidence": {
            "validation_prior_utilization_attribution_pct":
                68.52025594108491,

            "locked_test_prior_utilization_attribution_pct":
                77.274016,

            "validation_to_test_difference_pp":
                8.753760,
        },
    },

    "D14-RISK-003": {
        "risk_name":
            "SUBGROUP_OPERATING_HETEROGENEITY",

        "reference_evidence": {
            "primary_dimensions":
                (
                    "race",
                    "gender",
                    "age",
                ),

            "interpretation":
                "AGE_STRONGEST_DESCRIPTIVE_HETEROGENEITY",
        },
    },

    "D14-RISK-004": {
        "risk_name":
            "ADMISSION_CONTEXT_HETEROGENEITY",

        "reference_evidence": {
            "admission_source_id_6_encounters":
                324,

            "admission_source_id_6_sensitivity":
                0.1379,

            "admission_source_id_6_alert_rate":
                0.1667,
        },
    },

    "D14-RISK-005": {
        "risk_name":
            "LIMITED_MODEL_DISCRIMINATION",

        "reference_evidence": {
            "pr_auc":
                0.182040618234,

            "roc_auc":
                0.623405163566,
        },
    },

    "D14-RISK-006": {
        "risk_name":
            "EXTERNAL_TRANSPORTABILITY",

        "reference_evidence": {
            "external_validation_established":
                False,
        },
    },

    "D14-RISK-007": {
        "risk_name":
            "CLINICAL_EFFECTIVENESS",

        "reference_evidence": {
            "clinical_effectiveness_established":
                False,
        },
    },
}


# ============================================================
# D15.56 — MONITORING THRESHOLD GOVERNANCE
# ============================================================
#
# We deliberately do NOT assign arbitrary numeric WATCH,
# ALERT, or CRITICAL thresholds in this section.
#
# Thresholds must later be justified using:
#
#   1. frozen internal reference evidence;
#   2. clinically meaningful change;
#   3. statistical uncertainty;
#   4. monitoring-window sample size;
#   5. operational capacity;
#   6. prospective evidence where required.
#
# This prevents D15 from manufacturing unsupported limits.
# ============================================================


D15_THRESHOLD_GOVERNANCE = {
    "automatic_model_retraining":
        False,

    "automatic_model_recalibration":
        False,

    "automatic_threshold_adjustment":
        False,

    "subgroup_specific_threshold_adjustment":
        False,

    "monitoring_alert_changes_model":
        False,

    "monitoring_alert_triggers_review":
        True,

    "numeric_limits_require_evidence":
        True,

    "missing_outcome_evidence_is_safe":
        False,
}


# ============================================================
# D15.57 — VALIDATE MONITORING CONTROL CATALOGUE
# ============================================================


def validate_d15_monitoring_control_catalogue(
) -> dict[str, Any]:
    """
    Validate completeness, uniqueness, residual-risk coverage,
    outcome-maturity separation, and governance boundaries of
    the D15 monitoring control catalogue.
    """

    controls = (
        D15_MONITORING_CONTROL_CATALOGUE
    )

    control_ids = [
        item["control_id"]
        for item in controls
    ]

    domains = [
        item["domain"]
        for item in controls
    ]

    expected_risk_ids = {
        f"D14-RISK-{index:03d}"
        for index in range(
            1,
            8,
        )
    }

    covered_risk_ids = {
        risk_id
        for item in controls
        for risk_id in item[
            "d14_risk_ids"
        ]
    }

    declared_monitoring_domains = set(
        D15_REQUIRED_MONITORING_DOMAINS
    )

    catalogue_domains = set(
        domains
    )

    outcome_domains = set(
        D15_OUTCOME_DEPENDENT_MONITORING_DOMAINS
    )

    immediate_domains = set(
        D15_IMMEDIATE_MONITORING_DOMAINS
    )

    checks = {
        "seventeen_monitoring_controls_declared":
            len(controls)
            == 17,

        "control_ids_unique":
            len(control_ids)
            == len(
                set(control_ids)
            ),

        "all_required_monitoring_domains_implemented":
            declared_monitoring_domains
            == catalogue_domains,

        "all_seven_d14_residual_risks_covered":
            expected_risk_ids.issubset(
                covered_risk_ids
            ),

        "no_unknown_d14_risk_ids":
            covered_risk_ids.issubset(
                expected_risk_ids
            ),

        "outcome_and_immediate_domains_do_not_overlap":
            outcome_domains.isdisjoint(
                immediate_domains
            ),

        "outcome_and_immediate_domains_cover_catalogue":
            (
                outcome_domains
                | immediate_domains
            )
            == catalogue_domains,

        "incident_control_covers_all_residual_risks":
            set(
                next(
                    item["d14_risk_ids"]
                    for item in controls
                    if item["control_id"]
                    == "D15-MON-017"
                )
            )
            == expected_risk_ids,

        "automatic_retraining_prohibited":
            D15_THRESHOLD_GOVERNANCE[
                "automatic_model_retraining"
            ]
            is False,

        "automatic_recalibration_prohibited":
            D15_THRESHOLD_GOVERNANCE[
                "automatic_model_recalibration"
            ]
            is False,

        "automatic_threshold_adjustment_prohibited":
            D15_THRESHOLD_GOVERNANCE[
                "automatic_threshold_adjustment"
            ]
            is False,

        "subgroup_threshold_adjustment_prohibited":
            D15_THRESHOLD_GOVERNANCE[
                "subgroup_specific_threshold_adjustment"
            ]
            is False,

        "monitoring_alert_triggers_review":
            D15_THRESHOLD_GOVERNANCE[
                "monitoring_alert_triggers_review"
            ]
            is True,

        "missing_outcome_evidence_not_interpreted_as_safe":
            D15_THRESHOLD_GOVERNANCE[
                "missing_outcome_evidence_is_safe"
            ]
            is False,

        "d14_reference_threshold_preserved":
            D15_D14_LOCKED_TEST_REFERENCE[
                "frozen_threshold"
            ]
            == 0.12,

        "external_validation_remains_unestablished":
            D15_RESIDUAL_RISK_REFERENCE_SIGNALS[
                "D14-RISK-006"
            ][
                "reference_evidence"
            ][
                "external_validation_established"
            ]
            is False,

        "clinical_effectiveness_remains_unestablished":
            D15_RESIDUAL_RISK_REFERENCE_SIGNALS[
                "D14-RISK-007"
            ][
                "reference_evidence"
            ][
                "clinical_effectiveness_established"
            ]
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "validation_classification":
            "D15_MONITORING_CONTROL_CATALOGUE_GATE",

        "monitoring_control_count":
            len(controls),

        "covered_residual_risk_count":
            len(
                covered_risk_ids
            ),

        "outcome_dependent_domain_count":
            len(
                outcome_domains
            ),

        "immediate_domain_count":
            len(
                immediate_domains
            ),

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_MONITORING_METRIC_ENGINE"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_MONITORING_CATALOGUE"
            ),
    }


# ============================================================
# D15.58 — PRINT MONITORING CONTROL EVIDENCE
# ============================================================


def print_d15_monitoring_control_catalogue(
) -> None:
    """
    Print the governed D15 monitoring-control catalogue gate.
    """

    evidence = (
        validate_d15_monitoring_control_catalogue()
    )

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "MONITORING & DRIFT CONTROL CATALOGUE"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Monitoring controls"
    )

    print(
        "-" * 112
    )

    for item in (
        D15_MONITORING_CONTROL_CATALOGUE
    ):
        risks = (
            ", ".join(
                item["d14_risk_ids"]
            )
            if item["d14_risk_ids"]
            else "GENERAL_CONTROL"
        )

        print(
            f"{item['control_id']:<14}"
            f"{item['domain']:<34}"
            f"{risks}"
        )

    print()

    print(
        "Monitoring architecture"
    )

    print(
        "-" * 112
    )

    print(
        f"Controls:                       "
        f"{evidence['monitoring_control_count']}"
    )

    print(
        f"D14 residual risks covered:     "
        f"{evidence['covered_residual_risk_count']}"
    )

    print(
        f"Immediate monitoring domains:   "
        f"{evidence['immediate_domain_count']}"
    )

    print(
        f"Outcome-dependent domains:      "
        f"{evidence['outcome_dependent_domain_count']}"
    )

    print()

    print(
        "Governance validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "checks"
    ].items():
        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"MONITORING CATALOGUE STATUS:     "
        f"{evidence['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )


# ============================================================
# D15.59 — MONITORING GOVERNANCE INTERPRETATION
# ============================================================

# The monitoring catalogue converts the seven unresolved D14
# risks into explicit operational surveillance requirements.
#
# Two monitoring classes are deliberately separated:
#
# IMMEDIATE SIGNALS
# -----------------
# Can be assessed before outcomes mature:
#
#   data quality
#   schema integrity
#   missingness
#   unknown categories
#   input distributions
#   prediction distributions
#   alert rates
#   explanation stability
#   human overrides
#   workflow adoption
#   incidents
#
# OUTCOME-DEPENDENT SIGNALS
# -------------------------
# Cannot be validly assessed until 30-day outcomes are mature:
#
#   discrimination
#   calibration
#   operating-point performance
#   subgroup performance
#   utilization-dependent performance
#   admission-context performance
#
# Absence of mature outcome evidence must never be interpreted
# as evidence that model performance is stable.
#
# Monitoring alerts initiate governance review. They do not
# automatically modify the frozen candidate.
#
# Production deployment remains unauthorized.
# ============================================================

# ============================================================
# D15.60 — MONITORING METRIC ENGINE
# ============================================================
#
# Purpose:
# Calculate governed monitoring-window metrics for the frozen
# clinical decision-support candidate.
#
# The engine separates:
#
#   1. immediate inference-time monitoring; and
#   2. outcome-matured retrospective monitoring.
#
# Outcome-dependent metrics are NOT calculated unless valid
# binary 30-day outcomes are supplied.
#
# Monitoring does not modify the frozen candidate.
# ============================================================


from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    brier_score_loss,
    log_loss,
)


# ============================================================
# D15.61 — MONITORING WINDOW CONTRACT
# ============================================================


D15_MONITORING_REQUIRED_COLUMNS = (
    "prediction_probability",
    "advisory_flag",
    "race",
    "gender",
    "age",
    "admission_type_id",
    "admission_source_id",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
)


D15_MONITORING_OUTCOME_COLUMN = (
    "readmitted_30d"
)


D15_VALID_BINARY_OUTCOMES = {
    0,
    1,
}


# ============================================================
# D15.62 — VALIDATE MONITORING WINDOW
# ============================================================


def validate_d15_monitoring_window(
    monitoring_df: pd.DataFrame,
    *,
    require_outcomes: bool = False,
) -> dict[str, Any]:
    """
    Validate a monitoring window before metric calculation.
    """

    checks: dict[str, bool] = {}

    checks[
        "monitoring_input_is_dataframe"
    ] = isinstance(
        monitoring_df,
        pd.DataFrame,
    )

    if not checks[
        "monitoring_input_is_dataframe"
    ]:
        return {
            "checks": checks,
            "overall_pass": False,
            "validation_status": "FAIL",
            "outcomes_available": False,
        }

    checks[
        "monitoring_window_not_empty"
    ] = len(
        monitoring_df
    ) > 0

    required_columns = set(
        D15_MONITORING_REQUIRED_COLUMNS
    )

    actual_columns = set(
        monitoring_df.columns
    )

    checks[
        "required_monitoring_columns_present"
    ] = required_columns.issubset(
        actual_columns
    )

    outcomes_available = (
        D15_MONITORING_OUTCOME_COLUMN
        in monitoring_df.columns
    )

    if require_outcomes:
        checks[
            "outcome_column_present"
        ] = outcomes_available

    if required_columns.issubset(
        actual_columns
    ):
        probability = pd.to_numeric(
            monitoring_df[
                "prediction_probability"
            ],
            errors="coerce",
        )

        checks[
            "probabilities_nonmissing"
        ] = probability.notna().all()

        checks[
            "probabilities_finite"
        ] = bool(
            np.isfinite(
                probability.to_numpy(
                    dtype=float
                )
            ).all()
        )

        checks[
            "probabilities_bounded"
        ] = bool(
            (
                (
                    probability
                    >= 0.0
                )
                & (
                    probability
                    <= 1.0
                )
            ).all()
        )

        checks[
            "advisory_flags_valid"
        ] = bool(
            monitoring_df[
                "advisory_flag"
            ].isin(
                D15_ALLOWED_ADVISORY_FLAGS
            ).all()
        )

    else:
        checks[
            "probabilities_nonmissing"
        ] = False

        checks[
            "probabilities_finite"
        ] = False

        checks[
            "probabilities_bounded"
        ] = False

        checks[
            "advisory_flags_valid"
        ] = False

    if outcomes_available:
        outcome = pd.to_numeric(
            monitoring_df[
                D15_MONITORING_OUTCOME_COLUMN
            ],
            errors="coerce",
        )

        checks[
            "outcomes_nonmissing"
        ] = outcome.notna().all()

        checks[
            "outcomes_binary"
        ] = bool(
            set(
                outcome.dropna().astype(
                    int
                ).unique()
            ).issubset(
                D15_VALID_BINARY_OUTCOMES
            )
        )

    elif require_outcomes:
        checks[
            "outcomes_nonmissing"
        ] = False

        checks[
            "outcomes_binary"
        ] = False

    overall_pass = all(
        checks.values()
    )

    return {
        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "outcomes_available":
            outcomes_available,

        "monitoring_window_size":
            len(
                monitoring_df
            ),
    }


# ============================================================
# D15.63 — IMMEDIATE MONITORING METRICS
# ============================================================


def calculate_d15_immediate_monitoring_metrics(
    monitoring_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Calculate monitoring signals that do not require matured
    30-day outcomes.
    """

    validation = (
        validate_d15_monitoring_window(
            monitoring_df,
            require_outcomes=False,
        )
    )

    if not validation[
        "overall_pass"
    ]:
        raise D15InferenceBlockedError(
            "Monitoring window failed immediate-monitoring "
            f"validation: {validation['checks']}"
        )

    probability = pd.to_numeric(
        monitoring_df[
            "prediction_probability"
        ],
        errors="raise",
    ).astype(float)

    alert_mask = (
        monitoring_df[
            "advisory_flag"
        ]
        == "PRIORITIZE_FOR_HUMAN_REVIEW"
    )

    utilization_intensity = (
        pd.to_numeric(
            monitoring_df[
                "prior_utilization_intensity"
            ],
            errors="raise",
        ).astype(float)
    )

    utilization_domains = (
        pd.to_numeric(
            monitoring_df[
                "prior_utilization_domain_count"
            ],
            errors="raise",
        ).astype(int)
    )

    zero_utilization_mask = (
        utilization_domains
        == 0
    )

    one_domain_mask = (
        utilization_domains
        == 1
    )

    two_plus_domain_mask = (
        utilization_domains
        >= 2
    )

    intensity_ge_3_mask = (
        utilization_intensity
        >= 3
    )

    def _safe_alert_rate(
        mask: pd.Series,
    ) -> float | None:
        count = int(
            mask.sum()
        )

        if count == 0:
            return None

        return float(
            alert_mask[
                mask
            ].mean()
        )

    return {
        "monitoring_mode":
            "IMMEDIATE",

        "encounter_count":
            int(
                len(
                    monitoring_df
                )
            ),

        "prediction_probability_mean":
            float(
                probability.mean()
            ),

        "prediction_probability_std":
            float(
                probability.std(
                    ddof=0
                )
            ),

        "prediction_probability_min":
            float(
                probability.min()
            ),

        "prediction_probability_max":
            float(
                probability.max()
            ),

        "prediction_probability_median":
            float(
                probability.median()
            ),

        "alert_count":
            int(
                alert_mask.sum()
            ),

        "alert_rate":
            float(
                alert_mask.mean()
            ),

        "alerts_per_100":
            float(
                alert_mask.mean()
                * 100.0
            ),

        "zero_utilization_count":
            int(
                zero_utilization_mask.sum()
            ),

        "zero_utilization_fraction":
            float(
                zero_utilization_mask.mean()
            ),

        "zero_utilization_alert_rate":
            _safe_alert_rate(
                zero_utilization_mask
            ),

        "one_domain_count":
            int(
                one_domain_mask.sum()
            ),

        "one_domain_fraction":
            float(
                one_domain_mask.mean()
            ),

        "one_domain_alert_rate":
            _safe_alert_rate(
                one_domain_mask
            ),

        "two_plus_domains_count":
            int(
                two_plus_domain_mask.sum()
            ),

        "two_plus_domains_fraction":
            float(
                two_plus_domain_mask.mean()
            ),

        "two_plus_domains_alert_rate":
            _safe_alert_rate(
                two_plus_domain_mask
            ),

        "intensity_ge_3_count":
            int(
                intensity_ge_3_mask.sum()
            ),

        "intensity_ge_3_fraction":
            float(
                intensity_ge_3_mask.mean()
            ),

        "intensity_ge_3_alert_rate":
            _safe_alert_rate(
                intensity_ge_3_mask
            ),

        "race_distribution":
            monitoring_df[
                "race"
            ].astype(
                str
            ).value_counts(
                normalize=True,
                dropna=False,
            ).to_dict(),

        "gender_distribution":
            monitoring_df[
                "gender"
            ].astype(
                str
            ).value_counts(
                normalize=True,
                dropna=False,
            ).to_dict(),

        "age_distribution":
            monitoring_df[
                "age"
            ].astype(
                str
            ).value_counts(
                normalize=True,
                dropna=False,
            ).to_dict(),

        "admission_type_distribution":
            monitoring_df[
                "admission_type_id"
            ].astype(
                str
            ).value_counts(
                normalize=True,
                dropna=False,
            ).to_dict(),

        "admission_source_distribution":
            monitoring_df[
                "admission_source_id"
            ].astype(
                str
            ).value_counts(
                normalize=True,
                dropna=False,
            ).to_dict(),

        "outcome_dependent_performance_status":
            "NOT_ASSESSABLE_WITHOUT_MATURED_OUTCOMES",
    }


# ============================================================
# D15.64 — THRESHOLD PERFORMANCE ENGINE
# ============================================================


def calculate_d15_threshold_performance(
    y_true: pd.Series | np.ndarray,
    probability: pd.Series | np.ndarray,
    *,
    threshold: float = D15_FROZEN_OPERATING_THRESHOLD,
) -> dict[str, Any]:
    """
    Calculate frozen operating-point performance.

    The threshold is observational here. It is not optimized.
    """

    y = np.asarray(
        y_true,
        dtype=int,
    )

    p = np.asarray(
        probability,
        dtype=float,
    )

    if len(y) != len(p):
        raise ValueError(
            "Outcome and probability vectors must have "
            "equal length."
        )

    prediction = (
        p
        >= threshold
    ).astype(
        int
    )

    tp = int(
        (
            (y == 1)
            & (prediction == 1)
        ).sum()
    )

    fp = int(
        (
            (y == 0)
            & (prediction == 1)
        ).sum()
    )

    tn = int(
        (
            (y == 0)
            & (prediction == 0)
        ).sum()
    )

    fn = int(
        (
            (y == 1)
            & (prediction == 0)
        ).sum()
    )

    def _safe_divide(
        numerator: float,
        denominator: float,
    ) -> float | None:
        if denominator == 0:
            return None

        return float(
            numerator
            / denominator
        )

    sensitivity = (
        _safe_divide(
            tp,
            tp + fn,
        )
    )

    specificity = (
        _safe_divide(
            tn,
            tn + fp,
        )
    )

    ppv = (
        _safe_divide(
            tp,
            tp + fp,
        )
    )

    npv = (
        _safe_divide(
            tn,
            tn + fn,
        )
    )

    f1 = (
        _safe_divide(
            2 * tp,
            (2 * tp) + fp + fn,
        )
    )

    alert_count = (
        tp
        + fp
    )

    alert_rate = (
        _safe_divide(
            alert_count,
            len(y),
        )
    )

    return {
        "threshold":
            float(
                threshold
            ),

        "tp":
            tp,

        "fp":
            fp,

        "tn":
            tn,

        "fn":
            fn,

        "sensitivity":
            sensitivity,

        "specificity":
            specificity,

        "ppv":
            ppv,

        "npv":
            npv,

        "f1":
            f1,

        "alert_count":
            alert_count,

        "alert_rate":
            alert_rate,

        "alerts_per_100":
            (
                None
                if alert_rate is None
                else float(
                    alert_rate
                    * 100.0
                )
            ),
    }


# ============================================================
# D15.65 — OUTCOME-MATURED PERFORMANCE ENGINE
# ============================================================


def calculate_d15_outcome_matured_metrics(
    monitoring_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Calculate outcome-dependent monitoring metrics once valid
    30-day outcomes have matured.
    """

    validation = (
        validate_d15_monitoring_window(
            monitoring_df,
            require_outcomes=True,
        )
    )

    if not validation[
        "overall_pass"
    ]:
        raise D15InferenceBlockedError(
            "Monitoring window failed outcome-matured "
            f"validation: {validation['checks']}"
        )

    y_true = pd.to_numeric(
        monitoring_df[
            D15_MONITORING_OUTCOME_COLUMN
        ],
        errors="raise",
    ).astype(
        int
    )

    probability = pd.to_numeric(
        monitoring_df[
            "prediction_probability"
        ],
        errors="raise",
    ).astype(
        float
    )

    unique_classes = set(
        y_true.unique()
    )

    discrimination_assessable = (
        unique_classes
        == {
            0,
            1,
        }
    )

    if discrimination_assessable:
        pr_auc = float(
            average_precision_score(
                y_true,
                probability,
            )
        )

        roc_auc = float(
            roc_auc_score(
                y_true,
                probability,
            )
        )

    else:
        pr_auc = None
        roc_auc = None

    brier = float(
        brier_score_loss(
            y_true,
            probability,
        )
    )

    observed_log_loss = float(
        log_loss(
            y_true,
            probability,
            labels=[
                0,
                1,
            ],
        )
    )

    threshold_metrics = (
        calculate_d15_threshold_performance(
            y_true,
            probability,
            threshold=(
                D15_FROZEN_OPERATING_THRESHOLD
            ),
        )
    )

    return {
        "monitoring_mode":
            "OUTCOME_MATURED",

        "encounter_count":
            int(
                len(
                    monitoring_df
                )
            ),

        "positive_count":
            int(
                (
                    y_true
                    == 1
                ).sum()
            ),

        "negative_count":
            int(
                (
                    y_true
                    == 0
                ).sum()
            ),

        "prevalence":
            float(
                y_true.mean()
            ),

        "discrimination_assessable":
            discrimination_assessable,

        "pr_auc":
            pr_auc,

        "roc_auc":
            roc_auc,

        "brier_score":
            brier,

        "log_loss":
            observed_log_loss,

        "threshold_performance":
            threshold_metrics,
    }


# ============================================================
# D15.66 — UTILIZATION-DEPENDENCE MONITORING
# ============================================================


def calculate_d15_utilization_monitoring(
    monitoring_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Monitor the utilization-dependent model behavior identified
    as D14-RISK-001.

    If matured outcomes exist, both alert behavior and outcome-
    dependent performance are calculated by utilization slice.
    """

    immediate = (
        calculate_d15_immediate_monitoring_metrics(
            monitoring_df
        )
    )

    outcomes_available = (
        D15_MONITORING_OUTCOME_COLUMN
        in monitoring_df.columns
    )

    slices = {
        "ZERO_UTILIZATION":
            (
                monitoring_df[
                    "prior_utilization_domain_count"
                ]
                == 0
            ),

        "ONE_DOMAIN":
            (
                monitoring_df[
                    "prior_utilization_domain_count"
                ]
                == 1
            ),

        "TWO_PLUS_DOMAINS":
            (
                monitoring_df[
                    "prior_utilization_domain_count"
                ]
                >= 2
            ),

        "INTENSITY_GE_3":
            (
                monitoring_df[
                    "prior_utilization_intensity"
                ]
                >= 3
            ),
    }

    slice_evidence: dict[
        str,
        Any,
    ] = {}

    for (
        slice_name,
        mask,
    ) in slices.items():

        subset = (
            monitoring_df.loc[
                mask
            ].copy()
        )

        if len(subset) == 0:
            slice_evidence[
                slice_name
            ] = {
                "encounter_count":
                    0,

                "status":
                    "NOT_ASSESSABLE_NO_ENCOUNTERS",
            }

            continue

        alert_rate = float(
            (
                subset[
                    "advisory_flag"
                ]
                == "PRIORITIZE_FOR_HUMAN_REVIEW"
            ).mean()
        )

        evidence: dict[
            str,
            Any,
        ] = {
            "encounter_count":
                int(
                    len(
                        subset
                    )
                ),

            "alert_rate":
                alert_rate,

            "alerts_per_100":
                float(
                    alert_rate
                    * 100.0
                ),
        }

        if outcomes_available:
            outcome_validation = (
                validate_d15_monitoring_window(
                    subset,
                    require_outcomes=True,
                )
            )

            if outcome_validation[
                "overall_pass"
            ]:
                outcome_metrics = (
                    calculate_d15_outcome_matured_metrics(
                        subset
                    )
                )

                evidence[
                    "outcome_performance"
                ] = (
                    outcome_metrics
                )

                evidence[
                    "outcome_status"
                ] = "ASSESSED"

            else:
                evidence[
                    "outcome_status"
                ] = "NOT_ASSESSABLE"

        else:
            evidence[
                "outcome_status"
            ] = (
                "NOT_ASSESSABLE_WITHOUT_MATURED_OUTCOMES"
            )

        slice_evidence[
            slice_name
        ] = evidence

    return {
        "risk_id":
            "D14-RISK-001",

        "risk_name":
            "UTILIZATION_DEPENDENT_MODEL_BEHAVIOR",

        "overall_alert_rate":
            immediate[
                "alert_rate"
            ],

        "slice_evidence":
            slice_evidence,

        "model_modified":
            False,

        "threshold_modified":
            False,
    }


# ============================================================
# D15.67 — REFERENCE COMPARISON ENGINE
# ============================================================


def compare_d15_metrics_to_d14_reference(
    outcome_metrics: dict[str, Any],
) -> dict[str, Any]:
    """
    Compare an outcome-matured monitoring window with the
    historical D14 locked-test reference.

    Differences are descriptive only. This function does not
    assign WATCH/ALERT/CRITICAL status.
    """

    reference = (
        D15_D14_LOCKED_TEST_REFERENCE
    )

    threshold_metrics = (
        outcome_metrics[
            "threshold_performance"
        ]
    )

    comparisons = {
        "prevalence": {
            "reference":
                reference[
                    "prevalence"
                ],

            "observed":
                outcome_metrics[
                    "prevalence"
                ],
        },

        "pr_auc": {
            "reference":
                reference[
                    "pr_auc"
                ],

            "observed":
                outcome_metrics[
                    "pr_auc"
                ],
        },

        "roc_auc": {
            "reference":
                reference[
                    "roc_auc"
                ],

            "observed":
                outcome_metrics[
                    "roc_auc"
                ],
        },

        "brier_score": {
            "reference":
                reference[
                    "brier_score"
                ],

            "observed":
                outcome_metrics[
                    "brier_score"
                ],
        },

        "log_loss": {
            "reference":
                reference[
                    "log_loss"
                ],

            "observed":
                outcome_metrics[
                    "log_loss"
                ],
        },

        "sensitivity": {
            "reference":
                reference[
                    "sensitivity"
                ],

            "observed":
                threshold_metrics[
                    "sensitivity"
                ],
        },

        "specificity": {
            "reference":
                reference[
                    "specificity"
                ],

            "observed":
                threshold_metrics[
                    "specificity"
                ],
        },

        "ppv": {
            "reference":
                reference[
                    "ppv"
                ],

            "observed":
                threshold_metrics[
                    "ppv"
                ],
        },

        "npv": {
            "reference":
                reference[
                    "npv"
                ],

            "observed":
                threshold_metrics[
                    "npv"
                ],
        },

        "f1": {
            "reference":
                reference[
                    "f1"
                ],

            "observed":
                threshold_metrics[
                    "f1"
                ],
        },

        "alert_rate": {
            "reference":
                reference[
                    "alert_rate"
                ],

            "observed":
                threshold_metrics[
                    "alert_rate"
                ],
        },
    }

    for evidence in (
        comparisons.values()
    ):
        reference_value = (
            evidence[
                "reference"
            ]
        )

        observed_value = (
            evidence[
                "observed"
            ]
        )

        if (
            reference_value is None
            or observed_value is None
        ):
            evidence[
                "absolute_difference"
            ] = None

            evidence[
                "relative_difference"
            ] = None

            continue

        evidence[
            "absolute_difference"
        ] = float(
            observed_value
            - reference_value
        )

        if reference_value == 0:
            evidence[
                "relative_difference"
            ] = None

        else:
            evidence[
                "relative_difference"
            ] = float(
                (
                    observed_value
                    - reference_value
                )
                / reference_value
            )

    return {
        "comparison_type":
            "DESCRIPTIVE_D14_INTERNAL_REFERENCE_COMPARISON",

        "comparisons":
            comparisons,

        "automatic_status_assignment":
            False,

        "model_change_triggered":
            False,

        "threshold_change_triggered":
            False,
    }


# ============================================================
# D15.68 — AUTHORITATIVE MONITORING ENGINE
# ============================================================


def run_d15_monitoring_metric_engine(
    monitoring_df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Execute the governed D15 monitoring metric engine.

    Outcome-dependent metrics are calculated only when the
    30-day outcome column is present and valid.
    """

    immediate_validation = (
        validate_d15_monitoring_window(
            monitoring_df,
            require_outcomes=False,
        )
    )

    if not immediate_validation[
        "overall_pass"
    ]:
        raise D15InferenceBlockedError(
            "D15 monitoring metric engine blocked by "
            "invalid monitoring window."
        )

    immediate_metrics = (
        calculate_d15_immediate_monitoring_metrics(
            monitoring_df
        )
    )

    utilization_monitoring = (
        calculate_d15_utilization_monitoring(
            monitoring_df
        )
    )

    outcomes_available = (
        D15_MONITORING_OUTCOME_COLUMN
        in monitoring_df.columns
    )

    if outcomes_available:
        outcome_validation = (
            validate_d15_monitoring_window(
                monitoring_df,
                require_outcomes=True,
            )
        )

        if outcome_validation[
            "overall_pass"
        ]:
            outcome_metrics = (
                calculate_d15_outcome_matured_metrics(
                    monitoring_df
                )
            )

            reference_comparison = (
                compare_d15_metrics_to_d14_reference(
                    outcome_metrics
                )
            )

            outcome_status = (
                "ASSESSED"
            )

        else:
            outcome_metrics = None
            reference_comparison = None
            outcome_status = (
                "NOT_ASSESSABLE_INVALID_OUTCOME_EVIDENCE"
            )

    else:
        outcome_validation = None
        outcome_metrics = None
        reference_comparison = None
        outcome_status = (
            "NOT_ASSESSABLE_WITHOUT_MATURED_OUTCOMES"
        )

    engine_checks = {
        "immediate_monitoring_valid":
            immediate_validation[
                "overall_pass"
            ],

        "frozen_threshold_preserved":
            D15_FROZEN_OPERATING_THRESHOLD
            == 0.12,

        "automatic_retraining_disabled":
            D15_THRESHOLD_GOVERNANCE[
                "automatic_model_retraining"
            ]
            is False,

        "automatic_recalibration_disabled":
            D15_THRESHOLD_GOVERNANCE[
                "automatic_model_recalibration"
            ]
            is False,

        "automatic_threshold_adjustment_disabled":
            D15_THRESHOLD_GOVERNANCE[
                "automatic_threshold_adjustment"
            ]
            is False,

        "subgroup_threshold_adjustment_disabled":
            D15_THRESHOLD_GOVERNANCE[
                "subgroup_specific_threshold_adjustment"
            ]
            is False,

        "monitoring_does_not_authorize_deployment":
            D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
            is False,
    }

    engine_pass = all(
        engine_checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "engine_classification":
            "GOVERNED_MONITORING_METRIC_ENGINE",

        "monitoring_mode":
            (
                "OUTCOME_MATURED"
                if outcome_status
                == "ASSESSED"
                else "IMMEDIATE_ONLY"
            ),

        "immediate_metrics":
            immediate_metrics,

        "outcome_status":
            outcome_status,

        "outcome_metrics":
            outcome_metrics,

        "utilization_monitoring":
            utilization_monitoring,

        "d14_reference_comparison":
            reference_comparison,

        "engine_validation": {
            "checks":
                engine_checks,

            "overall_pass":
                engine_pass,

            "validation_status":
                (
                    "PASS"
                    if engine_pass
                    else "FAIL"
                ),
        },

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_MONITORING_STATUS_AND_ESCALATION_ENGINE"
                if engine_pass
                else
                "STOP_AND_REMEDIATE_MONITORING_METRIC_ENGINE"
            ),
    }


# ============================================================
# D15.69 — PRINT MONITORING METRIC ENGINE EVIDENCE
# ============================================================


def print_d15_monitoring_metric_engine(
    monitoring_df: pd.DataFrame,
) -> None:
    """
    Print concise monitoring-engine evidence.
    """

    evidence = (
        run_d15_monitoring_metric_engine(
            monitoring_df
        )
    )

    immediate = evidence[
        "immediate_metrics"
    ]

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "MONITORING METRIC ENGINE"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Monitoring window"
    )

    print(
        "-" * 112
    )

    print(
        f"Mode:                           "
        f"{evidence['monitoring_mode']}"
    )

    print(
        f"Encounters:                     "
        f"{immediate['encounter_count']}"
    )

    print(
        f"Mean probability:               "
        f"{immediate['prediction_probability_mean']:.6f}"
    )

    print(
        f"Alert rate:                     "
        f"{immediate['alert_rate']:.6f}"
    )

    print(
        f"Alerts per 100:                 "
        f"{immediate['alerts_per_100']:.3f}"
    )

    print(
        f"Zero-utilization fraction:      "
        f"{immediate['zero_utilization_fraction']:.6f}"
    )

    print(
        f"Outcome-dependent status:       "
        f"{evidence['outcome_status']}"
    )

    print()

    if evidence[
        "outcome_metrics"
    ] is not None:

        outcome = evidence[
            "outcome_metrics"
        ]

        threshold = outcome[
            "threshold_performance"
        ]

        print(
            "Outcome-matured performance"
        )

        print(
            "-" * 112
        )

        print(
            f"Prevalence:                     "
            f"{outcome['prevalence']:.6f}"
        )

        print(
            f"PR-AUC:                         "
            f"{outcome['pr_auc']}"
        )

        print(
            f"ROC-AUC:                        "
            f"{outcome['roc_auc']}"
        )

        print(
            f"Brier score:                    "
            f"{outcome['brier_score']:.6f}"
        )

        print(
            f"Log loss:                       "
            f"{outcome['log_loss']:.6f}"
        )

        print(
            f"Sensitivity @ 0.12:             "
            f"{threshold['sensitivity']}"
        )

        print(
            f"Specificity @ 0.12:             "
            f"{threshold['specificity']}"
        )

        print()

    print(
        "Engine validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "engine_validation"
    ][
        "checks"
    ].items():
        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"MONITORING ENGINE STATUS:        "
        f"{evidence['engine_validation']['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )

# ============================================================
# D15.70 — MONITORING STATUS & ESCALATION ENGINE
# ============================================================
#
# Purpose:
# Translate governed monitoring evidence into operational
# governance states and escalation actions.
#
# IMPORTANT:
#
# Monitoring status does NOT automatically:
#
#   - retrain the model;
#   - recalibrate probabilities;
#   - change the frozen 0.12 threshold;
#   - create subgroup thresholds;
#   - authorize deployment;
#   - establish clinical effectiveness.
#
# Quantitative performance-drift limits remain evidence-
# dependent and are not invented in this section.
# ============================================================


# ============================================================
# D15.71 — ESCALATION LEVELS
# ============================================================


D15_ESCALATION_LEVELS = {
    "NORMAL": {
        "severity_rank": 0,
        "governance_action":
            "CONTINUE_GOVERNED_MONITORING",
        "model_operation":
            "NO_CHANGE",
    },

    "WATCH": {
        "severity_rank": 1,
        "governance_action":
            "INCREASE_REVIEW_AND_INVESTIGATE",
        "model_operation":
            "NO_AUTOMATIC_CHANGE",
    },

    "ALERT": {
        "severity_rank": 2,
        "governance_action":
            "FORMAL_GOVERNANCE_REVIEW_REQUIRED",
        "model_operation":
            "NO_AUTOMATIC_CHANGE",
    },

    "CRITICAL": {
        "severity_rank": 3,
        "governance_action":
            "CONSIDER_SUSPENSION_OR_ROLLBACK_PENDING_REVIEW",
        "model_operation":
            "NO_AUTOMATIC_CHANGE",
    },

    "NOT_ASSESSABLE": {
        "severity_rank": -1,
        "governance_action":
            "OBTAIN_REQUIRED_EVIDENCE_BEFORE_INTERPRETATION",
        "model_operation":
            "NO_CHANGE",
    },
}


# ============================================================
# D15.72 — ESCALATION TRIGGER CATALOGUE
# ============================================================


D15_ESCALATION_TRIGGER_CATALOGUE = (
    {
        "trigger_id": "D15-ESC-001",
        "domain": "SCHEMA_INTEGRITY",
        "trigger_type": "DETERMINISTIC",
        "condition":
            "SCHEMA_VALIDATION_FAILURE",
        "status": "CRITICAL",
        "action":
            "BLOCK_INFERENCE_AND_ESCALATE_SCHEMA_CHANGE",
    },
    {
        "trigger_id": "D15-ESC-002",
        "domain": "DATA_QUALITY",
        "trigger_type": "DETERMINISTIC",
        "condition":
            "REQUIRED_INPUT_VALIDATION_FAILURE",
        "status": "CRITICAL",
        "action":
            "BLOCK_INFERENCE_AND_REVIEW_DATA_PIPELINE",
    },
    {
        "trigger_id": "D15-ESC-003",
        "domain": "MODEL_VERSION_CONTROL",
        "trigger_type": "DETERMINISTIC",
        "condition":
            "FROZEN_ARTIFACT_IDENTITY_FAILURE",
        "status": "CRITICAL",
        "action":
            "BLOCK_INFERENCE_AND_ACTIVATE_MODEL_INTEGRITY_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-004",
        "domain": "INCIDENTS",
        "trigger_type": "EVENT",
        "condition":
            "MODEL_SAFETY_OR_GOVERNANCE_INCIDENT",
        "status": "CRITICAL",
        "action":
            "ACTIVATE_INCIDENT_MANAGEMENT",
    },
    {
        "trigger_id": "D15-ESC-005",
        "domain": "MODEL_DISCRIMINATION",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_DISCRIMINATION_CHANGE",
        "status": "ALERT",
        "action":
            "FORMAL_PERFORMANCE_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-006",
        "domain": "MODEL_CALIBRATION",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_CALIBRATION_CHANGE",
        "status": "ALERT",
        "action":
            "FORMAL_CALIBRATION_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-007",
        "domain": "OPERATING_POINT_PERFORMANCE",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_OPERATING_POINT_CHANGE",
        "status": "ALERT",
        "action":
            "FORMAL_OPERATING_POINT_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-008",
        "domain": "SUBGROUP_PERFORMANCE",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_SUBGROUP_HETEROGENEITY_CHANGE",
        "status": "ALERT",
        "action":
            "RESPONSIBLE_AI_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-009",
        "domain": "UTILIZATION_DEPENDENCE",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_UTILIZATION_DEPENDENCE_CHANGE",
        "status": "ALERT",
        "action":
            "STRUCTURAL_MODEL_BEHAVIOR_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-010",
        "domain": "ADMISSION_CONTEXT_PERFORMANCE",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_ADMISSION_CONTEXT_CHANGE",
        "status": "ALERT",
        "action":
            "CONTEXT_SPECIFIC_PERFORMANCE_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-011",
        "domain": "EXPLAINABILITY_STABILITY",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_ATTRIBUTION_SHIFT",
        "status": "ALERT",
        "action":
            "EXPLAINABILITY_GOVERNANCE_REVIEW",
    },
    {
        "trigger_id": "D15-ESC-012",
        "domain": "INPUT_DISTRIBUTION",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_INPUT_DISTRIBUTION_SHIFT",
        "status": "WATCH",
        "action":
            "INVESTIGATE_POPULATION_AND_DATA_SHIFT",
    },
    {
        "trigger_id": "D15-ESC-013",
        "domain": "PREDICTION_DISTRIBUTION",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_PREDICTION_DISTRIBUTION_SHIFT",
        "status": "WATCH",
        "action":
            "INVESTIGATE_MODEL_BEHAVIOR_SHIFT",
    },
    {
        "trigger_id": "D15-ESC-014",
        "domain": "ALERT_RATE",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_ALERT_RATE_CHANGE",
        "status": "WATCH",
        "action":
            "INVESTIGATE_WORKLOAD_AND_OPERATING_BEHAVIOR",
    },
    {
        "trigger_id": "D15-ESC-015",
        "domain": "CLINICAL_OVERRIDE_RATE",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_OVERRIDE_PATTERN_CHANGE",
        "status": "WATCH",
        "action":
            "REVIEW_HUMAN_MODEL_DISAGREEMENT",
    },
    {
        "trigger_id": "D15-ESC-016",
        "domain": "WORKFLOW_ADOPTION",
        "trigger_type": "EVIDENCE_DEPENDENT",
        "condition":
            "MATERIAL_WORKFLOW_ADOPTION_CHANGE",
        "status": "WATCH",
        "action":
            "REVIEW_WORKFLOW_INTEGRATION",
    },
    {
        "trigger_id": "D15-ESC-017",
        "domain": "OUTCOME_EVIDENCE",
        "trigger_type": "EVIDENCE_AVAILABILITY",
        "condition":
            "OUTCOME_EVIDENCE_NOT_MATURE",
        "status": "NOT_ASSESSABLE",
        "action":
            "DO_NOT_INFER_PERFORMANCE_STABILITY",
    },
)


# ============================================================
# D15.73 — STATUS SEVERITY RESOLUTION
# ============================================================


def resolve_d15_highest_monitoring_status(
    statuses: list[str],
) -> str:
    """
    Resolve the highest actionable monitoring status.

    NOT_ASSESSABLE is retained only when no actionable
    NORMAL/WATCH/ALERT/CRITICAL state is present.
    """

    if not statuses:
        return "NOT_ASSESSABLE"

    invalid_statuses = [
        status
        for status in statuses
        if status
        not in D15_ESCALATION_LEVELS
    ]

    if invalid_statuses:
        raise ValueError(
            "Unknown D15 monitoring status: "
            f"{invalid_statuses}"
        )

    actionable = [
        status
        for status in statuses
        if status
        != "NOT_ASSESSABLE"
    ]

    if not actionable:
        return "NOT_ASSESSABLE"

    return max(
        actionable,
        key=lambda status:
            D15_ESCALATION_LEVELS[
                status
            ][
                "severity_rank"
            ],
    )


# ============================================================
# D15.74 — STRUCTURAL ESCALATION ENGINE
# ============================================================


def evaluate_d15_structural_escalation(
    *,
    schema_valid: bool = True,
    required_inputs_valid: bool = True,
    artifact_identity_valid: bool = True,
    incident_present: bool = False,
) -> dict[str, Any]:
    """
    Evaluate deterministic fail-closed operational triggers.
    """

    triggered: list[
        dict[str, Any]
    ] = []

    if not schema_valid:
        triggered.append(
            {
                "trigger_id":
                    "D15-ESC-001",
                "status":
                    "CRITICAL",
                "reason":
                    "SCHEMA_VALIDATION_FAILURE",
            }
        )

    if not required_inputs_valid:
        triggered.append(
            {
                "trigger_id":
                    "D15-ESC-002",
                "status":
                    "CRITICAL",
                "reason":
                    "REQUIRED_INPUT_VALIDATION_FAILURE",
            }
        )

    if not artifact_identity_valid:
        triggered.append(
            {
                "trigger_id":
                    "D15-ESC-003",
                "status":
                    "CRITICAL",
                "reason":
                    "FROZEN_ARTIFACT_IDENTITY_FAILURE",
            }
        )

    if incident_present:
        triggered.append(
            {
                "trigger_id":
                    "D15-ESC-004",
                "status":
                    "CRITICAL",
                "reason":
                    "MODEL_SAFETY_OR_GOVERNANCE_INCIDENT",
            }
        )

    if triggered:
        overall_status = (
            resolve_d15_highest_monitoring_status(
                [
                    item["status"]
                    for item in triggered
                ]
            )
        )

    else:
        overall_status = "NORMAL"

    return {
        "evaluation_type":
            "STRUCTURAL_ESCALATION",

        "triggered":
            triggered,

        "trigger_count":
            len(
                triggered
            ),

        "overall_status":
            overall_status,

        "governance_action":
            D15_ESCALATION_LEVELS[
                overall_status
            ][
                "governance_action"
            ],

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.75 — OUTCOME-EVIDENCE STATUS
# ============================================================


def evaluate_d15_outcome_evidence_status(
    monitoring_engine_evidence: dict[str, Any],
) -> dict[str, Any]:
    """
    Translate outcome availability into a governance state.

    Missing outcome evidence does not generate a false
    performance PASS.
    """

    outcome_status = (
        monitoring_engine_evidence[
            "outcome_status"
        ]
    )

    if outcome_status == "ASSESSED":
        status = "NORMAL"

        interpretation = (
            "OUTCOME_EVIDENCE_AVAILABLE_FOR_GOVERNED_REVIEW"
        )

    else:
        status = "NOT_ASSESSABLE"

        interpretation = (
            "OUTCOME_DEPENDENT_PERFORMANCE_NOT_ESTABLISHED_"
            "FOR_THIS_MONITORING_WINDOW"
        )

    return {
        "trigger_id":
            "D15-ESC-017",

        "status":
            status,

        "source_outcome_status":
            outcome_status,

        "interpretation":
            interpretation,

        "performance_stability_claim_allowed":
            outcome_status
            == "ASSESSED",
    }


# ============================================================
# D15.76 — EVIDENCE-DEPENDENT TRIGGER PLACEHOLDERS
# ============================================================
#
# These controls deliberately remain UNCALIBRATED until
# quantitative limits are justified.
#
# They cannot silently produce NORMAL merely because no
# threshold has yet been defined.
# ============================================================


D15_UNCALIBRATED_EVIDENCE_DEPENDENT_TRIGGERS = (
    "D15-ESC-005",
    "D15-ESC-006",
    "D15-ESC-007",
    "D15-ESC-008",
    "D15-ESC-009",
    "D15-ESC-010",
    "D15-ESC-011",
    "D15-ESC-012",
    "D15-ESC-013",
    "D15-ESC-014",
    "D15-ESC-015",
    "D15-ESC-016",
)


def build_d15_uncalibrated_trigger_evidence(
) -> list[dict[str, Any]]:
    """
    Make uncalibrated quantitative triggers explicit.
    """

    catalogue_by_id = {
        item["trigger_id"]:
            item
        for item in (
            D15_ESCALATION_TRIGGER_CATALOGUE
        )
    }

    evidence: list[
        dict[str, Any]
    ] = []

    for trigger_id in (
        D15_UNCALIBRATED_EVIDENCE_DEPENDENT_TRIGGERS
    ):
        item = (
            catalogue_by_id[
                trigger_id
            ]
        )

        evidence.append(
            {
                "trigger_id":
                    trigger_id,

                "domain":
                    item["domain"],

                "calibration_status":
                    "NOT_YET_CALIBRATED",

                "automatic_status_assignment":
                    False,

                "default_normal_assumption":
                    False,

                "required_action":
                    "DEFINE_EVIDENCE_BASED_LIMITS_BEFORE_USE",
            }
        )

    return evidence


# ============================================================
# D15.77 — AUTHORITATIVE STATUS & ESCALATION ENGINE
# ============================================================


def run_d15_monitoring_status_and_escalation_engine(
    monitoring_engine_evidence: dict[str, Any],
    *,
    schema_valid: bool = True,
    required_inputs_valid: bool = True,
    artifact_identity_valid: bool = True,
    incident_present: bool = False,
) -> dict[str, Any]:
    """
    Execute the governed D15 status and escalation engine.
    """

    structural = (
        evaluate_d15_structural_escalation(
            schema_valid=schema_valid,
            required_inputs_valid=(
                required_inputs_valid
            ),
            artifact_identity_valid=(
                artifact_identity_valid
            ),
            incident_present=(
                incident_present
            ),
        )
    )

    outcome_evidence = (
        evaluate_d15_outcome_evidence_status(
            monitoring_engine_evidence
        )
    )

    uncalibrated = (
        build_d15_uncalibrated_trigger_evidence()
    )

    status_inputs = [
        structural[
            "overall_status"
        ],
        outcome_evidence[
            "status"
        ],
    ]

    overall_status = (
        resolve_d15_highest_monitoring_status(
            status_inputs
        )
    )

    checks = {
        "structural_engine_returns_valid_status":
            structural[
                "overall_status"
            ]
            in D15_ESCALATION_LEVELS,

        "outcome_evidence_returns_valid_status":
            outcome_evidence[
                "status"
            ]
            in D15_ESCALATION_LEVELS,

        "uncalibrated_triggers_are_explicit":
            len(
                uncalibrated
            )
            == len(
                D15_UNCALIBRATED_EVIDENCE_DEPENDENT_TRIGGERS
            ),

        "uncalibrated_triggers_do_not_default_normal":
            all(
                item[
                    "default_normal_assumption"
                ]
                is False
                for item in uncalibrated
            ),

        "automatic_model_change_disabled":
            structural[
                "automatic_model_change"
            ]
            is False,

        "automatic_threshold_change_disabled":
            structural[
                "automatic_threshold_change"
            ]
            is False,

        "production_deployment_not_authorized":
            structural[
                "production_deployment_authorized"
            ]
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "engine_classification":
            "GOVERNED_MONITORING_STATUS_AND_ESCALATION_ENGINE",

        "structural_escalation":
            structural,

        "outcome_evidence":
            outcome_evidence,

        "uncalibrated_quantitative_triggers":
            uncalibrated,

        "overall_monitoring_status":
            overall_status,

        "overall_governance_action":
            D15_ESCALATION_LEVELS[
                overall_status
            ][
                "governance_action"
            ],

        "validation": {
            "checks":
                checks,

            "overall_pass":
                overall_pass,

            "validation_status":
                (
                    "PASS"
                    if overall_pass
                    else "FAIL"
                ),
        },

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_QUANTITATIVE_MONITORING_LIMIT_DESIGN"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_ESCALATION_ENGINE"
            ),
    }


# ============================================================
# D15.78 — PRINT STATUS & ESCALATION EVIDENCE
# ============================================================


def print_d15_monitoring_status_and_escalation(
    monitoring_engine_evidence: dict[str, Any],
    *,
    schema_valid: bool = True,
    required_inputs_valid: bool = True,
    artifact_identity_valid: bool = True,
    incident_present: bool = False,
) -> None:
    """
    Print governed monitoring status and escalation evidence.
    """

    evidence = (
        run_d15_monitoring_status_and_escalation_engine(
            monitoring_engine_evidence,
            schema_valid=schema_valid,
            required_inputs_valid=(
                required_inputs_valid
            ),
            artifact_identity_valid=(
                artifact_identity_valid
            ),
            incident_present=(
                incident_present
            ),
        )
    )

    structural = evidence[
        "structural_escalation"
    ]

    outcome = evidence[
        "outcome_evidence"
    ]

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "MONITORING STATUS & ESCALATION ENGINE"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Structural controls"
    )

    print(
        "-" * 112
    )

    print(
        f"Structural status:              "
        f"{structural['overall_status']}"
    )

    print(
        f"Triggered structural controls:  "
        f"{structural['trigger_count']}"
    )

    print()

    print(
        "Outcome evidence"
    )

    print(
        "-" * 112
    )

    print(
        f"Outcome status:                 "
        f"{outcome['source_outcome_status']}"
    )

    print(
        f"Governance state:               "
        f"{outcome['status']}"
    )

    print(
        f"Performance stability claim:    "
        f"{outcome['performance_stability_claim_allowed']}"
    )

    print()

    print(
        "Quantitative trigger calibration"
    )

    print(
        "-" * 112
    )

    print(
        f"Evidence-dependent triggers:    "
        f"{len(evidence['uncalibrated_quantitative_triggers'])}"
    )

    print(
        "Calibration status:             "
        "NOT_YET_CALIBRATED"
    )

    print(
        "Default-to-normal permitted:    False"
    )

    print()

    print(
        "Engine validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "validation"
    ][
        "checks"
    ].items():
        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"OVERALL MONITORING STATUS:       "
        f"{evidence['overall_monitoring_status']}"
    )

    print(
        f"GOVERNANCE ACTION:               "
        f"{evidence['overall_governance_action']}"
    )

    print(
        f"ESCALATION ENGINE STATUS:        "
        f"{evidence['validation']['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )


# ============================================================
# D15.79 — ESCALATION GOVERNANCE INTERPRETATION
# ============================================================
#
# Deterministic integrity failures are fail-closed:
#
#   - schema failure;
#   - required-input failure;
#   - frozen-artifact identity failure;
#   - safety/governance incident.
#
# These can immediately produce CRITICAL status.
#
# Quantitative drift/performance triggers remain explicitly
# uncalibrated until evidence-based limits are established.
# They must not silently default to NORMAL.
#
# Missing 30-day outcome evidence produces NOT_ASSESSABLE for
# outcome-dependent performance. It is not a performance PASS.
#
# No monitoring state automatically retrains, recalibrates,
# changes the threshold, or authorizes deployment.
# ============================================================

# ============================================================
# D15.80 — QUANTITATIVE MONITORING LIMIT FOUNDATION
# ============================================================
#
# Purpose:
# Establish evidence-based quantitative surveillance reference
# limits without converting internal locked-test behavior into
# production performance targets.
#
# D14 values are INTERNAL HISTORICAL REFERENCES.
#
# They are NOT:
#
#   - clinical acceptability thresholds;
#   - production performance guarantees;
#   - external-validation targets;
#   - clinical-effectiveness targets;
#   - authorization criteria.
#
# ============================================================


from statistics import NormalDist


# ============================================================
# D15.81 — QUANTITATIVE LIMIT GOVERNANCE CONTRACT
# ============================================================


D15_QUANTITATIVE_LIMIT_GOVERNANCE = {
    "reference_source":
        "D14_INTERNAL_LOCKED_TEST",

    "reference_classification":
        "INTERNAL_HISTORICAL_SURVEILLANCE_REFERENCE",

    "reference_is_production_target":
        False,

    "reference_is_clinical_acceptability_threshold":
        False,

    "reference_establishes_external_validity":
        False,

    "reference_establishes_clinical_effectiveness":
        False,

    "single_window_breach_automatically_changes_model":
        False,

    "single_window_breach_automatically_changes_threshold":
        False,

    "single_window_breach_automatically_recalibrates":
        False,

    "insufficient_sample_defaults_to_normal":
        False,

    "known_bad_historical_behavior_is_acceptable_target":
        False,

    "persistent_material_change_requires_review":
        True,

    "production_deployment_authorized":
        False,
}


# ============================================================
# D15.82 — REFERENCE COUNTS
# ============================================================


D15_D14_RATE_REFERENCE_COUNTS = {
    "prevalence": {
        "events": 1707,
        "denominator": 15038,
        "reference_rate": 1707 / 15038,
    },

    "alert_rate": {
        "events": 4759,
        "denominator": 15038,
        "reference_rate": 4759 / 15038,
    },

    "sensitivity": {
        "events": 832,
        "denominator": 1707,
        "reference_rate": 832 / 1707,
    },

    "specificity": {
        "events": 9404,
        "denominator": 13331,
        "reference_rate": 9404 / 13331,
    },

    "ppv": {
        "events": 832,
        "denominator": 4759,
        "reference_rate": 832 / 4759,
    },

    "npv": {
        "events": 9404,
        "denominator": 10279,
        "reference_rate": 9404 / 10279,
    },
}


# ============================================================
# D15.83 — KNOWN-RISK SLICE REFERENCES
# ============================================================
#
# IMPORTANT:
# These are risk-reference observations, not acceptable targets.
# ============================================================


D15_D14_KNOWN_RISK_SLICE_REFERENCES = {
    "ZERO_UTILIZATION": {
        "n": 8248,
        "positive_n": 696,
        "negative_n": 7552,
        "alert_count": 0,
        "alert_rate": 0.0,
        "true_positives": 0,
        "sensitivity": 0.0,
        "risk_interpretation":
            "KNOWN_MATERIAL_UTILIZATION_DEPENDENCE",
        "acceptable_target":
            False,
    },

    "ONE_DOMAIN": {
        "n": 4767,
        "positive_n": 679,
        "negative_n": 4088,
        "alert_count": 2887,
        "alert_rate": 2887 / 4767,
        "true_positives": 507,
        "sensitivity": 507 / 679,
        "risk_interpretation":
            "KNOWN_MATERIAL_UTILIZATION_DEPENDENCE",
        "acceptable_target":
            False,
    },

    "TWO_PLUS_DOMAINS": {
        "n": 2023,
        "positive_n": 332,
        "negative_n": 1691,
        "alert_count": 1872,
        "alert_rate": 1872 / 2023,
        "true_positives": 325,
        "sensitivity": 325 / 332,
        "risk_interpretation":
            "KNOWN_MATERIAL_UTILIZATION_DEPENDENCE",
        "acceptable_target":
            False,
    },

    "INTENSITY_GE_3": {
        "n": 2414,
        "positive_n": 446,
        "negative_n": 1968,
        "alert_count": 2089,
        "alert_rate": 2089 / 2414,
        "true_positives": 429,
        "sensitivity": 429 / 446,
        "risk_interpretation":
            "KNOWN_MATERIAL_UTILIZATION_DEPENDENCE",
        "acceptable_target":
            False,
    },

    "ADMISSION_SOURCE_ID_6": {
        "n": 324,
        "positive_n": 29,
        "negative_n": 295,
        "alert_count": 54,
        "alert_rate": 54 / 324,
        "true_positives": 4,
        "sensitivity": 4 / 29,
        "risk_interpretation":
            "KNOWN_ADMISSION_CONTEXT_HETEROGENEITY",
        "acceptable_target":
            False,
    },
}


# ============================================================
# D15.84 — WILSON SCORE INTERVAL
# ============================================================


def calculate_d15_wilson_interval(
    events: int,
    denominator: int,
    *,
    confidence_level: float = 0.95,
) -> dict[str, float | int]:
    """
    Calculate a Wilson score interval for a binary proportion.

    Used for internal statistical surveillance references.
    """

    if denominator <= 0:
        raise ValueError(
            "Wilson interval denominator must be positive."
        )

    if events < 0 or events > denominator:
        raise ValueError(
            "Wilson interval events must satisfy "
            "0 <= events <= denominator."
        )

    if not (
        0.0
        < confidence_level
        < 1.0
    ):
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    p_hat = (
        events
        / denominator
    )

    alpha = (
        1.0
        - confidence_level
    )

    z = NormalDist().inv_cdf(
        1.0
        - alpha / 2.0
    )

    z2 = (
        z ** 2
    )

    denominator_adjustment = (
        1.0
        + z2 / denominator
    )

    centre = (
        p_hat
        + z2 / (
            2.0
            * denominator
        )
    ) / denominator_adjustment

    half_width = (
        z
        * (
            (
                p_hat
                * (
                    1.0
                    - p_hat
                )
                / denominator
            )
            + (
                z2
                / (
                    4.0
                    * denominator ** 2
                )
            )
        ) ** 0.5
        / denominator_adjustment
    )

    lower = max(
        0.0,
        centre
        - half_width,
    )

    upper = min(
        1.0,
        centre
        + half_width,
    )

    return {
        "events":
            int(
                events
            ),

        "denominator":
            int(
                denominator
            ),

        "observed_rate":
            float(
                p_hat
            ),

        "confidence_level":
            float(
                confidence_level
            ),

        "lower_bound":
            float(
                lower
            ),

        "upper_bound":
            float(
                upper
            ),
    }


# ============================================================
# D15.85 — BUILD INTERNAL RATE REFERENCE BANDS
# ============================================================


def build_d15_internal_rate_reference_bands(
    *,
    confidence_level: float = 0.95,
) -> dict[str, dict[str, Any]]:
    """
    Build Wilson reference intervals from the frozen D14
    internal locked-test counts.

    These are surveillance reference bands, not production
    acceptance limits.
    """

    output: dict[
        str,
        dict[str, Any],
    ] = {}

    for (
        metric_name,
        reference,
    ) in (
        D15_D14_RATE_REFERENCE_COUNTS.items()
    ):
        interval = (
            calculate_d15_wilson_interval(
                reference[
                    "events"
                ],
                reference[
                    "denominator"
                ],
                confidence_level=(
                    confidence_level
                ),
            )
        )

        output[
            metric_name
        ] = {
            **interval,

            "reference_classification":
                "INTERNAL_HISTORICAL_SURVEILLANCE_REFERENCE",

            "production_acceptance_limit":
                False,

            "clinical_acceptability_limit":
                False,
        }

    return output


# ============================================================
# D15.86 — MONITORING SAMPLE-SUFFICIENCY MODEL
# ============================================================
#
# These minimum counts are governance eligibility conditions,
# not claims of formal statistical power.
#
# They prevent unstable small windows from being interpreted
# as reliable performance evidence.
# ============================================================


D15_MONITORING_SAMPLE_SUFFICIENCY = {
    "overall_encounters_minimum":
        500,

    "positive_outcomes_minimum":
        50,

    "negative_outcomes_minimum":
        50,

    "subgroup_encounters_minimum":
        100,

    "subgroup_positive_outcomes_minimum":
        20,

    "subgroup_negative_outcomes_minimum":
        20,
}


def assess_d15_monitoring_sample_sufficiency(
    *,
    encounter_count: int,
    positive_count: int | None = None,
    negative_count: int | None = None,
    subgroup: bool = False,
) -> dict[str, Any]:
    """
    Determine whether a monitoring window has sufficient
    support for governed interpretation.

    This is an interpretation eligibility gate, not a formal
    power calculation.
    """

    if subgroup:
        encounter_minimum = (
            D15_MONITORING_SAMPLE_SUFFICIENCY[
                "subgroup_encounters_minimum"
            ]
        )

        positive_minimum = (
            D15_MONITORING_SAMPLE_SUFFICIENCY[
                "subgroup_positive_outcomes_minimum"
            ]
        )

        negative_minimum = (
            D15_MONITORING_SAMPLE_SUFFICIENCY[
                "subgroup_negative_outcomes_minimum"
            ]
        )

    else:
        encounter_minimum = (
            D15_MONITORING_SAMPLE_SUFFICIENCY[
                "overall_encounters_minimum"
            ]
        )

        positive_minimum = (
            D15_MONITORING_SAMPLE_SUFFICIENCY[
                "positive_outcomes_minimum"
            ]
        )

        negative_minimum = (
            D15_MONITORING_SAMPLE_SUFFICIENCY[
                "negative_outcomes_minimum"
            ]
        )

    checks = {
        "encounter_support_sufficient":
            encounter_count
            >= encounter_minimum,
    }

    if positive_count is not None:
        checks[
            "positive_support_sufficient"
        ] = (
            positive_count
            >= positive_minimum
        )

    if negative_count is not None:
        checks[
            "negative_support_sufficient"
        ] = (
            negative_count
            >= negative_minimum
        )

    sufficient = all(
        checks.values()
    )

    return {
        "subgroup":
            subgroup,

        "checks":
            checks,

        "sufficient":
            sufficient,

        "interpretation_status":
            (
                "SUFFICIENT_FOR_GOVERNED_INTERPRETATION"
                if sufficient
                else
                "INSUFFICIENT_EVIDENCE"
            ),
    }


# ============================================================
# D15.87 — RATE REFERENCE COMPARISON
# ============================================================


def compare_d15_observed_rate_to_reference(
    *,
    metric_name: str,
    observed_events: int,
    observed_denominator: int,
    confidence_level: float = 0.95,
) -> dict[str, Any]:
    """
    Compare a monitoring-window binary rate against the D14
    internal historical surveillance reference.

    This comparison is descriptive and statistical.
    It does not independently establish clinical materiality.
    """

    reference_bands = (
        build_d15_internal_rate_reference_bands(
            confidence_level=(
                confidence_level
            )
        )
    )

    if metric_name not in reference_bands:
        raise KeyError(
            "No D15 binary-rate reference available for "
            f"{metric_name!r}."
        )

    observed = (
        calculate_d15_wilson_interval(
            observed_events,
            observed_denominator,
            confidence_level=(
                confidence_level
            ),
        )
    )

    reference = (
        reference_bands[
            metric_name
        ]
    )

    observed_rate = (
        observed[
            "observed_rate"
        ]
    )

    reference_rate = (
        reference[
            "observed_rate"
        ]
    )

    outside_reference_band = bool(
        observed_rate
        < reference[
            "lower_bound"
        ]
        or observed_rate
        > reference[
            "upper_bound"
        ]
    )

    interval_separation = bool(
        observed[
            "upper_bound"
        ]
        < reference[
            "lower_bound"
        ]
        or observed[
            "lower_bound"
        ]
        > reference[
            "upper_bound"
        ]
    )

    return {
        "metric_name":
            metric_name,

        "reference":
            reference,

        "observed":
            observed,

        "absolute_difference":
            float(
                observed_rate
                - reference_rate
            ),

        "outside_reference_point_interval":
            outside_reference_band,

        "reference_and_observed_intervals_separated":
            interval_separation,

        "statistical_signal":
            (
                "REFERENCE_SHIFT_SIGNAL"
                if interval_separation
                else
                "NO_CLEAR_REFERENCE_SHIFT_SIGNAL"
            ),

        "clinical_materiality_established":
            False,

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,
    }


# ============================================================
# D15.88 — DISCRIMINATION LIMIT GOVERNANCE
# ============================================================


D15_DISCRIMINATION_LIMIT_GOVERNANCE = {
    "pr_auc_reference":
        D15_D14_LOCKED_TEST_REFERENCE[
            "pr_auc"
        ],

    "roc_auc_reference":
        D15_D14_LOCKED_TEST_REFERENCE[
            "roc_auc"
        ],

    "simple_binomial_interval_permitted":
        False,

    "bootstrap_uncertainty_required":
        True,

    "clinical_materiality_required":
        True,

    "automatic_model_change":
        False,

    "calibration_status":
        "REQUIRES_BOOTSTRAP_AND_MATERIALITY_DESIGN",
}


# ============================================================
# D15.89 — VALIDATE QUANTITATIVE LIMIT FOUNDATION
# ============================================================


def validate_d15_quantitative_monitoring_limit_foundation(
) -> dict[str, Any]:
    """
    Validate the quantitative monitoring-limit foundation.
    """

    reference_bands = (
        build_d15_internal_rate_reference_bands()
    )

    known_risk_references = (
        D15_D14_KNOWN_RISK_SLICE_REFERENCES
    )

    checks = {
        "six_binary_rate_reference_bands_created":
            len(
                reference_bands
            )
            == 6,

        "all_reference_intervals_bounded":
            all(
                0.0
                <= item[
                    "lower_bound"
                ]
                <= item[
                    "observed_rate"
                ]
                <= item[
                    "upper_bound"
                ]
                <= 1.0
                for item in (
                    reference_bands.values()
                )
            ),

        "internal_reference_not_production_target":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "reference_is_production_target"
            ]
            is False,

        "internal_reference_not_clinical_acceptability":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "reference_is_clinical_acceptability_threshold"
            ]
            is False,

        "known_bad_behavior_not_acceptable_target":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "known_bad_historical_behavior_is_acceptable_target"
            ]
            is False,

        "all_known_risk_slices_not_acceptable_targets":
            all(
                item[
                    "acceptable_target"
                ]
                is False
                for item in (
                    known_risk_references.values()
                )
            ),

        "insufficient_sample_does_not_default_normal":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "insufficient_sample_defaults_to_normal"
            ]
            is False,

        "discrimination_uses_no_false_binomial_interval":
            D15_DISCRIMINATION_LIMIT_GOVERNANCE[
                "simple_binomial_interval_permitted"
            ]
            is False,

        "discrimination_requires_bootstrap":
            D15_DISCRIMINATION_LIMIT_GOVERNANCE[
                "bootstrap_uncertainty_required"
            ]
            is True,

        "automatic_model_change_disabled":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "single_window_breach_automatically_changes_model"
            ]
            is False,

        "automatic_threshold_change_disabled":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "single_window_breach_automatically_changes_threshold"
            ]
            is False,

        "production_deployment_not_authorized":
            D15_QUANTITATIVE_LIMIT_GOVERNANCE[
                "production_deployment_authorized"
            ]
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "validation_classification":
            "D15_QUANTITATIVE_MONITORING_LIMIT_FOUNDATION",

        "reference_band_count":
            len(
                reference_bands
            ),

        "known_risk_reference_count":
            len(
                known_risk_references
            ),

        "reference_bands":
            reference_bands,

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_BOOTSTRAP_AND_MATERIALITY_CONTROL_DESIGN"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_QUANTITATIVE_LIMIT_FOUNDATION"
            ),
    }


def print_d15_quantitative_monitoring_limit_foundation(
) -> None:
    """
    Print D15 quantitative monitoring-limit evidence.
    """

    evidence = (
        validate_d15_quantitative_monitoring_limit_foundation()
    )

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "QUANTITATIVE MONITORING LIMIT FOUNDATION"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Internal D14 surveillance reference bands"
    )

    print(
        "-" * 112
    )

    for (
        metric_name,
        reference,
    ) in evidence[
        "reference_bands"
    ].items():

        print(
            f"{metric_name:<18}"
            f"rate={reference['observed_rate']:.6f}  "
            f"95% reference interval="
            f"[{reference['lower_bound']:.6f}, "
            f"{reference['upper_bound']:.6f}]"
        )

    print()

    print(
        "Known-risk reference controls"
    )

    print(
        "-" * 112
    )

    print(
        f"Known-risk slices retained:      "
        f"{evidence['known_risk_reference_count']}"
    )

    print(
        "Historical risk = acceptable target: False"
    )

    print()

    print(
        "Governance validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "checks"
    ].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"QUANTITATIVE LIMIT STATUS:       "
        f"{evidence['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )

# ============================================================
# D15.90 — BOOTSTRAP UNCERTAINTY & MATERIALITY FOUNDATION
# ============================================================
#
# Purpose:
# Quantify sampling uncertainty around the frozen D14 locked-
# TEST discrimination estimates without retraining, retuning,
# recalibrating, refitting, or changing the operating point.
#
# IMPORTANT:
#
# Bootstrap intervals are INTERNAL HISTORICAL UNCERTAINTY
# estimates. They are not:
#
#   - production acceptance limits;
#   - clinical-effectiveness thresholds;
#   - external-validation evidence;
#   - deployment authorization criteria.
#
# ============================================================


D15_BOOTSTRAP_RANDOM_SEED = 42

D15_BOOTSTRAP_REPLICATES = 2000

D15_BOOTSTRAP_CONFIDENCE_LEVEL = 0.95


# ============================================================
# D15.91 — LOAD FROZEN D14 HISTORICAL PAIRS
# ============================================================


def load_d15_d14_locked_test_prediction_pairs(
) -> dict[str, Any]:
    """
    Reconstruct the frozen D14 locked-TEST transformation and
    generate probabilities using the already frozen candidate.

    This function performs read-only historical inference.

    It does NOT:
        - retrain;
        - retune;
        - recalibrate;
        - refit preprocessing;
        - optimize the threshold;
        - authorize deployment.
    """

    from src.models.locked_test_evaluation import (
        generate_d14_frozen_test_predictions,
    )

    prediction_bundle = (
        generate_d14_frozen_test_predictions()
    )

    transformed_bundle = (
        prediction_bundle[
            "transformed_bundle"
        ]
    )

    locked_test = (
        transformed_bundle[
            "locked_test"
        ]
    )

    if "readmitted_30d" not in locked_test.columns:
        raise KeyError(
            "Authoritative D14 locked TEST does not contain "
            "'readmitted_30d'."
        )

    y_true = (
        pd.to_numeric(
            locked_test[
                "readmitted_30d"
            ],
            errors="raise",
        )
        .astype(int)
        .to_numpy()
    )

    probability = np.asarray(
        prediction_bundle[
            "positive_probabilities"
        ],
        dtype=float,
    )

    if y_true.shape[0] != probability.shape[0]:
        raise RuntimeError(
            "D14 locked TEST outcome and probability counts "
            "do not match."
        )

    if y_true.shape[0] != 15038:
        raise RuntimeError(
            "Unexpected D14 locked TEST encounter count."
        )

    if set(
        np.unique(
            y_true
        )
    ) != {
        0,
        1,
    }:
        raise RuntimeError(
            "D14 locked TEST outcome must contain both "
            "binary classes."
        )

    if not np.isfinite(
        probability
    ).all():
        raise RuntimeError(
            "D14 frozen probabilities contain non-finite "
            "values."
        )

    if not (
        (
            probability
            >= 0.0
        )
        & (
            probability
            <= 1.0
        )
    ).all():
        raise RuntimeError(
            "D14 frozen probabilities fall outside [0, 1]."
        )

    positive_count = int(
        (
            y_true
            == 1
        ).sum()
    )

    negative_count = int(
        (
            y_true
            == 0
        ).sum()
    )

    checks = {
        "locked_test_count_is_15038":
            len(
                y_true
            )
            == 15038,

        "positive_count_is_1707":
            positive_count
            == 1707,

        "negative_count_is_13331":
            negative_count
            == 13331,

        "probability_count_matches_outcomes":
            len(
                probability
            )
            == len(
                y_true
            ),

        "model_artifact_identity_unchanged":
            prediction_bundle[
                "model_artifact_identity_unchanged"
            ]
            is True,

        "model_not_retrained":
            prediction_bundle[
                "model_retrained"
            ]
            is False,

        "model_not_retuned":
            prediction_bundle[
                "model_retuned"
            ]
            is False,

        "preprocessor_not_refitted":
            prediction_bundle[
                "preprocessor_refitted"
            ]
            is False,

        "threshold_not_retuned":
            prediction_bundle[
                "threshold_retuned"
            ]
            is False,

        "model_not_recalibrated":
            prediction_bundle[
                "model_recalibrated"
            ]
            is False,

        "deployment_not_authorized":
            prediction_bundle[
                "deployment_authorized"
            ]
            is False,
    }

    if not all(
        checks.values()
    ):
        raise RuntimeError(
            "D15 historical bootstrap source failed frozen "
            f"candidate validation: {checks}"
        )

    return {
        "y_true":
            y_true,

        "probability":
            probability,

        "encounter_count":
            int(
                len(
                    y_true
                )
            ),

        "positive_count":
            positive_count,

        "negative_count":
            negative_count,

        "prediction_bundle":
            prediction_bundle,

        "checks":
            checks,

        "overall_pass":
            True,
    }


# ============================================================
# D15.92 — STRATIFIED BOOTSTRAP INDEX GENERATOR
# ============================================================


def generate_d15_stratified_bootstrap_indices(
    y_true: np.ndarray,
    *,
    n_bootstrap: int = D15_BOOTSTRAP_REPLICATES,
    random_seed: int = D15_BOOTSTRAP_RANDOM_SEED,
) -> list[np.ndarray]:
    """
    Generate deterministic stratified bootstrap indices.

    Positive and negative observations are sampled separately
    with replacement to preserve class representation.
    """

    y = np.asarray(
        y_true,
        dtype=int,
    )

    positive_indices = np.flatnonzero(
        y
        == 1
    )

    negative_indices = np.flatnonzero(
        y
        == 0
    )

    if (
        len(
            positive_indices
        )
        == 0
        or len(
            negative_indices
        )
        == 0
    ):
        raise ValueError(
            "Stratified bootstrap requires both outcome "
            "classes."
        )

    if n_bootstrap <= 0:
        raise ValueError(
            "n_bootstrap must be positive."
        )

    rng = np.random.default_rng(
        random_seed
    )

    bootstrap_indices: list[
        np.ndarray
    ] = []

    for _ in range(
        n_bootstrap
    ):
        sampled_positive = (
            rng.choice(
                positive_indices,
                size=len(
                    positive_indices
                ),
                replace=True,
            )
        )

        sampled_negative = (
            rng.choice(
                negative_indices,
                size=len(
                    negative_indices
                ),
                replace=True,
            )
        )

        combined = np.concatenate(
            [
                sampled_positive,
                sampled_negative,
            ]
        )

        bootstrap_indices.append(
            combined
        )

    return bootstrap_indices


# ============================================================
# D15.93 — BOOTSTRAP DISCRIMINATION ENGINE
# ============================================================


def calculate_d15_bootstrap_discrimination_uncertainty(
    y_true: np.ndarray,
    probability: np.ndarray,
    *,
    n_bootstrap: int = D15_BOOTSTRAP_REPLICATES,
    confidence_level: float = D15_BOOTSTRAP_CONFIDENCE_LEVEL,
    random_seed: int = D15_BOOTSTRAP_RANDOM_SEED,
) -> dict[str, Any]:
    """
    Estimate percentile bootstrap uncertainty for PR-AUC and
    ROC-AUC using frozen outcome/probability pairs.
    """

    y = np.asarray(
        y_true,
        dtype=int,
    )

    p = np.asarray(
        probability,
        dtype=float,
    )

    if len(
        y
    ) != len(
        p
    ):
        raise ValueError(
            "Outcome and probability vectors must have equal "
            "length."
        )

    if set(
        np.unique(
            y
        )
    ) != {
        0,
        1,
    }:
        raise ValueError(
            "Bootstrap discrimination requires both binary "
            "classes."
        )

    if not (
        0.0
        < confidence_level
        < 1.0
    ):
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    point_pr_auc = float(
        average_precision_score(
            y,
            p,
        )
    )

    point_roc_auc = float(
        roc_auc_score(
            y,
            p,
        )
    )

    index_sets = (
        generate_d15_stratified_bootstrap_indices(
            y,
            n_bootstrap=n_bootstrap,
            random_seed=random_seed,
        )
    )

    pr_values = np.empty(
        n_bootstrap,
        dtype=float,
    )

    roc_values = np.empty(
        n_bootstrap,
        dtype=float,
    )

    for index, sample_indices in enumerate(
        index_sets
    ):
        sample_y = y[
            sample_indices
        ]

        sample_probability = p[
            sample_indices
        ]

        pr_values[
            index
        ] = average_precision_score(
            sample_y,
            sample_probability,
        )

        roc_values[
            index
        ] = roc_auc_score(
            sample_y,
            sample_probability,
        )

    alpha = (
        1.0
        - confidence_level
    )

    lower_percentile = (
        100.0
        * alpha
        / 2.0
    )

    upper_percentile = (
        100.0
        * (
            1.0
            - alpha / 2.0
        )
    )

    pr_lower, pr_upper = np.percentile(
        pr_values,
        [
            lower_percentile,
            upper_percentile,
        ],
    )

    roc_lower, roc_upper = np.percentile(
        roc_values,
        [
            lower_percentile,
            upper_percentile,
        ],
    )

    return {
        "method":
            "STRATIFIED_PERCENTILE_BOOTSTRAP",

        "bootstrap_replicates":
            int(
                n_bootstrap
            ),

        "random_seed":
            int(
                random_seed
            ),

        "confidence_level":
            float(
                confidence_level
            ),

        "pr_auc": {
            "point_estimate":
                point_pr_auc,

            "bootstrap_mean":
                float(
                    np.mean(
                        pr_values
                    )
                ),

            "bootstrap_std":
                float(
                    np.std(
                        pr_values,
                        ddof=1,
                    )
                ),

            "lower_bound":
                float(
                    pr_lower
                ),

            "upper_bound":
                float(
                    pr_upper
                ),
        },

        "roc_auc": {
            "point_estimate":
                point_roc_auc,

            "bootstrap_mean":
                float(
                    np.mean(
                        roc_values
                    )
                ),

            "bootstrap_std":
                float(
                    np.std(
                        roc_values,
                        ddof=1,
                    )
                ),

            "lower_bound":
                float(
                    roc_lower
                ),

            "upper_bound":
                float(
                    roc_upper
                ),
        },

        "invalid_bootstrap_replicates":
            0,

        "model_retrained":
            False,

        "model_retuned":
            False,

        "threshold_retuned":
            False,

        "model_recalibrated":
            False,
    }


# ============================================================
# D15.94 — BOOTSTRAP REPRODUCIBILITY VALIDATION
# ============================================================


def validate_d15_bootstrap_reproducibility(
    y_true: np.ndarray,
    probability: np.ndarray,
    *,
    validation_replicates: int = 100,
) -> dict[str, Any]:
    """
    Verify deterministic bootstrap behavior using a smaller
    reproducibility run.
    """

    first = (
        calculate_d15_bootstrap_discrimination_uncertainty(
            y_true,
            probability,
            n_bootstrap=(
                validation_replicates
            ),
            random_seed=(
                D15_BOOTSTRAP_RANDOM_SEED
            ),
        )
    )

    second = (
        calculate_d15_bootstrap_discrimination_uncertainty(
            y_true,
            probability,
            n_bootstrap=(
                validation_replicates
            ),
            random_seed=(
                D15_BOOTSTRAP_RANDOM_SEED
            ),
        )
    )

    checks = {
        "pr_auc_point_reproducible":
            first[
                "pr_auc"
            ][
                "point_estimate"
            ]
            == second[
                "pr_auc"
            ][
                "point_estimate"
            ],

        "pr_auc_lower_reproducible":
            first[
                "pr_auc"
            ][
                "lower_bound"
            ]
            == second[
                "pr_auc"
            ][
                "lower_bound"
            ],

        "pr_auc_upper_reproducible":
            first[
                "pr_auc"
            ][
                "upper_bound"
            ]
            == second[
                "pr_auc"
            ][
                "upper_bound"
            ],

        "roc_auc_point_reproducible":
            first[
                "roc_auc"
            ][
                "point_estimate"
            ]
            == second[
                "roc_auc"
            ][
                "point_estimate"
            ],

        "roc_auc_lower_reproducible":
            first[
                "roc_auc"
            ][
                "lower_bound"
            ]
            == second[
                "roc_auc"
            ][
                "lower_bound"
            ],

        "roc_auc_upper_reproducible":
            first[
                "roc_auc"
            ][
                "upper_bound"
            ]
            == second[
                "roc_auc"
            ][
                "upper_bound"
            ],
    }

    return {
        "checks":
            checks,

        "overall_pass":
            all(
                checks.values()
            ),
    }


# ============================================================
# D15.95 — DISCRIMINATION REFERENCE VALIDATION
# ============================================================


def validate_d15_bootstrap_point_estimates(
    bootstrap_evidence: dict[str, Any],
) -> dict[str, Any]:
    """
    Confirm that the historical point estimates reproduced by
    D15 match the authoritative D14 locked-test metrics.
    """

    observed_pr = (
        bootstrap_evidence[
            "pr_auc"
        ][
            "point_estimate"
        ]
    )

    observed_roc = (
        bootstrap_evidence[
            "roc_auc"
        ][
            "point_estimate"
        ]
    )

    expected_pr = (
        D15_D14_LOCKED_TEST_REFERENCE[
            "pr_auc"
        ]
    )

    expected_roc = (
        D15_D14_LOCKED_TEST_REFERENCE[
            "roc_auc"
        ]
    )

    checks = {
        "pr_auc_matches_d14_reference":
            np.isclose(
                observed_pr,
                expected_pr,
                rtol=0.0,
                atol=1e-12,
            ),

        "roc_auc_matches_d14_reference":
            np.isclose(
                observed_roc,
                expected_roc,
                rtol=0.0,
                atol=1e-12,
            ),

        "pr_auc_inside_bootstrap_interval":
            (
                bootstrap_evidence[
                    "pr_auc"
                ][
                    "lower_bound"
                ]
                <= observed_pr
                <= bootstrap_evidence[
                    "pr_auc"
                ][
                    "upper_bound"
                ]
            ),

        "roc_auc_inside_bootstrap_interval":
            (
                bootstrap_evidence[
                    "roc_auc"
                ][
                    "lower_bound"
                ]
                <= observed_roc
                <= bootstrap_evidence[
                    "roc_auc"
                ][
                    "upper_bound"
                ]
            ),

        "no_invalid_bootstrap_replicates":
            bootstrap_evidence[
                "invalid_bootstrap_replicates"
            ]
            == 0,

        "model_not_retrained":
            bootstrap_evidence[
                "model_retrained"
            ]
            is False,

        "model_not_retuned":
            bootstrap_evidence[
                "model_retuned"
            ]
            is False,

        "threshold_not_retuned":
            bootstrap_evidence[
                "threshold_retuned"
            ]
            is False,

        "model_not_recalibrated":
            bootstrap_evidence[
                "model_recalibrated"
            ]
            is False,
    }

    return {
        "checks":
            checks,

        "overall_pass":
            all(
                checks.values()
            ),
    }


# ============================================================
# D15.96 — MATERIALITY GOVERNANCE MODEL
# ============================================================
#
# Statistical difference and materiality are intentionally
# separated.
#
# A statistical signal alone does not establish clinical harm.
# Conversely, an operationally important change should not be
# ignored merely because a small monitoring window lacks
# statistical precision.
# ============================================================


D15_MATERIALITY_GOVERNANCE = {
    "statistical_signal_equals_clinical_materiality":
        False,

    "single_window_signal_equals_persistent_drift":
        False,

    "materiality_requires_contextual_review":
        True,

    "clinical_review_required_for_clinical_materiality":
        True,

    "operational_review_required_for_workload_materiality":
        True,

    "responsible_ai_review_required_for_subgroup_materiality":
        True,

    "automatic_model_change":
        False,

    "automatic_threshold_change":
        False,
}


# ============================================================
# D15.97 — PERSISTENCE GOVERNANCE MODEL
# ============================================================


D15_PERSISTENCE_GOVERNANCE = {
    "single_adequate_window":
        "WATCH_ELIGIBLE",

    "repeated_adequate_windows":
        "ALERT_ELIGIBLE",

    "critical_integrity_failure_requires_persistence":
        False,

    "clinical_safety_incident_requires_persistence":
        False,

    "performance_signal_requires_sample_sufficiency":
        True,

    "subgroup_signal_requires_sample_sufficiency":
        True,

    "insufficient_evidence_state":
        "NOT_ASSESSABLE",

    "automatic_retraining":
        False,
}


# ============================================================
# D15.98 — BUILD BOOTSTRAP FOUNDATION EVIDENCE
# ============================================================


def build_d15_bootstrap_materiality_evidence(
    *,
    n_bootstrap: int = D15_BOOTSTRAP_REPLICATES,
) -> dict[str, Any]:
    """
    Build authoritative D15 bootstrap uncertainty evidence from
    the frozen D14 historical prediction/outcome pairs.
    """

    source = (
        load_d15_d14_locked_test_prediction_pairs()
    )

    bootstrap = (
        calculate_d15_bootstrap_discrimination_uncertainty(
            source[
                "y_true"
            ],
            source[
                "probability"
            ],
            n_bootstrap=(
                n_bootstrap
            ),
            confidence_level=(
                D15_BOOTSTRAP_CONFIDENCE_LEVEL
            ),
            random_seed=(
                D15_BOOTSTRAP_RANDOM_SEED
            ),
        )
    )

    point_validation = (
        validate_d15_bootstrap_point_estimates(
            bootstrap
        )
    )

    reproducibility = (
        validate_d15_bootstrap_reproducibility(
            source[
                "y_true"
            ],
            source[
                "probability"
            ],
        )
    )

    checks = {
        "historical_pair_source_valid":
            source[
                "overall_pass"
            ],

        "bootstrap_point_estimates_valid":
            point_validation[
                "overall_pass"
            ],

        "bootstrap_reproducible":
            reproducibility[
                "overall_pass"
            ],

        "statistical_signal_not_clinical_materiality":
            D15_MATERIALITY_GOVERNANCE[
                "statistical_signal_equals_clinical_materiality"
            ]
            is False,

        "single_window_not_persistent_drift":
            D15_MATERIALITY_GOVERNANCE[
                "single_window_signal_equals_persistent_drift"
            ]
            is False,

        "sample_sufficiency_required":
            D15_PERSISTENCE_GOVERNANCE[
                "performance_signal_requires_sample_sufficiency"
            ]
            is True,

        "automatic_model_change_disabled":
            D15_MATERIALITY_GOVERNANCE[
                "automatic_model_change"
            ]
            is False,

        "automatic_threshold_change_disabled":
            D15_MATERIALITY_GOVERNANCE[
                "automatic_threshold_change"
            ]
            is False,

        "production_deployment_not_authorized":
            D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "evidence_classification":
            "D15_BOOTSTRAP_UNCERTAINTY_AND_MATERIALITY_FOUNDATION",

        "historical_source":
            {
                "encounter_count":
                    source[
                        "encounter_count"
                    ],

                "positive_count":
                    source[
                        "positive_count"
                    ],

                "negative_count":
                    source[
                        "negative_count"
                    ],
            },

        "bootstrap":
            bootstrap,

        "point_validation":
            point_validation,

        "reproducibility":
            reproducibility,

        "materiality_governance":
            D15_MATERIALITY_GOVERNANCE,

        "persistence_governance":
            D15_PERSISTENCE_GOVERNANCE,

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_INTEGRATED_WATCH_ALERT_CONTROL_ENGINE"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_BOOTSTRAP_FOUNDATION"
            ),
    }


# ============================================================
# D15.99 — PRINT BOOTSTRAP & MATERIALITY EVIDENCE
# ============================================================


def print_d15_bootstrap_materiality_evidence(
    *,
    n_bootstrap: int = D15_BOOTSTRAP_REPLICATES,
) -> None:
    """
    Print D15 bootstrap uncertainty and materiality evidence.
    """

    evidence = (
        build_d15_bootstrap_materiality_evidence(
            n_bootstrap=n_bootstrap
        )
    )

    bootstrap = evidence[
        "bootstrap"
    ]

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "BOOTSTRAP UNCERTAINTY & MATERIALITY FOUNDATION"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Frozen historical source"
    )

    print(
        "-" * 112
    )

    print(
        f"Encounters:                     "
        f"{evidence['historical_source']['encounter_count']}"
    )

    print(
        f"Positive outcomes:              "
        f"{evidence['historical_source']['positive_count']}"
    )

    print(
        f"Negative outcomes:              "
        f"{evidence['historical_source']['negative_count']}"
    )

    print()

    print(
        "Bootstrap configuration"
    )

    print(
        "-" * 112
    )

    print(
        f"Method:                         "
        f"{bootstrap['method']}"
    )

    print(
        f"Replicates:                     "
        f"{bootstrap['bootstrap_replicates']}"
    )

    print(
        f"Random seed:                    "
        f"{bootstrap['random_seed']}"
    )

    print(
        f"Confidence level:               "
        f"{bootstrap['confidence_level']:.2f}"
    )

    print()

    print(
        "Discrimination uncertainty"
    )

    print(
        "-" * 112
    )

    print(
        f"PR-AUC point estimate:          "
        f"{bootstrap['pr_auc']['point_estimate']:.12f}"
    )

    print(
        f"PR-AUC bootstrap 95% CI:        "
        f"[{bootstrap['pr_auc']['lower_bound']:.12f}, "
        f"{bootstrap['pr_auc']['upper_bound']:.12f}]"
    )

    print(
        f"ROC-AUC point estimate:         "
        f"{bootstrap['roc_auc']['point_estimate']:.12f}"
    )

    print(
        f"ROC-AUC bootstrap 95% CI:       "
        f"[{bootstrap['roc_auc']['lower_bound']:.12f}, "
        f"{bootstrap['roc_auc']['upper_bound']:.12f}]"
    )

    print()

    print(
        "Governance validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "checks"
    ].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"BOOTSTRAP FOUNDATION STATUS:     "
        f"{evidence['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )

# ============================================================
# D15.100 — INTEGRATED WATCH / ALERT CONTROL ENGINE
# ============================================================
#
# Purpose:
# Integrate sample sufficiency, statistical surveillance,
# persistence, materiality review, structural controls and
# outcome availability into governed monitoring states.
#
# Statistical change != clinical materiality.
# Monitoring signal != automatic model modification.
# ============================================================


# ============================================================
# D15.101 — CONTROL STATES
# ============================================================


D15_INTEGRATED_CONTROL_STATES = (
    "NORMAL",
    "WATCH",
    "ALERT",
    "CRITICAL",
    "NOT_ASSESSABLE",
)


D15_INTEGRATED_CONTROL_GOVERNANCE = {
    "statistical_signal_alone_can_trigger_watch":
        True,

    "statistical_signal_alone_can_trigger_alert":
        False,

    "persistent_signal_can_trigger_alert_review":
        True,

    "clinical_materiality_requires_human_review":
        True,

    "subgroup_materiality_requires_responsible_ai_review":
        True,

    "critical_integrity_failure_is_fail_closed":
        True,

    "automatic_retraining":
        False,

    "automatic_recalibration":
        False,

    "automatic_threshold_change":
        False,

    "automatic_subgroup_threshold_change":
        False,

    "production_deployment_authorized":
        False,
}


# ============================================================
# D15.102 — BINARY RATE SIGNAL ENGINE
# ============================================================


def evaluate_d15_binary_rate_signal(
    *,
    metric_name: str,
    observed_events: int,
    observed_denominator: int,
    encounter_count: int,
    positive_count: int | None = None,
    negative_count: int | None = None,
    subgroup: bool = False,
) -> dict[str, Any]:
    """
    Evaluate a binary monitoring rate against the frozen D14
    internal surveillance reference.

    Statistical signal does not independently establish
    clinical materiality.
    """

    sufficiency = (
        assess_d15_monitoring_sample_sufficiency(
            encounter_count=encounter_count,
            positive_count=positive_count,
            negative_count=negative_count,
            subgroup=subgroup,
        )
    )

    if not sufficiency[
        "sufficient"
    ]:
        return {
            "metric_name":
                metric_name,

            "status":
                "NOT_ASSESSABLE",

            "sample_sufficiency":
                sufficiency,

            "statistical_signal":
                "NOT_ASSESSABLE_INSUFFICIENT_EVIDENCE",

            "materiality_confirmed":
                False,

            "automatic_model_change":
                False,

            "automatic_threshold_change":
                False,
        }

    comparison = (
        compare_d15_observed_rate_to_reference(
            metric_name=metric_name,
            observed_events=observed_events,
            observed_denominator=observed_denominator,
        )
    )

    statistical_signal = (
        comparison[
            "reference_and_observed_intervals_separated"
        ]
    )

    status = (
        "WATCH"
        if statistical_signal
        else "NORMAL"
    )

    return {
        "metric_name":
            metric_name,

        "status":
            status,

        "sample_sufficiency":
            sufficiency,

        "comparison":
            comparison,

        "statistical_signal":
            (
                "REFERENCE_SHIFT_SIGNAL"
                if statistical_signal
                else
                "NO_CLEAR_REFERENCE_SHIFT_SIGNAL"
            ),

        "materiality_confirmed":
            False,

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,
    }


# ============================================================
# D15.103 — DISCRIMINATION SIGNAL ENGINE
# ============================================================


def evaluate_d15_discrimination_signal(
    *,
    metric_name: str,
    observed_value: float,
    monitoring_interval_lower: float,
    monitoring_interval_upper: float,
    reference_bootstrap_evidence: dict[str, Any],
    sample_sufficient: bool,
) -> dict[str, Any]:
    """
    Compare monitoring discrimination uncertainty with the
    historical D14 bootstrap reference.

    Supported metrics:
        PR_AUC
        ROC_AUC
    """

    metric_lookup = {
        "PR_AUC": "pr_auc",
        "ROC_AUC": "roc_auc",
    }

    if metric_name not in metric_lookup:
        raise KeyError(
            "Unsupported discrimination metric: "
            f"{metric_name!r}"
        )

    if not sample_sufficient:
        return {
            "metric_name":
                metric_name,

            "status":
                "NOT_ASSESSABLE",

            "statistical_signal":
                "NOT_ASSESSABLE_INSUFFICIENT_EVIDENCE",

            "materiality_confirmed":
                False,
        }

    key = (
        metric_lookup[
            metric_name
        ]
    )

    reference = (
        reference_bootstrap_evidence[
            key
        ]
    )

    reference_lower = (
        reference[
            "lower_bound"
        ]
    )

    reference_upper = (
        reference[
            "upper_bound"
        ]
    )

    intervals_separated = bool(
        monitoring_interval_upper
        < reference_lower
        or monitoring_interval_lower
        > reference_upper
    )

    return {
        "metric_name":
            metric_name,

        "observed_value":
            float(
                observed_value
            ),

        "monitoring_interval":
            {
                "lower_bound":
                    float(
                        monitoring_interval_lower
                    ),

                "upper_bound":
                    float(
                        monitoring_interval_upper
                    ),
            },

        "reference_interval":
            {
                "lower_bound":
                    float(
                        reference_lower
                    ),

                "upper_bound":
                    float(
                        reference_upper
                    ),
            },

        "intervals_separated":
            intervals_separated,

        "statistical_signal":
            (
                "REFERENCE_SHIFT_SIGNAL"
                if intervals_separated
                else
                "NO_CLEAR_REFERENCE_SHIFT_SIGNAL"
            ),

        "status":
            (
                "WATCH"
                if intervals_separated
                else "NORMAL"
            ),

        "materiality_confirmed":
            False,
    }


# ============================================================
# D15.104 — PERSISTENCE ENGINE
# ============================================================


def evaluate_d15_signal_persistence(
    window_statuses: list[str],
) -> dict[str, Any]:
    """
    Determine whether a surveillance signal persists across
    adequate sequential monitoring windows.

    This function does not infer that windows are independent.
    """

    valid = {
        "NORMAL",
        "WATCH",
        "ALERT",
        "CRITICAL",
        "NOT_ASSESSABLE",
    }

    invalid = [
        status
        for status in window_statuses
        if status not in valid
    ]

    if invalid:
        raise ValueError(
            "Invalid monitoring statuses: "
            f"{invalid}"
        )

    assessable = [
        status
        for status in window_statuses
        if status
        != "NOT_ASSESSABLE"
    ]

    if not assessable:
        return {
            "status":
                "NOT_ASSESSABLE",

            "persistent_signal":
                False,

            "consecutive_watch_or_higher":
                0,
        }

    consecutive = 0

    for status in reversed(
        assessable
    ):
        if status in {
            "WATCH",
            "ALERT",
            "CRITICAL",
        }:
            consecutive += 1

        else:
            break

    persistent_signal = (
        consecutive
        >= 2
    )

    return {
        "status":
            (
                "PERSISTENT_SIGNAL"
                if persistent_signal
                else "NO_PERSISTENT_SIGNAL"
            ),

        "persistent_signal":
            persistent_signal,

        "consecutive_watch_or_higher":
            consecutive,

        "windows_reviewed":
            len(
                window_statuses
            ),

        "assessable_windows":
            len(
                assessable
            ),
    }


# ============================================================
# D15.105 — MATERIALITY REVIEW RECORD
# ============================================================


def build_d15_materiality_review_record(
    *,
    clinical_materiality_confirmed: bool = False,
    operational_materiality_confirmed: bool = False,
    subgroup_materiality_confirmed: bool = False,
    reviewer_authorized: bool = False,
    review_documented: bool = False,
) -> dict[str, Any]:
    """
    Represent formal human materiality review.

    Materiality cannot be treated as confirmed unless the
    review is both authorized and documented.
    """

    requested_confirmation = any(
        [
            clinical_materiality_confirmed,
            operational_materiality_confirmed,
            subgroup_materiality_confirmed,
        ]
    )

    effective_confirmation = bool(
        requested_confirmation
        and reviewer_authorized
        and review_documented
    )

    return {
        "clinical_materiality_confirmed":
            bool(
                clinical_materiality_confirmed
            ),

        "operational_materiality_confirmed":
            bool(
                operational_materiality_confirmed
            ),

        "subgroup_materiality_confirmed":
            bool(
                subgroup_materiality_confirmed
            ),

        "reviewer_authorized":
            bool(
                reviewer_authorized
            ),

        "review_documented":
            bool(
                review_documented
            ),

        "materiality_confirmed":
            effective_confirmation,

        "automatic_confirmation_permitted":
            False,
    }


# ============================================================
# D15.106 — INTEGRATED STATUS RESOLUTION
# ============================================================


def resolve_d15_integrated_monitoring_status(
    *,
    structural_status: str,
    metric_status: str,
    persistent_signal: bool,
    materiality_confirmed: bool,
) -> dict[str, Any]:
    """
    Resolve the integrated governance state.

    Rules:
      CRITICAL structural failure -> CRITICAL
      insufficient evidence       -> NOT_ASSESSABLE
      no statistical signal       -> NORMAL
      single statistical signal   -> WATCH
      persistent signal           -> ALERT review
      confirmed materiality       -> ALERT review

    ALERT remains a review state and does not modify the model.
    """

    if structural_status == "CRITICAL":
        status = "CRITICAL"

        reason = (
            "FAIL_CLOSED_STRUCTURAL_OR_INCIDENT_TRIGGER"
        )

    elif metric_status == "NOT_ASSESSABLE":
        status = "NOT_ASSESSABLE"

        reason = (
            "INSUFFICIENT_OR_UNAVAILABLE_EVIDENCE"
        )

    elif metric_status == "NORMAL":
        status = "NORMAL"

        reason = (
            "NO_CLEAR_SURVEILLANCE_SHIFT_SIGNAL"
        )

    elif (
        metric_status == "WATCH"
        and (
            persistent_signal
            or materiality_confirmed
        )
    ):
        status = "ALERT"

        reason = (
            "PERSISTENT_OR_MATERIAL_SURVEILLANCE_SIGNAL"
        )

    elif metric_status == "WATCH":
        status = "WATCH"

        reason = (
            "SINGLE_ADEQUATE_SURVEILLANCE_SIGNAL"
        )

    elif metric_status in {
        "ALERT",
        "CRITICAL",
    }:
        status = metric_status

        reason = (
            "UPSTREAM_ESCALATED_MONITORING_STATE"
        )

    else:
        raise ValueError(
            "Unsupported metric status: "
            f"{metric_status!r}"
        )

    return {
        "status":
            status,

        "reason":
            reason,

        "governance_action":
            D15_ESCALATION_LEVELS[
                status
            ][
                "governance_action"
            ],

        "automatic_model_change":
            False,

        "automatic_recalibration":
            False,

        "automatic_threshold_change":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.107 — CHANGE-CONTROL BOUNDARY
# ============================================================


D15_MONITORING_CHANGE_CONTROL_BOUNDARY = {
    "watch_requires_investigation":
        True,

    "alert_requires_formal_governance_review":
        True,

    "critical_requires_fail_closed_or_suspension_review":
        True,

    "model_change_requires_separate_change_control":
        True,

    "model_change_requires_revalidation":
        True,

    "threshold_change_requires_revalidation":
        True,

    "preprocessor_change_requires_revalidation":
        True,

    "feature_change_requires_revalidation":
        True,

    "new_version_required_after_authorized_model_change":
        True,

    "test_driven_silent_redesign_permitted":
        False,

    "automatic_model_change_permitted":
        False,
}


# ============================================================
# D15.108 — VALIDATE INTEGRATED CONTROL ENGINE
# ============================================================


def validate_d15_integrated_watch_alert_control_engine(
) -> dict[str, Any]:
    """
    Validate the governance behavior of the integrated control
    engine using deterministic synthetic control scenarios.
    """

    normal = (
        resolve_d15_integrated_monitoring_status(
            structural_status="NORMAL",
            metric_status="NORMAL",
            persistent_signal=False,
            materiality_confirmed=False,
        )
    )

    watch = (
        resolve_d15_integrated_monitoring_status(
            structural_status="NORMAL",
            metric_status="WATCH",
            persistent_signal=False,
            materiality_confirmed=False,
        )
    )

    persistent_alert = (
        resolve_d15_integrated_monitoring_status(
            structural_status="NORMAL",
            metric_status="WATCH",
            persistent_signal=True,
            materiality_confirmed=False,
        )
    )

    material_alert = (
        resolve_d15_integrated_monitoring_status(
            structural_status="NORMAL",
            metric_status="WATCH",
            persistent_signal=False,
            materiality_confirmed=True,
        )
    )

    critical = (
        resolve_d15_integrated_monitoring_status(
            structural_status="CRITICAL",
            metric_status="NORMAL",
            persistent_signal=False,
            materiality_confirmed=False,
        )
    )

    not_assessable = (
        resolve_d15_integrated_monitoring_status(
            structural_status="NORMAL",
            metric_status="NOT_ASSESSABLE",
            persistent_signal=False,
            materiality_confirmed=False,
        )
    )

    unauthorized_materiality = (
        build_d15_materiality_review_record(
            clinical_materiality_confirmed=True,
            reviewer_authorized=False,
            review_documented=False,
        )
    )

    authorized_materiality = (
        build_d15_materiality_review_record(
            clinical_materiality_confirmed=True,
            reviewer_authorized=True,
            review_documented=True,
        )
    )

    persistence = (
        evaluate_d15_signal_persistence(
            [
                "NORMAL",
                "WATCH",
                "WATCH",
            ]
        )
    )

    checks = {
        "normal_scenario_resolves_normal":
            normal[
                "status"
            ]
            == "NORMAL",

        "single_signal_resolves_watch":
            watch[
                "status"
            ]
            == "WATCH",

        "persistent_signal_resolves_alert":
            persistent_alert[
                "status"
            ]
            == "ALERT",

        "material_signal_resolves_alert":
            material_alert[
                "status"
            ]
            == "ALERT",

        "critical_structural_failure_overrides_normal_metric":
            critical[
                "status"
            ]
            == "CRITICAL",

        "insufficient_evidence_remains_not_assessable":
            not_assessable[
                "status"
            ]
            == "NOT_ASSESSABLE",

        "unauthorized_materiality_cannot_confirm":
            unauthorized_materiality[
                "materiality_confirmed"
            ]
            is False,

        "authorized_documented_materiality_can_confirm":
            authorized_materiality[
                "materiality_confirmed"
            ]
            is True,

        "two_consecutive_watch_windows_are_persistent":
            persistence[
                "persistent_signal"
            ]
            is True,

        "watch_does_not_auto_retrain":
            watch[
                "automatic_model_change"
            ]
            is False,

        "alert_does_not_auto_retrain":
            persistent_alert[
                "automatic_model_change"
            ]
            is False,

        "alert_does_not_auto_recalibrate":
            persistent_alert[
                "automatic_recalibration"
            ]
            is False,

        "alert_does_not_change_threshold":
            persistent_alert[
                "automatic_threshold_change"
            ]
            is False,

        "change_requires_revalidation":
            D15_MONITORING_CHANGE_CONTROL_BOUNDARY[
                "model_change_requires_revalidation"
            ]
            is True,

        "automatic_model_change_prohibited":
            D15_MONITORING_CHANGE_CONTROL_BOUNDARY[
                "automatic_model_change_permitted"
            ]
            is False,

        "production_deployment_not_authorized":
            D15_INTEGRATED_CONTROL_GOVERNANCE[
                "production_deployment_authorized"
            ]
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "engine_classification":
            "INTEGRATED_WATCH_ALERT_CONTROL_ENGINE",

        "scenario_results": {
            "normal":
                normal,

            "watch":
                watch,

            "persistent_alert":
                persistent_alert,

            "material_alert":
                material_alert,

            "critical":
                critical,

            "not_assessable":
                not_assessable,
        },

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_INCIDENT_CHANGE_ROLLBACK_AND_CONTINUITY_CONTROLS"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_INTEGRATED_CONTROL_ENGINE"
            ),
    }


# ============================================================
# D15.109 — PRINT INTEGRATED CONTROL EVIDENCE
# ============================================================


def print_d15_integrated_watch_alert_control_engine(
) -> None:
    """
    Print D15 integrated monitoring-control evidence.
    """

    evidence = (
        validate_d15_integrated_watch_alert_control_engine()
    )

    scenarios = evidence[
        "scenario_results"
    ]

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "INTEGRATED WATCH / ALERT CONTROL ENGINE"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Deterministic governance scenarios"
    )

    print(
        "-" * 112
    )

    print(
        f"Healthy monitoring state:       "
        f"{scenarios['normal']['status']}"
    )

    print(
        f"Single surveillance signal:     "
        f"{scenarios['watch']['status']}"
    )

    print(
        f"Persistent surveillance signal: "
        f"{scenarios['persistent_alert']['status']}"
    )

    print(
        f"Confirmed material signal:      "
        f"{scenarios['material_alert']['status']}"
    )

    print(
        f"Structural integrity failure:   "
        f"{scenarios['critical']['status']}"
    )

    print(
        f"Insufficient evidence:          "
        f"{scenarios['not_assessable']['status']}"
    )

    print()

    print(
        "Governance validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "checks"
    ].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"INTEGRATED CONTROL STATUS:       "
        f"{evidence['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )

# ============================================================
# D15.110 — INCIDENT, CHANGE, ROLLBACK & BUSINESS CONTINUITY
# ============================================================
#
# Purpose:
# Define operational governance for incidents, controlled
# change, rollback and service continuity for the frozen
# clinical decision-support candidate.
#
# These controls remain PRE-DEPLOYMENT DESIGN CONTROLS.
# They do not authorize production deployment.
# ============================================================


# ============================================================
# D15.111 — INCIDENT SEVERITY MODEL
# ============================================================


D15_INCIDENT_SEVERITY_MODEL = {
    "SEV1": {
        "classification":
            "CRITICAL",

        "examples": (
            "FROZEN_ARTIFACT_IDENTITY_FAILURE",
            "SYSTEMATICALLY_INVALID_PREDICTIONS",
            "PATIENT_SAFETY_EVENT_POTENTIALLY_RELATED_TO_MODEL",
            "UNAUTHORIZED_MODEL_OR_THRESHOLD_CHANGE",
            "MATERIAL_SECURITY_OR_PRIVACY_INCIDENT",
        ),

        "required_action":
            "IMMEDIATE_FAIL_CLOSED_AND_FORMAL_INCIDENT_RESPONSE",

        "continued_ai_inference":
            False,
    },

    "SEV2": {
        "classification":
            "HIGH",

        "examples": (
            "MATERIAL_PERFORMANCE_DEGRADATION",
            "PERSISTENT_SUBGROUP_PERFORMANCE_CONCERN",
            "PERSISTENT_UTILIZATION_DEPENDENCE_CONCERN",
            "MATERIAL_WORKFLOW_OR_OVERRIDE_ANOMALY",
        ),

        "required_action":
            "FORMAL_GOVERNANCE_REVIEW_AND_SUSPENSION_CONSIDERATION",

        "continued_ai_inference":
            "REQUIRES_AUTHORIZED_DECISION",
    },

    "SEV3": {
        "classification":
            "MODERATE",

        "examples": (
            "NON_CRITICAL_DATA_QUALITY_ANOMALY",
            "SINGLE_MONITORING_WATCH_SIGNAL",
            "NON_CRITICAL_WORKFLOW_INTEGRATION_ISSUE",
        ),

        "required_action":
            "INVESTIGATE_DOCUMENT_AND_MONITOR",

        "continued_ai_inference":
            "CONDITIONAL_ON_CONTROL_INTEGRITY",
    },

    "SEV4": {
        "classification":
            "LOW",

        "examples": (
            "DOCUMENTATION_DEFECT",
            "NON_SAFETY_UI_DEFECT",
            "MINOR_TELEMETRY_ISSUE",
        ),

        "required_action":
            "ROUTINE_CORRECTIVE_ACTION",

        "continued_ai_inference":
            "CONDITIONAL_ON_CONTROL_INTEGRITY",
    },
}


# ============================================================
# D15.112 — INCIDENT RECORD CONTRACT
# ============================================================


D15_REQUIRED_INCIDENT_FIELDS = (
    "incident_id",
    "detected_at_utc",
    "severity",
    "incident_type",
    "detection_source",
    "affected_component",
    "candidate_registry_id",
    "candidate_model_version",
    "candidate_system_sha256",
    "frozen_threshold",
    "clinical_safety_relevance",
    "affected_population",
    "immediate_containment",
    "ai_service_status",
    "human_workflow_status",
    "governance_owner",
    "root_cause_status",
    "corrective_action_status",
    "revalidation_required",
    "closure_status",
)


def build_d15_incident_record(
    *,
    incident_id: str,
    severity: str,
    incident_type: str,
    detection_source: str,
    affected_component: str,
    clinical_safety_relevance: bool,
    affected_population: str,
    immediate_containment: str,
    ai_service_status: str,
    human_workflow_status: str,
    governance_owner: str,
) -> dict[str, Any]:
    """
    Build a governed D15 incident record.
    """

    if severity not in (
        D15_INCIDENT_SEVERITY_MODEL
    ):
        raise ValueError(
            "Unknown D15 incident severity: "
            f"{severity!r}"
        )

    if not incident_id.strip():
        raise ValueError(
            "incident_id must not be empty."
        )

    now_utc = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    return {
        "incident_id":
            incident_id,

        "detected_at_utc":
            now_utc,

        "severity":
            severity,

        "incident_type":
            incident_type,

        "detection_source":
            detection_source,

        "affected_component":
            affected_component,

        "candidate_registry_id":
            D15_EXPECTED_REGISTRY_ID,

        "candidate_model_version":
            D15_EXPECTED_MODEL_VERSION,

        "candidate_system_sha256":
            D15_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "frozen_threshold":
            D15_FROZEN_OPERATING_THRESHOLD,

        "clinical_safety_relevance":
            bool(
                clinical_safety_relevance
            ),

        "affected_population":
            affected_population,

        "immediate_containment":
            immediate_containment,

        "ai_service_status":
            ai_service_status,

        "human_workflow_status":
            human_workflow_status,

        "governance_owner":
            governance_owner,

        "root_cause_status":
            "OPEN",

        "corrective_action_status":
            "PENDING",

        "revalidation_required":
            severity
            in {
                "SEV1",
                "SEV2",
            },

        "closure_status":
            "OPEN",

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,

        "production_deployment_authorized":
            False,
    }


def validate_d15_incident_record(
    incident_record: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate incident evidence completeness.
    """

    missing_fields = [
        field
        for field in (
            D15_REQUIRED_INCIDENT_FIELDS
        )
        if field
        not in incident_record
    ]

    severity = (
        incident_record.get(
            "severity"
        )
    )

    checks = {
        "required_incident_fields_present":
            len(
                missing_fields
            )
            == 0,

        "severity_valid":
            severity
            in D15_INCIDENT_SEVERITY_MODEL,

        "candidate_identity_preserved":
            (
                incident_record.get(
                    "candidate_registry_id"
                )
                == D15_EXPECTED_REGISTRY_ID
                and incident_record.get(
                    "candidate_model_version"
                )
                == D15_EXPECTED_MODEL_VERSION
                and incident_record.get(
                    "candidate_system_sha256"
                )
                == D15_EXPECTED_CANDIDATE_SYSTEM_SHA256
            ),

        "threshold_identity_preserved":
            incident_record.get(
                "frozen_threshold"
            )
            == D15_FROZEN_OPERATING_THRESHOLD,

        "automatic_model_change_disabled":
            incident_record.get(
                "automatic_model_change"
            )
            is False,

        "automatic_threshold_change_disabled":
            incident_record.get(
                "automatic_threshold_change"
            )
            is False,

        "production_deployment_not_authorized":
            incident_record.get(
                "production_deployment_authorized"
            )
            is False,
    }

    return {
        "checks":
            checks,

        "missing_fields":
            missing_fields,

        "overall_pass":
            all(
                checks.values()
            ),
    }


# ============================================================
# D15.113 — CHANGE CLASSIFICATION
# ============================================================


D15_CHANGE_CLASSIFICATION = {
    "DOCUMENTATION_ONLY": {
        "model_behavior_change":
            False,

        "revalidation_required":
            False,

        "new_model_version_required":
            False,
    },

    "NON_MODEL_TECHNICAL": {
        "model_behavior_change":
            False,

        "revalidation_required":
            True,

        "new_model_version_required":
            False,
    },

    "MODEL_AFFECTING": {
        "model_behavior_change":
            True,

        "revalidation_required":
            True,

        "new_model_version_required":
            True,
    },

    "CLINICAL_USE_CHANGE": {
        "model_behavior_change":
            "POSSIBLE",

        "revalidation_required":
            True,

        "new_model_version_required":
            "REVIEW_REQUIRED",
    },
}


D15_MODEL_AFFECTING_CHANGE_TYPES = (
    "MODEL_PARAMETERS",
    "MODEL_ALGORITHM",
    "TRAINING_DATA",
    "FEATURE_SET",
    "FEATURE_ENGINEERING",
    "PREPROCESSING",
    "CALIBRATION",
    "OPERATING_THRESHOLD",
    "SUBGROUP_THRESHOLD",
)


# ============================================================
# D15.114 — CHANGE REQUEST CONTRACT
# ============================================================


def build_d15_change_request(
    *,
    change_id: str,
    change_classification: str,
    change_type: str,
    change_description: str,
    rationale: str,
    requested_by: str,
) -> dict[str, Any]:
    """
    Build a governed change request.

    Submission of a request does not authorize implementation.
    """

    if change_classification not in (
        D15_CHANGE_CLASSIFICATION
    ):
        raise ValueError(
            "Unknown D15 change classification: "
            f"{change_classification!r}"
        )

    if not change_id.strip():
        raise ValueError(
            "change_id must not be empty."
        )

    policy = (
        D15_CHANGE_CLASSIFICATION[
            change_classification
        ]
    )

    model_affecting_by_type = (
        change_type
        in D15_MODEL_AFFECTING_CHANGE_TYPES
    )

    model_affecting = bool(
        policy[
            "model_behavior_change"
        ]
        is True
        or model_affecting_by_type
    )

    revalidation_required = bool(
        policy[
            "revalidation_required"
        ]
        or model_affecting
    )

    new_version_required = bool(
        policy[
            "new_model_version_required"
        ]
        is True
        or model_affecting
    )

    return {
        "change_id":
            change_id,

        "requested_at_utc":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "change_classification":
            change_classification,

        "change_type":
            change_type,

        "change_description":
            change_description,

        "rationale":
            rationale,

        "requested_by":
            requested_by,

        "current_registry_id":
            D15_EXPECTED_REGISTRY_ID,

        "current_model_version":
            D15_EXPECTED_MODEL_VERSION,

        "current_candidate_system_sha256":
            D15_EXPECTED_CANDIDATE_SYSTEM_SHA256,

        "current_threshold":
            D15_FROZEN_OPERATING_THRESHOLD,

        "model_affecting":
            model_affecting,

        "revalidation_required":
            revalidation_required,

        "new_version_required":
            new_version_required,

        "implementation_authorized":
            False,

        "approval_status":
            "PENDING_GOVERNANCE_REVIEW",

        "automatic_implementation":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.115 — CHANGE AUTHORIZATION GATE
# ============================================================


def evaluate_d15_change_authorization(
    change_request: dict[str, Any],
    *,
    governance_approved: bool = False,
    clinical_review_completed: bool = False,
    technical_review_completed: bool = False,
    responsible_ai_review_completed: bool = False,
    revalidation_completed: bool = False,
    version_registered: bool = False,
) -> dict[str, Any]:
    """
    Evaluate whether a proposed change has sufficient evidence
    to progress.

    This function does not modify the frozen candidate.
    """

    revalidation_required = bool(
        change_request[
            "revalidation_required"
        ]
    )

    new_version_required = bool(
        change_request[
            "new_version_required"
        ]
    )

    required_checks = {
        "governance_approved":
            governance_approved,

        "clinical_review_completed":
            clinical_review_completed,

        "technical_review_completed":
            technical_review_completed,

        "responsible_ai_review_completed":
            responsible_ai_review_completed,

        "revalidation_requirement_satisfied":
            (
                revalidation_completed
                if revalidation_required
                else True
            ),

        "version_registration_requirement_satisfied":
            (
                version_registered
                if new_version_required
                else True
            ),
    }

    authorized_to_progress = all(
        required_checks.values()
    )

    return {
        "change_id":
            change_request[
                "change_id"
            ],

        "required_checks":
            required_checks,

        "authorized_to_progress":
            authorized_to_progress,

        "authorization_status":
            (
                "AUTHORIZED_TO_PROGRESS_THROUGH_CONTROLLED_CHANGE"
                if authorized_to_progress
                else
                "NOT_AUTHORIZED_TO_IMPLEMENT"
            ),

        "current_frozen_candidate_modified":
            False,

        "automatic_implementation":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.116 — ROLLBACK CONTROL
# ============================================================


D15_ROLLBACK_TRIGGERS = (
    "FROZEN_ARTIFACT_IDENTITY_FAILURE",
    "SYSTEMATIC_INVALID_INFERENCE",
    "PATIENT_SAFETY_INCIDENT",
    "UNAUTHORIZED_CHANGE",
    "CRITICAL_DATA_PIPELINE_FAILURE",
    "CRITICAL_MONITORING_ALERT",
    "SECURITY_OR_PRIVACY_INCIDENT",
)


D15_ROLLBACK_GOVERNANCE = {
    "rollback_target_must_be_authorized":
        True,

    "rollback_target_must_be_identifiable":
        True,

    "rollback_target_integrity_must_be_verified":
        True,

    "rollback_event_must_be_audited":
        True,

    "rollback_requires_post_event_review":
        True,

    "rollback_may_disable_ai_service":
        True,

    "fallback_to_standard_clinical_workflow":
        True,

    "fallback_may_generate_replacement_ai_prediction":
        False,

    "automatic_retraining_during_rollback":
        False,

    "automatic_threshold_change_during_rollback":
        False,
}


def build_d15_rollback_decision(
    *,
    trigger: str,
    rollback_target_available: bool,
    rollback_target_authorized: bool,
    rollback_target_integrity_verified: bool,
) -> dict[str, Any]:
    """
    Determine the governed rollback disposition.
    """

    if trigger not in (
        D15_ROLLBACK_TRIGGERS
    ):
        raise ValueError(
            "Unknown rollback trigger: "
            f"{trigger!r}"
        )

    safe_rollback_available = all(
        [
            rollback_target_available,
            rollback_target_authorized,
            rollback_target_integrity_verified,
        ]
    )

    if safe_rollback_available:
        disposition = (
            "CONTROLLED_ROLLBACK_ELIGIBLE"
        )

        fallback = (
            "AUTHORIZED_VERIFIED_ROLLBACK_TARGET"
        )

    else:
        disposition = (
            "AI_SERVICE_SUSPENSION_REQUIRED"
        )

        fallback = (
            "STANDARD_CLINICIAN_LED_WORKFLOW_WITHOUT_AI"
        )

    return {
        "trigger":
            trigger,

        "safe_rollback_available":
            safe_rollback_available,

        "disposition":
            disposition,

        "fallback":
            fallback,

        "replacement_prediction_generated":
            False,

        "automatic_model_change":
            False,

        "automatic_threshold_change":
            False,

        "post_event_review_required":
            True,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.117 — BUSINESS CONTINUITY MODEL
# ============================================================


D15_BUSINESS_CONTINUITY_CONTROL = {
    "ai_service_is_advisory":
        True,

    "clinical_workflow_must_continue_without_ai":
        True,

    "ai_unavailability_blocks_clinical_care":
        False,

    "fallback_workflow":
        "STANDARD_CLINICIAN_LED_DISCHARGE_AND_READMISSION_PREVENTION_WORKFLOW",

    "fallback_requires_manual_ai_score":
        False,

    "fallback_generates_synthetic_ai_score":
        False,

    "clinical_team_retains_decision_authority":
        True,

    "service_restoration_requires_integrity_validation":
        True,

    "service_restoration_requires_incident_resolution":
        True,

    "service_restoration_requires_governance_clearance_when_material":
        True,

    "downtime_must_be_logged":
        True,

    "missed_ai_predictions_must_not_be_backfilled_as_if_real_time":
        True,
}


def evaluate_d15_business_continuity(
    *,
    ai_service_available: bool,
    artifact_integrity_valid: bool,
    unresolved_critical_incident: bool,
) -> dict[str, Any]:
    """
    Resolve the safe operational workflow during AI service
    availability or failure.
    """

    ai_use_permitted = bool(
        ai_service_available
        and artifact_integrity_valid
        and not unresolved_critical_incident
    )

    if ai_use_permitted:
        workflow_status = (
            "AI_ADVISORY_SERVICE_AVAILABLE"
        )

        clinical_workflow = (
            "CLINICIAN_LED_WORKFLOW_WITH_AI_ADVISORY_SUPPORT"
        )

    else:
        workflow_status = (
            "AI_ADVISORY_SERVICE_UNAVAILABLE_OR_SUSPENDED"
        )

        clinical_workflow = (
            D15_BUSINESS_CONTINUITY_CONTROL[
                "fallback_workflow"
            ]
        )

    return {
        "ai_use_permitted":
            ai_use_permitted,

        "workflow_status":
            workflow_status,

        "clinical_workflow":
            clinical_workflow,

        "clinical_care_blocked":
            False,

        "manual_replacement_ai_score_required":
            False,

        "synthetic_replacement_prediction_generated":
            False,

        "clinical_decision_authority":
            "HUMAN_CLINICAL_TEAM",

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.118 — SERVICE RESTORATION GATE
# ============================================================


def evaluate_d15_service_restoration(
    *,
    artifact_integrity_verified: bool,
    root_cause_resolved: bool,
    corrective_action_completed: bool,
    required_revalidation_completed: bool,
    governance_clearance_completed: bool,
) -> dict[str, Any]:
    """
    Determine whether an interrupted AI advisory service is
    eligible for controlled restoration.
    """

    checks = {
        "artifact_integrity_verified":
            artifact_integrity_verified,

        "root_cause_resolved":
            root_cause_resolved,

        "corrective_action_completed":
            corrective_action_completed,

        "required_revalidation_completed":
            required_revalidation_completed,

        "governance_clearance_completed":
            governance_clearance_completed,
    }

    restoration_eligible = all(
        checks.values()
    )

    return {
        "checks":
            checks,

        "restoration_eligible":
            restoration_eligible,

        "restoration_status":
            (
                "ELIGIBLE_FOR_CONTROLLED_SERVICE_RESTORATION"
                if restoration_eligible
                else
                "SERVICE_RESTORATION_BLOCKED"
            ),

        "automatic_restoration":
            False,

        "production_deployment_authorized":
            False,
    }


# ============================================================
# D15.119 — VALIDATE OPERATIONAL GOVERNANCE CONTROLS
# ============================================================


def validate_d15_incident_change_rollback_continuity_controls(
) -> dict[str, Any]:
    """
    Validate D15 incident, change, rollback and business-
    continuity governance using deterministic control cases.
    """

    incident = (
        build_d15_incident_record(
            incident_id="D15-SYNTHETIC-INCIDENT-001",
            severity="SEV1",
            incident_type=(
                "FROZEN_ARTIFACT_IDENTITY_FAILURE"
            ),
            detection_source=(
                "D15_CONTROL_VALIDATION"
            ),
            affected_component=(
                "FROZEN_MODEL_ARTIFACT"
            ),
            clinical_safety_relevance=True,
            affected_population=(
                "SYNTHETIC_CONTROL_SCENARIO"
            ),
            immediate_containment=(
                "BLOCK_AI_INFERENCE"
            ),
            ai_service_status=(
                "SUSPENDED"
            ),
            human_workflow_status=(
                "STANDARD_CLINICIAN_LED_WORKFLOW_ACTIVE"
            ),
            governance_owner=(
                "MODEL_GOVERNANCE"
            ),
        )
    )

    incident_validation = (
        validate_d15_incident_record(
            incident
        )
    )

    change_request = (
        build_d15_change_request(
            change_id="D15-SYNTHETIC-CHANGE-001",
            change_classification=(
                "MODEL_AFFECTING"
            ),
            change_type=(
                "OPERATING_THRESHOLD"
            ),
            change_description=(
                "Synthetic threshold-change governance test."
            ),
            rationale=(
                "CONTROL_VALIDATION_ONLY"
            ),
            requested_by=(
                "D15_CONTROL_VALIDATION"
            ),
        )
    )

    unauthorized_change = (
        evaluate_d15_change_authorization(
            change_request
        )
    )

    authorized_change_path = (
        evaluate_d15_change_authorization(
            change_request,
            governance_approved=True,
            clinical_review_completed=True,
            technical_review_completed=True,
            responsible_ai_review_completed=True,
            revalidation_completed=True,
            version_registered=True,
        )
    )

    rollback_without_safe_target = (
        build_d15_rollback_decision(
            trigger=(
                "FROZEN_ARTIFACT_IDENTITY_FAILURE"
            ),
            rollback_target_available=False,
            rollback_target_authorized=False,
            rollback_target_integrity_verified=False,
        )
    )

    rollback_with_safe_target = (
        build_d15_rollback_decision(
            trigger=(
                "FROZEN_ARTIFACT_IDENTITY_FAILURE"
            ),
            rollback_target_available=True,
            rollback_target_authorized=True,
            rollback_target_integrity_verified=True,
        )
    )

    continuity_failure = (
        evaluate_d15_business_continuity(
            ai_service_available=False,
            artifact_integrity_valid=False,
            unresolved_critical_incident=True,
        )
    )

    continuity_normal = (
        evaluate_d15_business_continuity(
            ai_service_available=True,
            artifact_integrity_valid=True,
            unresolved_critical_incident=False,
        )
    )

    restoration_blocked = (
        evaluate_d15_service_restoration(
            artifact_integrity_verified=True,
            root_cause_resolved=False,
            corrective_action_completed=False,
            required_revalidation_completed=False,
            governance_clearance_completed=False,
        )
    )

    restoration_eligible = (
        evaluate_d15_service_restoration(
            artifact_integrity_verified=True,
            root_cause_resolved=True,
            corrective_action_completed=True,
            required_revalidation_completed=True,
            governance_clearance_completed=True,
        )
    )

    checks = {
        "sev1_incident_record_valid":
            incident_validation[
                "overall_pass"
            ],

        "sev1_requires_revalidation":
            incident[
                "revalidation_required"
            ]
            is True,

        "model_affecting_change_requires_revalidation":
            change_request[
                "revalidation_required"
            ]
            is True,

        "model_affecting_change_requires_new_version":
            change_request[
                "new_version_required"
            ]
            is True,

        "unapproved_change_is_blocked":
            unauthorized_change[
                "authorized_to_progress"
            ]
            is False,

        "fully_reviewed_change_can_progress_controlled_path":
            authorized_change_path[
                "authorized_to_progress"
            ]
            is True,

        "safe_rollback_requires_verified_authorized_target":
            rollback_with_safe_target[
                "disposition"
            ]
            == "CONTROLLED_ROLLBACK_ELIGIBLE",

        "unsafe_rollback_target_causes_ai_suspension":
            rollback_without_safe_target[
                "disposition"
            ]
            == "AI_SERVICE_SUSPENSION_REQUIRED",

        "ai_failure_does_not_block_clinical_care":
            continuity_failure[
                "clinical_care_blocked"
            ]
            is False,

        "ai_failure_falls_back_to_human_workflow":
            continuity_failure[
                "clinical_decision_authority"
            ]
            == "HUMAN_CLINICAL_TEAM",

        "ai_failure_generates_no_replacement_prediction":
            continuity_failure[
                "synthetic_replacement_prediction_generated"
            ]
            is False,

        "healthy_service_supports_advisory_workflow":
            continuity_normal[
                "workflow_status"
            ]
            == "AI_ADVISORY_SERVICE_AVAILABLE",

        "incomplete_remediation_blocks_restoration":
            restoration_blocked[
                "restoration_eligible"
            ]
            is False,

        "complete_remediation_can_be_restoration_eligible":
            restoration_eligible[
                "restoration_eligible"
            ]
            is True,

        "restoration_is_not_automatic":
            restoration_eligible[
                "automatic_restoration"
            ]
            is False,

        "rollback_does_not_auto_retrain":
            rollback_with_safe_target[
                "automatic_model_change"
            ]
            is False,

        "rollback_does_not_change_threshold":
            rollback_with_safe_target[
                "automatic_threshold_change"
            ]
            is False,

        "production_deployment_not_authorized":
            D15_PRODUCTION_DEPLOYMENT_AUTHORIZED
            is False,
    }

    overall_pass = all(
        checks.values()
    )

    return {
        "stage_id":
            D15_STAGE_ID,

        "control_classification":
            "INCIDENT_CHANGE_ROLLBACK_AND_BUSINESS_CONTINUITY",

        "synthetic_incident":
            incident,

        "synthetic_change_request":
            change_request,

        "unauthorized_change":
            unauthorized_change,

        "authorized_change_path":
            authorized_change_path,

        "rollback_without_safe_target":
            rollback_without_safe_target,

        "rollback_with_safe_target":
            rollback_with_safe_target,

        "continuity_failure":
            continuity_failure,

        "continuity_normal":
            continuity_normal,

        "restoration_blocked":
            restoration_blocked,

        "restoration_eligible":
            restoration_eligible,

        "checks":
            checks,

        "overall_pass":
            overall_pass,

        "validation_status":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "production_deployment_authorized":
            False,

        "next_controlled_action":
            (
                "D15_OPERATIONAL_GOVERNANCE_TESTING"
                if overall_pass
                else
                "STOP_AND_REMEDIATE_OPERATIONAL_CONTROLS"
            ),
    }


def print_d15_incident_change_rollback_continuity_controls(
) -> None:
    """
    Print operational-governance control evidence.
    """

    evidence = (
        validate_d15_incident_change_rollback_continuity_controls()
    )

    print(
        "=" * 112
    )

    print(
        "D15 — DEPLOYMENT & MONITORING DESIGN"
    )

    print(
        "INCIDENT, CHANGE, ROLLBACK & BUSINESS CONTINUITY"
    )

    print(
        "=" * 112
    )

    print()

    print(
        "Synthetic control scenarios"
    )

    print(
        "-" * 112
    )

    print(
        f"SEV1 incident valid:            "
        f"{evidence['checks']['sev1_incident_record_valid']}"
    )

    print(
        f"Unapproved model change:        "
        f"{evidence['unauthorized_change']['authorization_status']}"
    )

    print(
        f"Fully controlled change path:   "
        f"{evidence['authorized_change_path']['authorization_status']}"
    )

    print(
        f"No safe rollback target:        "
        f"{evidence['rollback_without_safe_target']['disposition']}"
    )

    print(
        f"Verified rollback target:       "
        f"{evidence['rollback_with_safe_target']['disposition']}"
    )

    print(
        f"AI failure workflow:            "
        f"{evidence['continuity_failure']['clinical_workflow']}"
    )

    print(
        f"Incomplete restoration:         "
        f"{evidence['restoration_blocked']['restoration_status']}"
    )

    print(
        f"Complete restoration evidence:  "
        f"{evidence['restoration_eligible']['restoration_status']}"
    )

    print()

    print(
        "Governance validation"
    )

    print(
        "-" * 112
    )

    for (
        check_name,
        passed,
    ) in evidence[
        "checks"
    ].items():

        print(
            f"{check_name:<78}"
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    print(
        "-" * 112
    )

    print(
        f"OPERATIONAL CONTROL STATUS:      "
        f"{evidence['validation_status']}"
    )

    print(
        f"NEXT CONTROLLED ACTION:          "
        f"{evidence['next_controlled_action']}"
    )

    print(
        f"PRODUCTION DEPLOYMENT AUTHORIZED: "
        f"{evidence['production_deployment_authorized']}"
    )

    print(
        "=" * 112
    )

# ============================================================
