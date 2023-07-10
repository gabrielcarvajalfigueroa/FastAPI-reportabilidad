from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from sqlalchemy.orm import Session
from schemas import CreateJobRequest
from database import get_db
from models import Job


app = FastAPI()

origins = [
    config("FRONTEND_URL")
]

#Se utiliza el middleware para aceptar las request del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
def create(details: CreateJobRequest, db: Session = Depends(get_db)):
    to_create = Job(
        title=details.title,
        description=details.description
    )
    db.add(to_create)
    db.commit()
    return { 
        "success": True,
        "created_id": to_create.id
    }

@app.get("/")
def get_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.id == id).first()