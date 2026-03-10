import yt_dlp
import json

playlist_url = "https://www.youtube.com/playlist?list=PLTDARY42LDV7WGmlzZtY-w9pemyPrKNUZ"

ydl_opts = {
    "quiet": True,
    "extract_flat": True
}

video_links = {}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist = ydl.extract_info(playlist_url, download=False)

    for video in playlist["entries"]:
        title = video["title"].replace(" ", "_")
        url = f"https://www.youtube.com/watch?v={video['id']}"

        video_links[title] = url

print(video_links)

# Save mapping
with open("video_links.json", "w", encoding="utf-8") as f:
    json.dump(video_links, f, indent=4)

print("Video links extracted successfully!")