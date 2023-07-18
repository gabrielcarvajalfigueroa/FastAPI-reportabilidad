from datetime import date
from pydantic import BaseModel
from fastapi import File, UploadFile

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool

class UserRequestCreate(BaseModel):
    name: str
    email: str
    date: date
    status: str
    message: str

class UserRequestUpdate(BaseModel):
    id_request: int
    status: str


class FileSchema(BaseModel):
    archivoRecibido: UploadFile 
