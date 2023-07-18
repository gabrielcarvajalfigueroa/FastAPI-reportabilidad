from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import func, cast, Numeric


# Carga las variables de entorno del archivo .env
load_dotenv()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/next-test"

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

def get_daily_reports_objects():
    from models import Daily_report  # Importar el modelo Phase desde el archivo correspondiente
    db = SessionLocal()
    daily_reports = db.query(Daily_report).all()
    daily_reports_data = []
    for daily_report in daily_reports:
        daily_report_data = {
            "date": daily_report.date,
            "phase": daily_report.phase,
            "dailyValue": daily_report.real,
            "ISOWeek": daily_report.ISO_weekly,
            "MovingWeekly": daily_report.movil_weekly,
            "MonthlyActual": daily_report.month_real,
            "AnnualActual": daily_report.annual_real,
        }
        daily_reports_data.append(daily_report_data)
    db.close()
    return daily_reports_data

from sqlalchemy import func, cast, Numeric

def get_total_extraction_objects():
    from models import Pit, Phase, Daily_report   
    db = SessionLocal()
    query = db.query(
        Pit.name,
        Daily_report.phase,
        cast(func.round(func.sum(Daily_report.real) / 1000, 0), Numeric(10, 0)).label("total_real")
    ).join(Phase, Phase.id_pit == Pit.id_pit).join(Daily_report, Daily_report.phase == Phase.name).group_by(Daily_report.phase, Pit.name).order_by(Pit.name)

    results = query.all()

    total_extraction_data = []
    for result in results:
        extraction_data = {
            "name": result.name,
            "phase": result.phase,
            "total_real": result.total_real,
        }
        total_extraction_data.append(extraction_data)

    db.close()
    return total_extraction_data


# ---------------------------------------#
#|  Aqui va lo que respecta a usuarios  |#
# ---------------------------------------#

def get_users_objects():
    from models import User  # Importar el modelo User desde el archivo correspondiente
    db = SessionLocal()
    users = db.query(User).all()
    users_data = []
    for user in users:
        user_data = {
            "id_user": user.id_user,
            "is_admin": user.is_admin,
            "email": user.email,            
            "password": user.password,
            "name": user.name,
        }
        users_data.append(user_data)
    db.close()
    return users_data

def get_requests_objects():
    from models import User_request  # Importar el modelo User desde el archivo correspondiente
    db = SessionLocal()
    users_requests = db.query(User_request).all()
    users_request_data = []
    for user_request in users_requests:
        user_request_data = {
            "id_request": user_request.id_request,
            "email": user_request.email,
            "message": user_request.message,                        
        }
        users_request_data.append(user_request_data)
    db.close()
    return users_request_data