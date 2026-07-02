# ============================================================
# app.py — CustomerLens: Customer Segmentation Dashboard
# Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

st.set_page_config(page_title="CustomerLens", page_icon="🏷️", layout="wide")

# ── DESIGN TOKENS ────────────────────────────────────────────
# Palette: "ledger / price-tag" — paper surface, ink text, a muted
# retail-tag colorway for segments instead of default chart colors.
BG        = "#F3F1EA"   # paper background
SURFACE   = "#EDEAE0"   # sidebar / recessed surface
CARD      = "#FDFCF9"   # card surface (lighter than paper -> punch-hole works)
INK       = "#1C201B"   # near-black text
INK_SOFT  = "#5B6058"   # muted secondary text
LINE      = "#D6D0C0"   # hairline / dashed rule color

SEGMENT_PALETTE = ["#2F6F4F", "#C98A2C", "#B4533C", "#3E6494", "#7A5C7E", "#6E7A3B"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {{ font-family: 'Public Sans', sans-serif; }}

.stApp {{ background: {BG}; color: {INK}; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px dashed {LINE};
}}
[data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {{
    color: {INK_SOFT} !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: {CARD} !important;
    border: 1px solid {LINE} !important;
    border-radius: 4px !important;
}}

.main .block-container {{ padding: 1.6rem 2.2rem 2.4rem; max-width: 1360px; }}

/* ── Masthead ── */
.eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {INK_SOFT};
    margin-bottom: 6px;
}}
.masthead-title {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: {INK};
    line-height: 1.05;
}}
.masthead-sub {{
    font-size: 0.9rem;
    color: {INK_SOFT};
    margin-top: 6px;
}}
.masthead-rule {{
    border: none;
    border-top: 1px dashed {LINE};
    margin: 18px 0 26px;
}}

/* ── Section eyebrow headers ── */
.section-eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {INK_SOFT};
    display: flex; align-items: center; gap: 10px;
    margin: 30px 0 14px;
}}
.section-eyebrow::after {{
    content: ''; flex: 1; height: 0; border-top: 1px dashed {LINE};
}}

/* ── Tag-style KPI cards ── */
.tag-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
.tag-card {{
    position: relative;
    background: {CARD};
    border: 1px solid {LINE};
    border-radius: 6px;
    padding: 16px 18px 16px 30px;
}}
.tag-card::before {{
    content: '';
    position: absolute; left: -8px; top: 50%; transform: translateY(-50%);
    width: 15px; height: 15px; border-radius: 50%;
    background: {BG}; border: 1px solid {LINE};
}}
.tag-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.64rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: {INK_SOFT}; margin-bottom: 8px;
}}
.tag-value {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.7rem; font-weight: 700; letter-spacing: -0.01em; color: {INK};
}}
.tag-swatch {{
    display: inline-block; width: 8px; height: 8px; border-radius: 2px;
    margin-right: 6px; position: relative; top: -1px;
}}

/* ── Chart card wrapper ── */
.chart-card {{
    background: {CARD}; border: 1px solid {LINE}; border-radius: 8px;
    padding: 16px 18px 6px;
}}
.chart-title {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.02rem; font-weight: 600; color: {INK}; margin-bottom: 2px;
}}
.chart-note {{ font-size: 0.76rem; color: {INK_SOFT}; margin-bottom: 6px; }}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{ background: {CARD}; border-radius: 8px; border: 1px solid {LINE}; }}
[data-testid="stDataFrame"] th {{
    background: {SURFACE} !important; color: {INK_SOFT} !important;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem;
    letter-spacing: 0.06em; text-transform: uppercase;
}}
[data-testid="stDataFrame"] td {{ color: {INK} !important; font-size: 0.82rem; }}

[data-testid="stExpander"] {{ background: {CARD} !important; border: 1px solid {LINE} !important; border-radius: 8px !important; }}

h1, h2, h3 {{ color: {INK} !important; }}
.stCaption, [data-testid="stCaptionContainer"] {{ color: {INK_SOFT} !important; }}
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ─────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Public Sans", color=INK_SOFT, size=11),
    xaxis=dict(gridcolor=LINE, zerolinecolor=LINE, tickcolor=LINE, linecolor=LINE),
    yaxis=dict(gridcolor=LINE, zerolinecolor=LINE, tickcolor=LINE, linecolor=LINE),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=LINE),
    margin=dict(l=10, r=10, t=10, b=10),
    colorway=SEGMENT_PALETTE,
)

def themed(fig, height=320, **overrides):
    """Apply CHART_THEME with safe overrides (merges instead of double-passing
    keys like xaxis/yaxis/legend, which would raise a duplicate-kwarg error)."""
    layout = {**CHART_THEME, **overrides}
    fig.update_layout(height=height, **layout)
    return fig

def chart_card(title, note=""):
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-title">{title}</div>
        <div class="chart-note">{note}</div>
    """, unsafe_allow_html=True)

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────
DATA_PATH = "data/final_data.csv"

if not os.path.exists(DATA_PATH):
    st.warning(f"⚠️ Data file not found at `{DATA_PATH}`. Run the pipeline that produces it, then reload.")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

segments_all = sorted(df["Segment"].unique().tolist())
seg_color = {seg: SEGMENT_PALETTE[i % len(SEGMENT_PALETTE)] for i, seg in enumerate(segments_all)}

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="eyebrow">Filter</div>', unsafe_allow_html=True)
    st.markdown("### Segments")
    segment = st.multiselect("Select segment", options=segments_all, default=segments_all, label_visibility="collapsed")
    st.markdown("---")
    st.caption(f"{len(df):,} customers · {len(segments_all)} segments")
    st.caption("RFM + K-Means + CLV")

filtered = df[df["Segment"].isin(segment)] if segment else df.iloc[0:0]

# ── MASTHEAD ──────────────────────────────────────────────────
st.markdown(f"""
<div class="eyebrow">Customer Intelligence · RFM · K-Means · CLV</div>
<div class="masthead-title">CustomerLens 🏷️</div>
<div class="masthead-sub">Who your customers are, what they're worth, and where to focus next.</div>
<hr class="masthead-rule" />
""", unsafe_allow_html=True)

if filtered.empty:
    st.info("Select at least one segment in the sidebar to see results.")
    st.stop()

# ── KPI TAGS ──────────────────────────────────────────────────
total_customers = filtered["customer_unique_id"].nunique()
total_revenue   = filtered["Monetary"].sum()
avg_clv         = filtered["CLV_Predicted"].mean()
n_segments      = filtered["Segment"].nunique()

st.markdown(f"""
<div class="tag-row">
    <div class="tag-card">
        <div class="tag-label">Customers</div>
        <div class="tag-value">{total_customers:,}</div>
    </div>
    <div class="tag-card">
        <div class="tag-label">Total Revenue</div>
        <div class="tag-value">R$ {total_revenue:,.0f}</div>
    </div>
    <div class="tag-card">
        <div class="tag-label">Avg Predicted CLV</div>
        <div class="tag-value">R$ {avg_clv:,.0f}</div>
    </div>
    <div class="tag-card">
        <div class="tag-label">Segments in View</div>
        <div class="tag-value">{n_segments}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SEGMENT LEADERBOARD (ranked — order carries real meaning here) ──
st.markdown('<div class="section-eyebrow">Segment leaderboard, by revenue</div>', unsafe_allow_html=True)

leaderboard = (filtered.groupby("Segment")
               .agg(customers=("customer_unique_id", "nunique"),
                    revenue=("Monetary", "sum"),
                    avg_clv=("CLV_Predicted", "mean"),
                    avg_recency=("Recency", "mean"),
                    avg_frequency=("Frequency", "mean"))
               .sort_values("revenue", ascending=False)
               .reset_index())
leaderboard.insert(0, "Rank", range(1, len(leaderboard) + 1))

legend_html = "".join(
    f'<span class="tag-swatch" style="background:{seg_color[s]}"></span>{s}&nbsp;&nbsp;&nbsp;'
    for s in leaderboard["Segment"]
)
st.markdown(f'<div style="font-size:0.8rem; color:{INK_SOFT}; margin-bottom:10px;">{legend_html}</div>', unsafe_allow_html=True)

st.dataframe(
    leaderboard.style.format({
        "revenue": "R$ {:,.0f}",
        "avg_clv": "R$ {:,.0f}",
        "avg_recency": "{:.0f} days",
        "avg_frequency": "{:.1f}",
    }),
    use_container_width=True, hide_index=True
)

# ── ROW 1: Revenue rank + Revenue share ─────────────────────
st.markdown('<div class="section-eyebrow">Segment performance</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    chart_card("Revenue by segment", "Ranked highest to lowest")
    seg_rev = leaderboard.sort_values("revenue")
    fig1 = go.Figure(go.Bar(
        y=seg_rev["Segment"], x=seg_rev["revenue"], orientation="h",
        marker=dict(color=[seg_color[s] for s in seg_rev["Segment"]]),
        text=seg_rev["revenue"].map(lambda v: f"R$ {v:,.0f}"),
        textposition="outside", textfont=dict(color=INK_SOFT, size=10),
    ))
    themed(fig1, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    end_card()

with col2:
    chart_card("Revenue share", "Proportion of total revenue")
    fig2 = px.pie(filtered, names="Segment", values="Monetary", hole=0.55,
                  color="Segment", color_discrete_map=seg_color)
    fig2.update_traces(textinfo="percent", marker=dict(line=dict(color=BG, width=2)))
    themed(fig2, showlegend=True, legend=dict(orientation="h", y=-0.1, bgcolor="rgba(0,0,0,0)", bordercolor=LINE))
    st.plotly_chart(fig2, use_container_width=True)
    end_card()

# ── ROW 2: RFM scatter + Avg CLV ─────────────────────────────
st.markdown('<div class="section-eyebrow">Customer behavior</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    chart_card("Recency vs. revenue", "Bubble size = predicted CLV")
    fig3 = px.scatter(filtered, x="Recency", y="Monetary", color="Segment",
                       size="CLV_Predicted", color_discrete_map=seg_color,
                       hover_data=["Frequency"])
    themed(fig3, height=340, legend=dict(orientation="h", y=-0.18, bgcolor="rgba(0,0,0,0)", bordercolor=LINE))
    st.plotly_chart(fig3, use_container_width=True)
    end_card()

with col4:
    chart_card("Avg predicted CLV by segment", "Lifetime value estimate")
    clv_seg = leaderboard.sort_values("avg_clv")
    fig4 = go.Figure(go.Bar(
        y=clv_seg["Segment"], x=clv_seg["avg_clv"], orientation="h",
        marker=dict(color=[seg_color[s] for s in clv_seg["Segment"]]),
        text=clv_seg["avg_clv"].map(lambda v: f"R$ {v:,.0f}"),
        textposition="outside", textfont=dict(color=INK_SOFT, size=10),
    ))
    themed(fig4, height=340, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    end_card()

# ── ROW 3: Frequency + Recency spread ────────────────────────
st.markdown('<div class="section-eyebrow">Distribution &amp; spread</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    chart_card("Avg purchase frequency", "Orders per customer, by segment")
    freq = leaderboard.sort_values("avg_frequency")
    fig5 = go.Figure(go.Bar(
        y=freq["Segment"], x=freq["avg_frequency"], orientation="h",
        marker=dict(color=[seg_color[s] for s in freq["Segment"]]),
        text=freq["avg_frequency"].map(lambda v: f"{v:.1f}"),
        textposition="outside", textfont=dict(color=INK_SOFT, size=10),
    ))
    themed(fig5, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    end_card()

with col6:
    chart_card("Recency distribution", "Days since last purchase, by segment")
    fig6 = px.box(filtered, x="Segment", y="Recency", color="Segment", color_discrete_map=seg_color)
    themed(fig6, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)
    end_card()

# ── RAW DATA ──────────────────────────────────────────────────
st.markdown('<div class="section-eyebrow">Raw data</div>', unsafe_allow_html=True)
with st.expander("View filtered customer records"):
    st.dataframe(
        filtered[["customer_unique_id", "Segment", "Recency", "Frequency", "Monetary", "CLV_Predicted"]],
        use_container_width=True, hide_index=True
    )

st.caption("CustomerLens — Python · MySQL · K-Means · RFM · Streamlit")
