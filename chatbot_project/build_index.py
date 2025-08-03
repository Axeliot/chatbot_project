# build_index.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load your products
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare descriptions for embedding
descriptions = [product["description"] for product in products]
embeddings = model.encode(descriptions, convert_to_numpy=True)

# Build FAISS index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)

# ✅ Save FAISS index using FAISS method, NOT pickle
faiss.write_index(index, "faiss_index.faiss")

# Save product data
with open("product_data.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("✅ FAISS index and product data saved.")

