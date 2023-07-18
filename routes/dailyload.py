from fastapi import APIRouter, Depends
from sqlalchemy import func, extract, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.reflection import Inspector
from database import get_pits, get_phases, get_db
from models import Pit, Phase, Daily_report
import pandas as pd
import os
from datetime import datetime, timedelta

# APIRouter se encarga de administrar las rutas para poder ser llamadas desde el main
dailyload = APIRouter()

# ETL de los .csv    
# Obtener la semana ISO
def get_week_of_year(date_obj):
    return date_obj.isocalendar()[1]

# Obtener la semana móvil
def get_moving_week(date_obj):
    return (date_obj - pd.DateOffset(weeks=1)).isocalendar()[1]

# Obtener el mes
def get_month(date_obj):
    return date_obj.month

# Obtener el año
def get_year(date_obj):
    return date_obj.year


@dailyload.get("/api/dailyload")
def get_by_id(db: Session = Depends(get_db)):
    """
    Esta es la función que realiza el ETL.
    """
    try:
        # Obtener la ruta de la carpeta de archivos
        folder_path = 'Data/Cargas Diarias'

        # Obtener la lista de archivos en la carpeta
        files = os.listdir(folder_path)

        for file_name in files:
            # Combinar la ruta de la carpeta y el nombre del archivo
            file_path = os.path.join(folder_path, file_name)

            # Lectura del origen de datos
            df = pd.read_csv(file_path, sep=';', encoding='UTF-8', decimal=',')

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
                if rajo not in rajos_db:
                    to_create = Pit(name=rajo)
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
                fase = row.Zona
                id_pit_db = row.id_pit
                tonelaje = row.Tonelaje 
                fecha = row.Fecha

                # Convertir la fecha al formato correcto
                date_obj = datetime.strptime(fecha, '%d-%m-%Y')

                if fase not in phases_in_db:            
                    to_create_phase = Phase(
                        name=fase,
                        id_pit=id_pit_db
                    )
                    db.add(to_create_phase)

                # Calcular los valores de semana móvil, semana ISO, valor mensual y valor anual
                ISO_week = get_week_of_year(date_obj)
                moving_week = get_moving_week(date_obj)
                month = get_month(date_obj)
                year = get_year(date_obj)

                # Calcular el valor acumulado anual hasta la fecha
                annual_accumulated = db.query(func.sum(Daily_report.real)).filter(
                    Daily_report.phase == fase,
                    extract('year', Daily_report.date) == year,
                    Daily_report.date <= date_obj
                ).scalar()

                # Calcular el valor acumulado mensual hasta la fecha
                monthly_accumulated = db.query(func.sum(Daily_report.real)).filter(
                    Daily_report.phase == fase,
                    extract('year', Daily_report.date) == year,
                    extract('month', Daily_report.date) == month,
                    Daily_report.date <= date_obj
                ).scalar()

                # Realizar el insert a la tabla daily reports
                to_create_daily_report = Daily_report(
                    date=date_obj,
                    phase=fase,
                    real=tonelaje,
                    ISO_weekly=ISO_week,
                    movil_weekly=moving_week,
                    month_real=monthly_accumulated if monthly_accumulated else 0,  # Si no hay valores acumulados, se asigna 0
                    annual_real=annual_accumulated if annual_accumulated else 0  # Si no hay valores acumulados, se asigna 0
                )
                db.add(to_create_daily_report)

            db.commit()

        return {"status": "ETL completed successfully"}
    
    except SQLAlchemyError as e:
        return {"status": "ETL error", "error_message": str(e)}

# Ping para revisar las tablas de la db
@dailyload.get("/api/ping")
def ping_db(db: Session = Depends(get_db)):
    """
    Sirve para realizar un ping a la base de datos ademas de retornar todas las tablas que tiene la db
    """
    try:       

        # Obtener la lista de tablas utilizando el objeto Inspector
        inspector = Inspector.from_engine(db.bind)
        tables = inspector.get_table_names()
        
        return {"status": "Database connection successful", "tables": tables}
    
    except SQLAlchemyError as e:
        return {"status": "Database connection error", "error_message": str(e)}