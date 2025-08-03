# chatbot_project
This is a full-stack functional AI chatbot, built specifically for PT Elmecon Multikencana as a Coding challenge.

This project combine a FAQ-based chatbot and product recommendation system powered by semantic search using FAISS and MiniLM embeddings.

The features including (but not limited to) :
- Natural language FAQ response system using MySQL Workbench
- Semantic product search using FAISS and sentence-transformers
- Deepseek AI fallback for complex queries
- Web-based frontend with persistent chat history

---------------------------------------------------------------------------------------------------

Limitations :
- This AI is not built using PHP CodeIgniter4 Framework, Python is used fully, with js and html for frontend
- The threshold for product similarity is still in test phase, recommendation between 0.5 to 0.9

---------------------------------------------------------------------------------------------------

Setup instructions :
1. Clone the repository

```bash
git clone https://github.com/your-repo/chatbot_project.git
cd chatbot_project

2. Install dependencies 

pip install -r requirements.text

3. Prepare your MySQL Database

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


note : you can change the FAQ on the list, according to your liking

4. Run these python app to embed the datas and generate and save FAISS index

python embed_products.py
python build_index.py

5. Run the app

python app.py

then visit the link provided from the app console

---------------------------------------------------------------------------------------------------
Author
Axel Julian Sutanto

Contact: axeliotandai@gmail.com
