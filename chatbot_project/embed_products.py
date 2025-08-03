import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load product data
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Use title + description for embedding
texts = [f"{p['title']} {p.get('description', '')}" for p in products]

# Save original metadata for later retrieval
metadata = [{"title": p["title"], "url": p["url"], "description": p.get("description", "")} for p in products]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, convert_to_numpy=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, "product_index.faiss")
with open("product_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("✅ Embeddings created and saved.")
