# D4 Prediction-Time Contract

## Project

Diabetes Readmission Clinical AI

## Purpose

This document establishes the formal information boundary for
feature eligibility before model development.

A variable appearing in the retrospective source dataset is not
automatically eligible for modeling. Eligibility depends on whether
the information could legitimately have been available at or before
the defined prediction timestamp.

## Clinical Decision Point

**Population:** Eligible adult inpatient encounters involving patients with diabetes represented in the governed cohort.

**Setting:** Acute-care inpatient hospitalization.

**Primary users:** Discharge planning team, Care management team, Treating clinicians

**Decision supported:** Identify patients who may warrant enhanced readmission-prevention planning before discharge.

**Prediction timestamp:** Before discharge, at the point when the model output would be used to support discharge-planning decisions.

**Prediction horizon:** Readmission occurring within 30 days after discharge.

**Outcome:** Binary 30-day readmission outcome: readmitted_30d = 1 when readmitted == '<30'; otherwise 0.

**Intended action:** Support prioritization for clinician-reviewed readmission-prevention interventions. The model does not autonomously determine discharge or treatment.

## Prediction-Time Governance Contract

### Core Rule

A modeling feature must represent information that is legitimately available at or before the defined prediction timestamp.

### Historical Information

Information from prior encounters may be eligible when it can be established that it occurred before the current prediction timestamp.

### Current Encounter Information

Current-encounter variables require evidence that the value would already be known at the prediction timestamp and does not summarize information generated after that point.

### Retrospective Totals

Final encounter-level totals must not be assumed to be prediction-time-safe merely because they appear in the source dataset.

### Outcome Information

The source outcome and all deterministic or indirect representations of the outcome are prohibited as modeling features.

### Identifiers

Patient and encounter identifiers are retained for governance, traceability, patient-level splitting, and audit purposes only. They are not modeling features.

### Ambiguous Timing

When the availability timestamp cannot be established with sufficient confidence, the feature must not be automatically approved. It is classified as CONDITIONAL or BLOCKED pending evidence.

### Locked Test

No feature-governance decision may be informed by performance on the locked test partition.

## Governance Principle

Feature availability must be established independently of model
performance. No feature may be approved because it improves
validation or test performance.

The locked test partition must not influence feature-governance
decisions.

## Status

Prediction-time contract established before model development.
