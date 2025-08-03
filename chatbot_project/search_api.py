from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

app = Flask(__name__)

# Load FAISS index
index = faiss.read_index("product_index.faiss")

# Load metadata
with open("product_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    # Embed query
    query_vector = model.encode([query])
    
    # Search FAISS
    k = 3
    D, I = index.search(np.array(query_vector), k)

    # Prepare results
    results = []
    for i, score in zip(I[0], D[0]):
        if i < len(metadata):
            results.append({
                "name": metadata[i]["name"],
                "description": metadata[i]["description"],
                "score": float(score)
            })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
