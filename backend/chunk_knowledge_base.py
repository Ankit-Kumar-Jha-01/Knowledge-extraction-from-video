import json

with open("video_knowledge_base.json", "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)

chunks = []

CHUNK_SIZE = 3
OVERLAP = 1

for topic in knowledge_base["topics"]:

    segments = topic["transcript_segments"]

    for i in range(0, len(segments), CHUNK_SIZE - OVERLAP):

        group = segments[i:i + CHUNK_SIZE]

        if not group:
            break

        transcript_text = " ".join(
            segment["text"] for segment in group
        )

        start_time = group[0]["start"]
        end_time = group[-1]["end"]

        chunk_text = f"""
Topic: {topic['title']}

Spoken Content: {transcript_text}
"""

        chunks.append({
            "chunk_id": len(chunks) + 1,
            "topic": topic["title"],
            "start_seconds": start_time,
            "end_seconds": end_time,
            "text": chunk_text.strip()
        })

        if i + CHUNK_SIZE >= len(segments):
            break


with open("video_chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=4, ensure_ascii=False)

print("Chunking completed!")
print("Total chunks:", len(chunks))
print("Saved as video_chunks.json")