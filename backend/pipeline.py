import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from google import genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

BACKEND_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = BACKEND_DIR / "video_chunks.json"
EMBEDDINGS_PATH = BACKEND_DIR / "video_embeddings.npy"
TARGET_VIDEO_PATH = BACKEND_DIR / "sample.mp4"

_embedding_model = None
_gemini_client = None


def _get_models():
    global _embedding_model, _gemini_client
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    if _gemini_client is None:
        _gemini_client = genai.Client()
    return _embedding_model, _gemini_client


def run_video_pipeline(video_path: str):
    """Copies uploaded video to backend/sample.mp4 and runs all 5 backend scripts."""
    src = Path(video_path).resolve()
    if src != TARGET_VIDEO_PATH.resolve():
        shutil.copyfile(src, TARGET_VIDEO_PATH)

    stages = [
        (20, "1/5 Transcribing audio with Faster-Whisper (main.py)...", "main.py"),
        (45, "2/5 Analyzing video visuals with Gemini (test_agentic_video.py)...", "test_agentic_video.py"),
        (70, "3/5 Building combined knowledge base (build_knowledge_base.py)...", "build_knowledge_base.py"),
        (85, "4/5 Chunking knowledge base (chunk_knowledge_base.py)...", "chunk_knowledge_base.py"),
        (98, "5/5 Generating semantic embeddings (generate_embeddings.py)...", "generate_embeddings.py"),
    ]

    for progress, message, script_name in stages:
        yield progress, message, False

        result = subprocess.run(
            [sys.executable, script_name],
            cwd=str(BACKEND_DIR),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            raise RuntimeError(f"Error in {script_name}:\n{error_msg}")

    yield 100, "Knowledge base & embeddings ready!", True


def query_knowledge_base(question: str, video_path: str) -> dict:
    """Retrieves top 3 chunks and generates a grounded Gemini answer."""
    if not CHUNKS_PATH.exists() or not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            "Processed files not found. Please click 'Process Video' first."
        )

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    embeddings = np.load(EMBEDDINGS_PATH)
    embedding_model, client = _get_models()

    question_embedding = embedding_model.encode([question])
    similarities = cosine_similarity(question_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:3]

    retrieved_context = ""
    for rank, index in enumerate(top_indices, start=1):
        chunk = chunks[index]
        retrieved_context += f"""
[Source {rank}]
Topic: {chunk['topic']}
Start: {chunk['start_seconds']} seconds
End: {chunk['end_seconds']} seconds
Content:
{chunk['text']}
-------------------------
"""

    prompt = f"""
You are a helpful assistant that answers questions about a video.

Answer the user's question using ONLY the video information
provided below.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. Give a simple, clear answer.
4. Add source references like [Source 1] where relevant.
5. If the provided information does not answer the question,
   output exactly INSUFFICIENT on the first line.

VIDEO INFORMATION:
{retrieved_context}

USER QUESTION:
{question}

Write the answer:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    answer = response.text.strip()

    if answer.startswith("INSUFFICIENT"):
        return {
            "answer": "The video information is insufficient to answer this question.",
            "sources": [],
        }

    sources = []
    for rank, index in enumerate(top_indices, start=1):
        chunk = chunks[index]
        start = int(chunk["start_seconds"])
        end = int(chunk["end_seconds"])

        start_time = f"{start // 60:02d}:{start % 60:02d}"
        end_time = f"{end // 60:02d}:{end % 60:02d}"

        clean_text = chunk["text"].strip()
        topic_prefix = f"Topic: {chunk['topic']}"
        if clean_text.startswith(topic_prefix):
            clean_text = clean_text[len(topic_prefix):].strip()

        sources.append({
            "rank": rank,
            "topic": chunk["topic"],
            "timestamp": f"{start_time} - {end_time}",
            "start_seconds": start,
            "text": clean_text,
        })

    return {
        "answer": answer,
        "sources": sources,
    }