from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

def get_pits():
    from models import Pit  # Importar el modelo Pit desde el archivo correspondiente
    db = SessionLocal()
    pits = db.query(Pit.name).all()
    pits_names = [name for (name,) in pits]  # Comprensión de listas para desempaquetar los valores de las tuplas
    db.close()
    return pits_names      

def get_phases():
    from models import Phase  # Importar el modelo Phase desde el archivo correspondiente
    db = SessionLocal()
    phases = db.query(Phase.name).all()
    phases_names = [name for (name,) in phases]  # Comprensión de listas para desempaquetar los valores de las tuplas
    db.close()
    return phases_names

def get_phases_objects():
    from models import Phase  # Importar el modelo Phase desde el archivo correspondiente
    db = SessionLocal()
    phases = db.query(Phase).all()
    phases_data = []
    for phase in phases:
        phase_data = {
            "id_phase": phase.id_phase,
            "name": phase.name,
            "id_pit": phase.id_pit,            
        }
        phases_data.append(phase_data)
    db.close()
    return phases_data

def get_pits_objects():
    from models import Pit  # Importar el modelo Pit desde el archivo correspondiente
    db = SessionLocal()
    pits = db.query(Pit).all()    
    db.close()
    return pits