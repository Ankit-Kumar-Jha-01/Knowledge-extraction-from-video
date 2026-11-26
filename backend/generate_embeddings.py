import json
import numpy as np
from sentence_transformers import SentenceTransformer

with open("video_chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in chunks]

print("Generating embeddings...")
embeddings = model.encode(texts)

np.save("video_embeddings.npy", embeddings)

print("\nEmbeddings generated successfully!")
print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("Saved as video_embeddings.npy")