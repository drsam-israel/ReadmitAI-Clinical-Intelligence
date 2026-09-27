# ReadmitAI Clinical Intelligence

### 30-Day Hospital Readmission Clinical Decision-Support Prototype

**Clinical Risk Intelligence | Explainability | Governance | Monitoring**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Clinical_AI_App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-172B4D)](https://xgboost.ai/)[![SHAP](https://img.shields.io/badge/Explainability-SHAP-5B5B5B)](https://shap.readthedocs.io/)![Model Version](https://img.shields.io/badge/Model-v1.0.0-2563EB)
![Validation](https://img.shields.io/badge/Status-Research_%26_Validation-F59E0B)![Deployment](https://img.shields.io/badge/Production-NOT_AUTHORIZED-B91C1C)![Clinical AI](https://img.shields.io/badge/Domain-Clinical_AI-0F766E)![Human Oversight](https://img.shields.io/badge/Human_Oversight-Required-7C3AED)

---

## Launch ReadmitAI

> **Interactive Clinical AI Prototype**

[**Launch ReadmitAI Clinical Intelligence →**](YOUR_STREAMLIT_APP_URL)

**Deployment status:** Research & Validation Prototype  
**Clinical use:** Not authorized for production clinical care  
**Human oversight:** Required

---

**Frozen Model:** `DIABETES_READMISSION_XGB_D13_V1`  
**Model Version:** `1.0.0`  
**Frozen Operating Threshold:** `0.12`  
**Production Deployment:** `NOT AUTHORIZED`

---

## 1. Project Overview

ReadmitAI Clinical Intelligence is an end-to-end Clinical AI project for predicting and supporting clinician review of 30-day hospital readmission risk among patients with diabetes.

The project extends beyond predictive model development to demonstrate the broader clinical AI lifecycle required to translate a machine-learning model into a governed decision-support prototype.

The implementation incorporates:

- reproducible data engineering;
- clinically governed cohort and outcome construction;
- leakage prevention;
- governed feature engineering;
- patient-level data partitioning;
- reproducible preprocessing;
- machine-learning model development and selection;
- clinical operating-point governance;
- subgroup and fairness evaluation;
- robustness and transportability assessment;
- patient-level and global explainability;
- model registry and artifact freezing;
- locked-test evaluation;
- deployment and monitoring design;
- clinical safety and human-oversight controls; and
- Streamlit-based clinical decision-support translation.

The resulting ReadmitAI application connects the frozen model to five integrated clinical AI modules:

1. **Risk Assessment**
2. **Explainability**
3. **Model Evidence**
4. **Governance & Safety**
5. **Monitoring**

ReadmitAI is a **research and validation prototype**. It is not authorized for production clinical deployment.

---

## 2. Clinical Problem

Hospital readmission is an important clinical, operational, and health-system challenge.

Patients with diabetes frequently have complex combinations of chronic disease, prior healthcare utilization, acute admission circumstances, medication requirements, and care-transition needs.

The objective of this project is therefore not to automate clinical decisions.

Instead, ReadmitAI investigates whether machine-learning-derived readmission risk can provide a governed **prioritization signal** that may support clinicians in identifying patients who warrant additional consideration for readmission-prevention review.

The model estimate remains decision support.

**Clinical decision authority remains with the healthcare professional.**

---

## 3. Intended Use

ReadmitAI is designed as a:

> **Clinician-facing prioritization support prototype for 30-day hospital readmission-prevention review among patients with diabetes.**

The system produces:

- an estimated 30-day readmission probability;
- a governed model advisory based on the frozen operating threshold;
- patient-level explainability;
- relevant model limitations and safety context; and
- supporting model-validation and governance evidence.

The system does **not** independently determine:

- discharge decisions;
- diagnosis;
- treatment selection;
- eligibility for care;
- denial or restriction of care; or
- final clinical management.

---

## 4. Dataset and Analytical Cohort

The project uses the **Diabetes 130-US Hospitals dataset**, containing hospital encounters involving patients with diabetes.

### Source Dataset

- **Original encounters:** 101,766
- **Original variables:** 50

### Governed Analytical Cohort

- **Encounters:** 69,944
- **Unique patients:** 49,307
- **30-day readmissions:** 7,907
- **30-day readmission rate:** 11.30%

The project applies explicit cohort construction, outcome engineering, data-quality assessment, leakage controls, and patient-level partitioning before model development.

Raw and derived patient-level datasets are not committed to Git.

---

## 5. End-to-End Clinical AI Lifecycle

The project was developed through a governed sequential lifecycle.

### Data and Engineering

1. Project Engineering & Reproducibility
2. Data Ingestion & Validation
3. Data Quality & Bias Assessment
4. Cohort & Outcome Engineering
5. Leakage & Feature Governance
6. Governed Patient-Level Data Splitting
7. Feature Engineering
8. Reproducible Preprocessing

### Model Development and Clinical Validation

9. Model Development & Selection
10. Clinical Utility & Operating-Threshold Governance
11. Fairness & Subgroup Evaluation
12. Robustness & Transportability Assessment
13. Explainability & Model Interpretation
14. Model Registry & Artifact Freeze
15. Locked-Test Evaluation

### Clinical Translation

16. Deployment & Monitoring Design
17. ReadmitAI Clinical Decision-Support Prototype

Each major lifecycle stage produces persisted technical or governance evidence rather than relying exclusively on notebook state.

---

## 6. Governed Feature Architecture

The frozen model uses **10 governed source features**.

### Patient Profile

- Race
- Gender
- Age

### Admission Context

- Admission Type
- Admission Source

### Prior Healthcare Utilization

Five governed utilization features are derived from prior outpatient, emergency, and inpatient encounters:

- `prior_outpatient_use`
- `prior_emergency_use`
- `prior_inpatient_use`
- `prior_utilization_intensity`
- `prior_utilization_domain_count`

The frozen preprocessing pipeline transforms the 10 governed source features into **49 model-ready features**.

The Streamlit application does not independently recreate the feature-engineering equations. It calls the governed feature-engineering implementation used by the underlying model pipeline.

---

## 7. Frozen Model

The registered model candidate is:

`DIABETES_READMISSION_XGB_D13_V1`

### Model Configuration

- **Algorithm:** XGBoost
- **Model Version:** 1.0.0
- **Operating Threshold:** 0.12
- **Raw Governed Features:** 10
- **Transformed Features:** 49
- **Candidate State:** Frozen
- **Production Deployment:** Not Authorized

The frozen model, preprocessing pipeline, transformed feature schema, metadata, manifests, and governance evidence are persisted as controlled project artifacts.

Post-freeze model modification requires explicit change control and a new governed model identity.

---

## 8. Locked-Test Evaluation

Final internal confirmatory evaluation was performed against the locked test partition without threshold retuning or test-driven model redesign.

### Locked-Test Cohort

- **Encounters:** 15,038
- **30-day readmissions:** 1,707
- **Non-readmissions:** 13,331
- **Prevalence:** 11.35%

### Model Performance

| Metric | Locked-Test Result |
|---|---:|
| ROC-AUC | 0.6234 |
| PR-AUC | 0.1820 |
| Brier Score | 0.0983 |
| Log Loss | 0.3433 |
| Sensitivity | 48.74% |
| Specificity | 70.54% |
| Positive Predictive Value | 17.48% |
| Negative Predictive Value | 91.49% |
| F1 Score | 0.2573 |
| Alert Rate | 31.65% |
| Number Needed to Evaluate | 5.72 |

The locked-test results support internal validation of the frozen candidate but do not establish external transportability, clinical effectiveness, or production readiness.

---

## 9. ReadmitAI Application

ReadmitAI translates the validated model and its governance evidence into an interactive Streamlit clinical AI prototype.

### 9.1 Risk Assessment

The Risk Assessment module accepts clinically organized patient information covering:

- patient profile;
- admission context; and
- prior healthcare utilization.

The application then executes the governed pipeline:

**User Input**

→ Input Validation  
→ Governed Feature Engineering  
→ Frozen D7 Preprocessor  
→ 49 Transformed Features  
→ Frozen XGBoost Model  
→ Predicted Readmission Probability  
→ Frozen 0.12 Operating Threshold  
→ Model Advisory  
→ Safety Context

The model output deliberately separates:

**MODEL ESTIMATE**

from

**MODEL ADVISORY**

from

**HUMAN CLINICAL DECISION**

---

## 10. Explainability

ReadmitAI provides patient-level model explanations using SHAP-based attribution.

The Explainability module connects:

**Patient-Level Explanation**

→ **Global Model Behavior**

→ **Model Governance**

Feature contributions describe how model inputs influenced the prediction relative to the model baseline.

They must not be interpreted as clinical causality.

A major model-governance finding is the model's substantial dependence on prior healthcare-utilization features. This dependency is explicitly surfaced within the application rather than hidden from the user.

---

## 11. Clinical Safety Controls

The application incorporates runtime safety messaging derived from model-validation evidence.

### Zero Prior-Utilization Safeguard

When a patient has no recorded prior:

- outpatient utilization;
- emergency utilization; or
- inpatient utilization,

ReadmitAI displays a specific model-limitation warning.

Internal robustness evaluation demonstrated poor sensitivity within this utilization profile at the frozen operating threshold.

Therefore:

> Absence of a model priority flag must not be interpreted as absence of readmission risk.

This limitation is translated from validation evidence into an application-level clinical safety control.

---

## 12. Model Evidence

The Model Evidence module exposes persisted locked-test evidence rather than recalculating model performance during application use.

It presents:

- validation status;
- frozen evaluation contract;
- locked-test cohort;
- discrimination;
- calibration-related evidence;
- operating-point performance;
- alert burden;
- validation-to-test stability;
- residual risks; and
- governance disposition.

### Current Evidence Status

| Evidence Domain | Status |
|---|---|
| Internal Locked-Test Validation | COMPLETED |
| External Validation | NOT ESTABLISHED |
| Clinical Effectiveness | NOT ESTABLISHED |
| Production Deployment | NOT AUTHORIZED |

---

## 13. Governance & Safety

ReadmitAI treats governance as part of the application architecture rather than as separate documentation.

The Governance & Safety module communicates:

- intended use;
- clinical decision authority;
- prohibited uses;
- runtime safety controls;
- model limitations;
- residual risks;
- lifecycle status; and
- deployment authorization status.

### Open Residual-Risk Domains

The final internal governance assessment retains seven documented residual-risk domains:

1. Utilization-dependent model behavior
2. Explainability utilization dominance
3. Subgroup operating heterogeneity
4. Admission-context heterogeneity
5. Limited model discrimination
6. External transportability
7. Clinical effectiveness

These risks remain visible rather than being obscured by the user interface.

---

## 14. Monitoring & Drift Governance

The D15 deployment-and-monitoring design defines a structured monitoring architecture for future operational use.

It contains:

- **17 monitoring controls**
- **17 escalation triggers**
- **6 quantitative historical surveillance references**
- traceability to the seven residual-risk domains.

Monitoring domains include:

- data quality;
- schema integrity;
- missingness;
- unknown-category rates;
- input-distribution shift;
- prediction-distribution shift;
- alert rate;
- discrimination;
- calibration;
- operating-point performance;
- subgroup performance;
- utilization dependence;
- admission-context performance;
- explainability stability;
- clinical override patterns;
- workflow adoption; and
- safety/governance incidents.

### Governed Escalation States

D15 defines four monitoring-response states:

| State | Governance Meaning |
|---|---|
| CRITICAL | Deterministic integrity or safety failure requiring immediate control action |
| ALERT | Material evidence-dependent change requiring formal governance review |
| WATCH | Emerging surveillance signal requiring investigation |
| NOT ASSESSABLE | Required evidence is not sufficiently mature |

The project does not invent a generic `NORMAL` state where one has not been defined by the governance contract.

### Monitoring Prototype Boundary

The Monitoring Command Center is explicitly labeled:

**SIMULATED / DESIGN DEMONSTRATION**

No live production telemetry is connected.

The monitoring interface therefore demonstrates the governed monitoring architecture without falsely claiming current production-health information.

---

## 15. Historical Surveillance References

D15 carries forward internal locked-test evidence as historical surveillance references.

Examples include:

| Metric | Historical Reference |
|---|---:|
| Prevalence | 11.35% |
| Alert Rate | 31.65% |
| Sensitivity | 48.74% |
| Specificity | 70.54% |
| PPV | 17.48% |
| NPV | 91.49% |

These are **internal historical surveillance references**.

They are not:

- production acceptance limits;
- clinical acceptability limits;
- external validation evidence; or
- evidence of clinical effectiveness.

---

## 16. Technical Architecture

The project uses a modular Python architecture separating model development, governed evidence, persisted artifacts, and application services.

### Core Technologies

- Python
- Pandas
- NumPy
- scikit-learn
- XGBoost
- SHAP
- Streamlit
- Altair
- joblib
- YAML
- JSON
- CSV
- Jupyter

### Application Architecture

```text
Clinical User Input
        |
        v
Input Validation
        |
        v
Governed Feature Engineering
        |
        v
Frozen Preprocessing Pipeline
        |
        v
49 Transformed Features
        |
        v
Frozen XGBoost Model
        |
        v
Readmission Probability
        |
        v
Frozen Threshold = 0.12
        |
        v
Model Advisory
        |
        +----------------------+
        |                      |
        v                      v
SHAP Explanation        Safety Context
        |                      |
        +----------+-----------+
                   |
                   v
          Human Clinical Review

---

Diabetes_Readmission_Clinical_AI/
|
|-- app/
|   |-- assets/
|   |-- components/
|   |-- config/
|   |-- pages/
|   |-- services/
|   `-- readmitai.py
|
|-- artifacts/
|   |-- manifests/
|   |-- models/
|   |-- preprocessors/
|   |-- registry/
|   `-- audit_logs/
|
|-- config/
|
|-- data/
|   |-- raw/
|   |-- interim/
|   `-- processed/
|
|-- docs/
|
|-- notebooks/
|
|-- reports/
|   |-- figures/
|   |-- tables/
|   `-- governance/
|
|-- src/
|   |-- features/
|   `-- models/
|
|-- tests/
|
|-- README.md
|-- requirements.txt
|-- requirements-lock.txt
|-- pyproject.toml
`-- .gitignore

---

18. Reproducibility & Artifact Governance
A core engineering principle of this project is:
If the computational environment is restarted, the project must remain reproducible from source data, version-controlled code, configuration, and persisted governed artifacts.

Jupyter notebooks function as analysis and evidence interfaces.
They are not the sole system of record for critical project state.
Governed evidence is persisted through:
- model artifacts;
- preprocessing artifacts;
- transformed feature schemas;
- configuration files;
- lifecycle manifests;
- model registry records;
- locked-test evidence;
- governance records;
- quantitative reference tables; and
- deployment-monitoring contracts.
Artifact identities and cryptographic hashes are used where appropriate to preserve frozen-candidate traceability.

---
19. Running ReadmitAI
From the project root, activate the project virtual environment.
Windows PowerShell
.\.venv\Scripts\Activate.ps1

Install project dependencies if required:
pip install -r requirements.txt

Launch ReadmitAI:
python -m streamlit run .\app\readmitai.py

The application will open in the local Streamlit interface.

---
20. Data Governance
Raw and derived patient-level datasets are not intended for source-control distribution.
The repository separates:
- source data;
- processed analytical data;
- transformation logic;
- model artifacts;
- governance evidence; and
- application code.
Dataset provenance, integrity checks, configuration, transformation logic, governance decisions, and reproducibility metadata are maintained separately within the project structure.

---
21. Key Limitations
ReadmitAI should be interpreted in the context of several important limitations.
Internal Validation Only
The frozen model has undergone internal locked-test evaluation.
External validation has not been established.
Limited Discrimination
Locked-test discrimination remains modest:
- ROC-AUC: 0.6234
- PR-AUC: 0.1820
The model should therefore be interpreted as a prioritization-support signal rather than a deterministic predictor.
Utilization Dependence
Prior healthcare utilization contributes substantially to model behavior.
Patients without recorded prior utilization represent a particularly important model-limitation profile.
Subgroup and Context Heterogeneity
Performance varies across some demographic, utilization, and admission-context groups.
Clinical Effectiveness Not Established
The project has not demonstrated that use of ReadmitAI improves patient outcomes, reduces readmissions, or improves healthcare-system performance.
No Production Deployment
ReadmitAI has not been authorized for real-world production clinical use.

---
22. Project Status
The core Clinical AI lifecycle and ReadmitAI prototype are complete at the research and validation stage.
Completed
- Data engineering and validation
- Data-quality and bias assessment
- Cohort and outcome governance
- Leakage controls
- Patient-level partitioning
- Feature engineering
- Preprocessing
- Model development and selection
- Operating-threshold governance
- Fairness and subgroup evaluation
- Robustness and transportability assessment
- Explainability
- Model registry and artifact freeze
- Locked-test evaluation
- Deployment and monitoring design
- Risk Assessment application
- Patient-level Explainability
- Model Evidence interface
- Governance & Safety interface
- Monitoring Command Center design
Not Established / Not Authorized
- External clinical validation
- Prospective clinical validation
- Clinical effectiveness
- Live production monitoring
- Production deployment authorization

---
23. Portfolio Significance
ReadmitAI was developed to demonstrate that healthcare machine learning should not stop at model training and performance metrics.
The project integrates:
Clinical Problem Definition
→ Data & Feature Governance
→ Machine Learning
→ Clinical Validation
→ Explainability
→ Responsible AI
→ Model Governance
→ Deployment Design
→ Monitoring Design
→ Clinical Decision-Support Translation
The emphasis is therefore not simply on building a predictive model, but on demonstrating how a clinical AI system can be developed, evaluated, governed, translated, and communicated responsibly across its lifecycle.

---
24. Author
Dr. Samuel Israel, MD
Healthcare AI | Clinical AI | AI Strategy & Transformation | Responsible AI Governance | Digital Health
25. Disclaimer
ReadmitAI Clinical Intelligence is a research and validation prototype developed for educational, technical, clinical-AI, governance, and portfolio demonstration purposes.
It is not a medical device, not medical advice, and not authorized for production clinical use.
Predictions and model advisories must not be used independently to make diagnosis, treatment, discharge, eligibility, denial-of-care, or other clinical decisions.
Human clinical judgment remains authoritative.