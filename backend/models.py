from pydantic import BaseModel

class SignUpData(BaseModel):
  email: str
  username: str
  password: str

class LogInData(BaseModel):
  email: str
  username: str
  password: str

class TransactionData(BaseModel):
  username: str
  date: str
  category: str
  amount: float
  description: str
  type: str