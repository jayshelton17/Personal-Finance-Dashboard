from fastapi import FastAPI, HTTPException
from user import UserManagement, TransactionManagement
from models import SignUpData, LogInData, TransactionData

app = FastAPI()
user_manager = UserManagement()
transaction_manager = TransactionManagement(user_manager)

# Sign Up page
@app.get("/signup")
def signup_get():
  return {"message": "This is the signup page (GET)"}

@app.post("/signup")
def sign_up(data: SignUpData):
  for user in user_manager.users:
    if user['email'] == data.email:
      raise HTTPException(status_code=400, detail="Email already exists")
    if user['username'] == data.username:
      raise HTTPException(status_code=400, detail="Username already exists")
    
  hashed_pw = user_manager.hash_password(data.password)

  user_manager.users.append({
    'email': data.email,
    'username': data.username,
    'password': hashed_pw
  })
  user_manager.user_transactions[data.username] = []
  return {'message': f"{data.username} successfully signed up!"}


# Login Page
@app.get("/login")
def login_get():
  return {"message": "This is the login page (GET)"}

@app.post("/login")
def login(data: LogInData):
  for user in user_manager.users:
    if user['username'] == data.username:
      if user_manager.verify_password(data.password, user['password']):
        return {'message': f"{data.username} has successfully logged in!"}
      raise HTTPException(status_code=401, detail="Incorrect password")
  raise HTTPException(status_code=404, detail="No username found")

# Adding Transactions
@app.post("/transactions/add")
def add_transactions(data: TransactionData):
  if data.username not in user_manager.user_transactions:
    raise HTTPException(status_code=404, detail="User not found")
  
  user_manager.user_transactions[data.username].append({
    "date": data.date,
    "category": data.category,
    "amount": data.amount,
    "description": data.description,
    "type": data.type
  })

  return {"message": f"Transaction added for {data.username}"}

# Removing Transactions
@app.delete("/transactions/remove")
def remove_transactions(username: str, index: int):
  transactions = user_manager.user_transactions.get(username, [])
  if not transactions:
    raise HTTPException(status_code=404, detail="No transactions to remove")
  
  if index < 0 or index >= len(transactions):
    raise HTTPException(status_code=400, detail="Invalid transaction index")
  
  removed_transaction = transactions.pop(index)
  return {"message": f"Removed transaction: {removed_transaction}"}

# Viewing Transactions
@app.get("/transactions/view")
def view_transactions(username: str):
  transactions = user_manager.user_transactions.get(username, [])
  if not transactions:
    return {"message": "No transactions found."}
  
  return {"transactions": transactions}