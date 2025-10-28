class UserManagement:
  def __init__(self):
    self.users = []
    self.user_transactions = {}

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
      
    self.users.append({
    'email': email,
    'username': user_name,
    'password': password
    })
    self.user_transactions[user_name] = []
    print("Successfully signed up!")
    

  def login(self):
    user_name = input("Enter your username: ")
    password = input("Enter your password: ")
    
    for user in self.users:
      if user['username'] == user_name:
        if user['password'] == password:
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


while True:
  # Login Page
  print('\n1. Sign Up')
  print('2. Login')
  print('3. Exit')
  try:
    user_choice = int(input('Enter an option: '))
  except ValueError:
    print("Invalid input. Please enter a number.")
    continue

  if user_choice == 1:
    calling_um.sign_up()

  elif user_choice == 2:
    logged_in_user = calling_um.login()
    if not logged_in_user:
      continue

    # Logged in menu
    while True:
      print('\n===========================')
      print(f"Welcome, {logged_in_user}")
      print('Personal Finance Dashboard')
      print('1. Add Transaction')
      print('2. Remove Transaction')
      print('3. View Transactions')
      print('4. Logout')
      print('===========================')
      
      try:
        choice = int(input('Enter an option: '))
      except ValueError:
        print('Invalid input. Please enter a number.')
        continue

      if choice == 1:
        calling_tr.add_transaction(logged_in_user)
      elif choice == 2:
        calling_tr.remove_transaction(logged_in_user)
      elif choice == 3:
        calling_tr.view_transactions(logged_in_user)
      elif choice == 4:
        print("Logging out")
        break
      else:
        print('Invalid option please try again.')

  elif user_choice == 3:
    print("Goodbye!")
    break

  else:
    print('Invalid. Try again!')