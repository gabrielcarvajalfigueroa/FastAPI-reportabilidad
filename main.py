from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from sqlalchemy.orm import Session
from schemas import CreateJobRequest
from database import get_db
from routes.dailyload import dailyload
from models import Pit
import pandas as pd


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

app.include_router(dailyload)