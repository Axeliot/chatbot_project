# chatbot\_project

This is a full-stack functional AI chatbot, built specifically for PT Elmecon Multikencana as a coding challenge.

This project combines a FAQ-based chatbot and a product recommendation system powered by semantic search using **FAISS** and **MiniLM** embeddings.

## ✨ Features

* Natural language FAQ response system using MySQL
* Semantic product search using FAISS and Sentence-Transformers
* Deepseek AI fallback for complex queries
* Web-based frontend with persistent chat history

---

## ⚠️ Limitations

* This chatbot is **not** built using PHP CodeIgniter4 as initially requested — it's fully built with **Python**, HTML, and JavaScript.
* Product similarity threshold is still under experimentation (recommendation scores typically range between **0.5 to 0.9**).

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/chatbot_project.git
cd chatbot_project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare your MySQL database

```sql
CREATE DATABASE chatbot_db;
USE chatbot_db;

CREATE TABLE faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO faq (question, answer) VALUES
('What are your business hours?', 'We are open from 9 AM to 5 PM, Monday to Friday.'),
('Do you offer international shipping?', 'Yes, we ship worldwide.'),
('How can I reset my password?', 'Click on "Forgot password" at the login screen.'),
('Where is your store located?', 'We are located at 123 Main Street, Jakarta.'),
('What payment methods are accepted?', 'We accept credit cards, PayPal, and bank transfers.'),
('How can I track my order?', 'You can track your order status from your account dashboard under "My Orders".'),
('Do you provide installation services?', 'Yes, we offer installation services for select products. Please contact support for details.'),
('What payment methods do you accept?', 'We accept credit/debit cards, bank transfers, and e-wallets.'),
('Can I get a quotation before purchasing?', 'Yes, you can request a quotation by contacting our sales team through email or the contact form.'),
('What is your return policy?', 'Returns are accepted within 14 days of delivery for unused items in original packaging.');
```

📝 **Note**: You can modify the FAQ entries according to your business needs.

🔐 **Don't forget** to edit your credentials in `app.py` and `config.py` (e.g., database password, API keys, etc.)

---

### 4. Embed the product data and generate FAISS index

```bash
python embed_products.py
python build_index.py
```

These scripts will:

* Load `products.json`
* Embed product descriptions using MiniLM
* Build a FAISS index and save it to `faiss_index.pkl`
* Save product metadata to `product_data.json`

### 5. Run the chatbot app

```bash
python app.py
```

Visit the local link displayed in your terminal to open the web-based chat interface.

---

## 📦 Sample Product Data

Your product data must be saved in a file named `products.json` before embedding. Here's a sample structure:

```json
[
  {
    "title": "Miniature Circuit Breaker S202-C16",
    "description": "The S202-C16 from ABB is a 2-pole miniature circuit breaker with C characteristic and 16A rated current.",
    "url": "https://electgo.com/product/ab-2cds252001r0164-s202-c16"
  },
  {
    "title": "Contactor A9F74210",
    "description": "Schneider Electric A9F74210 circuit breaker 2-pole, 10A, DIN rail mounted.",
    "url": "https://electgo.com/product/se-a9f74210"
  }
]
```

---

## 📡 Example API Request and Response

### Endpoint

```http
POST /chat
```

### Request Body

```json
{
  "message": "Do you have a 16A miniature circuit breaker?"
}
```

### Response (example)

```json
{
  "response": "Yes, we have a Miniature Circuit Breaker available: Miniature Circuit Breaker S202-C16 - [View Product](https://electgo.com/product/ab-2cds252001r0164-s202-c16)"
}
```

---------------------------------------------------------------------------------------------------
Author
Axel Julian Sutanto

Contact: axeliotandai@gmail.com
