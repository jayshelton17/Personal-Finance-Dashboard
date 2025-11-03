import bcrypt

class UserManagement:
  def __init__(self):
    self.users = []
    self.user_transactions = {}

  def hash_password(self, password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
  
  def verify_password(self, password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

  def sign_up(self):
    email = input("Enter your email: ")
    user_name = input("Create a username: ")
    password = input("Create a password: ")

    for user in self.users:
      if user['email'] == email:
        print("Email already exists. Try again!")
        return
      elif user['username'] == user_name:
        print("Username already taken. Try again!")
        return

    hashed_pw = self.hash_password(password)  
    self.users.append({
    'email': email,
    'username': user_name,
    'password': hashed_pw
    })
    self.user_transactions[user_name] = []
    print("Successfully signed up!")
    
  def login(self):
    user_name = input("Enter your username: ")
    password = input("Enter your password: ")
    
    for user in self.users:
      if user['username'] == user_name:
        if self.verify_password(password, user['password']):
          print("Login Successfull")
          return user_name
        else:
          print("Incorrect password")
          return None
    
    print('Username not found')
    return None

class TransactionManagement:
  def __init__(self, user_manager):
    self.user_manager = user_manager

  def add_transaction(self, username):
    date = input("Enter today's date: ")
    category = input("Enter a category: ")
    amount = float(input("Enter how much was it: "))
    description = input("Enter a description: ")
    type = input("Was this an expense or income: ")

    transaction = {
    "date": date,
    "category": category,
    "amount": amount,
    "description": description,
    "type": type
    }
    self.user_manager.user_transactions[username].append(transaction)
    print(f"Transaction added for {username}")


  def remove_transaction(self, username):
    transactions = self.user_manager.user_transactions.get(username, [])
    if not transactions:
      print("No transactions to remove.")
      return
    
    self.view_transactions(username)
    try:
      remove_index = int(input("Enter the number of the transaction to remove: ")) - 1
      if 0 <= remove_index < len(transactions):
        removed = transactions.pop(remove_index)
        print(f"Transaction removed: {removed}")
      else:
        print("Invalid transaction number.")
    except ValueError:
      print("Please enter a valid number.")

  def view_transactions(self, username):
    transactions = self.user_manager.user_transactions.get(username, [])
    if not transactions:
      print("No transactions found.")
      return
    print(f"\nSaved Transactions for {username}:")
    for index, tr in enumerate(transactions):
      print(f"{index + 1}. {tr}")

# Calling Classes
calling_um = UserManagement()
calling_tr = TransactionManagement(calling_um)