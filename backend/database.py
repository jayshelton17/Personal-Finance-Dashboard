import sqlite3
import os

# Path to finance.db inside backend folder
db_path = os.path.join(os.path.dirname(__file__), "finance.db")

def get_db_connection():
    """Return a SQLite connection with dict-like rows."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Automatically create tables when database.py is imported
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT NOT NULL, 
        email TEXT NOT NULL, 
        hash_password TEXT NOT NULL, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        category_id INTEGER,
        description TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

# Call the initializer automatically
init_db()
