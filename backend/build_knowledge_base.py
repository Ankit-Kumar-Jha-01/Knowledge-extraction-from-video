
import json


with open("transcript.json", "r", encoding="utf-8") as file:
    transcript = json.load(file)

with open("video_knowledge.json", "r", encoding="utf-8") as file:
    video_knowledge = json.load(file)



topics = video_knowledge["topics"]

for topic in topics:

    topic_start = topic["start_seconds"]
    topic_end = topic["end_seconds"]

    matched_segments = []

    for segment in transcript:

        overlap = min(segment["end"], topic_end) - max(
            segment["start"], topic_start
        )

        if overlap > 0:
            matched_segments.append(segment)

    topic["transcript_segments"] = matched_segments



knowledge_base = {
    "video_summary": video_knowledge["video_summary"],
    "topics": topics
}



with open(
    "video_knowledge_base.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        knowledge_base,
        file,
        indent=4,
        ensure_ascii=False
    )


print("Knowledge base created successfully!")

print("\nTotal topics:", len(topics))

print("Total transcript segments:", sum(
    len(topic["transcript_segments"]) for topic in topics
))

print("\nSaved as video_knowledge_base.json")
