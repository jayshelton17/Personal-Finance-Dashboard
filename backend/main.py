from fastapi import FastAPI, HTTPException
from user import UserManagement, TransactionManagement
from models import SignUpData, LogInData

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
  return {'message': "Successfully signed up!"}


# Login Page
@app.get("/login")
def login_get():
  return {"message": "This is the login page (GET)"}

@app.post("/login")
def login(data: LogInData):
  for user in user_manager.users:
    if user['username'] == data.username:
      if user_manager.verify_password(data.password, user['password']):
        return {'message': "Successfully logged in!"}
      raise HTTPException(status_code=401, detail="Incorrect password")
  raise HTTPException(status_code=404, detail="No username found")