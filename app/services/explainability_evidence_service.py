"""
ReadmitAI Clinical Intelligence
D12 Explainability Evidence Service

Purpose
-------
Expose persisted, validated D12 global explainability evidence
to the ReadmitAI application.

Governance principles
---------------------
- Reads the authoritative D12 explainability manifest.
- Does not recompute SHAP attribution.
- Does not retrain the model.
- Does not refit preprocessing.
- Does not alter the operating threshold.
- Does not infer causality from attribution.
- Preserves D12 lifecycle and validation limitations.
"""

from pathlib import Path
from typing import Any

import yaml


# ============================================================
# AUTHORITATIVE D12 EVIDENCE SOURCE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

D12_MANIFEST_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "manifests"
    / "D12_explainability_model_interpretation_manifest.yaml"
)


# ============================================================
# GOVERNED D12 PRIOR-UTILIZATION FAMILY
# ============================================================

D12_PRIOR_UTILIZATION_FAMILY = (
    "prior_outpatient_use",
    "prior_emergency_use",
    "prior_inpatient_use",
    "prior_utilization_intensity",
    "prior_utilization_domain_count",
)


# ============================================================
# REQUIRED MANIFEST FIELDS
# ============================================================

REQUIRED_D12_FIELDS = (
    "validation_encounters",
    "validation_positives",
    "validation_negatives",
    "transformed_feature_count",
    "source_feature_family_count",
    "prior_utilization_absolute_attribution_percent",
    "local_explanation_case_count",
    "attribution_stability_slice_count",
    "adequate_support_slice_count",
    "low_support_slice_count",
    "clinical_plausibility_review_item_count",
    "d11_carry_forward_resolution_count",
    "explainability_limitation_count",
    "disposition",
    "progression_authorized",
    "next_lifecycle_stage",
    "clinical_appropriateness_established",
    "fairness_established",
    "causality_established",
    "external_validation_established",
)


# ============================================================
# LOAD AUTHORITATIVE D12 MANIFEST
# ============================================================

def load_d12_explainability_manifest() -> dict[str, Any]:
    """
    Load and validate the persisted D12 explainability manifest.

    The manifest is treated as the authoritative persisted source
    for validated global explainability evidence.
    """

    if not D12_MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "Authoritative D12 explainability manifest not found: "
            f"{D12_MANIFEST_PATH}"
        )

    with D12_MANIFEST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        manifest = yaml.safe_load(file)

    if not isinstance(manifest, dict):
        raise RuntimeError(
            "D12 explainability manifest did not load as a dictionary."
        )

    missing_fields = [
        field
        for field in REQUIRED_D12_FIELDS
        if field not in manifest
    ]

    if missing_fields:
        raise RuntimeError(
            "D12 explainability manifest is missing required fields: "
            + ", ".join(missing_fields)
        )

    return manifest


# ============================================================
# GLOBAL EXPLAINABILITY CONTEXT
# ============================================================

def get_global_explainability_context() -> dict[str, Any]:
    """
    Return application-ready global explainability evidence.

    No global SHAP analysis is recomputed at application runtime.
    Values originate from the persisted D12 validation manifest.
    """

    manifest = load_d12_explainability_manifest()

    utilization_attribution_percent = float(
        manifest[
            "prior_utilization_absolute_attribution_percent"
        ]
    )

    if not (
        0.0
        <= utilization_attribution_percent
        <= 100.0
    ):
        raise RuntimeError(
            "Invalid D12 prior-utilization attribution percentage: "
            f"{utilization_attribution_percent}"
        )

    transformed_feature_count = int(
        manifest["transformed_feature_count"]
    )

    source_feature_family_count = int(
        manifest["source_feature_family_count"]
    )

    if transformed_feature_count != 49:
        raise RuntimeError(
            "Unexpected D12 transformed feature count. "
            f"Expected=49, Observed={transformed_feature_count}"
        )

    if source_feature_family_count != 10:
        raise RuntimeError(
            "Unexpected D12 source-feature-family count. "
            f"Expected=10, Observed={source_feature_family_count}"
        )

    return {
        "prior_utilization_absolute_attribution_percent":
            utilization_attribution_percent,

        "prior_utilization_family":
            list(D12_PRIOR_UTILIZATION_FAMILY),

        "validation_encounters":
            int(
                manifest[
                    "validation_encounters"
                ]
            ),

        "validation_positives":
            int(
                manifest[
                    "validation_positives"
                ]
            ),

        "validation_negatives":
            int(
                manifest[
                    "validation_negatives"
                ]
            ),

        "transformed_feature_count":
            transformed_feature_count,

        "source_feature_family_count":
            source_feature_family_count,

        "local_explanation_case_count":
            int(
                manifest[
                    "local_explanation_case_count"
                ]
            ),

        "attribution_stability_slice_count":
            int(
                manifest[
                    "attribution_stability_slice_count"
                ]
            ),

        "adequate_support_slice_count":
            int(
                manifest[
                    "adequate_support_slice_count"
                ]
            ),

        "low_support_slice_count":
            int(
                manifest[
                    "low_support_slice_count"
                ]
            ),

        "clinical_plausibility_review_item_count":
            int(
                manifest[
                    "clinical_plausibility_review_item_count"
                ]
            ),

        "d11_carry_forward_resolution_count":
            int(
                manifest[
                    "d11_carry_forward_resolution_count"
                ]
            ),

        "explainability_limitation_count":
            int(
                manifest[
                    "explainability_limitation_count"
                ]
            ),

        "disposition":
            str(
                manifest[
                    "disposition"
                ]
            ),

        "progression_authorized":
            bool(
                manifest[
                    "progression_authorized"
                ]
            ),

        "next_lifecycle_stage":
            str(
                manifest[
                    "next_lifecycle_stage"
                ]
            ),

        "clinical_appropriateness_established":
            bool(
                manifest[
                    "clinical_appropriateness_established"
                ]
            ),

        "fairness_established":
            bool(
                manifest[
                    "fairness_established"
                ]
            ),

        "causality_established":
            bool(
                manifest[
                    "causality_established"
                ]
            ),

        "external_validation_established":
            bool(
                manifest[
                    "external_validation_established"
                ]
            ),

        "evidence_source":
            "D12_explainability_model_interpretation_manifest.yaml",

        "runtime_global_shap_recomputed":
            False,
    }