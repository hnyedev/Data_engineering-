import pandas as pd
import json

# ── Load each CSV individually ────────────────────────────────
CSV_FILES = {
    1: "team_1_gaming_videos.csv",
    2: "team_2_tech_videos.csv",
    3: "team_3_education_videos.csv",
    4: "team_4_entertainment_videos.csv",
    5: "team_5_music_videos.csv",
}

full_report = {}

for team_num, filename in CSV_FILES.items():
    print(f"\n{'='*60}")
    print(f" QA Report — {filename}")
    print(f"{'='*60}")

    df = pd.read_csv(filename)
    df['published_at'] = pd.to_datetime(df['published_at'])

    team_report = {}

    # 1. Shape and dtypes
    team_report['shape'] = {'rows': df.shape[0], 'columns': df.shape[1]}
    team_report['dtypes'] = df.dtypes.astype(str).to_dict()

    # 2. Duplicate video IDs
    n_dupes = int(df['video_id'].duplicated().sum())
    team_report['duplicate_video_ids'] = {
        'count': n_dupes,
        'ids': df[df['video_id'].duplicated(keep=False)]['video_id'].tolist()
    }

    # 3. Missing values
    missing = df.isnull().sum()
    team_report['missing_values'] = {
        'counts':  missing.to_dict(),
        'pct':     (missing / len(df) * 100).round(2).to_dict()
    }

    # 4. Unique channels per category
    team_report['channels'] = {
        'unique_count':   int(df['channel_name'].nunique()),
        'channel_names':  df['channel_name'].unique().tolist(),
        'videos_per_channel': df['channel_name'].value_counts().to_dict()
    }

    # 5. Value ranges
    team_report['value_ranges'] = (
        df[['views', 'likes', 'comments', 'duration_minutes']]
        .describe().round(2).to_dict()
    )

    # 6. Date range
    team_report['date_range'] = {
        'min': str(df['published_at'].min().date()),
        'max': str(df['published_at'].max().date()),
        'span_days': int((df['published_at'].max() - df['published_at'].min()).days)
    }

    # 7. Outliers (views > 99th percentile)
    p99 = df['views'].quantile(0.99)
    outliers = df[df['views'] > p99][['video_id', 'title', 'channel_name', 'views']]
    team_report['view_outliers_p99'] = {
        'threshold': int(p99),
        'count':     len(outliers),
        'videos':    outliers.to_dict(orient='records')
    }

    # 8. Zero-view videos
    zeros = df[df['views'] == 0]
    team_report['zero_view_videos'] = {
        'count': len(zeros),
        'ids':   zeros['video_id'].tolist()
    }

    full_report[filename] = team_report

    # ── Print summary per file ────────────────────────────────
    print(f"  Rows            : {team_report['shape']['rows']}")
    print(f"  Duplicates      : {n_dupes}")
    print(f"  Missing likes   : {team_report['missing_values']['counts']['likes']} ({team_report['missing_values']['pct']['likes']}%)")
    print(f"  Missing comments: {team_report['missing_values']['counts']['comments']} ({team_report['missing_values']['pct']['comments']}%)")
    print(f"  Date range      : {team_report['date_range']['min']} → {team_report['date_range']['max']}")
    print(f"  Channels        : {team_report['channels']['channel_names']}")
    print(f"  P99 outliers    : {team_report['view_outliers_p99']['count']} videos above {team_report['view_outliers_p99']['threshold']:,} views")
    print(f"  Zero-view vids  : {team_report['zero_view_videos']['count']}")

# ── Save full report ──────────────────────────────────────────
with open("qa_report_detailed.json", "w") as f:
    json.dump(full_report, f, indent=2, default=str)

print(f"\n✅ Detailed QA report saved as qa_report_detailed.json")