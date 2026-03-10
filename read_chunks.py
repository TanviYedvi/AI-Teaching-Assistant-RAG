import requests
import os
import json
import pandas as pd
import joblib

def create_embedding(text_list):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )

    r.raise_for_status()

    return r.json()["embeddings"]


json_folder = "jsons"
json_files = sorted(os.listdir(json_folder))

all_chunks = []
chunk_id = 0


for json_file in json_files:

    with open(f"{json_folder}/{json_file}", encoding="utf-8") as f:
        content = json.load(f)

    print(f"Creating embeddings for {json_file}")

    # remove empty texts
    texts = [c["text"].strip() for c in content["chunks"] if c["text"].strip() != ""]

    embeddings = create_embedding(texts)

    embed_index = 0

    for chunk in content["chunks"]:

        text = chunk["text"].strip()

        if text == "":
            continue

        chunk["chunk_id"] = chunk_id
        chunk["embedding"] = embeddings[embed_index]

        all_chunks.append(chunk)

        chunk_id += 1
        embed_index += 1


df = pd.DataFrame(all_chunks)

print("Total chunks:", len(df))

# Save embeddings dataset
joblib.dump(df, "embeddings.joblib")

print("Embeddings saved successfully.")