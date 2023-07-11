from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#from schemas import CreateJobRequest
from database import get_pits
from database import get_db
from models import Pit
import pandas as pd


dailyload = APIRouter()

    
@dailyload.get("/api/dailyload")
def get_by_id(db: Session = Depends(get_db)):
    
    rajos_db = get_pits()

    df = pd.read_csv('Data/Cargas Diarias/01062023.csv',sep=';',encoding='UTF-8')

    rajos_archivo = df['Rajo'].unique()

    for rajo in rajos_archivo:
        #Si uno de los rajos no existe debe agregarse a la db
        if rajo not in rajos_db:
            to_create = Pit(
                name=rajo
            )
            db.add(to_create)

    db.commit()
    

    fases = df['Zona'].unique()

    #print(fases)    

    return "Hola"        