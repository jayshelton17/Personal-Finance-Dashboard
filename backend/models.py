class UserManagement:
  def __init__(self):
    self.users

class TransactionManagement:
  def __init__(self):
    self.transaction = []

  def add_transaction(self, transaction):
    self.transaction.append(transaction)
    print(f"Transaction {transaction} added.")
  
  def remove_transaction(self, transaction):
    if transaction in self.transaction:
      self.transaction.remove(transaction)
      print(f'Transaction {transaction} removed.')
    else:
      print(f'Transaction {transaction} not found.')

  def view_transactions(self):
    print('Saved Transactions:')
    for index, tr in enumerate(self.transaction):
      print(f"{index + 1}. {tr}")

calling = TransactionManagement()

while True:
  print('===========================')
  print('Personal Finance Dashboard')
  print('1. Add Transaction')
  print('2. Remove Transaction')
  print('3. View Transactions')
  print('4. Exit')
  print('===========================')
  
  try:
    user = int(input('Enter an option: '))
  except ValueError:
    print('Invalid input. Please enter a number.')
    continue
  if user == 1:
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
    
    calling.add_transaction(transaction)

  elif user == 2:
    calling.view_transactions()
    try:
      remove_index = int(input("Enter the number of the transaction to remove: ")) - 1
      if 0 <= remove_index < len(calling.transaction):
        removed = calling.transaction.pop(remove_index)
        print(f"Transaction removed: {removed}")
      else:
        print("Invalid transaction.")
    except ValueError:
      print("Please enter a valid number.")

  elif user == 3:
    calling.view_transactions()
  
  elif user == 4:
    print("Exiting dashboard!")
    break

  else:
    print('Invalid option please try again.')