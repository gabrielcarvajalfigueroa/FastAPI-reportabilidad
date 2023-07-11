from sqlalchemy import Integer, String, ForeignKey
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