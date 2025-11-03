import sqlite3

conn = sqlite3.connect('finance.db')

cursor = conn.cursor()

command1 = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL, 
    email TEXT NOT NULL, 
    hash_password TEXT NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """

cursor.execute(command1)

command2 = """
CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  type TEXT NOT NULL,
  category_id INTEGER,
  description TEXT,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
  """

cursor.execute(command2)
conn.commit()
conn.close()

