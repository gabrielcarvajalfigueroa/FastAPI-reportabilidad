from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from sqlalchemy.orm import Session
from database import get_db
from routes.dailyload import dailyload
from routes.reports import reports
from routes.users import users
from models import Pit


# Se inicializa la FastAPI
app = FastAPI()

# Configurar los orígenes permitidos
origins = ["*"]  # O puedes especificar una lista de orígenes permitidos ['http://localhost:3000', 'https://example.com']

# Agregar el middleware CORS a la aplicación
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
app.include_router(users)