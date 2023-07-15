from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
#from schemas import CreateJobRequest
from database import get_pits, get_phases
from database import get_db
from models import Pit, Phase, Daily_report
import pandas as pd

# APIRouter se encarga de administrar las rutas para poder ser llamadas desde el main
dailyload = APIRouter()

    
@dailyload.get("/api/dailyload")
def get_by_id(db: Session = Depends(get_db)):
    
    # Lectura del origen de datos
    df = pd.read_csv('Data/Cargas Diarias/01062023.csv',sep=';',encoding='UTF-8', decimal=',')

    # Seleccion de las columnas relevantes
    df = df.loc[:, ['Fecha', 'Zona', 'Tonelaje', 'Rajo']]

    # Se agrupa y se suman los tonelajes, as_index es clave para que no se transforme en indices luego del groupby
    df_grouped = df.groupby(['Rajo', 'Zona', 'Fecha'], as_index=False).sum()

    # Configurar el ancho de visualización del DataFrame
    pd.set_option('display.width', 100)

    # Mostrar el DataFrame agrupado
    print(df_grouped)

    # -------------------------------- #
    # Inserción de los valores a la BD #
    # -------------------------------- #
    
    # Comprobar si los rajos existen y sino añadirlos a la bd

    rajos_db = get_pits()

    rajos_archivo = df['Rajo'].unique()

    for rajo in rajos_archivo:
        #Si uno de los rajos no existe debe agregarse a la db
        if rajo not in rajos_db:
            to_create = Pit(
                name=rajo
            )
            db.add(to_create)

    db.commit()          

    # Obtener los objetos Pit de la base de datos
    pits_in_db = db.query(Pit).all()

    # Crear un diccionario para mapear los nombres de los rajos a los ID correspondientes
    rajo_id_map = {pit.name: pit.id_pit for pit in pits_in_db}

    # Agregar la columna "id_pit" a df_grouped
    df_grouped['id_pit'] = df_grouped['Rajo'].map(rajo_id_map)

    # Mostrar el DataFrame resultante
    print(df_grouped)
  
    # Comprobar si las Fases estan agregadas y sino agregarlas junto a su id_pit
     # Realizar el insert a la tabla daily reports 
    
    phases_in_db = get_phases()

    for row in df_grouped.itertuples(index=False):
        #rajo_xd = row.Rajo
        fase = row.Zona
        id_pit_db = row.id_pit
        tonelaje = row.Tonelaje 
        fecha = row.Fecha       

        if fase not in phases_in_db:            
            to_create_phase = Phase(
                name = fase,
                id_pit = id_pit_db
            )
            db.add(to_create_phase)
    
        # todo: Falta agregar desde el ISO_weekly en adelante
        to_create_daily_report = Daily_report(
            date = fecha,
            phase = fase,
            real = tonelaje,
            ISO_weekly = -1,
            movil_weekly = -1,
            month_real = -1,
            annual_real = -1
        )
        db.add(to_create_daily_report)

    db.commit()
   

    return "Hola"        

@dailyload.get("/api/ping")
def ping_db(db: Session = Depends(get_db)):
    try:       

        # Obtener la lista de tablas utilizando el objeto Inspector
        inspector = Inspector.from_engine(db.bind)
        tables = inspector.get_table_names()
        
        return {"status": "Database connection successful", "tables": tables}
    
    except SQLAlchemyError as e:
        return {"status": "Database connection error", "error_message": str(e)}