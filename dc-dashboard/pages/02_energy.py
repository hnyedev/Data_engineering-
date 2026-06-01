import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_pue_trend, get_energy_breakdown, get_monthly_energy
from utils.charts import pue_trend_chart, energy_donut, monthly_energy_chart

st.set_page_config(page_title="Energy · DC Dashboard", layout="wide")
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

st.markdown("""<div class="page-header"><h1>⚡ Energy Efficiency</h1><p>PUE benchmarking, consumption analytics & interactive calculator — Unit 3</p></div>""", unsafe_allow_html=True)

pue_df   = get_pue_trend()
energy_df = get_energy_breakdown()
monthly_df = get_monthly_energy()

current_pue = float(pue_df["pue"].iloc[-1])
it_load_kw  = float(monthly_df["it_load_kw"].iloc[-1])
total_kw    = it_load_kw * current_pue
overhead_kw = total_kw - it_load_kw

# ── KPIs ─────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current PUE",      f"{current_pue:.2f}",  "-0.03 vs Jan")
c2.metric("IT Load",          f"{it_load_kw:.0f} kW", "+100 kW")
c3.metric("Total Facility",   f"{total_kw:.0f} kW",  "")
c4.metric("Overhead (waste)", f"{overhead_kw:.0f} kW", "")

# ── PUE Trend ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">PUE Trend — 2022 to 2024</p>', unsafe_allow_html=True)
st.plotly_chart(pue_trend_chart(pue_df), use_container_width=True, config={"displayModeBar": False})
st.caption("Source: Uptime Institute Global DC Survey 2024 — Global avg PUE 1.58 | Hyperscaler avg 1.20")

# ── Energy Breakdown ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Energy Consumption Breakdown</p>', unsafe_allow_html=True)
col_a, col_b = st.columns([1, 1])
with col_a:
    st.plotly_chart(energy_donut(energy_df), use_container_width=True, config={"displayModeBar": False})
with col_b:
    st.plotly_chart(monthly_energy_chart(monthly_df), use_container_width=True, config={"displayModeBar": False})

# ── PUE Calculator ────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Interactive PUE Calculator</p>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    it_input   = st.number_input("IT Equipment Load (kW)", min_value=10, max_value=50000, value=4200, step=100)
with col2:
    cool_input = st.number_input("Cooling Load (kW)", min_value=0, max_value=30000, value=2450, step=50)
with col3:
    other_input = st.number_input("Other Overhead (kW)", min_value=0, max_value=10000, value=920, step=10)

total_input = it_input + cool_input + other_input
calc_pue    = total_input / it_input
savings_kw  = (calc_pue - 1.40) * it_input   # vs target PUE 1.40

r1, r2, r3, r4 = st.columns(4)
r1.metric("Calculated PUE",   f"{calc_pue:.3f}")
r2.metric("Total Facility kW", f"{total_input:,}")
r3.metric("vs Target (1.40)",  f"{calc_pue - 1.40:+.3f}")
r4.metric("Waste vs Target",   f"{savings_kw:.0f} kW", help="kW that could be saved if PUE = 1.40")

rating = "🏆 Excellent" if calc_pue < 1.3 else ("✅ Good" if calc_pue < 1.5 else ("⚠️ Average" if calc_pue < 1.7 else "❌ Poor"))
st.info(f"**PUE Rating:** {rating} — Uptime Institute benchmark: <1.2 Hyperscale · 1.2–1.5 Good · 1.5–2.0 Average · >2.0 Poor")
st.markdown('</div>', unsafe_allow_html=True)