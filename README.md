# Diabetes Readmission Clinical AI

## Production-Grade Clinical Decision Support ML Project

This repository contains the development of a governed, reproducible, and clinically oriented machine-learning system for predicting 30-day hospital readmission among patients with diabetes.

## Project Objective

Develop and evaluate a production-oriented Clinical AI decision-support system that identifies patients at elevated risk of 30-day readmission while incorporating:

- rigorous data validation
- data quality and bias assessment
- clinically governed cohort and outcome engineering
- leakage prevention
- feature governance
- patient-level data partitioning
- reproducible preprocessing and modeling pipelines
- discrimination and calibration assessment
- clinically governed threshold selection
- clinical utility analysis
- subgroup and fairness evaluation
- explainability
- robustness and sensitivity testing
- model registry and artifact governance
- deployment architecture
- drift and performance monitoring

## Core Engineering Principle

> If the computational environment is restarted, the project must remain reproducible from source data, version-controlled code, configuration, and persisted governed artifacts.

Jupyter notebooks serve as analysis and evidence interfaces. They are not the system of record for critical project state.

## Clinical AI Lifecycle

1. Project Engineering & Reproducibility
2. Data Ingestion & Validation
3. Data Quality & Bias Assessment
4. Cohort & Outcome Engineering
5. Leakage & Feature Governance
6. Governed Patient-Level Splitting
7. Feature Engineering Pipeline
8. Preprocessing Pipeline
9. Model Development & Selection
10. Clinical Utility & Threshold Governance
11. Fairness & Subgroup Evaluation
12. Robustness & Transportability
13. Explainability
14. Model Registry & Artifact Freeze
15. Locked-Test Evaluation
16. Deployment & Monitoring Design

## Data Quality & Bias Framework

The project explicitly evaluates:

**Accuracy → Completeness → Currency → Consistency → Representation → Bias**

These assessments occur before model development and contribute to a formal Data Quality & Bias Gate.

## Data Governance

Raw and derived datasets are not committed to Git.

Dataset provenance, integrity checks, configuration, transformation logic, governance decisions, and reproducibility metadata are maintained separately within the repository.

## Repository Structure

- `config/` — governed project configuration
- `data/` — raw, interim, and processed data zones
- `notebooks/` — analysis and evidence notebooks
- `src/` — reusable production code
- `artifacts/` — governed model and pipeline artifacts
- `reports/` — figures, tables, and governance outputs
- `tests/` — automated validation and unit tests
- `docs/` — technical and governance documentation

## Status

Project initialization and reproducibility engineering in progress.