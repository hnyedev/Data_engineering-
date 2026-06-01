import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_tech_radar, get_adoption_timeline
from utils.charts import tech_radar_chart, adoption_timeline_chart

st.set_page_config(page_title="Emerging Tech · DC Dashboard", layout="wide")
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

st.markdown("""<div class="page-header"><h1>🚀 Emerging Technologies</h1><p>Technology radar, adoption timeline 2024–2030 & strategic recommendations — Unit 4</p></div>""", unsafe_allow_html=True)

radar_df    = get_tech_radar()
timeline_df = get_adoption_timeline()

adopt_count  = len(radar_df[radar_df["maturity"] == "Adopt"])
trial_count  = len(radar_df[radar_df["maturity"] == "Trial"])
assess_count = len(radar_df[radar_df["maturity"] == "Assess"])
hold_count   = len(radar_df[radar_df["maturity"] == "Hold"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Adopt Now",    adopt_count,  "Deploy immediately")
c2.metric("Trial Phase",  trial_count,  "Pilot projects")
c3.metric("Assess",       assess_count, "Monitor closely")
c4.metric("Hold",         hold_count,   "Not yet viable")

# ── Tech Radar ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Technology Radar — Maturity vs Horizon</p>', unsafe_allow_html=True)
st.caption("Bubble size = Readiness Level (1–5). Position = target adoption year.")
st.plotly_chart(tech_radar_chart(radar_df), use_container_width=True, config={"displayModeBar": False})

# ── Radar Table ───────────────────────────────────────────────────────────────
with st.expander("📋 Full Technology Detail Table"):
    maturity_icon = {"Adopt":"🟢 Adopt","Trial":"🔵 Trial","Assess":"🟡 Assess","Hold":"🔴 Hold"}
    display = radar_df.copy()
    display["maturity"] = display["maturity"].map(maturity_icon)
    st.dataframe(display[["technology","category","maturity","horizon_yr","impact","readiness"]],
                 use_container_width=True, hide_index=True)

# ── Adoption Timeline ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Adoption Timeline 2022–2030</p>', unsafe_allow_html=True)
st.plotly_chart(adoption_timeline_chart(timeline_df), use_container_width=True, config={"displayModeBar": False})

# ── Strategic Recommendations ─────────────────────────────────────────────────
st.markdown('<p class="section-title">Strategic Recommendations</p>', unsafe_allow_html=True)

recs = [
    ("badge-info", "🏗 Immediate (2024–2025)",
     "Deploy **liquid cooling (DtC)** for GPU/AI racks — PUE reduction 0.15–0.25 pts. "
     "Upgrade backbone to **400G** for AI workload throughput. "
     "Sign **renewable PPA** with CFE wind assets (Oaxaca corridor)."),
    ("badge-warn", "🔬 Short-Term (2025–2026)",
     "Pilot **AI-driven DCIM** for predictive cooling and capacity management. "
     "Deploy **digital twin** of the facility for ops simulation. "
     "Begin **NVMe-oF** fabric trial for storage consolidation."),
    ("badge-ok", "🔭 Medium-Term (2026–2028)",
     "Evaluate **immersion cooling** for next-gen GPU clusters (>1 kW/chip). "
     "Initiate **quantum-safe encryption** migration for cross-DC links. "
     "Assess **hydrogen fuel cells** as backup power alternative."),
    ("badge-crit", "🌐 Mexico-Specific Opportunity",
     "Querétaro and Mérida show **+32–40% YoY growth** — "
     "nearshoring demand from US firms drives colocation absorption. "
     "Edge DC deployment near automotive clusters (Saltillo, San Luis Potosí) represents "
     "an underserved $120M+ market segment."),
]

for badge_class, title, body in recs:
    st.markdown(f"""<div class="card">
        <span class="{badge_class}">{title}</span><br><br>
        <span>{body}</span>
    </div>""", unsafe_allow_html=True)