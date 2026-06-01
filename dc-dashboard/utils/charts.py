"""
charts.py — Reusable Plotly chart builders.
All charts share the Hostaro color system.
"""
import plotly.graph_objects as go
import plotly.express as px

# ── Design tokens ─────────────────────────────────────────────────────────────
BLUE       = "#3553D0"
NAVY       = "#1E2B5E"
ORANGE     = "#F5831F"
LIGHT_BLUE = "#6B8EF5"
BG         = "#F0F2F8"
CARD       = "#FFFFFF"
GREEN      = "#28A745"
RED        = "#DC3545"
YELLOW     = "#FFC107"

PALETTE = [BLUE, ORANGE, LIGHT_BLUE, "#9B59B6", GREEN, "#17A2B8", RED]

BASE_LAYOUT = dict(
    paper_bgcolor=CARD,
    plot_bgcolor=BG,
    font=dict(family="sans-serif", color=NAVY, size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor=CARD, bordercolor="#E0E5F2", borderwidth=1),
)

# ── Gauge ─────────────────────────────────────────────────────────────────────
def sla_gauge(value: float, title: str, tier: str) -> go.Figure:
    color = GREEN if value >= 99.98 else (ORANGE if value >= 99.74 else RED)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={"reference": 99.9, "valueformat": ".3f"},
        number={"suffix": "%", "valueformat": ".3f", "font": {"size": 24, "color": NAVY}},
        title={"text": f"<b>{title}</b><br><sub>{tier}</sub>", "font": {"size": 13, "color": NAVY}},
        gauge={
            "axis": {"range": [99.5, 100], "tickformat": ".2f", "tickcolor": NAVY},
            "bar":  {"color": color, "thickness": 0.25},
            "bgcolor": BG,
            "steps": [
                {"range": [99.5,  99.74], "color": "#FDECEA"},
                {"range": [99.74, 99.98], "color": "#FFF8E1"},
                {"range": [99.98, 100],   "color": "#E8F5E9"},
            ],
            "threshold": {"line": {"color": BLUE, "width": 2}, "thickness": 0.75, "value": 99.982},
        }
    ))
    fig.update_layout(**BASE_LAYOUT, height=220)
    return fig

# ── PUE Trend ─────────────────────────────────────────────────────────────────
def pue_trend_chart(df) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["pue"],
        name="Our PUE", mode="lines+markers",
        line=dict(color=BLUE, width=2.5),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["global_avg"],
        name="Global Avg (1.58)", mode="lines",
        line=dict(color=ORANGE, width=1.5, dash="dash"),
    ))
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["target"],
        name="Target (1.40)", mode="lines",
        line=dict(color=GREEN, width=1.5, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["hyperscaler"],
        name="Hyperscaler (1.20)", mode="lines",
        line=dict(color=LIGHT_BLUE, width=1.5, dash="dot"),
    ))
    fig.update_layout(**BASE_LAYOUT,
        title="PUE Trend — Jan 2022 to Sep 2024",
        yaxis_title="PUE",
        yaxis=dict(range=[1.1, 1.9]),
        height=350,
    )
    return fig

# ── Energy Donut ──────────────────────────────────────────────────────────────
def energy_donut(df) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=df["system"],
        values=df["mw"],
        hole=0.52,
        marker=dict(colors=PALETTE),
        textinfo="label+percent",
        textfont_size=11,
    ))
    fig.update_layout(**BASE_LAYOUT,
        title="Energy Consumption by System (MW)",
        height=340,
        showlegend=False,
    )
    return fig

# ── Monthly Energy Bar ────────────────────────────────────────────────────────
def monthly_energy_chart(df) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["month"], y=df["it_load_kw"],
        name="IT Load (kW)", marker_color=BLUE,
    ))
    fig.add_trace(go.Bar(
        x=df["month"], y=[t - i for t, i in zip(df["total_load_kw"], df["it_load_kw"])],
        name="Overhead (kW)", marker_color=LIGHT_BLUE,
    ))
    fig.update_layout(**BASE_LAYOUT,
        barmode="stack",
        title="Monthly Energy Load 2024 (kW)",
        yaxis_title="kW",
        height=320,
    )
    return fig

# ── Compliance Horizontal Bar ─────────────────────────────────────────────────
def compliance_bar(df) -> go.Figure:
    color_map = {"Implemented": GREEN, "Partial": ORANGE, "Not Implemented": RED}
    df = df.copy()
    df["color"] = df["status"].map(color_map)
    fig = go.Figure(go.Bar(
        x=df["score"], y=df["control"],
        orientation="h",
        marker_color=df["color"],
        text=df["score"].astype(str) + "%",
        textposition="inside",
    ))
    fig.update_layout(**BASE_LAYOUT,
        title="ISO 27001 Control Scores",
        xaxis=dict(range=[0, 100], title="Score (%)"),
        height=380,
        yaxis=dict(tickfont=dict(size=11)),
    )
    return fig

# ── Market Capacity Bar ───────────────────────────────────────────────────────
def market_capacity_chart(df) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["city"], y=df["capacity_mw"],
        name="Installed Capacity (MW)",
        marker_color=BLUE,
        text=df["capacity_mw"].astype(str) + " MW",
        textposition="outside",
    ))
    fig.add_trace(go.Scatter(
        x=df["city"], y=df["yoy_growth_pct"],
        name="YoY Growth %", yaxis="y2",
        mode="markers+lines",
        marker=dict(color=ORANGE, size=10),
        line=dict(color=ORANGE, width=2),
    ))
    fig.update_layout(**BASE_LAYOUT,
        title="Mexico DC Market — Installed Capacity & Growth",
        yaxis=dict(title="Capacity (MW)"),
        yaxis2=dict(title="YoY Growth (%)", overlaying="y", side="right", showgrid=False),
        height=360,
    )
    return fig

# ── Market Growth Line ────────────────────────────────────────────────────────
def market_growth_chart(df) -> go.Figure:
    hist = df[~df["forecast"]]
    fore = df[df["forecast"]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist["year"], y=hist["capacity_mw"],
        name="Actual (MW)", mode="lines+markers",
        line=dict(color=BLUE, width=2.5), marker=dict(size=7),
    ))
    fig.add_trace(go.Scatter(
        x=fore["year"], y=fore["capacity_mw"],
        name="Forecast (MW)", mode="lines+markers",
        line=dict(color=BLUE, width=2, dash="dash"), marker=dict(size=7, symbol="diamond"),
    ))
    fig.add_trace(go.Bar(
        x=df["year"], y=df["investment_musd"],
        name="Investment (M USD)", yaxis="y2",
        marker_color=ORANGE, opacity=0.5,
    ))
    fig.update_layout(**BASE_LAYOUT,
        title="Mexico DC Market Growth 2020–2026E",
        yaxis=dict(title="Capacity (MW)"),
        yaxis2=dict(title="Investment (M USD)", overlaying="y", side="right", showgrid=False),
        height=360,
    )
    return fig

# ── Tech Radar Scatter ────────────────────────────────────────────────────────
def tech_radar_chart(df) -> go.Figure:
    maturity_order = {"Adopt": 4, "Trial": 3, "Assess": 2, "Hold": 1}
    df = df.copy()
    df["m_val"] = df["maturity"].map(maturity_order)
    color_map = {"Adopt": GREEN, "Trial": BLUE, "Assess": ORANGE, "Hold": RED}
    category_map = {"Infrastructure": 1, "Operations": 2, "Network": 3,
                    "Energy": 4, "Storage": 5, "Compute": 6, "Security": 7, "Power": 8}
    df["cat_val"] = df["category"].map(category_map)

    fig = go.Figure()
    for maturity, color in color_map.items():
        sub = df[df["maturity"] == maturity]
        fig.add_trace(go.Scatter(
            x=sub["horizon_yr"],
            y=sub["m_val"] + (sub["cat_val"] * 0.05),
            mode="markers+text",
            name=maturity,
            text=sub["technology"],
            textposition="top center",
            textfont=dict(size=9),
            marker=dict(color=color, size=sub["readiness"] * 6, opacity=0.8, line=dict(width=1, color="white")),
        ))
    fig.update_layout(**BASE_LAYOUT,
        title="Technology Radar — Horizon & Maturity",
        xaxis=dict(title="Adoption Year", dtick=1, range=[2023, 2031]),
        yaxis=dict(
            title="Maturity",
            tickvals=[1, 2, 3, 4],
            ticktext=["Hold", "Assess", "Trial", "Adopt"],
        ),
        height=480,
    )
    return fig

# ── Adoption Timeline Gantt ───────────────────────────────────────────────────
def adoption_timeline_chart(df) -> go.Figure:
    fig = go.Figure()
    colors = PALETTE
    for i, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["end"] - row["start"]],
            y=[row["technology"]],
            base=[row["start"]],
            orientation="h",
            marker_color=colors[i % len(colors)],
            opacity=0.85,
            name=row["technology"],
            showlegend=False,
            hovertemplate=f"<b>{row['technology']}</b><br>Start: {row['start']}<br>Peak: {row['peak']}<br>End: {row['end']}<extra></extra>",
        ))
        fig.add_vline(x=row["peak"], line=dict(color=colors[i % len(colors)], width=1, dash="dot"), opacity=0.5)

    fig.add_vline(x=2024.75, line=dict(color=NAVY, width=2), annotation_text="NOW", annotation_position="top")
    fig.update_layout(**BASE_LAYOUT,
        title="Technology Adoption Timeline 2022–2030",
        xaxis=dict(title="Year", dtick=1, range=[2021, 2031]),
        height=420,
        barmode="overlay",
    )
    return fig