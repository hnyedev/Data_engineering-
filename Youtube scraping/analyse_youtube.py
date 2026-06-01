# ============================================================
#  YouTube Data API v3 — Data Integration & Descriptive Stats
#  Activity 11: Multiple Data Sources + Descriptive Statistics
# ============================================================
#  Instructions:
#  1. Make sure all 5 team CSV files are in the same folder
#  2. Run: python analyze_youtube.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Color palette (consistent across all plots) ──────────────
CATEGORY_COLORS = {
    'Gaming':        '#6B46C1',
    'Tech':          '#D69E2E',
    'Education':     '#2B6CB0',
    'Entertainment': '#C53030',
    'Music':         '#276749',
}

# ============================================================
#  PHASE 1 — MULTIPLE DATA SOURCES INTEGRATION
# ============================================================
print("=" * 65)
print("  PHASE 1 — MULTIPLE DATA SOURCES INTEGRATION")
print("=" * 65)

# ── Step 1: Load all team CSVs ────────────────────────────────
expected_files = {
    1: 'team_1_gaming_videos.csv',
    2: 'team_2_tech_videos.csv',
    3: 'team_3_education_videos.csv',
    4: 'team_4_entertainment_videos.csv',
    5: 'team_5_music_videos.csv',
}

dataframes = {}
print("\n📂 Loading team datasets...")
for team, filename in expected_files.items():
    if os.path.exists(filename):
        df_team = pd.read_csv(filename, parse_dates=['published_at'])
        df_team['team'] = team
        dataframes[team] = df_team
        print(f"  ✅ Team {team} | {filename:45} | {len(df_team):>4} rows")
    else:
        print(f"  ❌ Team {team} | {filename} NOT FOUND — skipping")

if len(dataframes) == 0:
    print("\n❌ No CSV files found. Make sure all team files are in the same folder.")
    exit()

# ── Step 2: Concatenate all datasets ─────────────────────────
print(f"\n🔗 Integrating {len(dataframes)} datasets with pd.concat()...")
df = pd.concat(dataframes.values(), ignore_index=True)

print(f"  ✅ Integrated dataset shape : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  ✅ Categories               : {sorted(df['category'].unique())}")
print(f"  ✅ Unique channels          : {df['channel_name'].nunique()}")
print(f"  ✅ Date range               : {df['published_at'].min().date()} → {df['published_at'].max().date()}")

# ── Step 3: Inspect the integration ──────────────────────────
print("\n📊 Videos per category after integration:")
category_counts = df.groupby('category')['video_id'].count().sort_values(ascending=False)
for cat, count in category_counts.items():
    bar = '█' * (count // 10)
    print(f"  {cat:<15} {count:>4} videos  {bar}")

# ── Step 4: Data quality check ────────────────────────────────
print("\n🔍 Data quality check:")
print(f"  Duplicate video_ids     : {df['video_id'].duplicated().sum()}")
print(f"  Missing views           : {df['views'].isna().sum()}")
print(f"  Missing likes           : {df['likes'].isna().sum()}")
print(f"  Missing comments        : {df['comments'].isna().sum()}")
print(f"  Missing duration        : {df['duration_minutes'].isna().sum()}")

# ── Step 5: Investigate unexpected channels ───────────────────
print("\n⚠️  Channel name check — expected 15 unique channels:")
channel_summary = df.groupby(['category', 'channel_name'])['video_id'].count().reset_index()
channel_summary.columns = ['category', 'channel_name', 'video_count']
print(channel_summary.to_string(index=False))

unexpected = df.groupby('category')['channel_name'].nunique()
issues = unexpected[unexpected > 3]
if len(issues) > 0:
    print(f"\n  🚨 Categories with more than 3 channels detected:")
    for cat, count in issues.items():
        print(f"     {cat}: {count} channels found (expected 3)")
        extra = df[df['category'] == cat]['channel_name'].value_counts()
        print(f"     Channels: {extra.to_dict()}")

# ── Step 6: Export integrated dataset ────────────────────────
df.to_csv('integrated_youtube_dataset.csv', index=False)
print(f"\n💾 Integrated dataset saved: integrated_youtube_dataset.csv")

# ============================================================
#  PHASE 2 — DESCRIPTIVE STATISTICS
# ============================================================
print("\n" + "=" * 65)
print("  PHASE 2 — DESCRIPTIVE STATISTICS")
print("=" * 65)

numeric_cols = ['views', 'likes', 'comments', 'duration_minutes']

# ── Step 7: Overall descriptive stats ────────────────────────
print("\n📈 Overall descriptive statistics (full dataset):")
stats_overall = df[numeric_cols].describe().round(2)
print(stats_overall.to_string())

# ── Step 8: Descriptive stats by category ────────────────────
print("\n📈 Descriptive statistics by category:")
stats_by_cat = df.groupby('category')[numeric_cols].agg([
    'count', 'mean', 'median', 'std', 'min', 'max',
    lambda x: x.quantile(0.25),
    lambda x: x.quantile(0.75),
]).round(2)
stats_by_cat.columns = ['_'.join(col).replace('<lambda_0>', 'Q1').replace('<lambda_1>', 'Q3')
                         for col in stats_by_cat.columns]

# Print views stats only for readability
views_stats = df.groupby('category')['views'].agg(
    count='count',
    mean='mean',
    median='median',
    std='std',
    min='min',
    max='max',
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75),
).round(0).astype(int)

print("\n  VIEWS by category:")
print(views_stats.to_string())

# ── Step 9: Key statistical insights ─────────────────────────
print("\n🔑 Key statistical insights:")

for cat in sorted(df['category'].unique()):
    subset = df[df['category'] == cat]['views']
    cv     = (subset.std() / subset.mean() * 100).round(1)
    skew   = subset.skew().round(2)
    print(f"  {cat:<15} | mean: {subset.mean():>12,.0f} | median: {subset.median():>12,.0f} | "
          f"CV: {cv:>6}% | skew: {skew:>6}")

print("\n  NOTE: When mean >> median, the distribution is right-skewed (outliers pulling the mean up)")

# ── Step 10: Correlation analysis ────────────────────────────
print("\n📉 Correlation matrix (full dataset):")
corr = df[numeric_cols].corr().round(3)
print(corr.to_string())

# ── Step 11: Export stats ─────────────────────────────────────
stats_by_cat.to_csv('descriptive_stats_by_category.csv')
print("\n💾 Descriptive stats saved: descriptive_stats_by_category.csv")

# ============================================================
#  PHASE 3 — VISUALIZATIONS
# ============================================================
print("\n" + "=" * 65)
print("  PHASE 3 — VISUALIZATIONS")
print("=" * 65)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.spines.top']   = False
plt.rcParams['axes.spines.right'] = False

colors = [CATEGORY_COLORS[c] for c in sorted(df['category'].unique())]

# ── Plot 1: Distribution of views by category (boxplot) ──────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Views Distribution by Category', fontsize=16, fontweight='bold', y=1.02)

# Boxplot — log scale to handle outliers
cat_order = sorted(df['category'].unique())
bp_data   = [df[df['category'] == c]['views'].dropna().values for c in cat_order]

bp = axes[0].boxplot(bp_data, labels=cat_order, patch_artist=True, notch=False)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0].set_yscale('log')
axes[0].set_title('Boxplot (log scale)', fontweight='bold')
axes[0].set_ylabel('Views')
axes[0].tick_params(axis='x', rotation=15)
axes[0].grid(axis='y', alpha=0.3)

# Median views bar chart
medians = df.groupby('category')['views'].median().reindex(cat_order)
bars = axes[1].bar(cat_order, medians, color=colors, alpha=0.85, edgecolor='white')
axes[1].set_title('Median Views per Category', fontweight='bold')
axes[1].set_ylabel('Median Views')
axes[1].tick_params(axis='x', rotation=15)
axes[1].grid(axis='y', alpha=0.3)
for bar, val in zip(bars, medians):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.02,
                 f'{val/1e6:.1f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('plot1_views_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ plot1_views_distribution.png")

# ── Plot 2: Mean vs Median (skewness visualization) ──────────
fig, ax = plt.subplots(figsize=(10, 6))
x      = np.arange(len(cat_order))
width  = 0.35
means  = df.groupby('category')['views'].mean().reindex(cat_order)
medians = df.groupby('category')['views'].median().reindex(cat_order)

bars1 = ax.bar(x - width/2, means,   width, label='Mean',   color=colors, alpha=0.9, edgecolor='white')
bars2 = ax.bar(x + width/2, medians, width, label='Median', color=colors, alpha=0.4,
               edgecolor=[CATEGORY_COLORS[c] for c in cat_order], linewidth=2)

ax.set_xticks(x)
ax.set_xticklabels(cat_order, rotation=15)
ax.set_ylabel('Views')
ax.set_title('Mean vs Median Views — Detecting Skewness', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f'{val/1e6:.0f}M'))
plt.tight_layout()
plt.savefig('plot2_mean_vs_median.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ plot2_mean_vs_median.png")

# ── Plot 3: Correlation heatmap ───────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask, k=1)] = True  # fix: k=1 keeps diagonal

sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            linewidths=0.5, ax=ax, mask=mask,
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Matrix — All Numeric Variables', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('plot3_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
# ── Plot 4: Views vs Likes scatter by category ───────────────
fig, ax = plt.subplots(figsize=(10, 7))
for cat in cat_order:
    subset = df[df['category'] == cat].dropna(subset=['views', 'likes'])
    ax.scatter(subset['views'], subset['likes'],
               color=CATEGORY_COLORS[cat], alpha=0.5, s=40, label=cat)

ax.set_xlabel('Views', fontsize=11)
ax.set_ylabel('Likes', fontsize=11)
ax.set_title('Views vs Likes by Category', fontsize=14, fontweight='bold')
ax.legend(title='Category')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f'{val/1e6:.0f}M'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f'{val/1e6:.1f}M'))
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plot4_views_vs_likes.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ plot4_views_vs_likes.png")

# ── Plot 5: Duration distribution by category ────────────────
fig, ax = plt.subplots(figsize=(12, 6))
for cat in cat_order:
    subset = df[df['category'] == cat]['duration_minutes'].dropna()
    subset = subset[subset <= 60]   # cap at 60 min for readability
    subset.plot.kde(ax=ax, color=CATEGORY_COLORS[cat], linewidth=2.5, label=cat)

ax.set_xlabel('Duration (minutes)', fontsize=11)
ax.set_ylabel('Density', fontsize=11)
ax.set_title('Video Duration Distribution by Category (KDE)', fontsize=14, fontweight='bold')
ax.legend(title='Category')
ax.set_xlim(0, 60)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plot5_duration_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ plot5_duration_distribution.png")

# ── Plot 6: Top 10 videos overall ────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
top10 = df.nlargest(10, 'views')[['title', 'channel_name', 'category', 'views']].reset_index(drop=True)
top10['label'] = top10['title'].str[:40] + '...\n(' + top10['channel_name'] + ')'
bar_colors = [CATEGORY_COLORS[c] for c in top10['category']]
bars = ax.barh(range(len(top10)), top10['views'], color=bar_colors, alpha=0.85, edgecolor='white')
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(top10['label'], fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Views')
ax.set_title('Top 10 Most Viewed Videos — All Categories', fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f'{val/1e6:.0f}M'))
ax.grid(axis='x', alpha=0.3)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=CATEGORY_COLORS[c], label=c) for c in cat_order]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
plt.tight_layout()
plt.savefig('plot6_top10_videos.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✅ plot6_top10_videos.png")

# ============================================================
#  FINAL SUMMARY
# ============================================================
print("\n" + "=" * 65)
print("  ANALYSIS COMPLETE")
print("=" * 65)
print(f"  Integrated dataset  : {len(df):,} videos from {df['channel_name'].nunique()} channels")
print(f"  Categories          : {len(df['category'].unique())}")
print(f"  Files exported      :")
print(f"    📄 integrated_youtube_dataset.csv")
print(f"    📄 descriptive_stats_by_category.csv")
print(f"    🖼️  plot1_views_distribution.png")
print(f"    🖼️  plot2_mean_vs_median.png")
print(f"    🖼️  plot3_correlation_heatmap.png")
print(f"    🖼️  plot4_views_vs_likes.png")
print(f"    🖼️  plot5_duration_distribution.png")
print(f"    🖼️  plot6_top10_videos.png")

print("\n📝 DISCUSSION QUESTIONS:")
print("  1. Which category has the highest mean views? Is the mean a good")
print("     representative measure here, or is the median more appropriate?")
print("  2. Team 2 (Tech) has missing likes and comments — how does this")
print("     affect the descriptive statistics for that category?")
print("  3. Which two variables have the strongest correlation? Does that")
print("     make intuitive sense?")
print("  4. Team 5 (Music) — how many unique channels appear in the dataset?")
print("     Why might there be more than 3? What should be done about it?")
print("  5. Which category shows the most right-skewed distribution?")
print("     What does that tell us about content performance in that category?")
