from pydantic import BaseModel

class LoginCredential(BaseModel):
    username: str
    password: str