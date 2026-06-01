import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_loader import get_tia942_checklist, get_iso27001_controls
from utils.charts import compliance_bar

st.set_page_config(page_title="Security · DC Dashboard", layout="wide")
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

st.markdown("""<div class="page-header"><h1>🔒 Security & Compliance</h1><p>TIA-942 physical controls, ISO 27001:2022 audit status — Unit 3</p></div>""", unsafe_allow_html=True)

tia_df = get_tia942_checklist()
iso_df = get_iso27001_controls()

pass_count    = len(tia_df[tia_df["status"] == "Pass"])
partial_count = len(tia_df[tia_df["status"] == "Partial"])
fail_count    = len(tia_df[tia_df["status"] == "Fail"])
tia_score     = round((pass_count + partial_count * 0.5) / len(tia_df) * 100, 1)
iso_score     = round(iso_df["score"].mean(), 1)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("TIA-942 Score",     f"{tia_score}%")
c2.metric("Controls Passed",   pass_count)
c3.metric("Partial Controls",  partial_count)
c4.metric("Failed Controls",   fail_count)
c5.metric("ISO 27001 Avg",     f"{iso_score}%")

# ── TIA-942 Checklist ─────────────────────────────────────────────────────────
st.markdown('<p class="section-title">TIA-942 Compliance Checklist</p>', unsafe_allow_html=True)

domain_filter = st.multiselect(
    "Filter by Domain",
    options=tia_df["domain"].unique().tolist(),
    default=tia_df["domain"].unique().tolist()
)
filtered = tia_df[tia_df["domain"].isin(domain_filter)].copy()

status_icon = {"Pass": "✅ Pass", "Partial": "⚠️ Partial", "Fail": "❌ Fail"}
risk_icon   = {"Low": "🟢 Low", "Med": "🟡 Medium", "High": "🔴 High"}
filtered["status"] = filtered["status"].map(status_icon)
filtered["risk"]   = filtered["risk"].map(risk_icon)

st.dataframe(filtered[["domain","control","tier_req","status","risk"]],
             use_container_width=True, hide_index=True)

col1, col2, col3 = st.columns(3)
col1.metric("", f"✅ {pass_count} Passed")
col2.metric("", f"⚠️ {partial_count} Partial")
col3.metric("", f"❌ {fail_count} Failed")

# ── ISO 27001 ─────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">ISO 27001:2022 Control Scores</p>', unsafe_allow_html=True)
col_a, col_b = st.columns([3, 2])
with col_a:
    st.plotly_chart(compliance_bar(iso_df), use_container_width=True, config={"displayModeBar": False})
with col_b:
    st.subheader("Audit Summary")
    for clause in iso_df["clause"].unique():
        sub = iso_df[iso_df["clause"] == clause]
        avg = sub["score"].mean()
        impl = len(sub[sub["status"] == "Implemented"])
        total = len(sub)
        color = "🟢" if avg >= 85 else ("🟡" if avg >= 70 else "🔴")
        st.markdown(f"{color} **{clause}** — avg {avg:.0f}% ({impl}/{total} implemented)")

    st.divider()
    st.markdown("**Standard:** ISO/IEC 27001:2022")
    st.markdown("**Last Audit:** September 2024")
    st.markdown("**Next Review:** March 2025")
    st.markdown("**Certification Body:** Bureau Veritas")

# ── Physical Security Controls ────────────────────────────────────────────────
st.markdown('<p class="section-title">Physical Security Control Summary</p>', unsafe_allow_html=True)
controls = {
    "🔐 Mantrap / Airlock":         ("Installed — Zone A, B", "Operational"),
    "📷 CCTV Coverage":             ("47 cameras, 90-day retention", "Operational"),
    "🪪 Biometric + Badge (2FA)":   ("HandKey + HID access", "Operational"),
    "🚨 Intrusion Detection":       ("PIR + glass-break sensors", "Operational"),
    "🔥 VESDA Smoke Detection":     ("Aspirating system, 24/7 monitoring", "Operational"),
    "🧯 FM-200 Suppression":        ("Clean agent, server room coverage", "Operational"),
    "⚖️ Weight-Sensor Mantrap":     ("Not installed — remediation planned Q1 2025", "⚠️ Gap"),
    "🔒 Cage Locks (MMR)":          ("Combination padlock + electronic", "Operational"),
}
for ctrl, (detail, status) in controls.items():
    icon = "✅" if status == "Operational" else "⚠️"
    st.markdown(f"{icon} **{ctrl}** — {detail} `{status}`")