import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CustomerLens", page_icon="🛍️", layout="wide")
st.title("🛍️ CustomerLens — Customer Segmentation Dashboard")

# ── Load Data ──────────────────────────────────────────
df = pd.read_csv("data/final_data.csv")

# ── KPI Row ────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{df['customer_unique_id'].nunique():,}")
col2.metric("Total Revenue", f"R$ {df['Monetary'].sum():,.0f}")
col3.metric("Avg CLV", f"R$ {df['CLV_Predicted'].mean():,.0f}")
col4.metric("Total Segments", df["Segment"].nunique())

st.divider()

# ── Sidebar ────────────────────────────────────────────
st.sidebar.title("Filters")
segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)
filtered = df[df["Segment"].isin(segment)]

# ── Row 1 Charts ───────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    seg_rev = filtered.groupby("Segment")["Monetary"].sum().reset_index()
    fig1 = px.bar(seg_rev, x="Segment", y="Monetary",
                  title="💰 Revenue by Segment",
                  color="Monetary", color_continuous_scale="Blues")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(filtered, names="Segment", values="Monetary",
                  title="📊 Revenue Share by Segment")
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2 Charts ───────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    fig3 = px.scatter(filtered, x="Recency", y="Monetary",
                      color="Segment", size="CLV_Predicted",
                      title="🎯 RFM Scatter — Recency vs Revenue",
                      hover_data=["Frequency"])
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    clv_seg = filtered.groupby("Segment")["CLV_Predicted"].mean().reset_index()
    fig4 = px.bar(clv_seg, x="Segment", y="CLV_Predicted",
                  title="📈 Avg Predicted CLV by Segment",
                  color="CLV_Predicted", color_continuous_scale="Greens")
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3 Charts ───────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    freq = filtered.groupby("Segment")["Frequency"].mean().reset_index()
    fig5 = px.bar(freq, x="Segment", y="Frequency",
                  title="🔁 Avg Purchase Frequency by Segment",
                  color="Frequency", color_continuous_scale="Oranges")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    fig6 = px.box(filtered, x="Segment", y="Recency",
                  title="📦 Recency Distribution by Segment",
                  color="Segment")
    st.plotly_chart(fig6, use_container_width=True)

# ── Raw Data ───────────────────────────────────────────
st.divider()
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered[[
        "customer_unique_id","Segment","Recency",
        "Frequency","Monetary","CLV_Predicted"
    ]], use_container_width=True)

st.caption("CustomerLens — Built with Python, MySQL, K-Means, RFM & Streamlit")