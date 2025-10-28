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