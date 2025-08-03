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
