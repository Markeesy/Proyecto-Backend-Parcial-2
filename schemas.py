from pydantic import BaseModel, ConfigDict
from typing import Optional

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
    idEstacionamiento: int

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
    idCalle: int
    numeroCalle: int
    fechaHoraEntrada: str
    fechaHoraSalida: Optional[str] = None
    duracionHs: int

class RegistroCreate(RegistroBase):
    pass

class RegistroUpdate(RegistroBase):
    idCalle: Optional[int] = None
    numeroCalle: Optional[int] = None
    fechaHoraEntrada: Optional[str] = None
    fechaHoraSalida: Optional[str] = None
    duracionHs: Optional[int] = None

class RegistroDelete(BaseModel):
    idRegistro: int

class RegistroResponse(RegistroBase):
    idRegistro: int

    model_config = ConfigDict(from_attributes=True)
