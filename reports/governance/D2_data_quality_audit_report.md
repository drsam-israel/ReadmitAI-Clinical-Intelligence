# D2 — Data Quality & Bias Audit Report

## Project

**Diabetes Readmission Clinical AI**

## Lifecycle Stage

**D2 — Data Quality & Bias Assessment**

## Audit Framework

Accuracy → Completeness → Currency → Consistency → Representation → Bias

---

## 1. Purpose

This audit evaluates whether the admitted raw dataset is sufficiently
understood and governed to proceed into cohort definition, outcome
engineering, feature governance, model development and subsequent
clinical AI evaluation.

A D2 gate decision does not constitute approval for clinical deployment.

---

## 2. Dataset Context

- Raw encounters: **101,766**
- Unique patients: **71,518**
- Source temporal coverage: **1999–2008**
- Years since latest source data at assessment: **18**
- Encounter-level calendar dates available: **No**

---

## 3. Accuracy / Conformance

**Disposition: CONDITIONAL PASS**

No invalid values were identified within the audited categorical
domains. Defined numeric plausibility checks and identifier checks
passed.

Missing-like sentinel states remain subject to governed completeness
and semantic review.

---

## 4. Completeness

**Disposition: CONDITIONAL PASS**

Material incompleteness exists in weight, glycemic testing,
medical-specialty and payer-related fields.

Missingness is not assumed to be random. In particular, absence of
laboratory results may represent whether a test was performed or
recorded rather than simple accidental data loss.

No automatic imputation or deletion decision is authorized by D2.

---

## 5. Currency

**Disposition: CONDITIONAL PASS — HIGH RISK**

The dataset is historically valuable for model development and methodological demonstration, but is not temporally current for direct contemporary clinical deployment.

**Required control:** Contemporary external validation and temporal recalibration are required before clinical deployment.

---

## 6. Consistency

**Disposition: CONDITIONAL PASS**

Core identifier, medication-exposure and readmission-domain checks
show strong internal consistency.

Medication-change semantics and a small number of diagnosis-sequence
patterns require review. These findings are audit flags and are not
automatically classified as source-data errors.

---

## 7. Representation

**Disposition: CONDITIONAL PASS**

The dataset contains 101,766 encounters from
71,518 patients.

Several racial groups and younger age groups have limited
representation. Subgroup evidence strength therefore differs across
the population.

Representation findings do not by themselves establish bias.

---

## 8. Pre-Model Bias Assessment

**Disposition: CONDITIONAL PASS**

Potential bias mechanisms identified include:

- temporal bias;
- representation bias;
- measurement / missingness bias;
- repeated-patient weighting;
- label / outcome bias.

Approximately **46.205%** of encounters belong to patients with
multiple encounters.

These are pre-model risks. Model fairness cannot be determined until
a model exists and subgroup error characteristics are evaluated.

---

## 9. Governance Implications

The following controls are mandatory downstream:

1. Patient-disjoint development and evaluation partitions.
2. Prediction-time feature governance.
3. Explicit treatment of missingness semantics.
4. Subgroup performance and uncertainty assessment.
5. Fairness evaluation after model development.
6. Contemporary external validation before any clinical deployment.
7. Explicit documentation of readmission-label limitations.
8. Locked-test governance before final evaluation.

---

## 10. Overall D2 Decision

**CONDITIONAL PASS**

The dataset is suitable to proceed to governed cohort and outcome
engineering for research, development and methodological evaluation.

The dataset is **not approved for direct contemporary clinical
deployment**.

All open D2 risks and controls remain traceable into downstream
lifecycle stages.

---

## 11. Next Lifecycle Stage

**D3 — Cohort & Outcome Engineering**
