import os
import subprocess

video_folder = "videos"
audio_folder = "audios"

# create audio folder if not exists
os.makedirs(audio_folder, exist_ok=True)

for file in os.listdir(video_folder):

    # process only video files
    if file.endswith((".mp4", ".mkv", ".webm")):

        video_path = os.path.join(video_folder, file)

        # clean filename
        name = os.path.splitext(file)[0]
        name = name.replace(" ", "_")

        audio_path = os.path.join(audio_folder, f"{name}.mp3")

        print(f"Converting: {file}")

        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-ab", "192k",
            audio_path
        ])

print("✅ All videos converted to MP3")