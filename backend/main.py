# from faster_whisper import WhisperModel

# # Load Whisper
# model = WhisperModel("small")

# # Transcribe the video
# segments, info = model.transcribe("sample.mp4")

# print("Detected language:", info.language)
# print("\nTranscript:\n")

# for segment in segments:
#     print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")


from faster_whisper import WhisperModel
import json

# Load Whisper
model = WhisperModel("small")

# Transcribe the video
segments, info = model.transcribe("sample.mp4")

transcript = []

for segment in segments:
    transcript.append({
        "start": round(segment.start, 2),
        "end": round(segment.end, 2),
        "text": segment.text.strip()
    })

# Save transcript
with open("transcript.json", "w", encoding="utf-8") as f:
    json.dump(transcript, f, indent=4, ensure_ascii=False)

print(f"Detected language: {info.language}")
print(f"Saved {len(transcript)} transcript segments to transcript.json")