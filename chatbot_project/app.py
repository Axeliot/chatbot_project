from flask import Flask, request, jsonify, render_template
import mysql.connector
import requests
import json
import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# API Key for deepseek
OPENROUTER_API_KEY = "enter your openrouter API key here"
DEEPSEEK_URL = "https://openrouter.ai/api/v1/chat/completions"

# Feel free to change the threshold below to suit your liking
EMBEDDING_THRESHOLD = 0.8 
TOP_K = 3

# Load model and prepare index 
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
try:
    index = faiss.read_index("faiss_index.faiss")
    print("✅ FAISS index loaded.")
except Exception as e:
    print(f"❌ Error loading FAISS index: {e}")

# Load product data
try:
    with open('product_data.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    print("Product data loaded.")
except Exception as e:
    print(f"Error loading product data: {e}")

# Database Connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Password1',
    database='chatbot_db'
)

# Routes
@app.route('/')
def home():
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chat_history ORDER BY created_at ASC LIMIT 20")
    history = cursor.fetchall()
    return render_template('chat.html', history=history)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    cursor = conn.cursor()

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    similar_products = []

    # Step 1: Check FAQ table
    cursor.execute("SELECT answer FROM faq WHERE question LIKE %s", (f"%{user_input}%",))
    faq_result = cursor.fetchone()

    if faq_result:
        response = faq_result[0]
    elif index is not None and products:
        # Step 2: Semantic product search
        query_embedding = model.encode([user_input])
        distances, indices = index.search(query_embedding, TOP_K)

        for i, dist in zip(indices[0], distances[0]):
            if i < len(products) and dist < EMBEDDING_THRESHOLD:
                similar_products.append(products[i])

        if similar_products:
            response = "Here are some products that match your query:\n\n"
            for p in similar_products:
                name = p.get('title', 'Unnamed Product')
                desc = p.get('description', 'No description available.')
                url = p.get('url', '#')
                response += f"- {name}: {desc}\n  👉 {url}\n\n"
        else:
            response = ask_deepseek(user_input, context_products=None)
    else:
        response = ask_deepseek(user_input, context_products=None)

    # Save chat history
    cursor.execute("INSERT INTO chat_history (user_message, bot_response) VALUES (%s, %s)", (user_input, response))
    conn.commit()

    return jsonify({"response": response})

# Deepseek fallback 
def ask_deepseek(user_input, context_products=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are a helpful assistant for ElectGo, an E-commerce platform offering a comprehensive range of industrial products from leading brands worldwide, such as 3M, ABB, Brady, Omron, Philips Lighting, Panduit, Schneider Electric, Werma, Weidmuller, and more. ElectGo has been expanding its range of products, carrying over 60,000 SKUs, from various industries to cater to the market demands. "
        "Recommend products clearly using the provided data. "
        "Never fabricate product information or links. "
        "If the data does not match the query, respond: 'Sorry, I couldn't find a matching product.'"
    )

    def format_product(p):
        name = p.get("title", "Unnamed Product")
        desc = p.get("description", "No description available.")
        url = p.get("url", "No URL available.")
        return f"""🔹 **{name}**
{desc}
📦 [View Product]({url})
"""

    if context_products:
        formatted = "\n\n".join(format_product(p) for p in context_products)
        user_prompt = f"""Here are some possibly related products:

{formatted}

Customer question: {user_input}"""
    else:
        user_prompt = user_input

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        r = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            print("Deepseek API Error:", r.text)
            return "Sorry, I couldn't process your request at the moment."
    except Exception as e:
        print(f"Error contacting Deepseek: {e}")
        return "I don't understand."


# Run the app 
if __name__ == '__main__':
    app.run(debug=True)
