from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SignUpData(BaseModel):
  email: str
  username: str
  password: str

class LogInData(BaseModel):
  username: str
  password: str

class TransactionData(BaseModel):
  username: str
  amount: float
  type: str
  category_id: Optional[int] = None
  description: Optional[str] = None
  date: Optional[datetime] = None