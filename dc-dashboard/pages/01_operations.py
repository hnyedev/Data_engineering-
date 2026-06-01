import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_sla_data, get_incident_log, get_mac_table
from utils.charts import sla_gauge

st.set_page_config(page_title="Operations · DC Dashboard", layout="wide")
st.markdown(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")).read().split("# ── Landing")[0].split("st.set_page_config")[0], unsafe_allow_html=True) if False else None

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

st.markdown("""<div class="page-header"><h1>🔧 Operations</h1><p>SLA compliance, incident management & change control — Unit 3</p></div>""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
sla_df = get_sla_data()
inc_df = get_incident_log()
mac_df = get_mac_table()

open_incidents  = len(inc_df[inc_df["status"] == "Open"])
avg_mttr        = inc_df["mttr_min"].mean()
pending_macs    = len(mac_df[mac_df["status"].isin(["Pending","In Progress"])])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tier III SLA",   "99.982%",  "+0.001%")
c2.metric("Open Incidents", open_incidents, f"-{2 - open_incidents} vs last month")
c3.metric("Avg MTTR",       f"{avg_mttr:.0f} min", "-8 min")
c4.metric("Pending MACs",   pending_macs, "")

# ── SLA Gauges ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Uptime SLA Gauges — Uptime Institute Tiers</p>', unsafe_allow_html=True)
cols = st.columns(4)
for i, row in sla_df.iterrows():
    with cols[i]:
        st.plotly_chart(
            sla_gauge(row["sla"], row["tier"], f'{row["label"]} · {row["redundancy"]}'),
            use_container_width=True, config={"displayModeBar": False}
        )
        st.caption(f"Max downtime: **{row['downtime_hrs']} hrs/yr**")

# ── Incident Log ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Incident Log</p>', unsafe_allow_html=True)

sev_filter = st.multiselect("Filter by Severity", ["P1","P2","P3","P4"], default=["P1","P2","P3","P4"])
filtered = inc_df[inc_df["severity"].isin(sev_filter)]

def color_severity(val):
    colors = {"P1": "background-color:#F8D7DA", "P2": "background-color:#FFF3CD",
               "P3": "background-color:#D4EDDA", "P4": "background-color:#D1ECF1"}
    return colors.get(val, "")

def color_status(val):
    return "background-color:#F8D7DA;font-weight:bold" if val == "Open" else ""

styled = filtered.style\
    .applymap(color_severity, subset=["severity"])\
    .applymap(color_status, subset=["status"])

st.dataframe(styled, use_container_width=True, hide_index=True)

# ── MAC Table ─────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">MAC Process Table — Moves / Adds / Changes</p>', unsafe_allow_html=True)

status_colors = {"Completed":"🟢","In Progress":"🟡","Pending":"🔵","Approved":"🟠"}
mac_display = mac_df.copy()
mac_display["status"] = mac_display["status"].map(lambda s: f"{status_colors.get(s,'')} {s}")

st.dataframe(mac_display, use_container_width=True, hide_index=True)