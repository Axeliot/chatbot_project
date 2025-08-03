import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def search_faq(keyword):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT answer FROM faq WHERE question LIKE %s", ('%' + keyword + '%',))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['answer'] if result else None

def save_chat_history(user_msg, bot_msg):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_message, bot_response) VALUES (%s, %s)", (user_msg, bot_msg))
    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat_history ORDER BY id DESC LIMIT 10")
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history
