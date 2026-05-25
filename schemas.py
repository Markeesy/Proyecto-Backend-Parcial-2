from sqlalchemy.engine import reflection
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

#Modelos para las Peticiones API (Entrada)
#Vehiculos
class VehiculoBase(BaseModel):
    vehiculoDescripcion: str

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoUpdate(VehiculoBase):
    vehiculoDescripcion: Optional[str] = None

class VehiculoDelete(BaseModel):
    idVehiculo: int

class VehiculoResponse(VehiculoBase):
    idVehiculo: int

    model_config = ConfigDict(from_attributes=True)


#Estacionamientos
class EstacionamientoBase(BaseModel):
    idCalle:int
    numeroCalle:int

class EstacionamientoCreate(EstacionamientoBase):
    pass

class EstacionamientoUpdate(EstacionamientoBase):
    idCalle: Optional[int] = None
    numeroCalle: Optional[int] = None

class EstacionamientoDelete(BaseModel):
    idEstacionamiento: int

class EstacionamientoResponse(EstacionamientoBase):

    model_config = ConfigDict(from_attributes=True)

#Calles
class CalleBase(BaseModel):
    nombreCalle: str

class CalleCreate(CalleBase):
    pass

class CalleUpdate(CalleBase):
    nombreCalle: Optional[str] = None

class CalleDelete(BaseModel):
    idCalle: int

class CalleResponse(CalleBase):
    idCalle: int

    model_config = ConfigDict(from_attributes=True)


#Registros
class RegistroBase(BaseModel):
    idVehiculo: Optional[int] = None
    idCalle: Optional[int] = None
    numeroCalle: Optional[int] = None
    fechaHoraEntrada: Optional[datetime] = None
    fechaHoraSalida: Optional[datetime] = None
    duracionHs: Optional[int] = None
    anulado: Optional[bool] = False

class RegistroCreate(RegistroBase):
    pass

class RegistroUpdate(RegistroBase):
    idVehiculo: Optional[int] = None
    idCalle: Optional[int] = None
    numeroCalle: Optional[int] = None
    fechaHoraEntrada: Optional[datetime] = None
    fechaHoraSalida: Optional[datetime] = None
    duracionHs: Optional[int] = None
    anulado: Optional[bool] = None

class RegistroDelete(BaseModel):
    idRegistro: int

class RegistroResponse(RegistroBase):
    idRegistro: int

    model_config = ConfigDict(from_attributes=True)

#Consulta Estacionamientos Ocupados
class ConsultaEstacionamientos(BaseModel):
    idCalle: Optional[int] = None
    numeroCalle: Optional[int] = None
    fechaHoraConsulta: Optional[datetime] = None

class ConsultaEstacionamientosResponse(BaseModel):
    idCalle: Optional[int] = None
    calle: Optional[str] = None
    numeroCalle: Optional[int] = None
    fechaHoraConsulta: Optional[datetime] = None
    disponibilidad: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ConsultaEstacionamientosPorRango(ConsultaEstacionamientos):
    fechaHoraFinal: Optional[datetime] = None

class OcupacionDetalle(BaseModel):
    idVehiculo: int
    FechaIngreso: datetime
    FechaSalida: datetime

class EstacionamientoOcupadoRangoResponse(BaseModel):
    idCalle: int
    Calle: str
    NumeroCalle: int
    Detalles: List[OcupacionDetalle]

    model_config = ConfigDict(from_attributes=True)

class EstacionamientoDisponibleResponse(BaseModel):
    idCalle: int
    Calle: str
    NumeroCalle: int

    model_config = ConfigDict(from_attributes=True)
