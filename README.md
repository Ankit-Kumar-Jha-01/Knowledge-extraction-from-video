<div align="center">

# 🎥 Video Knowledge Extraction — Automated Notes & Keyframe Pipeline

**End-to-end multimodal pipeline that transforms educational and technical videos into structured markdown notes paired with extracted keyframe screenshots**

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Whisper](https://img.shields.io/badge/OpenAI_Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-Summarization-FF6F00?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Screenshots & Demo](#-screenshots--demo)
3. [Requirements](#-requirements)
4. [Project Structure](#-project-structure)
5. [Data & Inputs](#-data--inputs)
6. [Installation](#-installation)
7. [Project Methodology](#-project-methodology)
8. [Output & Results](#-output--results)
9. [Technology Used](#-technology-used)
10. [Future Improvements](#-future-improvements)

---

## 🔎 Overview

Watching long-form lectures, tutorials, and technical presentations to take manual notes and capture slide screenshots is time-consuming. This project automates **multimodal knowledge extraction from video** by combining speech-to-text transcription, visual scene-change detection, and LLM-driven structuring into a single cohesive document.

- **Audio Pipeline (Transcription):** Extracts the audio track, generates timestamped transcripts, and segments spoken topics logically.
- **Visual Pipeline (Keyframe Screenshots):** Detects slide transitions, code changes, or major visual shifts to capture crisp, deduplicated keyframe screenshots.
- **Knowledge Synthesis (Alignment & Formatting):** Aligns timestamped transcript segments with their corresponding visual frames and synthesizes structured notes (headings, bullet points, definitions, and embedded screenshots).

| Component | Deliverable | Key Capability |
|---|---|---|
| Audio Processing | Timestamped Transcript (`.json` / `.srt`) | Accurate speech-to-text with segment-level timestamps |
| Visual Extraction | Deduplicated Keyframes (`screenshots/*.png`) | Automated scene/slide change detection filtering out static duplicates |
| Knowledge Output | Structured Study Guide (`output/notes.md` & `.pdf`) | Chronological markdown notes with inline screenshots aligned to topic timestamps |

---
## 🖼️ Screenshots & Demo

<div align="center">

### 1️⃣ Video Upload & Processing Pipeline

<table>
  <tr>
    <td align="center" width="50%">
      <img src="./screenshots/uploaded%20video.png" alt="Video Upload Interface" width="100%" />
      <br />
      <sub><b>Step 1 — Video Input:</b> Upload local video files directly through the dark-themed Streamlit interface</sub>
    </td>
    <td align="center" width="50%">
      <img src="./screenshots/steps%20for%20processing%20video.png" alt="Processing Pipeline Steps" width="100%" />
      <br />
      <sub><b>Step 2 — Multimodal Extraction:</b> Live progress tracking across audio transcription, frame extraction, and embedding generation</sub>
    </td>
  </tr>
</table>

---

### 2️⃣ Interactive Q&A & Timestamped Retrieval

<table>
  <tr>
    <td align="center" width="50%">
      <img src="./screenshots/general%20questions.png" alt="General Video Q&A" width="100%" />
      <br />
      <sub><b>Semantic Q&A:</b> Ask natural-language questions synthesized from both spoken audio and visual frames</sub>
    </td>
    <td align="center" width="50%">
      <img src="./screenshots/answers%20with%20timestamps.png" alt="Timestamp-Grounded Answers" width="100%" />
      <br />
      <sub><b>Exact Timestamp Citations:</b> Every generated answer points back to the exact video moments where the concept appears</sub>
    </td>
  </tr>
</table>

</div>

<details>
<summary>🔍 <b>Click to view full-resolution screenshots</b></summary>
<br />

- **Video Upload Interface:** ![Uploaded Video](./screenshots/uploaded%20video.png)
- **Processing Pipeline Steps:** ![Processing Steps](./screenshots/steps%20for%20processing%20video.png)
- **General Video Q&A:** ![General Questions](./screenshots/general%20questions.png)
- **Timestamped Answers:** ![Timestamped Answers](./screenshots/answers%20with%20timestamps.png)

</details>
---

## ⚙️ Requirements

**System Dependencies:**
- Python 3.10+
- **FFmpeg** (installed and available in system PATH for audio/video demuxing)
- Optional: CUDA-enabled GPU for faster Whisper transcription

**Python Packages:**
```
openai-whisper
opencv-python
scikit-image
numpy
Pillow
yt-dlp
google-generativeai   # or openai / langchain depending on your LLM backend
markdown2
```

---

## 🗂️ Project Structure

```
Video-Knowledge-Extraction/
├── assets/                                # README demo screenshots
│   ├── ui_overview.png
│   ├── extracted_keyframes.png
│   └── generated_notes_preview.png
├── input_videos/                          # Sample local videos (gitignored)
├── output/                                # Generated artifacts per video
│   ├── screenshots/                       # Extracted keyframe images (.png)
│   ├── transcript.json                    # Timestamped ASR output
│   └── knowledge_notes.md                 # Final structured document with inline images
├── src/
│   ├── audio_extractor.py                 # FFmpeg audio extraction & Whisper transcription
│   ├── frame_extractor.py                 # OpenCV / SSIM keyframe & slide-change detection
│   ├── aligner.py                         # Timestamp matching between text chunks & frames
│   └── summarizer.py                      # LLM prompt pipeline for structured knowledge synthesis
├── app.py                                 # Main CLI / Web entry point
├── requirements.txt
└── README.md                              # Top-level project documentation
```

## 🏗️ Architecture Pipeline

```
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


```

## 📊 Data & Inputs

**Supported Video Sources:**
- **Local video files:** `.mp4`, `.mkv`, `.avi`, `.mov`
- **Online URLs:** YouTube / lecture links (via `yt-dlp`)

**Intermediate & Output Data Artifacts:**
- **Audio Stream:** Mono 16kHz `.wav` extracted via FFmpeg for optimal ASR accuracy
- **Transcript Segments:** JSON array containing `{ "start": float, "end": float, "text": str }`
- **Candidate & Filtered Frames:** RGB frames sampled at fixed intervals (e.g., 1 FPS) and filtered via Structural Similarity Index (SSIM) / histogram difference thresholds to retain only meaningful visual transitions

---

## 🛠️ Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Video-Knowledge-Extraction

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Ensure FFmpeg is installed
ffmpeg -version

# 5. Set up your LLM API key (if using cloud LLM for summarization)
export GEMINI_API_KEY="your_api_key_here"   # or OPENAI_API_KEY

# 6. Run the pipeline on a video
python app.py --input "input_videos/sample_lecture.mp4" --output "output/"
```

---

## 🧭 Project Methodology

1. **Video Ingestion & Audio Extraction**
   - Accepts a local file or video URL and extracts a clean 16kHz mono `.wav` track using `FFmpeg`.
2. **Timestamped Speech-to-Text (ASR)**
   - Runs **OpenAI Whisper** to transcribe spoken content into timestamped segments (`start`, `end`, `text`).
3. **Keyframe & Slide Change Detection**
   - Samples frames across the video timeline using **OpenCV**.
   - Computes frame-to-frame visual difference using **SSIM (Structural Similarity Index)** / perceptual hashing to detect slide transitions, diagram updates, or code edits while discarding redundant static frames and blurry transitions.
4. **Multimodal Timestamp Alignment**
   - Groups transcript segments into coherent topic blocks and maps each block to the highest-clarity keyframe captured within its `[start, end]` window.
5. **LLM Knowledge Synthesis & Markdown Assembly**
   - Prompts an LLM to distill raw spoken transcripts into clean section headers, key takeaways, definitions, and code/formula callouts.
   - Injects relative Markdown image links (`![Slide at 04:12](./screenshots/frame_0252.png)`) directly beneath the relevant sections.

---

## 📈 Output & Results

- **Noise Reduction:** Keyframe deduplication typically reduces raw 1-FPS frame captures by **85%–95%**, keeping only distinct slides or visual states.
- **Structured Readability:** Converts unstructured spoken transcripts into hierarchical notes with executive summaries, bulleted insights, and visual context.
- **Portable Format:** Outputs pure Markdown (`.md`) alongside a self-contained `screenshots/` folder, ready for Notion, Obsidian, GitHub, or PDF export.

---

## 🧰 Technology Used

| Category | Tools |
|---|---|
| Video & Audio Processing | ![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?logo=ffmpeg&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white) `yt-dlp` |
| Speech Recognition (ASR) | ![Whisper](https://img.shields.io/badge/OpenAI_Whisper-412991?logo=openai&logoColor=white) |
| Image Similarity & Filtering | `scikit-image` (SSIM), `Pillow`, `NumPy` |
| Knowledge Structuring | LLM API (Gemini / OpenAI) + Prompt Engineering |
| Language & Runtime | ![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) |

---

## 🚀 Future Improvements

- 🔍 **OCR Integration (Tesseract / PaddleOCR):** Extract on-screen slide text and code snippets directly from keyframes to enrich LLM context when speakers reference visuals without reading them aloud
- 🗣️ **Speaker Diarization:** Integrate `pyannote.audio` to label multi-speaker interviews, podcasts, and panel discussions
- 🔎 **Semantic RAG Search:** Index extracted text chunks and image captions into a vector database (FAISS / ChromaDB) so users can ask questions across a library of videos
- 🌐 **Interactive Web UI:** Build a Streamlit or Gradio dashboard allowing users to preview timestamps, tweak sensitivity thresholds, and export directly to Notion or PDF

---


## 👤 Author

* **Ankit Kumar Jha** - [GitHub Profile](https://github.com/Ankit-Kumar-Jha-01) | [LinkedIn](https://www.linkedin.com/in/ankit-kumar-jhaa)

---

<div align="center">
Built for automated multimodal learning and video knowledge extraction
</div>

