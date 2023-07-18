from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, get_users_objects, get_requests_objects
from schemas import UserCreate, UserRequestCreate
from models import User, User_request

users = APIRouter()

@users.get("/api/users")
def get_users_in_db(db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios de la base de datos.
    """
    users_in_db = get_users_objects()
    return {"users": users_in_db}

@users.post("/api/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.

    - **user**: Objeto de tipo UserCreate que contiene los datos del usuario a crear.
    """
    new_user = User(
        email=user.email,
        password=user.password,
        name=user.username,
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}

@users.get("/api/users_requests")
def get_requests_in_db(db: Session = Depends(get_db)):
    """
    Obtiene todas las solicitudes de los usuarios del sistema.
    """
    users_requests_in_db = get_requests_objects()
    return {"users_requests": users_requests_in_db}

@users.post("/api/users_requests")
def create_user_request(user_request: UserRequestCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva solicitud de usuario en el sistema.

    - **user_request**: Objeto de tipo UserRequestCreate que contiene los datos de la solicitud de usuario.
    """
    new_user_request = User_request(
        email=user_request.email,
        message=user_request.message,        
    )
    db.add(new_user_request)
    db.commit()
    db.refresh(new_user_request)
    return {"message": "User request created successfully", "user_request": new_user_request}
