from fastapi import FastAPI, HTTPException
from models import SignUpData, LogInData, TransactionData
from database import get_db_connection
import bcrypt

app = FastAPI()

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed.decode('utf-8')
  
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_user_by_username(username: str):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
  user = cursor.fetchone()
  conn.close()
  return user

def get_user_by_email(email: str):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
  user = cursor.fetchone()
  conn.close()
  return user


@app.post("/signup")
def sign_up(data: SignUpData):
  if get_user_by_email(data.email):
    raise HTTPException(status_code=400, detail="Email already exists.")
  if get_user_by_username(data.username):
    raise HTTPException(status_code=400, detail="Username is taken.")
    
  hashed_pw = hash_password(data.password)
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
    "INSERT INTO users (username, email, hash_password) VALUES (?, ?, ?)",
    (data.username, data.email, hashed_pw)

  )
  conn.commit()
  conn.close()
  return {"message": f"{data.username} successfully signed up!"}

@app.post("/login")
def login(data: LogInData):
  user = get_user_by_username(data.username)
  if not user:
    raise HTTPException(status_code=404, detail="Username not found")
  if not verify_password(data.password, user["hash_password"]):
    raise HTTPException(status_code=401, detail="Incorrect password")
  return {"message": f"{data.username} successfully logged in!"}

# Adding Transactions
@app.post("/transactions/add")
def add_transactions(data: TransactionData):
  user = get_user_by_username(data.username)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
    "INSERT INTO transactions (user_id, amount, type, category_id, description, date) VALUES (?, ?, ?, ?, ?, ?)",
    (user["id"], data.amount, data.type, data.category_id, data.description, data.date)
  )
  conn.commit()
  conn.close()
  return {"message": f"Transaction added for {data.username}"}

# View Transactions
@app.get("/transactions/view")
def view_transactions(username: str):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user["id"],))
    transactions = [dict(tx) for tx in cursor.fetchall()]
    conn.close()

    if not transactions:
        return {"message": "No transactions found."}
    return {"transactions": transactions}


# Remove Transaction by ID
@app.delete("/transactions/remove")
def remove_transaction(username: str, transaction_id: int):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user["id"]))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Transaction not found")
    conn.commit()
    conn.close()
    return {"message": f"Transaction {transaction_id} removed for {username}"}