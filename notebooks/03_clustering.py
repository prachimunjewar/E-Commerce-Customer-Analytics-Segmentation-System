import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

rfm = pd.read_csv("data/rfm_data.csv")

# ── Scale Features ─────────────────────────────────────
features = rfm[["Recency", "Frequency", "Monetary"]]
scaler   = StandardScaler()
scaled   = scaler.fit_transform(features)

# ── Elbow Method ───────────────────────────────────────
inertia = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(scaled)
    inertia.append(km.inertia_)

plt.figure(figsize=(8,4))
plt.plot(K_range, inertia, "bo-")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method — Optimal K")
plt.xticks(K_range)
plt.grid(True)
plt.tight_layout()
plt.savefig("data/elbow_plot.png")
plt.show()

# ── Silhouette Score ───────────────────────────────────
sil_scores = []
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(scaled)
    sil_scores.append(silhouette_score(scaled, labels))

best_k = K_range[np.argmax(sil_scores)]
print(f"Best K by Silhouette Score: {best_k}")

plt.figure(figsize=(8,4))
plt.plot(K_range, sil_scores, "ro-")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Score per K")
plt.xticks(K_range)
plt.grid(True)
plt.tight_layout()
plt.savefig("data/silhouette_plot.png")
plt.show()

# ── Final Clustering ───────────────────────────────────
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
rfm["Cluster"] = kmeans.fit_predict(scaled)

# ── Cluster Summary ────────────────────────────────────
cluster_summary = rfm.groupby("Cluster").agg(
    Count     = ("customer_unique_id", "count"),
    Avg_Recency   = ("Recency",   "mean"),
    Avg_Frequency = ("Frequency", "mean"),
    Avg_Monetary  = ("Monetary",  "mean")
).reset_index()

print(cluster_summary)

# ── 3D Scatter Plot ────────────────────────────────────
fig = px.scatter_3d(rfm, x="Recency", y="Frequency", z="Monetary",
                    color=rfm["Cluster"].astype(str),
                    title="Customer Segments — 3D RFM View",
                    labels={"color": "Cluster"})
fig.show()

# ── Save ───────────────────────────────────────────────
rfm.to_csv("data/clustered_data.csv", index=False)
print("Clustered data saved!")