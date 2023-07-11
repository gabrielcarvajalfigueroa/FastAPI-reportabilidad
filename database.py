from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/next-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()    

def get_pits():
    from models import Pit  # Importar el modelo Pit desde el archivo correspondiente
    db = SessionLocal()
    pits = db.query(Pit.name).all()
    pits_names = [name for (name,) in pits]  # Comprensión de listas para desempaquetar los valores de las tuplas
    db.close()
    return pits_names      