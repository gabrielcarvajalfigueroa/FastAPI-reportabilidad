from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, get_pits, get_phases_objects

# APIRouter se encarga de administrar las rutas para poder ser llamadas desde el main
reports = APIRouter()

# Retorna todos los pits(rajos) que posee la mina
@reports.get("/api/reports/pits")
def get_pits_in_db(db: Session = Depends(get_db)):

    pits_in_db = get_pits()

    return {"pits": pits_in_db}

# Retorna todas las phases(fases) que posee cada rajo
@reports.get("/api/reports/phases")
def get_phases_in_db(db: Session = Depends(get_db)):
    phases_in_db = get_phases_objects()
    return {"phases": phases_in_db}



