---
layout: page
title: Reproducing a Published Air-Quality Model
description: A reproducibility audit of a peer-reviewed benzene-estimation study — rebuilding its results from the data and methods alone to see what holds up
img: assets/img/air_quality_reproduction.png
importance: 4
category: work
---

A published result is only as useful as your ability to reproduce it. I took a peer-reviewed sensor-calibration study, worked only from its dataset and written methodology (no code was shared), and tried to rebuild its headline results from scratch. The goal wasn't to check a box — it was to find *where* a credible paper becomes hard to reproduce, and why that matters for anyone who has to trust a number before acting on it.

**The study.** De Vito et al. (*Sensors and Actuators B: Chemical*, 2007) calibrate a low-cost electronic-nose sensor to estimate benzene (C₆H₆) concentrations in urban air. The data is the [UCI Air Quality dataset](https://archive.ics.uci.edu/dataset/360/air+quality): 9,357 hourly readings of CO, NOₓ, NO₂, benzene and more, collected in an Italian city between March 2004 and April 2005.

I reproduced two of the paper's core claims — its **pollutant correlation structure** and its **neural-network benzene estimates** — and paired each with a statistical-power check to separate "real effect" from "lucky sample."

---

## What reproduced, and what didn't

### Correlation structure

Most pairwise correlations came back cleanly, with statistical power of 1.0 at *n* = 9,357. But three pairs collapsed — reproduced correlations near zero where the paper reported strong relationships — and their power dropped with them.

| Pollutant pair | Reproduced *r* | Original *r* | Reproduced power | Verdict |
|---|---:|---:|---:|---|
| NMHC – C₆H₆ | 0.94 | 0.98 | 1.00 | ✅ reproduced |
| NOₓ – NO₂ | 0.82 | 0.76 | 1.00 | ✅ reproduced |
| CO – NO₂ | 0.67 | 0.67 | 1.00 | ✅ reproduced |
| CO – NOₓ | 0.53 | 0.78 | 1.00 | ⚠️ weakened |
| CO – C₆H₆ | −0.03 | 0.90 | 0.83 | ❌ failed |
| C₆H₆ – NO₂ | −0.01 | 0.60 | 0.16 | ❌ failed |
| C₆H₆ – NOₓ | 0.00 | 0.72 | 0.05 | ❌ failed |

The failures weren't random. Every one of them involved benzene or NMHC, and the paper notes in passing that the **NMHC analyzer was out of service** for part of the collection window. Combined with preprocessing steps the paper describes but doesn't fully specify, that's enough to turn a strong reported correlation into noise on reproduction — a reminder that an undocumented data-cleaning decision can quietly carry an entire result.

### Neural-network benzene estimation

The second test was the paper's headline model: a back-propagation neural network trained on a 10-day window to estimate benzene, reported alongside error and environmental series.

<div class="row justify-content-center mt-3">
    <div class="col-sm-11">
        {% include figure.liquid loading="eager" path="assets/img/air_quality_reproduction.png" title="Reproduced benzene estimation" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    My reproduction of the model's reported series — relative and absolute error for benzene, actual vs. predicted concentration, and the accompanying temperature and humidity signals.
</div>

Following the written method, my reproduction tracked the real signal but with **noticeably higher error** than the paper reports. Rather than wave it away, I traced the gap to four concrete causes:

- **Undocumented architecture** — no layer count, neurons, or activation functions are given, so the network can't be rebuilt exactly.
- **A violated assumption** — the model treats observations as independent, but this is hourly time-series data with strong autocorrelation, so that assumption doesn't hold.
- **Too small a training window** — 10 days is a thin slice to learn from and invites underfitting.
- **Outliers and seasonality** — heavy-tailed benzene readings and unmodeled seasonal effects add noise the short window can't absorb.

---

## The takeaway

Reproducibility isn't a property a study either has or lacks — it degrades at specific, findable points. Here it held wherever the data and steps were fully specified, and broke wherever a preprocessing choice, a model detail, or a data-quality caveat was left implicit. The practical lesson carries straight into everyday analytics: a result you can't reproduce is a result you can't safely act on, and the fixes are unglamorous — write down the preprocessing, share the code, respect the structure of the data, and check that the sample is large enough to trust.

---

**Stack:** R — pairwise correlation and statistical-power analysis, neural-network reproduction, time-series diagnostics, and figure work.

<a href="https://archive.ics.uci.edu/dataset/360/air+quality" class="btn btn-sm z-depth-0 mt-2" role="button">Dataset (UCI)</a>
<a href="https://doi.org/10.1016/j.snb.2007.09.041" class="btn btn-sm z-depth-0 mt-2" role="button">Original Paper</a>
