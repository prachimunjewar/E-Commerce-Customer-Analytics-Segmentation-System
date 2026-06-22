import pandas as pd
import numpy as np

df = pd.read_csv("data/raw_data.csv", parse_dates=["order_purchase_timestamp"])

# ── Reference Date (day after last order) ──────────────
reference_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

# ── RFM Calculation ────────────────────────────────────
rfm = df.groupby("customer_unique_id").agg(
    Recency   = ("order_purchase_timestamp", lambda x: (reference_date - x.max()).days),
    Frequency = ("order_id", "nunique"),
    Monetary  = ("payment_value", "sum")
).reset_index()

print(rfm.shape)
print(rfm.describe())

# ── RFM Scoring (1–5 scale) ────────────────────────────
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    q=5,
    labels=[5,4,3,2,1]
)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1,2,3,4,5]
)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    q=5,
    labels=[1,2,3,4,5]
)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

rfm["RFM_Total"] = (
    rfm[["R_Score", "F_Score", "M_Score"]]
    .astype(int)
    .sum(axis=1)
)
# ── Segment Labels ─────────────────────────────────────
def segment_customer(score):
    if score >= 12:
        return "Champions"
    elif score >= 9:
        return "Loyal Customers"
    elif score >= 6:
        return "At Risk"
    elif score >= 3:
        return "Hibernating"
    else:
        return "Lost"

rfm["Segment"] = rfm["RFM_Total"].apply(segment_customer)

print(rfm["Segment"].value_counts())
print(rfm.head())

# ── Save ───────────────────────────────────────────────
rfm.to_csv("data/rfm_data.csv", index=False)
print("RFM data saved!")