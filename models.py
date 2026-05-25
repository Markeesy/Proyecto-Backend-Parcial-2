from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    idVehiculo = Column(Integer, primary_key=True, index = True)
    vehiculoDescripcion = Column(String, nullable=True)

class Estacionamiento(Base):
    __tablename__ = "estacionamientos"
    idCalle = Column(Integer, primary_key=True, index = True)
    numeroCalle = Column(Integer,primary_key=True, nullable=True)

class Calle(Base):
    __tablename__ = "calles"
    idCalle = Column(Integer, primary_key=True, index = True)
    nombreCalle = Column(String, nullable=True)

class Registro(Base):
    __tablename__ = "registros"
    idRegistro = Column(Integer, primary_key=True, index = True)
    idVehiculo = Column(Integer, nullable=True)
    idCalle = Column(Integer, nullable=True)
    numeroCalle = Column(Integer, nullable=True)
    fechaHoraEntrada = Column(DateTime, nullable=True)
    fechaHoraSalida = Column(DateTime, nullable=True)
    duracionHs = Column(Integer, nullable=True)
    anulado = Column(Boolean, default=False)