---
layout: page
title: E-commerce Customer Segmentation (SQL)
description: RFM segmentation of 93K customers across 99K real orders — Python ETL into SQLite, SQL window-function scoring, and a clear answer to where the revenue sits
img: assets/img/rfm_segments.png
importance: 3
category: work
github: https://github.com/yijiaw0725/ecommerce-sql-analysis
---

An end-to-end SQL analysis of ~100K real e-commerce orders from the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). A Python script loads five raw CSVs into a SQLite database, then SQL (CTEs, multi-table joins, `NTILE` window functions) scores every customer on Recency, Frequency, and Monetary value and assigns them to one of five actionable segments.

**Code:** [github.com/yijiaw0725/ecommerce-sql-analysis](https://github.com/yijiaw0725/ecommerce-sql-analysis)

---

## Data

| Table | Contents | Scale |
|---|---|---|
| `orders` | Order status and timestamps | 99,441 orders (2016–2018) |
| `customers` | Customer IDs and location | 96,096 unique customers |
| `payments` | Payment type and value | R$15.4M across delivered orders |
| `order_items` / `products` | Items, prices, categories | — |

Analysis uses the 96,478 **delivered** orders, with 2018-09-01 as the reference date for recency.

---

## Key Findings

**The single biggest opportunity is win-back, not acquisition.** 21,897 At Risk customers — people who used to spend well but have gone quiet for ~13 months on average — account for **R$5.3M (34%) of historical revenue**, the largest share of any segment.

<div class="row justify-content-center mt-3">
    <div class="col-sm-10">
        {% include figure.liquid loading="eager" path="assets/img/rfm_segments.png" title="Customers vs revenue share by RFM segment" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Customer share vs revenue share by segment. At Risk customers are the largest revenue block (34%); Standard customers are a third of the base but only 11% of revenue.
</div>

**Revenue is concentrated at the top.** Best + Loyal customers are 36% of the base but drive **52% of revenue**, with Best customers averaging R$310 each — nearly 6× a Standard customer.

**97% of customers purchased exactly once.** Repeat purchase, not traffic, is the structural growth lever for this marketplace.

<div class="row justify-content-center mt-3">
    <div class="col-sm-10">
        {% include figure.liquid loading="eager" path="assets/img/rfm_scatter.png" title="93K customers by recency and spend" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Each point is one customer, placed by days since last purchase (x) and total spend (y, log scale). The segment structure is visible directly: New &amp; Promising (yellow) bought recently, At Risk (red) spent well but went quiet, Best (teal) are recent high-spenders.
</div>

---

## How the segmentation works

Each customer is scored 1–5 on three dimensions with `NTILE(5)` window functions:

| Segment | Definition |
|---|---|
| **Best** | Top-tier on recency, frequency, and spend (all scores ≥ 4) |
| **Loyal** | Solid on all three dimensions (all scores ≥ 3) |
| **New & Promising** | First purchase within the last 90 days — worth nurturing |
| **At Risk** | Bottom 40% on recency but mid-to-high spend — worth winning back |
| **Standard** | Everyone else |

**A bug worth writing about.** My first version of the segment logic produced an empty New & Promising segment. Digging in revealed two issues: the recency filter contradicted the recency score direction, and — more interesting — since 97% of customers bought exactly once, ranking frequency with `NTILE` split tens of thousands of identical values into arbitrary buckets. The fix: tie-break frequency scores by spend, define "new" customers by raw recency instead of scores, and filter At Risk by monetary score so the segment captures *valuable* lapsed customers — a list a marketing team could actually act on.

---

## Stack

**SQLite** (CTEs, window functions, multi-table joins) · **Python/pandas** (CSV-to-database ETL) · **Matplotlib** (charts)
