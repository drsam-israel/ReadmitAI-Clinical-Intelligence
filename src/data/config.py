# ============================================================
# DIABETES READMISSION CLINICAL AI
# PROJECT PATH & CONFIGURATION LOADER
# ============================================================

from pathlib import Path
from typing import Any

import yaml


# ============================================================
# 1. PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# 2. GOVERNED PROJECT DIRECTORIES
# ============================================================

CONFIG_DIR = PROJECT_ROOT / "config"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SPLITS_DIR = ARTIFACTS_DIR / "splits"
PREPROCESSORS_DIR = ARTIFACTS_DIR / "preprocessors"
MODELS_DIR = ARTIFACTS_DIR / "models"
MANIFESTS_DIR = ARTIFACTS_DIR / "manifests"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
GOVERNANCE_REPORTS_DIR = REPORTS_DIR / "governance"


# ============================================================
# 3. CONFIGURATION LOADER
# ============================================================

def load_yaml_config(filename: str) -> dict[str, Any]:
    """
    Load a governed YAML configuration file from config/.

    Parameters
    ----------
    filename:
        YAML configuration filename, for example 'data.yaml'.

    Returns
    -------
    dict
        Parsed configuration.

    Raises
    ------
    FileNotFoundError
        If the requested configuration file does not exist.
    """

    config_path = CONFIG_DIR / filename

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            f"Configuration file is empty: {config_path}"
        )

    return config


# ============================================================
# 4. DATA CONFIGURATION
# ============================================================

def load_data_config() -> dict[str, Any]:
    """Load the governed data configuration."""

    return load_yaml_config("data.yaml")


# ============================================================
# 5. PRIMARY DATASET PATH
# ============================================================

def get_primary_dataset_path() -> Path:
    """
    Return the configured path to the primary raw dataset.
    """

    config = load_data_config()

    filename = config["data"]["primary_dataset"]["filename"]

    return RAW_DATA_DIR / filename


# ============================================================
# 6. SUPPORTING DATASET PATH
# ============================================================

def get_supporting_dataset_path() -> Path:
    """
    Return the configured path to the supporting mapping dataset.
    """

    config = load_data_config()

    filename = config["data"]["supporting_dataset"]["filename"]

    return RAW_DATA_DIR / filename