# 🎓 RAG-Based AI Teaching Assistant for YouTube Lectures

This project is an **AI Teaching Assistant** that answers questions from lecture videos using **Retrieval-Augmented Generation (RAG)**.  

It converts a YouTube playlist into searchable knowledge and allows students to **ask questions about the lecture content**.

The assistant retrieves relevant lecture segments and generates answers using a **Large Language Model (LLM)**.

---

# 🚀 Features

- ChatGPT-style interface using **Streamlit**
- Semantic search using **embeddings**
- **Retrieval Augmented Generation (RAG)**
- Lecture transcript generation using **OpenAI Whisper**
- **Local LLM inference** using Ollama (Llama3)
- YouTube **timestamp navigation**
- Built-in **video player inside the UI**
- Sidebar showing retrieved lecture chunks

---

# 📺 Dataset / Playlist Used

For this project, I used the **Machine Learning Playlist by Krish Naik**:

https://www.youtube.com/playlist?list=PLTDARY42LDV7WGmlzZtY-w9pemyPrKNUZ

However, this system is **generic** and can work with **any YouTube lecture playlist**.  
You only need to replace the playlist link.

---

# 🧠 How the System Works

The system follows this pipeline:

YouTube Playlist
↓
Download Videos
↓
Convert Video → Audio
↓
Transcribe Audio (Whisper)
↓
Split Transcript into Chunks
↓
Generate Embeddings (BGE-M3)
↓
Vector Similarity Search
↓
Retrieve Relevant Lecture Segments
↓
Generate Answer using LLM (Llama3)
↓
Display Result in Streamlit Chat Interface


---

# 🛠 Technologies Used

- Python
- Streamlit
- Ollama
- Llama3
- BGE-M3 Embeddings
- OpenAI Whisper
- Pandas / NumPy
- Scikit-learn
- yt-dlp

---

# 📂 Project Structure
app.py → Streamlit UI
ask_question.py → RAG query testing
download_audio.py → Download playlist videos
video_to_mp3.py → Convert videos to audio
mp3_to_json.py → Whisper transcription
read_chunks.py → Generate embeddings
extract_playlist_links.py → Extract video links
video_links.py → Video link mapping

requirements.txt
README.md

# ▶️ How to Run the Project

Follow these steps to run the AI Teaching Assistant locally.

1️⃣ Clone the Repository

git clone https://github.com/Tanvi2616/RAG-AI-Teaching-Assistant.git

cd RAG-AI-Teaching-Assistant

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Install and Run Ollama

Download Ollama from:
https://ollama.com

Start the Ollama server:

ollama serve

4️⃣ Download Required Models

ollama pull llama3
ollama pull bge-m3

5️⃣ Run the Streamlit Application

streamlit run app.py

6️⃣ Open the Application

Once the server starts, open your browser and go to:

http://localhost:8501

You can now ask questions about the lecture playlist and the AI assistant will retrieve relevant lecture segments and generate answers.

The assistant will:

- retrieve relevant lecture segments
- generate an explanation
- provide the lecture name
- show the timestamp
- display the YouTube video

---

# 💡 Future Improvements

- Add FAISS vector database for faster search
- Highlight transcript sections
- Support multiple playlists
- Deploy on cloud
- Add lecture search feature

---

# 👩‍💻 Author

**Tanvi Yedvi**  
BTech Artificial intelligence and data science

GitHub:  
https://github.com/TanviYedvi

---

# ⭐ If you like this project

Feel free to **star the repository** and use it for your own learning playlists!
