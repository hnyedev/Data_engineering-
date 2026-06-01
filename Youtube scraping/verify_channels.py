# ============================================================
#  YouTube API — Channel ID Verification
#  Run: python verify_channels.py
# ============================================================
# pip install google-api-python-client pandas

from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
youtube = build('youtube', 'v3', developerKey=API_KEY)

# ── Channel list to verify ────────────────────────────────────
channels = [
    # Team 1 - Gaming
    {"team": 1, "category": "Gaming",        "name": "Jacksepticeye",   "id": "UCYzPXprvl5Y-Sf0g4vX-m6g"},
    {"team": 1, "category": "Gaming",        "name": "Markiplier",       "id": "UC7_YxT-KID8kRbqZo7MyscQ"},  # FIXED! :D
    {"team": 1, "category": "Gaming",        "name": "VanossGaming",     "id": "UCKqH_9mk1waLgBiL2vT5b9g"},

    # Team 2 - Tech
    {"team": 2, "category": "Tech",          "name": "MKBHD",            "id": "UCBJycsmduvYEL83R_U4JriQ"},
    {"team": 2, "category": "Tech",          "name": "Linus Tech Tips",  "id": "UCXuqSBlHAE6Xw-yeJA0Tunw"},
    {"team": 2, "category": "Tech",          "name": "Unbox Therapy",    "id": "UCsTcErHg8oDvUnTzoqsYeNw"},

    # Team 3 - Education
    {"team": 3, "category": "Education",     "name": "Kurzgesagt",       "id": "UCsXVk37bltHxD1rDPwtNM8Q"},
    {"team": 3, "category": "Education",     "name": "Veritasium",       "id": "UCHnyfMqiRRG1u-2MsSQLbXA"},
    {"team": 3, "category": "Education",     "name": "TED",              "id": "UCAuUUnT6oDeKwE6v1NGQxug"},

    # Team 4 - Entertainment
    {"team": 4, "category": "Entertainment", "name": "MrBeast",          "id": "UCX6OQ3DkcsbYNE6H8uQQuVA"},
    {"team": 4, "category": "Entertainment", "name": "PewDiePie",        "id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"},
    {"team": 4, "category": "Entertainment", "name": "David Dobrik",     "id": "UCmh5gdwCx6lN7gEC20leNVA"},

    # Team 5 - Music
    {"team": 5, "category": "Music",         "name": "Justin Bieber",    "id": "UCIwFjwMjI0y7PDBVEO9-bkQ"},
    {"team": 5, "category": "Music",         "name": "Ed Sheeran",     "id": "UC0C-w0YjGpqDXGB8IHb662A"},       # FIXED! :D
    {"team": 5, "category": "Music",         "name": "BTS HYBE",         "id": "UCLkAepWjdylmXSltofFvsYQ"},
]

# ── Verify in batches of 5 ────────────────────────────────────
print("=" * 70)
print(f"{'TEAM':<6} {'CATEGORY':<15} {'NAME':<22} {'STATUS':<10} {'SUBS':>12} {'VIDEOS':>8}")
print("=" * 70)

results = []
batch_size = 5

for i in range(0, len(channels), batch_size):
    batch = channels[i:i+batch_size]
    ids   = [c['id'] for c in batch]

    try:
        response = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=','.join(ids)
        ).execute()

        found_ids = {item['id']: item for item in response.get('items', [])}

        for ch in batch:
            if ch['id'] in found_ids:
                item  = found_ids[ch['id']]
                stats = item.get('statistics', {})
                subs  = int(stats.get('subscriberCount', 0))
                vids  = int(stats.get('videoCount', 0))
                # Get uploads playlist ID (needed for Strategy 2)
                uploads_playlist = item['contentDetails']['relatedPlaylists']['uploads']
                status = "✅ OK"
            else:
                subs  = 0
                vids  = 0
                uploads_playlist = "NOT FOUND"
                status = "❌ INVALID"

            print(f"{ch['team']:<6} {ch['category']:<15} {ch['name']:<22} {status:<10} {subs:>12,} {vids:>8,}")

            results.append({
                "team":             ch['team'],
                "category":         ch['category'],
                "channel_name":     ch['name'],
                "channel_id":       ch['id'],
                "status":           status,
                "subscribers":      subs,
                "total_videos":     vids,
                "uploads_playlist": uploads_playlist,
            })

    except Exception as e:
        print(f"  ERROR in batch: {e}")

print("=" * 70)

# ── Summary ───────────────────────────────────────────────────
df = pd.DataFrame(results)
valid   = df[df['status'] == "✅ OK"]
invalid = df[df['status'] == "❌ INVALID"]

print(f"\n✅ Valid channels   : {len(valid)}")
print(f"❌ Invalid channels : {len(invalid)}")

if len(invalid) > 0:
    print("\nChannels to fix:")
    for _, row in invalid.iterrows():
        print(f"  Team {row['team']} | {row['channel_name']} | ID: {row['channel_id']}")

# ── Export verified list ──────────────────────────────────────
df.to_csv('verified_channels.csv', index=False)
print("\n📄 verified_channels.csv saved — use uploads_playlist column for Strategy 2 scraping!")

# ── Quota used ────────────────────────────────────────────────
calls = (len(channels) // batch_size) + (1 if len(channels) % batch_size else 0)
print(f"\n💡 Quota used: {calls} calls × 1 unit = {calls} units total")
