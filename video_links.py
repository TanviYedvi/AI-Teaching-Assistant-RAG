import json

# Load video links extracted from playlist
with open("video_links.json", "r", encoding="utf-8") as f:
    video_links = json.load(f)