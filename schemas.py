from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool

class UserRequestCreate(BaseModel):
    email: str
    message: str