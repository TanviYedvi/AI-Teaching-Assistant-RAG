import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
import json
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Teaching Assistant")
st.write("Ask anything about the Machine Learning playlist by Krish Naik")


# -----------------------------
# Load Data
# -----------------------------
@st.cache_resource
def load_embeddings():
    return joblib.load("embeddings.joblib")

df = load_embeddings()

@st.cache_resource
def load_links():
    with open("video_links.json", "r", encoding="utf-8") as f:
        return json.load(f)

video_links = load_links()


# -----------------------------
# Utility Functions
# -----------------------------
def format_time(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02d}"


def clean_title(title):
    return title.replace("_", " ")


# -----------------------------
# Embedding Function
# -----------------------------
def create_embedding(text):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": [text]
        }
    )

    return r.json()["embeddings"][0]


# -----------------------------
# LLM Response
# -----------------------------
def generate_answer(prompt):

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()["response"]


# -----------------------------
# Retrieve Similar Chunks
# -----------------------------
def retrieve_chunks(question):

    q_embedding = create_embedding(question)

    similarities = cosine_similarity(
        np.vstack(df["embedding"].values),
        [q_embedding]
    ).flatten()

    top_results = 5
    max_indx = similarities.argsort()[::-1][:top_results]

    return df.loc[max_indx]


# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -----------------------------
# User Input
# -----------------------------
question = st.chat_input("Ask a question about the ML lectures...")

if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking... 🤔"):

            chunks = retrieve_chunks(question)

            context_list = []
            video_link = None
            timestamp = None
            lecture_name = None

            for _, row in chunks.iterrows():

                title = row["title"]
                start = int(row["start"])
                end = int(row["end"])

                base_link = video_links.get(title, "")

                if base_link:
                    video_link = f"{base_link}&t={start}s"
                    timestamp = f"{format_time(start)} - {format_time(end)}"
                    lecture_name = clean_title(title)

                context_list.append({
                    "title": clean_title(title),
                    "start": format_time(start),
                    "end": format_time(end),
                    "text": row["text"]
                })


            # -----------------------------
            # RAG Prompt
            # -----------------------------
            rag_prompt = f"""
You are an AI teaching assistant trained on lecture transcripts from the
Machine Learning playlist by Krish Naik.

Lecture chunks:
{context_list}

Student Question:
{question}

Instructions:
1. Answer clearly.
2. Mention the lecture name.
3. Mention timestamp using format MM:SS.
4. Explain concept simply.
5. Guide the student to watch the lecture section.
"""

            answer = generate_answer(rag_prompt)

        st.write(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


        # -----------------------------
        # Show Lecture Info
        # -----------------------------
        if lecture_name:
            st.subheader("📚 Lecture")
            st.write(lecture_name)

        if timestamp:
            st.write(f"⏱ Timestamp: {timestamp}")

        if video_link:
            st.markdown(f"[▶ Watch on YouTube]({video_link})")

            st.subheader("📺 Watch Lecture")
            st.video(video_link)


# -----------------------------
# Sidebar: Retrieved Chunks
# -----------------------------
st.sidebar.title("Retrieved Lecture Chunks")

if question:

    for _, row in chunks.iterrows():

        title = clean_title(row["title"])
        timestamp = format_time(row["start"])

        st.sidebar.write(f"📚 {title}")
        st.sidebar.write(f"⏱ {timestamp}")
        st.sidebar.write("---")