from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import date
from sqlalchemy.orm import Session
from database import (
    get_db,
    get_pits,
    get_phases_objects,
    get_daily_reports_objects,
    get_total_extraction_objects,
    get_total_extraction_objects_filtered_by_month,
    get_total_extraction_objects_filtered_by_year,
)
from typing import Optional
# APIRouter se encarga de administrar las rutas para poder ser llamadas desde el main
reports = APIRouter()

# Retorna todos los pits(rajos) que posee la mina
@reports.get("/api/reports/pits")
def get_pits_in_db(db: Session = Depends(get_db)):
    """
    Retorna todos los rajos registrados en la db
    """
    pits_in_db = get_pits()
    return {"pits": pits_in_db}

# Retorna todas las phases(fases) que posee cada rajo
@reports.get("/api/reports/phases")
def get_phases_in_db(db: Session = Depends(get_db)):
    """
    Retorna todas las fases registradas en la db
    """
    phases_in_db = get_phases_objects()
    return {"phases": phases_in_db}

# Retorna los reportes diarios
@reports.get("/api/reports/dailyReports")
def get_daily_reports_in_db(
    target_date: date = Query(..., description="Fecha para obtener los reportes diarios. En formato: YYYY-MM-DD. \n Ej: /api/reports/dailyReports?target_date=2023-05-01"),
    db: Session = Depends(get_db)
):
    """
    Retorna todos los reportes diarios para la fecha especificada.
    """
    daily_reports_in_db = get_daily_reports_objects()
    
    # Filtrar los reportes diarios por la fecha especificada
    filtered_reports = [report for report in daily_reports_in_db if report['date'] == target_date]
    
    if not filtered_reports:
        raise HTTPException(status_code=404, detail="No existen reportes para la fecha especificada.")
    
    return filtered_reports

# Retorna la extraccion total de los rajos y por cada fase
@reports.get("/api/reports/totalExtraction")
def get_total_extraction_in_db(year: int, month: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retorna las extraciones totales de los rajos y por cada fase
    """
    if month is not None:
        # Realiza la consulta a la base de datos con el filtrado por mes y año
        total_extraction_in_db = get_total_extraction_objects_filtered_by_month(year, month)
    else:
        # Realiza la consulta a la base de datos con el filtrado solo por año
        total_extraction_in_db = get_total_extraction_objects_filtered_by_year(year)

    return total_extraction_in_db