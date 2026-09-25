# ============================================================
# D13 — MODEL REGISTRY & ARTIFACT FREEZE REPORTING
# ============================================================
# Purpose:
#   Persist the validated D13 registry evidence as reproducible,
#   reviewable governance artifacts without accessing the locked TEST
#   partition or changing the frozen predictive system.
# ============================================================

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from src.models import registry as d13


# ============================================================
# D13.R00 — REPORTING PATHS
# ============================================================

D13_REGISTRY_DIRECTORY = Path("artifacts") / "registry"
D13_MANIFEST_DIRECTORY = Path("artifacts") / "manifests"
D13_GOVERNANCE_DIRECTORY = Path("reports") / "governance"
D13_TABLE_DIRECTORY = Path("reports") / "tables"

D13_REGISTRY_RECORD_PATH = (
    D13_REGISTRY_DIRECTORY / "D13_registered_candidate.json"
)
D13_FREEZE_MANIFEST_PATH = (
    D13_MANIFEST_DIRECTORY / "D13_model_registry_freeze_manifest.json"
)
D13_CONTRACT_PATH = (
    D13_GOVERNANCE_DIRECTORY / "D13_model_registry_contract.md"
)
D13_GATE_DECISION_PATH = (
    D13_GOVERNANCE_DIRECTORY / "D13_model_registry_gate_decision.md"
)
D13_REGISTERED_CANDIDATE_TABLE_PATH = (
    D13_TABLE_DIRECTORY / "D13_registered_candidate.csv"
)
D13_ARTIFACT_INVENTORY_PATH = (
    D13_TABLE_DIRECTORY / "D13_artifact_inventory.csv"
)
D13_SOFTWARE_ENVIRONMENT_PATH = (
    D13_TABLE_DIRECTORY / "D13_software_environment.csv"
)
D13_FEATURE_CONTRACT_PATH = (
    D13_TABLE_DIRECTORY / "D13_feature_contract.csv"
)
D13_CHANGE_CONTROL_PATH = (
    D13_TABLE_DIRECTORY / "D13_change_control_record.csv"
)
D13_LIFECYCLE_PROVENANCE_PATH = (
    D13_TABLE_DIRECTORY / "D13_lifecycle_provenance.csv"
)


# ============================================================
# D13.R01 — SAFE FILE WRITERS
# ============================================================

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _ensure_parent(path)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> None:
    _ensure_parent(path)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(path: Path, content: str) -> None:
    _ensure_parent(path)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


# ============================================================
# D13.R02 — REPORTING EVIDENCE BUNDLE
# ============================================================

def build_d13_reporting_bundle() -> dict[str, Any]:
    system = d13.validate_d13_final_registered_candidate_identity()
    feature_contract = d13.validate_d13_source_feature_contract()
    environment = d13.validate_d13_software_environment_provenance()
    registry_bundle = d13.validate_d13_registry_evidence_bundle()
    registry_record = d13.build_d13_formal_registry_record()
    freeze_manifest = d13.build_d13_freeze_manifest()
    gate = d13.build_d13_registry_gate_decision()

    statuses = {
        "system_identity": system["final_validation_status"],
        "feature_contract": feature_contract["validation_status"],
        "software_environment": environment["validation_status"],
        "registry_evidence": registry_bundle["validation_status"],
        "gate": gate["validation_status"],
    }
    failed = [name for name, status in statuses.items() if status != "PASS"]

    return {
        "validation_status": "PASS" if not failed else "FAIL",
        "failed_components": failed,
        "system_identity": system,
        "feature_contract": feature_contract,
        "software_environment": environment,
        "registry_bundle": registry_bundle,
        "registry_record": registry_record,
        "freeze_manifest": freeze_manifest,
        "gate_decision": gate,
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }


def validate_d13_reporting_bundle(
    bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if bundle is None:
        bundle = build_d13_reporting_bundle()

    gate = bundle["gate_decision"]
    system = bundle["system_identity"]

    checks = {
        "runtime_components_pass":
            bundle["validation_status"] == "PASS",
        "candidate_fingerprint_consistent":
            gate["candidate_system_sha256"]
            == system["candidate_system_sha256"],
        "progression_is_d14_only":
            gate["gate_disposition"]
            == "PASS_PROGRESS_TO_D14_LOCKED_TEST_EVALUATION",
        "locked_test_not_accessed":
            bundle["locked_test_accessed"] is False,
        "locked_test_not_evaluated":
            bundle["locked_test_evaluated"] is False,
        "deployment_not_authorized":
            bundle["deployment_authorized"] is False,
    }
    failed = [key for key, passed in checks.items() if not passed]

    return {
        **bundle,
        "reporting_checks": checks,
        "reporting_failed_checks": failed,
        "reporting_validation_status": "PASS" if not failed else "FAIL",
    }


# ============================================================
# D13.R03 — TABULAR EVIDENCE BUILDERS
# ============================================================

def build_d13_registered_candidate_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    system = bundle["system_identity"]
    environment = bundle["software_environment"]
    manifest = bundle["freeze_manifest"]
    gate = bundle["gate_decision"]

    return [{
        "registry_id": system["registry_id"],
        "model_version": system["model_version"],
        "candidate_status": system["candidate_status"],
        "source_lifecycle_stage": system["source_lifecycle_stage"],
        "source_git_commit": system["source_git_commit"],
        "model_name": system["model_name"],
        "model_sha256": system["model_sha256"],
        "model_metadata_sha256": system["model_metadata_sha256"],
        "preprocessor_sha256": system["preprocessor_sha256"],
        "transformed_feature_schema_sha256":
            system["transformed_feature_schema_sha256"],
        "source_feature_contract_sha256":
            system["source_feature_contract_sha256"],
        "development_operating_threshold":
            system["development_operating_threshold"],
        "source_feature_count": system["source_feature_count"],
        "transformed_feature_count": system["transformed_feature_count"],
        "candidate_system_sha256": system["candidate_system_sha256"],
        "software_environment_sha256":
            environment["software_environment_sha256"],
        "freeze_manifest_sha256": manifest["freeze_manifest_sha256"],
        "gate_disposition": gate["gate_disposition"],
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }]


def build_d13_artifact_inventory_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    return list(bundle["registry_bundle"]["artifact_inventory"])


def build_d13_software_environment_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    environment = bundle["software_environment"]["software_environment"]
    return [
        {"component": key, "version_or_value": value}
        for key, value in environment.items()
    ]


def build_d13_feature_contract_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    feature = bundle["feature_contract"]
    categorical = set(feature["categorical_features"])
    numeric = set(feature["numeric_features"])
    rows = []
    for position, name in enumerate(
        feature["primary_candidate_features"],
        start=1,
    ):
        feature_type = (
            "categorical" if name in categorical
            else "numeric" if name in numeric
            else "unclassified"
        )
        rows.append({
            "position": position,
            "feature_name": name,
            "feature_type": feature_type,
            "authorized_for_primary_pathway": True,
            "source_feature_contract_sha256":
                feature["source_feature_contract_sha256"],
        })
    return rows


def build_d13_change_control_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    change = bundle["registry_bundle"]["change_control_status"]
    return [
        {"control": key, "value": value}
        for key, value in change.items()
    ]


def build_d13_lifecycle_provenance_rows(
    bundle: dict[str, Any],
) -> list[dict[str, Any]]:
    provenance = bundle["registry_bundle"]["lifecycle_provenance"]
    return [
        {"stage_or_reference": key, "provenance": value}
        for key, value in provenance.items()
    ]


# ============================================================
# D13.R04 — GOVERNANCE DOCUMENT BUILDERS
# ============================================================

def build_d13_registry_contract_markdown(
    bundle: dict[str, Any],
) -> str:
    system = bundle["system_identity"]
    environment = bundle["software_environment"]
    manifest = bundle["freeze_manifest"]

    return f"""# D13 Model Registry & Artifact Freeze — Governance Contract

## 1. Purpose

D13 creates the traceable, integrity-verifiable registry record for the exact
development-stage clinical-AI candidate that completed D12. D13 does not
evaluate model performance and does not authorize clinical deployment.

## 2. Registered Candidate

- Registry ID: `{system["registry_id"]}`
- Model version: `{system["model_version"]}`
- Candidate status: `{system["candidate_status"]}`
- Source lifecycle stage: `{system["source_lifecycle_stage"]}`
- Source Git commit: `{system["source_git_commit"]}`
- Model: `{system["model_name"]}`
- Development operating threshold: `{system["development_operating_threshold"]}`

## 3. Frozen Predictive-System Identity

- Candidate system SHA-256: `{system["candidate_system_sha256"]}`
- Model SHA-256: `{system["model_sha256"]}`
- Model metadata SHA-256: `{system["model_metadata_sha256"]}`
- D7 preprocessor SHA-256: `{system["preprocessor_sha256"]}`
- Transformed schema SHA-256: `{system["transformed_feature_schema_sha256"]}`
- Source feature contract SHA-256: `{system["source_feature_contract_sha256"]}`
- Source feature count: `{system["source_feature_count"]}`
- Transformed feature count: `{system["transformed_feature_count"]}`

## 4. Reproducibility Provenance

- Software environment SHA-256: `{environment["software_environment_sha256"]}`
- Freeze manifest SHA-256: `{manifest["freeze_manifest_sha256"]}`

The software-environment fingerprint is maintained as reproducibility
provenance and is not used to redefine the frozen predictive-system
fingerprint.

## 5. Change-Control Rule

Any post-freeze change to the model, model metadata, preprocessing artifact,
transformed schema, ordered source-feature contract, or development operating
threshold invalidates the registered candidate identity and requires governed
change control and a new registry identity/version as appropriate.

## 6. D13 Safety Boundary

D13 performs registry and integrity work only. It does not retrain or retune
the model, refit preprocessing, re-engineer features, recalibrate
probabilities, create subgroup-specific thresholds, generate evaluation
predictions, access or evaluate the locked TEST partition, or authorize
deployment.

## 7. Progression Rule

A PASS at D13 authorizes progression only to D14 Locked-Test Evaluation.
It is not deployment authorization.

- Locked TEST accessed in D13: **False**
- Locked TEST evaluated in D13: **False**
- Deployment authorized: **False**
"""


def build_d13_gate_decision_markdown(
    bundle: dict[str, Any],
) -> str:
    gate = bundle["gate_decision"]

    return f"""# D13 Model Registry & Artifact Freeze — Gate Decision

## Decision

**{gate["gate_disposition"]}**

## Evidence

- Validation status: `{gate["validation_status"]}`
- Registry ID: `{gate["registry_id"]}`
- Candidate system SHA-256: `{gate["candidate_system_sha256"]}`
- Freeze manifest SHA-256: `{gate["freeze_manifest_sha256"]}`
- Progression to D14 authorized: `{gate["progression_to_d14_authorized"]}`
- Locked TEST accessed: `{gate["locked_test_accessed"]}`
- Locked TEST evaluated: `{gate["locked_test_evaluated"]}`
- Deployment authorized: `{gate["deployment_authorized"]}`
- Failed checks: `{gate["failed_checks"]}`

## Governance Interpretation

The exact D12 development-stage candidate has been registered and frozen with
cryptographic identity, feature-contract binding, software provenance,
artifact inventory, lifecycle provenance, and explicit change control.

This decision authorizes one-way progression to D14 for locked TEST
evaluation under the frozen candidate identity. It does not authorize model
retraining, threshold retuning, validation-driven changes, or deployment.
"""


# ============================================================
# D13.R05 — PERSIST COMPLETE EVIDENCE PACKAGE
# ============================================================

def persist_d13_reporting_evidence() -> dict[str, Any]:
    bundle = validate_d13_reporting_bundle()
    if bundle["reporting_validation_status"] != "PASS":
        raise RuntimeError(
            "D13 reporting evidence persistence blocked because "
            f"validation failed: {bundle['reporting_failed_checks']}"
        )

    registry_record = bundle["registry_record"]
    manifest = bundle["freeze_manifest"]

    _write_json(D13_REGISTRY_RECORD_PATH, registry_record)

    manifest_for_disk = {
        "stage_id": d13.D13_STAGE_ID,
        "stage_name": d13.D13_STAGE_NAME,
        "freeze_status": manifest["freeze_status"],
        "freeze_manifest_sha256": manifest["freeze_manifest_sha256"],
        "candidate_system_sha256":
            registry_record["candidate_system_sha256"],
        "source_feature_contract_sha256":
            registry_record["source_feature_contract_sha256"],
        "software_environment_sha256":
            registry_record["software_environment_sha256"],
        "registry_record": registry_record,
        "post_freeze_change_requires_new_identity":
            manifest["post_freeze_change_requires_new_identity"],
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }
    _write_json(D13_FREEZE_MANIFEST_PATH, manifest_for_disk)

    candidate_rows = build_d13_registered_candidate_rows(bundle)
    _write_csv(
        D13_REGISTERED_CANDIDATE_TABLE_PATH,
        candidate_rows,
        list(candidate_rows[0].keys()),
    )

    artifact_rows = build_d13_artifact_inventory_rows(bundle)
    _write_csv(
        D13_ARTIFACT_INVENTORY_PATH,
        artifact_rows,
        ["component", "path", "sha256", "frozen"],
    )

    environment_rows = build_d13_software_environment_rows(bundle)
    _write_csv(
        D13_SOFTWARE_ENVIRONMENT_PATH,
        environment_rows,
        ["component", "version_or_value"],
    )

    feature_rows = build_d13_feature_contract_rows(bundle)
    _write_csv(
        D13_FEATURE_CONTRACT_PATH,
        feature_rows,
        [
            "position",
            "feature_name",
            "feature_type",
            "authorized_for_primary_pathway",
            "source_feature_contract_sha256",
        ],
    )

    change_rows = build_d13_change_control_rows(bundle)
    _write_csv(
        D13_CHANGE_CONTROL_PATH,
        change_rows,
        ["control", "value"],
    )

    lifecycle_rows = build_d13_lifecycle_provenance_rows(bundle)
    _write_csv(
        D13_LIFECYCLE_PROVENANCE_PATH,
        lifecycle_rows,
        ["stage_or_reference", "provenance"],
    )

    _write_markdown(
        D13_CONTRACT_PATH,
        build_d13_registry_contract_markdown(bundle),
    )
    _write_markdown(
        D13_GATE_DECISION_PATH,
        build_d13_gate_decision_markdown(bundle),
    )

    paths = [
        D13_REGISTRY_RECORD_PATH,
        D13_FREEZE_MANIFEST_PATH,
        D13_CONTRACT_PATH,
        D13_GATE_DECISION_PATH,
        D13_REGISTERED_CANDIDATE_TABLE_PATH,
        D13_ARTIFACT_INVENTORY_PATH,
        D13_SOFTWARE_ENVIRONMENT_PATH,
        D13_FEATURE_CONTRACT_PATH,
        D13_CHANGE_CONTROL_PATH,
        D13_LIFECYCLE_PROVENANCE_PATH,
    ]

    return {
        "validation_status": "PASS",
        "artifact_count": len(paths),
        "artifact_paths": [str(path) for path in paths],
        "registry_id": registry_record["registry_id"],
        "candidate_system_sha256":
            registry_record["candidate_system_sha256"],
        "software_environment_sha256":
            registry_record["software_environment_sha256"],
        "freeze_manifest_sha256":
            manifest["freeze_manifest_sha256"],
        "gate_disposition":
            bundle["gate_decision"]["gate_disposition"],
        "locked_test_accessed": False,
        "locked_test_evaluated": False,
        "deployment_authorized": False,
    }


# ============================================================
# D13.R06 — EXECUTABLE REPORTING CHECK
# ============================================================

def print_d13_reporting_evidence_summary() -> None:
    result = persist_d13_reporting_evidence()

    print("=" * 72)
    print("D13 MODEL REGISTRY & ARTIFACT FREEZE — PERSISTED EVIDENCE")
    print("=" * 72)
    for key in (
        "validation_status",
        "artifact_count",
        "registry_id",
        "candidate_system_sha256",
        "software_environment_sha256",
        "freeze_manifest_sha256",
        "gate_disposition",
        "locked_test_accessed",
        "locked_test_evaluated",
        "deployment_authorized",
    ):
        print(f"{key}: {result[key]}")

    print("artifact_paths:")
    for path in result["artifact_paths"]:
        print(f"  - {path}")


if __name__ == "__main__":
    print_d13_reporting_evidence_summary()
