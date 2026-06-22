import pandas as pd
import numpy as np
import plotly.express as px

# ── Load Data ──────────────────────────────────────────
df = pd.read_csv("D:/PROJECTS/customer segmentation/data/raw_data.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nNull Values:\n", df.isnull().sum())
print("\nBasic Stats:\n", df.describe())

# ── 1. Monthly Revenue ─────────────────────────────────
df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
monthly = df.groupby("month")["payment_value"].sum().reset_index()

fig1 = px.line(monthly, x="month", y="payment_value",
               title="Monthly Revenue Trend",
               labels={"payment_value": "Revenue (BRL)", "month": "Month"})
fig1.show()

# ── 2. Top 10 States by Orders ─────────────────────────
state_orders = df.groupby("customer_state")["order_id"].nunique().reset_index()
state_orders.columns = ["state", "order_count"]
state_orders = state_orders.sort_values("order_count", ascending=False).head(10)

fig2 = px.bar(state_orders, x="state", y="order_count",
              title="Top 10 States by Orders",
              color="order_count", color_continuous_scale="Blues")
fig2.show()

# ── 3. Payment Type Distribution ───────────────────────
payment = df["payment_type"].value_counts().reset_index()
payment.columns = ["payment_type", "count"]

fig3 = px.pie(payment, names="payment_type", values="count",
              title="Payment Type Distribution")
fig3.show()

# ── 4. Revenue Distribution ────────────────────────────
fig4 = px.histogram(df, x="payment_value", nbins=50,
                    title="Payment Value Distribution",
                    labels={"payment_value": "Payment Value (BRL)"})
fig4.show()

# ── 5. Top 10 Cities by Revenue ────────────────────────
city = df.groupby("customer_city")["payment_value"].sum().reset_index()
city = city.sort_values("payment_value", ascending=False).head(10)

fig5 = px.bar(city, x="customer_city", y="payment_value",
              title="Top 10 Cities by Revenue",
              color="payment_value", color_continuous_scale="Viridis")
fig5.show()

print("\n✅ EDA Complete!")