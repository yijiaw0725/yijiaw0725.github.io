---
layout: page
title: Retail Operations Dashboard (Power BI)
description: End-to-end Power BI analytics for a fictional specialty retail chain — semantic model design, 18 custom DAX measures, and two interactive dashboards covering executive KPIs and labor efficiency
img: assets/img/retail_cover.png
importance: 2
category: work
---

> **⚠️ Note:** This project uses **fully synthetic data** generated programmatically. The fictional company "Westbound Retail Co." is **not based on any real business** — all 25 stores, 150 employees, transactions, and labor records were created from scratch using a Python script to demonstrate a complete BI workflow without disclosing any real-world commercial information.

A complete Power BI analytics solution for a **fictional 25-store specialty retail chain** (Westbound Retail Co.). Built end-to-end from synthetic data generation through semantic modeling, DAX measure design, and dashboard layout — covering **$41.6M in (fictional) sales** and **899K labor hours** across 2022–2023.

The project demonstrates the full BI lifecycle: data engineering in Python, star-schema modeling in Power BI, custom DAX with time intelligence, and executive-ready visual design.

---

## Tooling

| Layer | Tool |
|---|---|
| Data generation | Python (pandas, numpy) — fully synthetic data with seasonality, weekend effects, YoY growth |
| Storage | Excel (.xlsx) — 5 sheets, ~400K fact-table rows |
| Modeling | Power BI Desktop — star schema, Power Query (M), DAX |
| Visualization | Power BI Desktop — interactive dashboards with slicers, drill-down, conditional formatting |

---

## Semantic Model

A clean **star schema** with two fact tables sharing a custom Date dimension:

```
              Dim_Date  ◄──┬── Sales_Transaction_Fact ──► Product_Ref
                           │           │  │
                           │           │  └──► Employee_Ref
                           │           ▼
                           │     Store_Hierarchy_Ref
                           │           ▲
                           └───► Labor_Operations_Fact
```

| Table | Type | Rows |
|---|---|---|
| `Sales_Transaction_Fact` | Fact | 382,349 transactions |
| `Labor_Operations_Fact` | Fact | 18,250 store-day labor records |
| `Dim_Date` | Custom date dimension (DAX calculated table) | 730 days |
| `Store_Hierarchy_Ref` | Dim — Region → District → Store | 25 stores |
| `Employee_Ref` | Dim | 150 employees |
| `Product_Ref` | Dim | 40 SKUs across 5 categories |

---

## Executive Dashboard

KPI cards, monthly trend with prior-year comparison, Top/Bottom 5 stores, category profitability, and district breakdown.

<div class="row justify-content-center mt-3">
    <div class="col-sm-12">
        {% include figure.liquid loading="eager" path="assets/img/retail_executive.png" title="Executive Dashboard" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Executive view: $41.56M total sales, +4.8% YoY, Q4 holiday season dominance (39.9% of annual revenue), and store-level performance ranking. All numbers are from synthetic data.
</div>

**Key findings**

- 📈 **+4.8% YoY** sales growth (2022 → 2023)
- 🎄 **Q4 holiday season accounts for 39.9%** of annual sales — Q4 2023 hit $8.53M vs. ~$4M average in other quarters
- 🏪 **Top store is 3.4× the bottom store** ($2.93M vs. $0.87M) — significant operational variance
- 💡 **Sales per Sqft** ranges from $99 to $1,603 — an **8× productivity gap** that pinpoints which underperforming stores need attention vs. closure

---

## Labor Efficiency Dashboard

Day-of-week labor patterns, monthly SPLH trend, store rankings by efficiency, weekend-vs-weekday comparison, and district-level labor metrics.

<div class="row justify-content-center mt-3">
    <div class="col-sm-12">
        {% include figure.liquid loading="eager" path="assets/img/retail_labor.png" title="Labor Efficiency Dashboard" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Labor efficiency view: $46.22 SPLH overall, 100% schedule adherence, $18.50 avg hourly wage. Weekend operations are 9.5% more efficient than weekdays. All numbers are from synthetic data.
</div>

**Key findings**

- ⏱️ **Sales per Labor Hour (SPLH) = $46.22** — high-performing retail efficiency tier
- ✅ **Schedule Adherence = 100.0%** — actual hours within 0.01% of planned (strong operational discipline)
- 💵 **Avg Hourly Wage = $18.50** — calibrated to industry-standard US retail compensation
- 🌟 **Weekend SPLH premium = +9.5%** — weekends deliver 75% more sales with only 60% more labor hours, making them the most efficient shifts
- 🌎 **NorCal district leads efficiency** ($47.07 SPLH, 39.3% Labor Cost %) vs. Mountain ($46.14 SPLH, 40.1%)

---

## Custom DAX Measures (18 total)

Selected examples demonstrating time intelligence, filter context manipulation, and conditional aggregation:

```dax
SPLH = 
    DIVIDE([Total Net Sales], SUM('Labor_Operations_Fact'[Actual_Labor_Hours]))

PY Net Sales = 
    CALCULATE([Total Net Sales], SAMEPERIODLASTYEAR('Dim_Date'[Date]))

YoY Sales % = 
    DIVIDE([Total Net Sales] - [PY Net Sales], [PY Net Sales])

Q4 Share % = 
    VAR _Q4 = CALCULATE([Total Net Sales], 'Dim_Date'[Quarter] = "Q4")
    VAR _Year = CALCULATE([Total Net Sales], ALL('Dim_Date'[Quarter]))
    RETURN DIVIDE(_Q4, _Year)

Weekend SPLH Premium % = 
    DIVIDE([Weekend SPLH] - [Weekday SPLH], [Weekday SPLH])
```

---

## Synthetic Data Pipeline

A reproducible Python script generates the fact tables with realistic retail patterns. **No real data was used at any stage** — the script outputs entirely fabricated transactions and labor records that mimic plausible retail behavior:

- **Weekend lift**: Saturday/Sunday transactions are 1.8× weekday volume
- **Q4 holiday effect**: October–December multiplier of 1.7×, plus Black Friday week boost
- **YoY growth**: 2023 is 1.05× of 2022 baseline
- **Store variation**: lognormal store-size factor — top stores 2–3× the volume of bottom stores
- **Category seasonality**: snow-sport products 2.5× in Dec–Feb, skate-sport products 1.6× in Jun–Aug
- **Labor scaling**: planned hours scale with traffic; actual hours = planned ± 5%; $18.50/hr fixed wage

The dimension tables (Employee, Product, Store) are preserved across regenerations so that the Power BI semantic model's relationships remain stable.

[Download the data generation script]({{ "/assets/code/retail_data_generator.py" | relative_url }})

---

## What I Learned

- **Model layer matters more than visuals.** Initial fact-table date columns came in as Excel serial integers, breaking all time-intelligence functions. Fixing the Power Query M expression to convert `Int64 → date` was a 30-second change that unlocked an entire class of analyses.
- **Synthetic data needs constraints, not just randomness.** A first-pass random dataset produced a 222% Labor Cost % — mathematically correct, business-impossible. Adding economic constraints (fixed wage × realistic hours / sufficient transaction volume) was essential.
- **Filter context shapes everything in DAX.** A `YoY %` measure that read perfectly at the year level returned 105% at the all-time level (because PY is implicitly the prior year's total). Understanding when to use `SAMEPERIODLASTYEAR` vs. explicit year filters became the most useful DAX lesson.
- **Conditional formatting amplifies noise.** A 0.21-percentage-point range can look like a crisis when colored min-max. Use absolute thresholds (e.g., red < 30%, green > 50%) over auto-scaling.

---

<a href="https://github.com/yijiaw0725" class="btn btn-sm z-depth-0 mt-2" role="button">GitHub Profile</a>
