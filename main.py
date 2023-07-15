from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from sqlalchemy.orm import Session
from schemas import CreateJobRequest
from database import get_db
from routes.dailyload import dailyload
from routes.reports import reports
from models import Pit
import pandas as pd

# Se inicializa la FastAPI
app = FastAPI()

# Se recopilan los datos del .env
origins = [
    config("FRONTEND_URL")
]

#Se utiliza el middleware para aceptar las request del frontend
# buscar forma para recibir todas las request sin agregar URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Se incluyen las rutas creadas en la carpeta routes
app.include_router(dailyload)
app.include_router(reports)