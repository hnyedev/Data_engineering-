# ============================================================
#  YouTube Data API v3 — Channel Video Scraper
#  Activity 11: Descriptive Statistics & Data Integration
# ============================================================
#  pip install google-api-python-client pandas
#
#  Instructions:
#  1. Replace API_KEY with your key
#  2. Replace TEAM_NUMBER with your team number (1-5)
#  3. Run the script: python scrape_youtube.py
#  4. Your dataset will be saved as team_X_videos.csv
# ============================================================

from googleapiclient.discovery import build
import pandas as pd
import re
import time

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
TEAM_NUMBER = 1       # Change to your team number (1, 2, 3, 4, or 5)
VIDEOS_PER_CHANNEL = 100
# ─────────────────────────────────────────────────────────────

# ── Channel assignments per team ─────────────────────────────
TEAMS = {
    1: {
        "category": "Gaming",
        "channels": [
            {"name": "Jacksepticeye", "id": "UCYzPXprvl5Y-Sf0g4vX-m6g"},
            {"name": "Markiplier",    "id": "UC7_YxT-KID8kRbqZo7MyscQ"},
            {"name": "VanossGaming",  "id": "UCKqH_9mk1waLgBiL2vT5b9g"},
        ]
    },
    2: {
        "category": "Tech",
        "channels": [
            {"name": "MKBHD",           "id": "UCBcRF18a7Qf58cCRy5xuWwQ"},
            {"name": "Linus Tech Tips", "id": "UCXuqSBlHAE6Xw-yeJA0Tunw"},
            {"name": "Unbox Therapy",   "id": "UCsTcErHg8oDvUnTzoqsYeNw"},
        ]
    },
    3: {
        "category": "Education",
        "channels": [
            {"name": "Kurzgesagt", "id": "UCsXVk37bltHxD1rDPwtNM8Q"},
            {"name": "Veritasium", "id": "UCHnyfMqiRRG1u-2MsSQLbXA"},
            {"name": "TED",        "id": "UCAuUUnT6oDeKwE6v1NGQxug"},
        ]
    },
    4: {
        "category": "Entertainment",
        "channels": [
            {"name": "MrBeast",      "id": "UCX6OQ3DkcsbYNE6H8uQQuVA"},
            {"name": "PewDiePie",    "id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"},
            {"name": "David Dobrik", "id": "UCmh5gdwCx6lN7gEC20leNVA"},
        ]
    },
    5: {
        "category": "Music",
        "channels": [
            {"name": "Justin Bieber", "id": "UCIwFjwMjI0y7PDBVEO9-bkQ"},
            {"name": "Ed Sheeran",    "id": "UC0C-w0YjGpqDXGB8IHb662A"},
            {"name": "BTS HYBE",      "id": "UCLkAepWjdylmXSltofFvsYQ"},
        ]
    },
}

# ── Helper: Parse ISO 8601 duration → minutes ────────────────
def parse_duration(iso_duration):
    """Convert PT12M34S → 12.57 minutes"""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', str(iso_duration))
    if not match:
        return None
    hours   = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return round(hours * 60 + minutes + seconds / 60, 2)

# ── Helper: Get uploads playlist ID for a channel ────────────
def get_uploads_playlist(youtube, channel_id):
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    if response['items']:
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return None

# ── Helper: Get video IDs from uploads playlist ───────────────
def get_video_ids(youtube, playlist_id, max_videos):
    video_ids    = []
    next_token   = None

    while len(video_ids) < max_videos:
        response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=min(50, max_videos - len(video_ids)),
            pageToken=next_token
        ).execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_token = response.get('nextPageToken')
        if not next_token:
            break

        time.sleep(0.3)   # polite delay

    return video_ids[:max_videos]

# ── Helper: Get stats for a batch of video IDs ───────────────
def get_video_stats(youtube, video_ids):
    rows = []
    # API allows max 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(batch)
        ).execute()

        for item in response['items']:
            snippet  = item.get('snippet', {})
            stats    = item.get('statistics', {})
            details  = item.get('contentDetails', {})

            duration_raw = details.get('duration', '')
            duration_min = parse_duration(duration_raw)

            rows.append({
                'video_id':         item['id'],
                'title':            snippet.get('title', ''),
                'channel_name':     snippet.get('channelTitle', ''),
                'channel_id':       snippet.get('channelId', ''),
                'published_at':     snippet.get('publishedAt', ''),
                'duration_minutes': duration_min,
                'views':            int(stats.get('viewCount',    0)),
                'likes':            int(stats.get('likeCount',    0)) if 'likeCount'    in stats else None,
                'comments':         int(stats.get('commentCount', 0)) if 'commentCount' in stats else None,
            })

        time.sleep(0.3)

    return rows

# ── MAIN ──────────────────────────────────────────────────────
print("=" * 60)
print(f" YouTube Scraper — Team {TEAM_NUMBER}")
print("=" * 60)

youtube  = build('youtube', 'v3', developerKey=API_KEY)
team     = TEAMS[TEAM_NUMBER]
category = team['category']
all_rows = []


for TEAM_NUMBER, team in TEAMS.items():
    category = team['category']
    print(f"\n{'='*60}")
    print(f" Team {TEAM_NUMBER} — {category}")
    print(f"{'='*60}")

    for ch in team['channels']:
        print(f"\n📺 Scraping: {ch['name']} ({category})")

        # Step 1 — get uploads playlist
        playlist_id = get_uploads_playlist(youtube, ch['id'])
        if not playlist_id:
            print(f"  ⚠️  Could not find uploads playlist for {ch['name']}, skipping.")
            continue
        print(f"  ✅ Uploads playlist: {playlist_id}")

        # Step 2 — get video IDs
        print(f"  🔍 Fetching up to {VIDEOS_PER_CHANNEL} video IDs...")
        video_ids = get_video_ids(youtube, playlist_id, VIDEOS_PER_CHANNEL)
        print(f"  ✅ Found {len(video_ids)} video IDs")

        # Step 3 — get video stats
        print(f"  📊 Fetching video statistics...")
        rows = get_video_stats(youtube, video_ids)

        # Step 4 — tag with category
        for row in rows:
            row['category'] = category

        all_rows.extend(rows)
        print(f"  ✅ {len(rows)} videos scraped successfully")
    # ── Export per team ───────────────────────────────────────
    team_rows = [r for r in all_rows if r['category'] == category]
    df_team   = pd.DataFrame(team_rows)
    df_team['published_at'] = pd.to_datetime(df_team['published_at'])
    df_team = df_team[df_team['duration_minutes'] >= 1].reset_index(drop=True)

    filename = f"team_{TEAM_NUMBER}_{category.lower()}_videos.csv"
    df_team.to_csv(filename, index=False)
    print(f"\n💾 Saved: {filename}  ({df_team.shape[0]} rows × {df_team.shape[1]} cols)")

# ── Build DataFrame ───────────────────────────────────────────
df = pd.DataFrame(all_rows)

# Parse published_at to datetime
df['published_at'] = pd.to_datetime(df['published_at'])

# Filter out Shorts (duration < 1 minute)
before = len(df)
df = df[df['duration_minutes'] >= 1].reset_index(drop=True)
after  = len(df)
print(f"\n🎬 Shorts filtered out: {before - after} videos removed (duration < 1 min)")

# ── Summary ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print(f" SCRAPING COMPLETE — Team {TEAM_NUMBER} | {category}")
print("=" * 60)
print(f"  Total videos collected : {len(df)}")
print(f"  Channels               : {df['channel_name'].nunique()}")
print(f"  Date range             : {df['published_at'].min().date()} → {df['published_at'].max().date()}")
print(f"  Missing likes          : {df['likes'].isna().sum()} videos")
print(f"  Missing comments       : {df['comments'].isna().sum()} videos")
print(f"\n  Top 5 videos by views:")
top5 = df.nlargest(5, 'views')[['title','channel_name','views']].values
for row in top5:
    print(f"    {row[2]:>12,} views | {row[1]:15} | {str(row[0])[:45]}")

# ── Quota estimate ────────────────────────────────────────────
channels_count = len(team['channels'])
playlist_calls = channels_count          # 1 unit each
video_id_calls = channels_count * 2      # ~2 pages per channel = 1 unit each
stats_calls    = (len(df) // 50) + 1    # 1 unit per 50 videos
total_units    = playlist_calls + video_id_calls + stats_calls

print(f"\n💡 Estimated quota used: ~{total_units} units (of 10,000 daily)")
