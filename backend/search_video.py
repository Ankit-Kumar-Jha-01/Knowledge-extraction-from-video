
# import json
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load chunks
# with open("video_chunks.json", "r", encoding="utf-8") as file:
#     chunks = json.load(file)

# # Load existing embeddings
# embeddings = np.load("video_embeddings.npy")

# # Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# while True:

#     question = input("\nAsk a question about the video (or type exit): ")

#     if question.lower() == "exit":
#         break

#     # Convert question into an embedding
#     question_embedding = model.encode([question])

#     # Compare question with all chunk embeddings
#     similarities = cosine_similarity(
#         question_embedding,
#         embeddings
#     )[0]

#     # Get the 3 most relevant chunks
#     top_indices = np.argsort(similarities)[::-1][:3]

#     print("\nMost relevant video sections:\n")

#     for index in top_indices:

#         chunk = chunks[index]

#         print("Topic:", chunk["topic"])
#         print("Start:", chunk["start_seconds"], "seconds")
#         print("End:", chunk["end_seconds"], "seconds")
#         print("Similarity:", round(float(similarities[index]), 3))
#         print("Content:", chunk["text"])
#         print("-" * 50)



import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai

# 1. Load knowledge chunks
with open("video_chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

# 2. Load existing embeddings
embeddings = np.load("video_embeddings.npy")

# 3. Load embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Connect to Gemini
client = genai.Client()

print("\nVideo Knowledge Assistant is ready!")

while True:
    question = input("\nAsk a question about the video (or type exit): ")

    if question.lower().strip() == "exit":
        print("Goodbye!")
        break

    # STEP 1: RETRIEVAL
    question_embedding = embedding_model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        embeddings
    )[0]

    top_indices = np.argsort(similarities)[::-1][:3]

    # Prepare retrieved context
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

    # STEP 2: AUGMENTATION
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

    # STEP 3: GENERATION
    print("\nGenerating answer...")

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        answer = response.text.strip()

        if answer.startswith("INSUFFICIENT"):
            print("\nAnswer:")
            print("The video information is insufficient to answer this question.")

        else:
            print("\nAnswer:\n")
            print(answer)

            # Display source timestamps
            print("\nVideo references:\n")

            for rank, index in enumerate(top_indices, start=1):
                chunk = chunks[index]

                start = chunk["start_seconds"]
                end = chunk["end_seconds"]

                start_time = f"{int(start // 60):02d}:{int(start % 60):02d}"
                end_time = f"{int(end // 60):02d}:{int(end % 60):02d}"

                print(
                    f"[Source {rank}] {chunk['topic']} "
                    f"({start_time} - {end_time})"
                )

    except Exception as error:
        print("\nSomething went wrong:")
        print(error)