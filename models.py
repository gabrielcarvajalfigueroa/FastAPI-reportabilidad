from sqlalchemy import Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from database import Base


class Pit(Base):
    __tablename__ = 'pits'

    id_pit = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phases = relationship('Phase')  # Relación uno a muchos con la clase Phase

class Phase(Base):
    __tablename__ = 'phases'

    id_phase = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id_pit = Column(Integer, ForeignKey('pits.id_pit'))  # Clave externa de la tabla pits
    pit = relationship('Pit')  # Relación con la clase Pit

class Daily_report(Base):
    __tablename__ = 'daily_reports'

    daily_report = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    phase = Column(String, ForeignKey('phases.name'))
    real = Column(Integer, nullable=False)
    ISO_weekly = Column(Integer, nullable=False)
    movil_weekly = Column(Integer, nullable=False)
    month_real = Column(Integer, nullable=False)
    annual_real = Column(Integer, nullable=False)
    phase_relation = relationship('Phase')

class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    is_admin = Column(Boolean, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)    

class User_request(Base):
    __tablename__ = 'users_requests'

    id_request = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=False)    