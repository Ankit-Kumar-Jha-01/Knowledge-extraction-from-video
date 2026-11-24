
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Load our chunks
with open("video_chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

# 2. Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. Extract text from every chunk
texts = [chunk["text"] for chunk in chunks]

# 4. Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(texts)

# 5. Save embeddings
np.save("video_embeddings.npy", embeddings)

print("\nEmbeddings generated successfully!")
print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("Saved as video_embeddings.npy")
