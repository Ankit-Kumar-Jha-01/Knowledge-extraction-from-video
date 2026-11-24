# 🎬 Video-to-Knowledge (Live Video Knowledge Extraction)

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![Gemini API](https://img.shields.io/badge/Google-Gemini_API-4285F4?logo=google&logoColor=white)
![Faster-Whisper](https://img.shields.io/badge/Audio-Faster--Whisper-10B981)
![SentenceTransformers](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-6366F1)

**Turn videos into searchable knowledge.**  
A multimodal Retrieval-Augmented Generation (RAG) web application that extracts spoken audio and visual context from MP4 videos, builds a timestamped semantic knowledge base, and answers user questions with clickable timestamp references.

---

## ✨ Key Features

- **Multimodal Extraction:** Combines audio transcription (`Faster-Whisper`) with visual frame analysis (`Google Gemini API`) so both spoken explanations and on-screen visuals are captured.
- **Semantic Chunking & Vector Search:** Chunks unified video knowledge and generates dense embeddings using `all-MiniLM-L6-v2` with cosine similarity retrieval.
- **Grounded Q&A with Hallucination Guard:** Answers strictly from retrieved video context and returns an insufficient-information response when a question is unrelated to the video.
- **Interactive Timestamp Jump:** Displays retrieved source chunks (`MM:SS - MM:SS`) with one-click jump buttons that seek the video player directly to the cited moment.

---

## 🏗️ Architecture Pipeline

```text
[MP4 Video Upload]
        │
        ├──► Faster-Whisper ──────► Audio Transcript (Timestamps)
        │
        └──► Gemini Vision API ───► Visual Scene Understanding
                    │
                    ▼
       Unified Multimodal Knowledge Base
                    │
                    ▼
       Semantic Chunking + all-MiniLM-L6-v2 Embeddings
                    │
                    ▼
       Cosine Similarity Search (Top-3 Chunks)
                    │
                    ▼
       Gemini Grounded Answer + Clickable Timestamps
