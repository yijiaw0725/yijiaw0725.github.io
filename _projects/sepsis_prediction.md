---
layout: page
title: Predicting Sepsis from Patient Vitals
description: A clinical risk model on severely imbalanced patient data — why accuracy lies, and how class-weighting plus the right metric surface the cases that matter
img: assets/img/sepsis_model_comparison.svg
importance: 5
category: work
---

Sepsis moves fast, and catching it early changes outcomes. The data makes that hard in a specific way: the overwhelming majority of patients never develop sepsis, so a model that quietly labels *everyone* healthy can look highly accurate while missing every case that actually matters. This project builds a sepsis-risk classifier that takes that imbalance seriously from the start.

---

## The data

Each patient contributes a set of lab and vital-sign measurements recorded over time. I aggregated those into **35 per-patient predictors** (the mean of each test), giving one clean row per patient, then handled missing values with mean imputation. That left ~15,000 labeled patients to train and evaluate on, plus ~6,500 unlabeled patients to score. A 70/30 train–test split kept the evaluation honest.

The defining feature of the dataset is its **class imbalance**: "no sepsis" dominates. That single fact drives every modeling decision below.

---

## Why I didn't trust accuracy

On data this skewed, raw accuracy is a trap — a model that predicts the majority class every time scores well and helps no one. So I evaluated on two metrics that can't be gamed that way:

- **Balanced Error Rate (BER)** — averages the error across both classes, so missing sepsis cases is penalized properly.
- **AUC** — measures how well the model *ranks* patients by risk, independent of any single threshold.

I then compared four models, each with explicit class-imbalance handling (balanced class weights or a positive-class scale factor):

<div class="row justify-content-center mt-3">
    <div class="col-sm-11">
        {% include figure.liquid loading="eager" path="assets/img/sepsis_model_comparison.svg" title="Model comparison: AUC and BER" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

| Model | BER (lower better) | AUC (higher better) |
|---|---:|---:|
| Weighted Logistic | 0.36 | 0.69 |
| Classification Tree | 0.38 | 0.66 |
| AdaBoost | 0.37 | 0.81 |
| **XGBoost** | **0.25** | **0.82** |

---

## What won, and why

**XGBoost was the clear pick** — lowest balanced error (0.25) and highest AUC (0.82). But the biggest lever wasn't the model family. Setting the positive-class weight to the ratio of negatives to positives cut the balanced error sharply while barely moving AUC; that one imbalance-aware step did more than any amount of model-swapping. Randomized cross-validation then tuned a deliberately **simple** final model — depth-2 trees, 60% row and column subsampling — strong on the held-out set without overfitting.

A quick clinical sanity check: the top predictors were **systolic blood pressure, temperature, and blood urea nitrogen** — all physiologically plausible sepsis signals. That's reassuring evidence the model learned something real rather than dataset noise.

---

## The takeaway

On imbalanced clinical data, the win comes from *framing* more than from firepower: pick a metric the majority class can't game, handle the imbalance head-on, and only then reach for a stronger algorithm. The final model outputs both a label and a calibrated risk score per patient — the latter being the more useful artifact, since it lets a care team triage by *how* likely sepsis is rather than a blunt yes/no.

---

**Stack:** Python — scikit-learn (logistic regression, decision trees, AdaBoost), XGBoost, randomized-search cross-validation, and BER / AUC evaluation for imbalanced classification.
