import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests
import json


# Load video links
with open("video_links.json", "r", encoding="utf-8") as f:
    video_links = json.load(f)


# Create embeddings using Ollama
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


# Send prompt to Ollama LLM
def inference(prompt):

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    r.raise_for_status()
    return r.json()["response"]


# Load embeddings dataset
df = joblib.load("embeddings.joblib")

print("Total chunks loaded:", len(df))


# Ask user question
incoming_query = input("Ask a Question: ").strip()


# Create embedding for question
question_embedding = create_embedding([incoming_query])[0]


# Calculate similarity
similarities = cosine_similarity(
    np.vstack(df["embedding"].values),
    [question_embedding]
).flatten()


# Retrieve top chunks
top_results = 5
max_indx = similarities.argsort()[::-1][:top_results]

new_df = df.loc[max_indx]


print("\nRetrieved Chunks:\n")
print(new_df[["title", "number", "start", "end"]])


# Build chunk context with video links
video_context = []

for index, row in new_df.iterrows():

    title = row["title"]
    start_time = int(row["start"])

    base_link = video_links.get(title, "Video link not available")

    if base_link != "Video link not available":
        link_with_time = f"{base_link}&t={start_time}s"
    else:
        link_with_time = base_link

    video_context.append({
        "title": title,
        "lecture_number": row["number"],
        "start": row["start"],
        "end": row["end"],
        "text": row["text"],
        "youtube_link": link_with_time
    })


# Build RAG prompt
prompt = f"""
You are an AI teaching assistant trained on lecture transcripts from the
Machine Learning playlist by Krish Naik.

Each chunk also contains the YouTube link to that lecture.

Lecture chunks:
{video_context}

---------------------------------

Student Question:
{incoming_query}

Instructions:

1. Answer the question clearly.
2. Mention the lecture/video where the concept is explained.
3. Provide the timestamp.
4. Provide the YouTube video link with timestamp.
5. Explain the concept simply.

If the question is unrelated to Machine Learning lectures,
say you can only answer questions related to this course.
"""


# Save prompt for debugging
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)


# Generate answer
response = inference(prompt)


print("\nAI Answer:\n")
print(response)


# Save response
with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)