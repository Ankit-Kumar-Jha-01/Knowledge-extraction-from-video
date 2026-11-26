from faster_whisper import WhisperModel
import json

model = WhisperModel("small")

segments, info = model.transcribe("sample.mp4")

transcript = []

for segment in segments:
    transcript.append({
        "start": round(segment.start, 2),
        "end": round(segment.end, 2),
        "text": segment.text.strip()
    })

with open("transcript.json", "w", encoding="utf-8") as f:
    json.dump(transcript, f, indent=4, ensure_ascii=False)

print(f"Detected language: {info.language}")
print(f"Saved {len(transcript)} transcript segments to transcript.json")