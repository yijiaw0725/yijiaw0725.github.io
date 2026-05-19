"""
Regenerate Zumiez retail demo data with realistic patterns.

Preserves: Employee_Ref, Product_Ref, Store_Hierarchy_Ref (untouched)
Regenerates: Sales_Transaction_Fact, Labor_Operations_Fact
Writes back to the same xlsx (your manual backup is safe).
"""
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

XLSX_PATH = Path(r"C:\Users\wangy\OneDrive\Desktop\Zumiez_Retail_Operations_Data.xlsx")
np.random.seed(42)

START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2023, 12, 31)
BASE_TRANS         = 14
WEEKEND_MULT       = 1.8
Q4_MULT            = 1.7
YOY                = 1.05
BASE_LABOR_HOURS   = 42
WEEKEND_LABOR      = 1.6
HOURLY_WAGE        = 18.50

CATEGORIES = {
    "Apparel":     {"w": 0.42, "lo": 18,  "hi": 80,  "margin": 0.62},
    "Footwear":    {"w": 0.25, "lo": 45,  "hi": 130, "margin": 0.48},
    "Accessories": {"w": 0.18, "lo": 8,   "hi": 45,  "margin": 0.70},
    "Skateboard":  {"w": 0.10, "lo": 50,  "hi": 280, "margin": 0.43},
    "Snowboard":   {"w": 0.05, "lo": 180, "hi": 650, "margin": 0.38},
}
SNOW_SEASON  = {12:2.5, 1:2.5, 2:2.2, 3:1.4, 4:0.8, 5:0.5, 6:0.3, 7:0.3, 8:0.3, 9:0.6, 10:1.2, 11:1.8}
SKATE_SEASON = {1:0.7, 2:0.7, 3:0.9, 4:1.1, 5:1.3, 6:1.6, 7:1.6, 8:1.5, 9:1.2, 10:0.9, 11:0.7, 12:0.7}

# ----- Load dim tables -----
print(f"Loading {XLSX_PATH.name}...")
xls = pd.ExcelFile(XLSX_PATH)
employees = pd.read_excel(xls, "Employee_Ref")
products  = pd.read_excel(xls, "Product_Ref")
stores    = pd.read_excel(xls, "Store_Hierarchy_Ref")
print(f"  Dims preserved: {len(employees)} employees, {len(products)} products, {len(stores)} stores")

products_by_cat = {c: products[products["Category"] == c]["ProductID"].tolist() for c in CATEGORIES if c in products["Category"].unique()}
emps_by_store   = {sid: employees[employees["StoreID"] == sid]["EmployeeID"].tolist() for sid in stores["StoreID"]}

# Store size variation (lognormal)
store_f_raw = np.random.lognormal(mean=0, sigma=0.35, size=len(stores))
store_f_raw = store_f_raw / store_f_raw.mean()
store_factor = dict(zip(stores["StoreID"], store_f_raw))

# ----- Sales_Transaction_Fact -----
print("Generating Sales_Transaction_Fact (~30-60s)...")
date_range = pd.date_range(START_DATE, END_DATE, freq="D")
cat_names = list(CATEGORIES.keys())
base_weights = np.array([CATEGORIES[c]["w"] for c in cat_names])

sales_rows = []
txn_id = 1
for d in date_range:
    is_weekend = d.weekday() >= 5
    is_q4 = d.month >= 10
    is_2023 = d.year == 2023
    is_bf = d.month == 11 and 23 <= d.day <= 29
    day_mult = 1.0
    if is_weekend: day_mult *= WEEKEND_MULT
    if is_q4:      day_mult *= Q4_MULT
    if is_2023:    day_mult *= YOY
    if is_bf:      day_mult *= 1.3

    season_mults = np.array([
        SNOW_SEASON[d.month]  if c == "Snowboard"
        else SKATE_SEASON[d.month] if c == "Skateboard"
        else 1.0
        for c in cat_names
    ])
    cw = base_weights * season_mults
    cw /= cw.sum()

    for sid, sf in store_factor.items():
        n = np.random.poisson(BASE_TRANS * day_mult * sf)
        if n == 0:
            continue
        store_emps = emps_by_store.get(sid, [])
        if not store_emps:
            continue
        cats = np.random.choice(cat_names, size=n, p=cw)
        qtys = np.random.choice([1, 2, 3], size=n, p=[0.75, 0.20, 0.05])
        emps = np.random.choice(store_emps, size=n)
        disc_max = 0.15 if (is_weekend or is_bf) else 0.10
        discs = np.round(np.random.uniform(0, disc_max, size=n), 4)
        for i in range(n):
            cat = cats[i]
            cp = CATEGORIES[cat]
            pid = np.random.choice(products_by_cat[cat])
            qty = int(qtys[i])
            price = round(np.random.uniform(cp["lo"], cp["hi"]), 2)
            cogs  = round(price * (1 - cp["margin"]) * np.random.uniform(0.95, 1.05), 2)
            disc  = float(discs[i])
            net   = round(qty * price * (1 - disc), 2)
            gm    = round(net - qty * cogs, 2)
            sales_rows.append({
                "Date": d, "TransactionID": f"TXN-{txn_id:08d}",
                "StoreID": sid, "EmployeeID": emps[i], "ProductID": pid,
                "Quantity": qty, "SellingPrice_PerUnit": price, "COGS_PerUnit": cogs,
                "Discount_Pct": disc, "Net_Sales": net, "Gross_Margin": gm,
            })
            txn_id += 1

sales_df = pd.DataFrame(sales_rows)
print(f"  -> {len(sales_df):,} transactions")

# ----- Labor_Operations_Fact -----
print("Generating Labor_Operations_Fact...")
labor_rows = []
for d in date_range:
    boost = WEEKEND_LABOR if d.weekday() >= 5 else 1.0
    for sid, sf in store_factor.items():
        planned = round(BASE_LABOR_HOURS * boost * sf * np.random.uniform(0.95, 1.05), 1)
        actual  = round(planned * np.random.uniform(0.95, 1.05), 1)
        cost    = round(actual * HOURLY_WAGE, 2)
        labor_rows.append({
            "Date": d, "StoreID": sid,
            "Planned_Labor_Hours": planned, "Actual_Labor_Hours": actual,
            "Total_Labor_Cost": cost,
        })
labor_df = pd.DataFrame(labor_rows)
print(f"  -> {len(labor_df):,} labor rows")

# ----- Validation -----
total_sales  = sales_df["Net_Sales"].sum()
total_margin = sales_df["Gross_Margin"].sum()
total_labor  = labor_df["Total_Labor_Cost"].sum()
total_hours  = labor_df["Actual_Labor_Hours"].sum()
print("\n========== KPI Validation ==========")
print(f"  Total Net Sales:       ${total_sales:>14,.0f}")
print(f"  Total Gross Margin:    ${total_margin:>14,.0f}")
print(f"  Gross Margin %:        {total_margin/total_sales:>15.1%}")
print(f"  Total Labor Cost:      ${total_labor:>14,.0f}")
print(f"  Total Actual Hours:    {total_hours:>14,.0f}")
print(f"  Implied Hourly Rate:   ${total_labor/total_hours:>14.2f}")
print(f"  Labor Cost %:          {total_labor/total_sales:>15.1%}")
print(f"  SPLH:                  ${total_sales/total_hours:>14.2f}")

we = sum(1 for d in date_range if d.weekday() >= 5)
wd = sum(1 for d in date_range if d.weekday() < 5)
sales_df["_dow"] = sales_df["Date"].dt.dayofweek
weekend_avg = sales_df[sales_df["_dow"] >= 5]["Net_Sales"].sum() / we
weekday_avg = sales_df[sales_df["_dow"] < 5]["Net_Sales"].sum() / wd
sales_df["_m"] = sales_df["Date"].dt.month
q4_share = sales_df[sales_df["_m"] >= 10]["Net_Sales"].sum() / total_sales
sales_df["_y"] = sales_df["Date"].dt.year
y22 = sales_df[sales_df["_y"] == 2022]["Net_Sales"].sum()
y23 = sales_df[sales_df["_y"] == 2023]["Net_Sales"].sum()
print(f"\n  Weekend/Weekday daily sales:  {weekend_avg/weekday_avg:.2f}x")
print(f"  Q4 share of total:             {q4_share:.1%}")
print(f"  2022 sales:  ${y22:,.0f}")
print(f"  2023 sales:  ${y23:,.0f}")
print(f"  YoY:                           {(y23/y22-1):+.1%}")
sales_df = sales_df.drop(columns=["_dow", "_m", "_y"])

# ----- Write back -----
print(f"\nWriting back to {XLSX_PATH.name}...")
try:
    with pd.ExcelWriter(XLSX_PATH, engine="openpyxl", mode="w") as w:
        sales_df.to_excel(w,  sheet_name="Sales_Transaction_Fact", index=False)
        labor_df.to_excel(w,  sheet_name="Labor_Operations_Fact",  index=False)
        employees.to_excel(w, sheet_name="Employee_Ref",           index=False)
        products.to_excel(w,  sheet_name="Product_Ref",            index=False)
        stores.to_excel(w,    sheet_name="Store_Hierarchy_Ref",    index=False)
except PermissionError:
    print("ERROR: File is open in Excel or Power BI. Close those and re-run.")
    raise

print(f"\nDONE. Now open Power BI Desktop, load .pbix, and tell Claude 'done'.")
