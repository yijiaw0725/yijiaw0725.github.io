---
layout: page
title: Seattle / King County Housing Analytics
description: Multi-source analysis of 271K property sales — price trends, school & waterfront premiums, and XGBoost hedonic pricing model
img: assets/img/kc_price_trend.png
importance: 1
category: work
---

An end-to-end data science project analyzing residential real estate in King County, WA. Four public datasets were acquired via three different methods — bulk download, Socrata JSON API, and ArcGIS REST API — then merged and analyzed across five Jupyter notebooks covering EDA, school quality, crime, buyer guidance, and predictive modeling.

---

## Data

| Dataset | Source | Records |
|---|---|---|
| Property sales | KC Assessor (bulk download) | 271,923 SFR sales (2015–2024) |
| Crime incidents | Seattle PD via Socrata API | 733,596 incidents (2015–2024) |
| School assessments | WA OSPI via Socrata API | All King County K–12 schools (2023–24) |
| School district boundaries & parcel coordinates | KC GIS ArcGIS REST | 20 districts, 669K parcels |

---

## Key Findings

**Price trend**

Median SFR price grew from ~$150K (1990) to a peak near $900K (2022), with a COVID-era surge in 2020–2022 followed by a modest correction in 2023–24. Price per sq ft rose from ~$150 to over $450.

<div class="row justify-content-center mt-3">
    <div class="col-sm-10">
        {% include figure.liquid loading="eager" path="assets/img/kc_price_trend.png" title="King County Median SFR Sale Price 1990–2024" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    King County median single-family home price (1990–2024), with COVID surge and 2023–24 correction annotated.
</div>

**Location premiums**
- Waterfront properties command a **+76.9% premium** ($1.4M vs. $850K median)
- Homes with any view reach ~$800K median vs. ~$600K for no-view, non-waterfront properties

**School quality & home prices**
- Top-quartile school districts: $1,015K median vs. $511K for bottom quartile — a **+99% premium**
- District-level school quality correlates strongly with median sale price (r = 0.77)

<div class="row justify-content-center mt-3">
    <div class="col-sm-10">
        {% include figure.liquid loading="eager" path="assets/img/kc_school_price_scatter.png" title="School Quality vs House Price by District" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Each bubble is one school district; bubble size = transaction volume. Mercer Island sits at top right — highest-scoring and most expensive district in the county. r = 0.77.
</div>

**Crime & prices**
- Raw price difference between safest and highest-crime quintiles: only −1.1%, substantially smaller than the school effect

**Predictive model**
- XGBoost hedonic pricing model: R² = 0.698 on full King County data, 0.678 on Seattle-only
- SHAP analysis identifies living area, building grade, and school quality as top price drivers

---

## Notebooks

| Notebook | Description |
|---|---|
| [`kc_housing_eda`](https://github.com/yijiaw0725/seattle-housing-analytics/blob/main/kc_housing_eda.ipynb) | Price trends, seasonal patterns, building characteristics, waterfront & view premiums |
| [`kc_schools_housing`](https://github.com/yijiaw0725/seattle-housing-analytics/blob/main/kc_schools_housing.ipynb) | School pass rates by district, spatial join to parcels, school quality premium quantification |
| [`kc_crime_housing`](https://github.com/yijiaw0725/seattle-housing-analytics/blob/main/kc_crime_housing.ipynb) | SPD crime trend analysis (2015–2024), neighborhood heatmaps, crime-price relationship |
| [`kc_buyer_guide`](https://github.com/yijiaw0725/seattle-housing-analytics/blob/main/kc_buyer_guide.ipynb) | Choropleth maps, value score rankings, budget guidance by bedroom count |
| [`kc_price_model`](https://github.com/yijiaw0725/seattle-housing-analytics/blob/main/kc_price_model.ipynb) | OLS baseline + XGBoost hedonic model, log transformation, SHAP feature importance |

<a href="https://github.com/yijiaw0725/seattle-housing-analytics" class="btn btn-sm z-depth-0 mt-2" role="button">GitHub Repository</a>
