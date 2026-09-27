"""
ReadmitAI Clinical Intelligence
D15 Monitoring Evidence Service

Purpose
-------
Expose authoritative D15 deployment-and-monitoring design evidence
to the ReadmitAI Monitoring Command Center.

Governance principles
---------------------
- Reads persisted D15 governance artifacts.
- Does not create production telemetry.
- Does not infer current production health.
- Does not treat historical reference bands as acceptance limits.
- Does not retrain the model or retune the frozen threshold.
- Preserves NOT ASSESSABLE states where operational/outcome evidence
  does not exist.
"""

from pathlib import Path
from typing import Any

import ast
import pandas as pd
import yaml


# ============================================================
# PROJECT & AUTHORITATIVE D15 PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "manifests"
    / "D15_deployment_monitoring_manifest.yaml"
)

MONITORING_CONTROLS_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D15_monitoring_control_catalogue.csv"
)

REFERENCE_BANDS_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D15_quantitative_reference_bands.csv"
)

ESCALATION_TRIGGERS_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "D15_escalation_trigger_catalogue.csv"
)


# ============================================================
# FROZEN CANDIDATE CONTRACT
# ============================================================

EXPECTED_REGISTRY_ID = "DIABETES_READMISSION_XGB_D13_V1"
EXPECTED_MODEL_VERSION = "1.0.0"
EXPECTED_THRESHOLD = 0.12

EXPECTED_CANDIDATE_SHA256 = (
    "9349A52C715517666540C0D5B1EDB148"
    "D48709C0FC2CC77BE9B53F10FE373679"
)

EXPECTED_MONITORING_CONTROL_COUNT = 17
EXPECTED_ESCALATION_TRIGGER_COUNT = 17


# ============================================================
# MANIFEST
# ============================================================

def load_d15_manifest() -> dict[str, Any]:
    """Load and validate the authoritative D15 manifest."""

    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            f"D15 manifest not found: {MANIFEST_PATH}"
        )

    with MANIFEST_PATH.open("r", encoding="utf-8") as file:
        manifest = yaml.safe_load(file)

    if not isinstance(manifest, dict):
        raise RuntimeError(
            "D15 manifest did not load as a dictionary."
        )

    required_fields = (
        "stage_id",
        "stage_name",
        "next_stage",
        "registry_id",
        "model_version",
        "candidate_system_sha256",
        "frozen_operating_threshold",
        "external_validation_established",
        "clinical_effectiveness_established",
        "production_deployment_authorized",
        "residual_risk_count",
        "gate_decision",
        "artifacts",
    )

    missing = [
        field
        for field in required_fields
        if field not in manifest
    ]

    if missing:
        raise RuntimeError(
            "D15 manifest is missing required fields: "
            + ", ".join(missing)
        )

    if manifest["stage_id"] != "D15":
        raise RuntimeError(
            "Unexpected lifecycle stage in D15 manifest."
        )

    if manifest["registry_id"] != EXPECTED_REGISTRY_ID:
        raise RuntimeError(
            "D15 registry identity does not match frozen candidate."
        )

    if str(manifest["model_version"]) != EXPECTED_MODEL_VERSION:
        raise RuntimeError(
            "D15 model version does not match frozen candidate."
        )

    if (
        manifest["candidate_system_sha256"]
        != EXPECTED_CANDIDATE_SHA256
    ):
        raise RuntimeError(
            "D15 candidate-system hash does not match frozen candidate."
        )

    threshold = float(
        manifest["frozen_operating_threshold"]
    )

    if abs(threshold - EXPECTED_THRESHOLD) > 1e-12:
        raise RuntimeError(
            "D15 frozen operating threshold does not match "
            "the governed threshold."
        )

    return manifest


# ============================================================
# MONITORING CONTROL CATALOGUE
# ============================================================

def load_d15_monitoring_controls() -> pd.DataFrame:
    """Load and validate the 17-control D15 monitoring catalogue."""

    if not MONITORING_CONTROLS_PATH.exists():
        raise FileNotFoundError(
            "D15 monitoring control catalogue not found: "
            f"{MONITORING_CONTROLS_PATH}"
        )

    df = pd.read_csv(MONITORING_CONTROLS_PATH)

    required_columns = {
        "control_id",
        "domain",
        "control_name",
        "signal",
        "reference_type",
        "cadence",
        "d14_risk_ids",
        "governance_action",
        "production_deployment_authorized",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise RuntimeError(
            "D15 monitoring catalogue is missing columns: "
            + ", ".join(sorted(missing))
        )

    if len(df) != EXPECTED_MONITORING_CONTROL_COUNT:
        raise RuntimeError(
            "Expected "
            f"{EXPECTED_MONITORING_CONTROL_COUNT} D15 monitoring controls, "
            f"found {len(df)}."
        )

    if df["control_id"].duplicated().any():
        raise RuntimeError(
            "Duplicate D15 monitoring control IDs detected."
        )

    expected_ids = {
        f"D15-MON-{index:03d}"
        for index in range(
            1,
            EXPECTED_MONITORING_CONTROL_COUNT + 1,
        )
    }

    observed_ids = set(
        df["control_id"].astype(str)
    )

    if observed_ids != expected_ids:
        raise RuntimeError(
            "D15 monitoring control identity set is incomplete "
            "or unexpected."
        )

    return df


# ============================================================
# QUANTITATIVE REFERENCE BANDS
# ============================================================

def load_d15_reference_bands() -> pd.DataFrame:
    """
    Load D15 internal historical surveillance reference bands.

    These are surveillance references only. They are NOT production
    acceptance limits or clinical acceptability limits.
    """

    if not REFERENCE_BANDS_PATH.exists():
        raise FileNotFoundError(
            "D15 quantitative reference bands not found: "
            f"{REFERENCE_BANDS_PATH}"
        )

    df = pd.read_csv(REFERENCE_BANDS_PATH)

    required_columns = {
        "metric",
        "events",
        "denominator",
        "observed_rate",
        "confidence_level",
        "lower_bound",
        "upper_bound",
        "reference_classification",
        "production_acceptance_limit",
        "clinical_acceptability_limit",
        "external_validation_established",
        "clinical_effectiveness_established",
        "production_deployment_authorized",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise RuntimeError(
            "D15 reference-band artifact is missing columns: "
            + ", ".join(sorted(missing))
        )

    if df.empty:
        raise RuntimeError(
            "D15 quantitative reference-band artifact is empty."
        )

    return df


# ============================================================
# ESCALATION TRIGGER CATALOGUE
# ============================================================

def load_d15_escalation_triggers() -> pd.DataFrame:
    """Load and validate the D15 escalation trigger catalogue."""

    if not ESCALATION_TRIGGERS_PATH.exists():
        raise FileNotFoundError(
            "D15 escalation trigger catalogue not found: "
            f"{ESCALATION_TRIGGERS_PATH}"
        )

    df = pd.read_csv(ESCALATION_TRIGGERS_PATH)

    required_columns = {
        "trigger_id",
        "domain",
        "trigger_type",
        "condition",
        "status",
        "action",
        "production_deployment_authorized",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise RuntimeError(
            "D15 escalation trigger catalogue is missing columns: "
            + ", ".join(sorted(missing))
        )

    if len(df) != EXPECTED_ESCALATION_TRIGGER_COUNT:
        raise RuntimeError(
            "Expected "
            f"{EXPECTED_ESCALATION_TRIGGER_COUNT} D15 escalation triggers, "
            f"found {len(df)}."
        )

    if df["trigger_id"].duplicated().any():
        raise RuntimeError(
            "Duplicate D15 escalation trigger IDs detected."
        )

    expected_ids = {
        f"D15-ESC-{index:03d}"
        for index in range(
            1,
            EXPECTED_ESCALATION_TRIGGER_COUNT + 1,
        )
    }

    observed_ids = set(
        df["trigger_id"].astype(str)
    )

    if observed_ids != expected_ids:
        raise RuntimeError(
            "D15 escalation trigger identity set is incomplete "
            "or unexpected."
        )

    allowed_statuses = {
        "CRITICAL",
        "ALERT",
        "WATCH",
        "NOT_ASSESSABLE",
    }

    observed_statuses = set(
        df["status"].astype(str)
    )

    unexpected_statuses = (
        observed_statuses - allowed_statuses
    )

    if unexpected_statuses:
        raise RuntimeError(
            "Unexpected D15 escalation states: "
            + ", ".join(sorted(unexpected_statuses))
        )

    return df


# ============================================================
# D14 RISK-ID PARSING
# ============================================================

def _parse_risk_ids(value: Any) -> list[str]:
    """Safely parse persisted D14 risk-ID lists."""

    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text or text == "[]":
        return []

    try:
        parsed = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return [text]

    if isinstance(parsed, list):
        return [str(item) for item in parsed]

    return [str(parsed)]


# ============================================================
# APPLICATION-READY MONITORING EVIDENCE
# ============================================================

def get_monitoring_evidence() -> dict[str, Any]:
    """
    Return authoritative application-ready D15 monitoring evidence.

    This function does NOT create or infer live monitoring observations.
    """

    manifest = load_d15_manifest()
    controls_df = load_d15_monitoring_controls()
    reference_df = load_d15_reference_bands()
    triggers_df = load_d15_escalation_triggers()

    controls = []

    for _, row in controls_df.iterrows():
        controls.append(
            {
                "control_id": str(row["control_id"]),
                "domain": str(row["domain"]),
                "control_name": str(row["control_name"]),
                "signal": str(row["signal"]),
                "reference_type": str(row["reference_type"]),
                "cadence": str(row["cadence"]),
                "d14_risk_ids": _parse_risk_ids(
                    row["d14_risk_ids"]
                ),
                "governance_action": str(
                    row["governance_action"]
                ),
                "production_deployment_authorized": bool(
                    row["production_deployment_authorized"]
                ),
            }
        )

    reference_bands = []

    for _, row in reference_df.iterrows():
        reference_bands.append(
            {
                "metric": str(row["metric"]),
                "events": int(row["events"]),
                "denominator": int(row["denominator"]),
                "observed_rate": float(
                    row["observed_rate"]
                ),
                "confidence_level": float(
                    row["confidence_level"]
                ),
                "lower_bound": float(
                    row["lower_bound"]
                ),
                "upper_bound": float(
                    row["upper_bound"]
                ),
                "reference_classification": str(
                    row["reference_classification"]
                ),
                "production_acceptance_limit": bool(
                    row["production_acceptance_limit"]
                ),
                "clinical_acceptability_limit": bool(
                    row["clinical_acceptability_limit"]
                ),
                "external_validation_established": bool(
                    row["external_validation_established"]
                ),
                "clinical_effectiveness_established": bool(
                    row["clinical_effectiveness_established"]
                ),
                "production_deployment_authorized": bool(
                    row["production_deployment_authorized"]
                ),
            }
        )

    triggers = []

    for _, row in triggers_df.iterrows():
        triggers.append(
            {
                "trigger_id": str(row["trigger_id"]),
                "domain": str(row["domain"]),
                "trigger_type": str(row["trigger_type"]),
                "condition": str(row["condition"]),
                "status": str(row["status"]),
                "action": str(row["action"]),
                "production_deployment_authorized": bool(
                    row["production_deployment_authorized"]
                ),
            }
        )

    status_counts = (
        triggers_df["status"]
        .astype(str)
        .value_counts()
        .to_dict()
    )

    reference_classes = sorted(
        reference_df[
            "reference_classification"
        ]
        .astype(str)
        .unique()
        .tolist()
    )

    return {
        # ----------------------------------------------------
        # Lifecycle identity
        # ----------------------------------------------------
        "stage_id":
            str(manifest["stage_id"]),

        "stage_name":
            str(manifest["stage_name"]),

        "next_stage":
            str(manifest["next_stage"]),

        "registry_id":
            str(manifest["registry_id"]),

        "model_version":
            str(manifest["model_version"]),

        "candidate_system_sha256":
            str(manifest["candidate_system_sha256"]),

        "frozen_operating_threshold":
            float(manifest["frozen_operating_threshold"]),

        # ----------------------------------------------------
        # Governance status
        # ----------------------------------------------------
        "external_validation_established":
            bool(manifest["external_validation_established"]),

        "clinical_effectiveness_established":
            bool(manifest["clinical_effectiveness_established"]),

        "production_deployment_authorized":
            bool(manifest["production_deployment_authorized"]),

        "residual_risk_count":
            int(manifest["residual_risk_count"]),

        "gate_decision":
            str(manifest["gate_decision"]),

        # ----------------------------------------------------
        # D15 monitoring architecture
        # ----------------------------------------------------
        "monitoring_control_count":
            len(controls),

        "monitoring_controls":
            controls,

        "reference_band_count":
            len(reference_bands),

        "reference_bands":
            reference_bands,

        "reference_classifications":
            reference_classes,

        "escalation_trigger_count":
            len(triggers),

        "escalation_triggers":
            triggers,

        "escalation_status_counts":
            {
                "CRITICAL": int(
                    status_counts.get("CRITICAL", 0)
                ),
                "ALERT": int(
                    status_counts.get("ALERT", 0)
                ),
                "WATCH": int(
                    status_counts.get("WATCH", 0)
                ),
                "NOT_ASSESSABLE": int(
                    status_counts.get(
                        "NOT_ASSESSABLE",
                        0,
                    )
                ),
            },

        # ----------------------------------------------------
        # Evidence provenance
        # ----------------------------------------------------
        "manifest_source":
            "D15_deployment_monitoring_manifest.yaml",

        "monitoring_control_source":
            "D15_monitoring_control_catalogue.csv",

        "reference_band_source":
            "D15_quantitative_reference_bands.csv",

        "escalation_trigger_source":
            "D15_escalation_trigger_catalogue.csv",

        # ----------------------------------------------------
        # Explicit runtime boundaries
        # ----------------------------------------------------
        "live_production_telemetry_available":
            False,

        "current_production_health_assessed":
            False,

        "runtime_monitoring_metrics_recomputed":
            False,

        "simulation_required_for_ui_demonstration":
            True,

        "reference_bands_are_production_acceptance_limits":
            False,

        "reference_bands_are_clinical_acceptability_limits":
            False,
    }