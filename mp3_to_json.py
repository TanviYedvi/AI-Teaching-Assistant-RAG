import whisper
import json
import os

# load whisper model
model = whisper.load_model("base")

audio_folder = "audios"
json_folder = "jsons"

# create json folder if it doesn't exist
os.makedirs(json_folder, exist_ok=True)

audios = os.listdir(audio_folder)

# desired chunk size (characters)
chunk_size = 600

for audio in audios:

    if "_" in audio and audio.endswith(".mp3"):

        number = audio.split("_")[0]
        title = "_".join(audio.split("_")[1:]).replace(".mp3", "")

        print("Processing:", number, title)

        result = model.transcribe(
            audio=f"{audio_folder}/{audio}",
            language="hi",
            task="translate",
            word_timestamps=False
        )

        chunks = []
        current_text = ""
        start_time = None

        for segment in result["segments"]:

            if start_time is None:
                start_time = segment["start"]

            current_text += " " + segment["text"]

            # if chunk becomes large enough, save it
            if len(current_text) >= chunk_size:

                chunks.append({
                    "number": number,
                    "title": title,
                    "start": start_time,
                    "end": segment["end"],
                    "text": current_text.strip()
                })

                current_text = ""
                start_time = None

        # save remaining text
        if current_text.strip() != "":
            chunks.append({
                "number": number,
                "title": title,
                "start": start_time,
                "end": segment["end"],
                "text": current_text.strip()
            })

        chunks_with_metadata = {
            "chunks": chunks,
            "full_text": result["text"]
        }

        json_path = os.path.join(json_folder, audio.replace(".mp3", ".json"))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f, indent=4)

print("All audios processed and JSON files created.")