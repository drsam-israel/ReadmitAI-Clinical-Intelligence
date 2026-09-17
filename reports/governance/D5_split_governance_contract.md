# D5 Governed Patient-Level Split Contract

## Project

Diabetes Readmission Clinical AI

## Purpose

This contract defines the governed development partitions used
throughout subsequent model-development stages.

The split unit is the patient rather than the encounter because
multiple encounters may belong to the same patient.

## Split Unit

**Grouping key:** `patient_nbr`

A patient may belong to one and only one partition.

Patient overlap across train, validation, and locked test is
prohibited.

## Outcome

**Target:** `readmitted_30d`

The patient-level outcome representation used for split balancing
is not a predictive feature.

## Partition Policy

**Training:** 70%

Used for fitting preprocessing transformations and models.

**Validation:** 15%

Model development, model comparison, calibration assessment, threshold selection, and other explicitly governed development decisions.

**Locked test:** 15%

Final locked evaluation only after feature engineering, preprocessing, model selection, calibration, and threshold decisions have been frozen.

## Reproducibility

**Random seed:** 42

The same governed cohort, patient-level outcome representation, split fractions, algorithm, and random seed must reproduce the same patient assignment.

The persisted patient assignment becomes the authoritative
downstream source of partition membership.

Downstream stages must load the persisted assignment rather than
silently generating a new split.

## Leakage Control

No patient may appear in more than one partition.

The locked test partition must not influence:

- feature engineering decisions;
- preprocessing decisions;
- model selection;
- hyperparameter selection;
- calibration decisions;
- threshold selection;
- clinical utility optimization.

## Governance Status

The locked test partition is **CREATED BUT PROTECTED**.

Creation of the locked test partition does not authorize its use
for model-development decisions.
