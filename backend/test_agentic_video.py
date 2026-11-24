import time
import json
from google import genai

client = genai.Client()

# Define the JSON structure Gemini must follow
video_schema = {
    "type": "OBJECT",
    "properties": {
        "video_summary": {
            "type": "STRING"
        },
        "topics": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "start_seconds": {
                        "type": "NUMBER"
                    },
                    "end_seconds": {
                        "type": "NUMBER"
                    },
                    "title": {
                        "type": "STRING"
                    },
                    "explanation": {
                        "type": "STRING"
                    },
                    "visual_details": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    },
                    "key_information": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                },
                "required": [
                    "start_seconds",
                    "end_seconds",
                    "title",
                    "explanation",
                    "visual_details",
                    "key_information"
                ]
            }
        }
    },
    "required": ["video_summary", "topics"]
}

try:
    # STEP 1: Upload video
    print("Uploading video...")

    video_file = client.files.upload(file="sample.mp4")

    # STEP 2: Wait for video preparation
    while video_file.state.name == "PROCESSING":
        print("Preparing video...")
        time.sleep(3)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        raise RuntimeError("Video preparation failed.")

    print("Video is ready!")

    # STEP 3: Analyze video and request structured JSON
    print("Starting video analysis...")

    interaction = client.interactions.create(
        model="gemini-4-hydrogen",
        input=[
            {
                "type": "video",
                "uri": video_file.uri,
                "mime_type": video_file.mime_type,
                "processing": "static"
            },
            {
                "type": "text",
                "text": """
                Analyze this programming tutorial.

                Divide the video into meaningful topics.

                For every topic:
                1. Identify its start and end timestamps.
                2. Give a short title.
                3. Explain what is discussed.
                4. Describe important visual information.
                5. Extract important information, code,
                   or text shown in the video.

                Timestamps must be numeric seconds from
                the beginning of the video.

                Do not invent details or timestamps.
                If a visual or key information is absent,
                return an empty list.

                Follow the supplied JSON structure exactly.
                """
            }
        ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": video_schema
        },
        background=True
    )

    # STEP 4: Wait for analysis
    while interaction.status in ("queued", "in_progress"):
        print("Gemini is analyzing the video...")
        time.sleep(5)
        interaction = client.interactions.get(interaction.id)

    # STEP 5: Parse and save JSON
    if interaction.status == "completed":

        video_knowledge = json.loads(interaction.output_text)

        with open(
            "video_knowledge.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                video_knowledge,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nVideo analysis completed!")
        print("Saved to video_knowledge.json")

        print("\nExtracted topics:")
        for topic in video_knowledge["topics"]:
            print(
                topic["start_seconds"],
                "-",
                topic["title"]
            )

    else:
        print("\nAnalysis failed.")
        print("Status:", interaction.status)
        print("Errors:", interaction.errors)

except json.JSONDecodeError as error:
    print("Gemini returned invalid JSON:", error)

except Exception as error:
    print("\nSomething went wrong:")
    print(error)
