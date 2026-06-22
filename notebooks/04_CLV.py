import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import plotly.express as px

rfm = pd.read_csv("data/clustered_data.csv")

# ── CLV Target: Monetary × Frequency proxy ─────────────
rfm["CLV"] = rfm["Monetary"] * np.log1p(rfm["Frequency"])

# ── Features & Target ──────────────────────────────────
X = rfm[["Recency", "Frequency", "Monetary", "RFM_Total"]]
y = rfm["CLV"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# ── Train Models ───────────────────────────────────────
lr  = LinearRegression()
rf  = RandomForestRegressor(n_estimators=100, random_state=42)

lr.fit(X_train_s, y_train)
rf.fit(X_train_s, y_train)

# ── Evaluate ───────────────────────────────────────────
for name, model in [("Linear Regression", lr), ("Random Forest", rf)]:
    preds = model.predict(X_test_s)
    print(f"\n{name}")
    print(f"  MAE : {mean_absolute_error(y_test, preds):.2f}")
    print(f"  R²  : {r2_score(y_test, preds):.4f}")

# ── Add CLV Predictions to DataFrame ───────────────────
rfm["CLV_Predicted"] = rf.predict(scaler.transform(X))

# ── CLV by Segment ─────────────────────────────────────
clv_segment = rfm.groupby("Segment")["CLV_Predicted"].mean().reset_index()
clv_segment.columns = ["Segment", "Avg_CLV"]

fig = px.bar(clv_segment.sort_values("Avg_CLV", ascending=False),
             x="Segment", y="Avg_CLV",
             title="Average Predicted CLV by Segment",
             color="Avg_CLV", color_continuous_scale="RdYlGn")
fig.show()

# ── Revenue Contribution by Segment ────────────────────
seg_revenue = rfm.groupby("Segment")["Monetary"].sum().reset_index()
fig2 = px.pie(seg_revenue, names="Segment", values="Monetary",
              title="Revenue Contribution by Segment")
fig2.show()

# ── Save Final Data ────────────────────────────────────
rfm.to_csv("data/final_data.csv", index=False)
print("Final data saved!")