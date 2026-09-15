# D1 — Data Ingestion & Validation Report

**Project:** Diabetes Readmission Clinical AI  
**Lifecycle Stage:** D1 — Data Ingestion & Validation  
**Gate Status:** PASS  
**Dataset:** `diabetic_data.csv`

---

## 1. Purpose

D1 establishes that the admitted source dataset is authentic, structurally intact, reproducibly loadable, and suitable to proceed to formal Data Quality & Bias Assessment.

No cleaning, imputation, cohort filtering, target engineering, feature engineering, or modeling was performed during D1.

---

## 2. Raw Data Governance

The primary dataset is maintained in:

`data/raw/diabetic_data.csv`

The raw-data zone is governed as immutable.

Controls established:

- raw dataset excluded from Git
- transformations prohibited within the raw-data zone
- derived target not created in the raw-data zone
- analytical transformations deferred to governed downstream stages
- provenance and integrity evidence retained under version control

---

## 3. Dataset Integrity

**Integrity Algorithm:** SHA-256

**Verified SHA-256:**

`0689E7EC031237DC63031B938805C48377748761A3B26ACAB621567AFA24DF97`

**Integrity Result:** PASS

The admitted raw dataset matched the governed cryptographic fingerprint.

---

## 4. Structural Validation

| Control | Result |
|---|---:|
| Rows | 101,766 |
| Columns | 50 |
| Expected row count | PASS |
| Expected column count | PASS |
| Required columns present | PASS |
| Missing required columns | 0 |
| Missing encounter IDs | 0 |
| Duplicate encounter IDs | 0 |
| Encounter ID integrity | PASS |
| Missing patient identifiers | 0 |
| Patient identifier presence | PASS |
| Source target missing values | 0 |
| Source target domain | `<30`, `>30`, `NO` |
| Target-domain validation | PASS |
| SHA-256 validation | PASS |

---

## 5. Automated Validation

The project-wide automated test suite completed successfully:

**15 tests passed**

The suite includes:

- project configuration controls
- governed path controls
- reproducibility controls
- dataset existence
- cryptographic integrity
- dimensional contract
- required schema
- encounter identifier integrity
- patient identifier presence
- source target contract
- D1 structural gate

---

## 6. D1 Gate Decision

### PASS

The raw dataset is admitted into the governed Clinical AI lifecycle.

This decision confirms structural and integrity fitness only.

It does **not** imply that the dataset is clinically accurate, complete, current, internally consistent, representative, unbiased, or suitable for modeling without further assessment.

Those questions are explicitly deferred to D2.

---

## 7. Next Lifecycle Gate

### D2 — Data Quality & Bias Assessment

The dataset will be evaluated sequentially across:

**Accuracy → Completeness → Currency → Consistency → Representation → Bias**

D2 will determine whether identified data-quality and bias risks are acceptable, controllable, or sufficiently material to prevent progression to downstream model development.