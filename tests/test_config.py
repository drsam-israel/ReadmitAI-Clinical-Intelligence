# ============================================================
# TESTS — PROJECT CONFIGURATION & PATH GOVERNANCE
# ============================================================

from pathlib import Path

from src.data.config import (
    PROJECT_ROOT,
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    load_data_config,
    get_primary_dataset_path,
    get_supporting_dataset_path,
)


# ============================================================
# TEST 1 — PROJECT ROOT
# ============================================================

def test_project_root_exists():
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()


# ============================================================
# TEST 2 — GOVERNED DATA DIRECTORIES
# ============================================================

def test_data_directories_exist():
    assert RAW_DATA_DIR.exists()
    assert INTERIM_DATA_DIR.exists()
    assert PROCESSED_DATA_DIR.exists()


# ============================================================
# TEST 3 — DATA CONFIGURATION LOADS
# ============================================================

def test_data_config_loads():
    config = load_data_config()

    assert isinstance(config, dict)
    assert config["project"]["name"] == "Diabetes Readmission Clinical AI"


# ============================================================
# TEST 4 — TARGET GOVERNANCE
# ============================================================

def test_target_configuration():
    config = load_data_config()

    assert config["target"]["source_column"] == "readmitted"
    assert config["target"]["derived_column"] == "readmitted_30d"
    assert config["target"]["positive_class"] == "<30"


# ============================================================
# TEST 5 — PRIMARY DATASET PATH
# ============================================================

def test_primary_dataset_path():
    expected = RAW_DATA_DIR / "diabetic_data.csv"

    assert get_primary_dataset_path() == expected
    assert isinstance(get_primary_dataset_path(), Path)


# ============================================================
# TEST 6 — SUPPORTING DATASET PATH
# ============================================================

def test_supporting_dataset_path():
    expected = RAW_DATA_DIR / "IDs_mapping.csv"

    assert get_supporting_dataset_path() == expected


# ============================================================
# TEST 7 — REPRODUCIBILITY CONTROLS
# ============================================================

def test_reproducibility_controls():
    config = load_data_config()

    assert config["reproducibility"]["random_seed"] == 42
    assert config["governance"]["raw_data_immutable"] is True
    assert config["governance"]["patient_level_splitting_required"] is True
    assert config["governance"]["locked_test_required"] is True
    assert config["governance"]["prediction_time_feature_review_required"] is True