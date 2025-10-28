from pydantic import BaseModel

class SignUpData(BaseModel):
  email: str
  username: str
  password: str

class LogInData(BaseModel):
  email: str
  username: str
  password: str