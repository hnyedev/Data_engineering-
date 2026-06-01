import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DATA_PATH  = Path("/home/seven/2409195_CESAR_PINTO/students/laboratories/4-ETL-Airflow-Orchestration/data/air_quality.csv")
OUTPUT_DIR = Path("/home/seven/2409195_CESAR_PINTO/students/laboratories/4-ETL-Airflow-Orchestration/data/reports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

POLLUTANTS = {
    "pm2_5":            ("PM2.5",  "ug/m3",  "#3498db"),
    "pm10":             ("PM10",   "ug/m3",  "#e74c3c"),
    "ozone":            ("O3",     "ug/m3",  "#2ecc71"),
    "nitrogen_dioxide": ("NO2",    "ug/m3",  "#f39c12"),
    "carbon_monoxide":  ("CO",     "ug/m3",  "#9b59b6"),
}

# AQI background bands (European scale)
AQI_BANDS = [
    (0,  20,  "#2ecc71", "Good"),
    (20, 40,  "#a8e063", "Fair"),
    (40, 60,  "#f9ca24", "Moderate"),
    (60, 80,  "#f0932b", "Poor"),
    (80, 100, "#e55039", "Very Poor"),
]

# ---------------------------------------------------------------------------
# LOAD & PREPARE
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Keep only the most recent day to avoid multi-day noise
latest_date = df["timestamp"].dt.date.max()
df_day = df[df["timestamp"].dt.date == latest_date].copy()
df_day = df_day.sort_values("timestamp").reset_index(drop=True)
df_day["hour"] = df_day["timestamp"].dt.hour

print(f"[INFO] Loaded {len(df)} total rows")
print(f"[INFO] Plotting day: {latest_date} — {len(df_day)} hourly records")

# ---------------------------------------------------------------------------
# CHART 1 — Individual boxplots, one per pollutant (own Y scale)
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 5, figsize=(16, 6))
fig.suptitle(
    f"Pollutant Distribution — CDMX — {latest_date}",
    fontsize=14, fontweight="bold", y=1.01
)

for ax, (col, (name, unit, color)) in zip(axes, POLLUTANTS.items()):
    data = df_day[col].dropna().values if col in df_day.columns else np.array([])

    if len(data) == 0:
        ax.set_visible(False)
        continue

    bp = ax.boxplot(
        data,
        patch_artist=True,
        widths=0.5,
        medianprops=dict(color="black", linewidth=2),
        whiskerprops=dict(linewidth=1.2),
        capprops=dict(linewidth=1.2),
        flierprops=dict(marker="o", markersize=4, linestyle="none",
                        markerfacecolor=color, alpha=0.6),
    )
    bp["boxes"][0].set_facecolor(color)
    bp["boxes"][0].set_alpha(0.75)

    # Annotate median
    median_val = np.median(data)
    ax.text(
        1, median_val, f"{median_val:.1f}",
        va="bottom", ha="center", fontsize=8,
        color="black", fontweight="bold"
    )
 


    ax.set_title(f"{name}", fontsize=11, fontweight="bold")
    ax.set_ylabel(unit, fontsize=9)
    ax.set_xticks([])
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    # WHO reference line for PM2.5 and NO2
    who_limits = {"pm2_5": 15, "nitrogen_dioxide": 25}
    if col in who_limits:
        ax.axhline(
            who_limits[col], color="red",
            linestyle="--", linewidth=1, alpha=0.7
        )
        ax.text(
            1.35, who_limits[col], "WHO",
            color="red", fontsize=7, va="bottom"
        )

plt.tight_layout()
bp_path = OUTPUT_DIR / "boxplots.png"
fig.savefig(bp_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"[OK] Boxplots saved → {bp_path}")

# ---------------------------------------------------------------------------
# CHART 2 — PM2.5 + O3 + NO2 daily evolution with AQI background bands
# ---------------------------------------------------------------------------
MAIN_POLLUTANTS = {
    "pm2_5":            ("PM2.5",  "#2980b9"),
    "ozone":            ("O3",     "#27ae60"),
    "nitrogen_dioxide": ("NO2",    "#e67e22"),
}

hours  = df_day["hour"].values
x_vals = np.arange(len(hours))

fig, ax = plt.subplots(figsize=(14, 6))

# AQI background bands
y_max_band = 100
for y0, y1, color, label in AQI_BANDS:
    ax.axhspan(y0, y1, facecolor=color, alpha=0.08, zorder=0)
    ax.text(
        -0.6, (y0 + y1) / 2, label,
        fontsize=7, va="center", ha="right",
        color=color, fontweight="bold"
    )

# One line per pollutant
for col, (name, color) in MAIN_POLLUTANTS.items():
    if col not in df_day.columns:
        continue
    vals = df_day[col].values.astype(float)

    # Rolling mean for smoothness
    smooth = pd.Series(vals).rolling(window=3, center=True, min_periods=1).mean().values

    # Raw dots
    ax.scatter(x_vals, vals, color=color, s=25, alpha=0.5, zorder=3)

    # Smooth line
    ax.plot(x_vals, smooth, color=color, linewidth=2.2,
            label=name, zorder=4)

# Axis formatting
ax.set_xticks(x_vals)
ax.set_xticklabels([f"{h:02d}h" for h in hours], fontsize=8, rotation=45)
ax.set_xlabel("Hour of day", fontsize=11)
ax.set_ylabel("Concentration (ug/m3)", fontsize=11)
ax.set_title(
    f"PM2.5 · O3 · NO2 hourly evolution — CDMX — {latest_date}",
    fontsize=13, fontweight="bold"
)
ax.set_xlim(-1, len(hours))
ax.yaxis.grid(True, linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.legend(fontsize=10, loc="upper right")

# AQI threshold lines (subtle)
for _, y1, color, _ in AQI_BANDS[1:]:
    ax.axhline(y1, color=color, linewidth=0.6, linestyle="--", alpha=0.5, zorder=1)

plt.tight_layout()
ts_path = OUTPUT_DIR / "timeseries.png"
fig.savefig(ts_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"[OK] Time series saved → {ts_path}")