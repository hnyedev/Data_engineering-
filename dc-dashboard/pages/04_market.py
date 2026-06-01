import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_mexico_market, get_deployment_models, get_market_growth
from utils.charts import market_capacity_chart, market_growth_chart

st.set_page_config(page_title="Market · DC Dashboard", layout="wide")
st.markdown("""<style>
/* ── FONTS ───────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');

* { font-family: 'Roboto', sans-serif; }

/* ── SIDEBAR ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #F4F6FF;
    border-right: 1px solid #E8E8E8;
}
[data-testid="stSidebarNav"] a {
    color: #1E2A6E;
    font-weight: 600;
    font-size: 0.92rem;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    display: block;
}
[data-testid="stSidebarNav"] a:hover {
    color: #3F5BD9;
    background: #E8EDFF;
}

/* ── METRIC CARDS ────────────────────────────────── */
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-left: 4px solid #3F5BD9;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(63,91,217,0.07);
}
div[data-testid="metric-container"] label {
    color: #666666 !important;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1E2A6E !important;
    font-size: 1.6rem;
    font-weight: 700;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #28A745;
    font-size: 0.82rem;
}

/* ── PAGE HERO BANNER ────────────────────────────── */
.page-header {
    background: linear-gradient(135deg, #3F5BD9 0%, #2A3AA8 100%);
    color: #FFFFFF;
    padding: 1.4rem 2rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    color: #FFFFFF;
    margin: 0;
    font-size: 1.6rem;
    font-weight: 700;
}
.page-header p {
    color: #C5D0FF;
    margin: 0.3rem 0 0;
    font-size: 0.88rem;
}

/* ── SECTION TITLES ──────────────────────────────── */
.section-title {
    color: #1E2A6E;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border-bottom: 2px solid #F5821A;
    padding-bottom: 4px;
    margin: 1.5rem 0 1rem;
}

/* ── GENERIC CARD ────────────────────────────────── */
.card {
    background: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-radius: 6px;
    padding: 1.2rem;
    box-shadow: 0 2px 8px rgba(63,91,217,0.07);
    margin-bottom: 1rem;
}

/* ── BADGES ──────────────────────────────────────── */
.badge-ok   { background:#D4EDDA; color:#1A5E2B; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
.badge-warn { background:#FFF3CD; color:#856404; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
.badge-crit { background:#F8D7DA; color:#842029; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
.badge-info { background:#D1ECF1; color:#0C5460; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }

/* ── ORANGE ACCENT BUTTON ────────────────────────── */
.btn-orange {
    background: #F5821A;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
}

/* ── DATAFRAME OVERRIDES ─────────────────────────── */
[data-testid="stDataFrame"] thead tr th {
    background-color: #3F5BD9 !important;
    color: #FFFFFF !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #F4F6FF !important;
}

/* ── DIVIDER ─────────────────────────────────────── */
hr {
    border: none;
    border-top: 1px solid #E8E8E8;
    margin: 1.2rem 0;
}

/* ── EXPANDER ────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #E8E8E8;
    border-radius: 6px;
}

/* ── MULTISELECT TAGS ────────────────────────────── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #3F5BD9;
    color: #FFFFFF;
}

/* ── INFO / WARNING BOXES ────────────────────────── */
[data-testid="stInfo"]    { border-left: 4px solid #3F5BD9; }
[data-testid="stWarning"] { border-left: 4px solid #F5821A; }
[data-testid="stError"]   { border-left: 4px solid #DC3545; }
[data-testid="stSuccess"] { border-left: 4px solid #28A745; }
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="page-header"><h1>📊 Market Intelligence — Mexico</h1><p>DC capacity, regional hotspots, operators & deployment models — Unit 4</p></div>""", unsafe_allow_html=True)

mkt_df   = get_mexico_market()
dep_df   = get_deployment_models()
grow_df  = get_market_growth()

total_mw    = mkt_df["capacity_mw"].sum()
avg_util    = mkt_df["utilization_pct"].mean()
fastest     = mkt_df.loc[mkt_df["yoy_growth_pct"].idxmax(), "city"]
fastest_pct = mkt_df["yoy_growth_pct"].max()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total MX Capacity",  f"{total_mw} MW",       "+18 MW vs 2023")
c2.metric("Avg Utilization",    f"{avg_util:.0f}%",      "+4pp YoY")
c3.metric("Fastest Growing",    fastest,                 f"+{fastest_pct}% YoY")
c4.metric("Avg Rack Price",     "~$290 USD/mo",          "vs $450 US avg")

# ── Market Charts ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Installed Capacity by City</p>', unsafe_allow_html=True)
col_a, col_b = st.columns([3, 2])
with col_a:
    st.plotly_chart(market_capacity_chart(mkt_df), use_container_width=True, config={"displayModeBar": False})
with col_b:
    st.markdown('<p class="section-title">Regional Hotspots</p>', unsafe_allow_html=True)
    for _, row in mkt_df.iterrows():
        util_bar = "█" * int(row["utilization_pct"] / 10) + "░" * (10 - int(row["utilization_pct"] / 10))
        st.markdown(f"""<div class="card">
            <b>{row['city']}</b> — {row['region']}<br>
            <small>🏗 {row['capacity_mw']} MW &nbsp;|&nbsp; 📈 +{row['yoy_growth_pct']}% YoY</small><br>
            <small>Utilization: {util_bar} {row['utilization_pct']}%</small><br>
            <small>💼 {row['operators']}</small>
        </div>""", unsafe_allow_html=True)

# ── Growth Forecast ────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Market Growth & Investment Forecast</p>', unsafe_allow_html=True)
st.plotly_chart(market_growth_chart(grow_df), use_container_width=True, config={"displayModeBar": False})
st.caption("Sources: CBRE Mexico DC Market Report 2024 · JLL Data Center Outlook 2024 · Nearshore Americas")

# ── Deployment Models ─────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Deployment Models Comparison</p>', unsafe_allow_html=True)

def badge(val):
    classes = {"Low": "badge-ok", "Medium": "badge-warn", "High": "badge-crit", "Full": "badge-info"}
    return f'<span class="{classes.get(val, "badge-info")}">{val}</span>'

cols = st.columns(len(dep_df))
for i, (_, row) in enumerate(dep_df.iterrows()):
    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <b>{row['model']}</b><br><br>
            CapEx: {badge(row['capex'])}<br><br>
            OpEx: {badge(row['opex'])}<br><br>
            Control: {badge(row['control'])}<br><br>
            Scale: {badge(row['scalability'])}<br><br>
            <small>{row['best_for']}</small>
        </div>
        """, unsafe_allow_html=True)