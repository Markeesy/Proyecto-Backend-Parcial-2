from fastapi import FastAPI, Depends, HTTPException, status  
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError, DataError
from typing import List, Optional, Annotated
from database import engine, SessionLocal, get_db
from datetime import datetime, timedelta
import models
import schemas

#Creamos la Base de datos si no existe
models.Base.metadata.create_all(bind=engine)

#Creamos la aplicación
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


#Creamos los CRUD de Vehiculos

@app.post("/vehiculos", response_model=schemas.VehiculoResponse, status_code=status.HTTP_201_CREATED)
def crear_vehiculo(item: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    db_item = models.Vehiculo(vehiculoDescripcion=item.vehiculoDescripcion)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/vehiculos', response_model=List[schemas.VehiculoResponse])
def leer_vehiculos(db: Session = Depends(get_db)):
    items = db.query(models.Vehiculo).all()
    items.sort(key=lambda x: x.idVehiculo)
    return items

@app.get('/vehiculos/{id}', response_model=schemas.VehiculoResponse)
def leer_vehiculo(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Vehiculo).filter(models.Vehiculo.idVehiculo == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return item

@app.put('/vehiculos/{id}', response_model=schemas.VehiculoResponse)
def actualizar_vehiculo(id: int, item: schemas.VehiculoUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Vehiculo).filter(models.Vehiculo.idVehiculo == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete('/vehiculos/{id}', response_model=schemas.VehiculoResponse)
def eliminar_vehiculo(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Vehiculo).filter(models.Vehiculo.idVehiculo == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    
    db.delete(item)
    db.commit()
    return item

#Creamos los CRUD de Calles

@app.post("/calles", response_model=schemas.CalleResponse, status_code=status.HTTP_201_CREATED)
def crear_calle(item: schemas.CalleCreate, db: Session = Depends(get_db)):
    db_item = models.Calle(nombreCalle=item.nombreCalle)
    if db_item.nombreCalle == "":
        raise HTTPException(status_code=400, detail="Nombre de la calle es requerido")
    
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Ocurrio un error al guardar la calle: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al guardar la calle: {str(e)}")


@app.get('/calles', response_model=List[schemas.CalleResponse])
def leer_calles(db: Session = Depends(get_db)):
    try:
        items = db.query(models.Calle).all()
        items.sort(key=lambda x: x.idCalle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al leer las calles: {str(e)}")
    return items


@app.get('/calles/{id}', response_model=schemas.CalleResponse)
def leer_calle(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(models.Calle).filter(models.Calle.idCalle == id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Calle no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al leer la calle: {str(e)}")
    return item


@app.put('/calles/{id}', response_model=schemas.CalleResponse)
def actualizar_calle(id: int, item: schemas.CalleUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Calle).filter(models.Calle.idCalle == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Calle no encontrada")
    
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    try:
        db.commit()
        db.refresh(db_item)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Ocurrio un error al actualizar la calle: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al actualizar la calle: {str(e)}")
    return db_item

@app.post('/estacionamientos', response_model=schemas.EstacionamientoResponse, status_code=status.HTTP_201_CREATED)
def crear_estacionamiento(item: schemas.EstacionamientoCreate, db: Session = Depends(get_db)):
    
    #Validamos que los datos de entrada sean validos
    if item.idCalle == None:
        raise HTTPException(status_code=400, detail="Calle es requerida")
    if item.numeroCalle == None:
        raise HTTPException(status_code=400, detail="Numero de calle es requerido")

    #Validamos que la calle exista
    if not db.query(models.Calle).filter(models.Calle.idCalle == item.idCalle).first():
        raise HTTPException(status_code=404, detail="Calle no encontrada")

    #Validamos que el estacionamiento no exista
    if db.query(models.Estacionamiento).filter(models.Estacionamiento.idCalle == item.idCalle, models.Estacionamiento.numeroCalle == item.numeroCalle).first():
        raise HTTPException(status_code=400, detail="Estacionamiento ya existe")

    db_item = models.Estacionamiento(
        idCalle=item.idCalle, 
        numeroCalle=item.numeroCalle
    )
    
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Ocurrio un error al guardar el estacionamiento: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al guardar el estacionamiento: {str(e)}")
    
    return db_item

@app.get('/estacionamientos', response_model=List[schemas.EstacionamientoResponse])
def leer_estacionamientos(db: Session = Depends(get_db)):
    try:
        items = db.query(models.Estacionamiento).all()
        items.sort(key=lambda x: x.idCalle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al leer los estacionamientos: {str(e)}")
    return items

@app.get('/estacionamientosid', response_model=str)
def leer_estacionamiento(idCalle:int, numeroCalle:int, db: Session = Depends(get_db)):
    try:
        item = db.query(models.Estacionamiento).filter(models.Estacionamiento.idCalle == idCalle, models.Estacionamiento.numeroCalle == numeroCalle).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Estacionamiento no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al leer el estacionamiento: {str(e)}")
    
    return f"Existe el estacionamiento: \nCalle:{idCalle} \nNumero:{numeroCalle}"

@app.delete('/estacionamientos', response_model=str)
def eliminar_estacionamiento(idCalle:int, numeroCalle:int, db: Session = Depends(get_db)):
    db_item = db.query(models.Estacionamiento).filter(models.Estacionamiento.idCalle == idCalle, models.Estacionamiento.numeroCalle == numeroCalle).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Estacionamiento no encontrado")
    
    try:
        db.delete(db_item)
        db.refresh(db_item)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Ocurrio un error al eliminar el estacionamiento: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al eliminar el estacionamiento: {str(e)}")
    
    return f"Estacionamiento eliminado: Calle:{idCalle} Numero:{numeroCalle}"

@app.delete('/calles/{id}', response_model=schemas.CalleResponse)
def eliminar_calle(id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(models.Calle).filter(models.Calle.idCalle == id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Calle no encontrada")
        
        db.delete(item)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al eliminar la calle: {str(e)}")
    return item

@app.post('/registros', response_model=schemas.RegistroResponse, status_code=status.HTTP_201_CREATED)
def crear_registro(item: schemas.RegistroCreate, db: Session = Depends(get_db)):
    db_item = models.Registro(
        idVehiculo=item.idVehiculo, 
        idCalle=item.idCalle,
        numeroCalle=item.numeroCalle,
        fechaHoraEntrada=item.fechaHoraEntrada,
        fechaHoraSalida=item.fechaHoraSalida,
        duracionHs=item.duracionHs,
        anulado=item.anulado if item.anulado is not None else False
    )

    #Validamos que los datos de entrada sean validos
    if db_item.idVehiculo == None:
        raise HTTPException(status_code=400, detail="Vehiculo es requerido")
    if db_item.idCalle == None:
        raise HTTPException(status_code=400, detail="Calle es requerida")
    if db_item.numeroCalle == None:
        raise HTTPException(status_code=400, detail="Numero de calle es requerido")
    if db_item.fechaHoraEntrada == None:
        raise HTTPException(status_code=400, detail="Fecha de entrada es requerida")
    if db_item.duracionHs == None:
        raise HTTPException(status_code=400, detail="Duracion es requerida")

    #Validamos que el vehiculo exista
    if not db.query(models.Vehiculo).filter(models.Vehiculo.idVehiculo == db_item.idVehiculo).first():
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    
    #Validamos que el estacionamiento exista
    if not db.query(models.Estacionamiento).filter(models.Estacionamiento.idCalle == db_item.idCalle, models.Estacionamiento.numeroCalle == db_item.numeroCalle).first():
        raise HTTPException(status_code=404, detail="Estacionamiento no encontrado")

    #Validamos que el estacionamiento no este ocupado
    print("El tipo de fecha Hora entrada es", type(db_item.fechaHoraEntrada))
    fechaHoraSalida = db_item.fechaHoraEntrada + timedelta(hours=db_item.duracionHs)
    
    db_item2 = db.query(models.Registro).filter(
        models.Registro.idCalle == db_item.idCalle,
        models.Registro.numeroCalle == db_item.numeroCalle,
        models.Registro.fechaHoraEntrada <= fechaHoraSalida,
        models.Registro.fechaHoraSalida >= db_item.fechaHoraEntrada,
        models.Registro.anulado == False
    ).first()

    if db_item2:
        raise HTTPException(status_code=400, detail=f"Estacionamiento ocupado por vehiculo {db_item2.idVehiculo}")
    
    db_item.fechaHoraSalida = fechaHoraSalida
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get('/registros', response_model=List[schemas.RegistroResponse])
def leer_registros(db: Session = Depends(get_db)):
    try:
        items = db.query(models.Registro).order_by(models.Registro.idRegistro).all()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrio un error al leer los registros: {str(e)}")

@app.put('/registros/{id}/anular', response_model=str)
def anular_registro(id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Registro).filter(models.Registro.idRegistro == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    db_item.anulado = True
    db.commit()
    db.refresh(db_item)
    return f"Registro anulado correctamente: {db_item.idRegistro}"

@app.get('/estacionamientos_ocupados', response_model=List[schemas.RegistroResponse])
def leer_estacionamientos_ocupados(item: schemas.ConsultaEstacionamientos, db: Session = Depends(get_db)):
    
    idCalle = item.idCalle
    numeroCalle = item.numeroCalle
    fechaHoraConsulta = item.fechaHoraConsulta

    if (idCalle == None and numeroCalle != None):
        raise HTTPException(status_code=400, detail="Si ingresa numero de calle debe ingresar tambien la calle")

    if idCalle != None:
        if not db.query(models.Calle).filter(models.Calle.idCalle == idCalle).first():
            raise HTTPException(status_code=404, detail="La calle consultada no existe")
    
    if numeroCalle != None and idCalle != None:
        if not db.query(models.Estacionamiento).filter(
            models.Estacionamiento.idCalle == idCalle, 
            models.Estacionamiento.numeroCalle == numeroCalle).first():
            raise HTTPException(status_code=404, detail="El estacionamiento consultado no existe")

    if fechaHoraConsulta == None:
        fechaHoraConsulta = datetime.now()

    filtrosBusqueda = [
        models.Registro.fechaHoraEntrada <= fechaHoraConsulta,
        models.Registro.fechaHoraSalida >= fechaHoraConsulta,
        models.Registro.anulado == False]

    if idCalle != None:
        filtrosBusqueda.append(models.Registro.idCalle == idCalle)
    if numeroCalle != None:
        filtrosBusqueda.append(models.Registro.numeroCalle == numeroCalle)

    db_item = db.query(models.Registro).filter(
        *filtrosBusqueda
    ).all()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="No hay estacionamientos ocupados")

    return db_item

@app.get('/estacionamientos_ocupados_por_rango', response_model=List[schemas.EstacionamientoOcupadoRangoResponse])
def leer_estacionamientos_ocupados_por_rango(item: schemas.ConsultaEstacionamientosPorRango, db: Session = Depends(get_db)):
    
    idCalle = item.idCalle
    numeroCalle = item.numeroCalle
    fechaHoraConsulta = item.fechaHoraConsulta
    fechaHoraFinal = item.fechaHoraFinal

    if (idCalle == None and numeroCalle != None):
        raise HTTPException(status_code=400, detail="Si ingresa numero de calle debe ingresar tambien la calle")

    if idCalle != None:
        if not db.query(models.Calle).filter(models.Calle.idCalle == idCalle).first():
            raise HTTPException(status_code=404, detail="La calle consultada no existe")
    
    if numeroCalle != None and idCalle != None:
        if not db.query(models.Estacionamiento).filter(
            models.Estacionamiento.idCalle == idCalle, 
            models.Estacionamiento.numeroCalle == numeroCalle).first():
            raise HTTPException(status_code=404, detail="El estacionamiento consultado no existe")

    if fechaHoraConsulta == None:
        fechaHoraConsulta = datetime.now()

    if fechaHoraFinal == None:
        fechaHoraFinal = datetime.now()

    if fechaHoraFinal < fechaHoraConsulta:
        raise HTTPException(status_code=400, detail="La fecha de fin no puede ser menor a la fecha de inicio")

    filtrosBusqueda = [
        models.Registro.fechaHoraEntrada <= fechaHoraFinal,
        models.Registro.fechaHoraSalida >= fechaHoraConsulta,
        models.Registro.anulado == False]

    if idCalle != None:
        filtrosBusqueda.append(models.Registro.idCalle == idCalle)
    if numeroCalle != None:
        filtrosBusqueda.append(models.Registro.numeroCalle == numeroCalle)

    db_item = db.query(models.Registro).filter(
        *filtrosBusqueda
    ).all()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="No hay estacionamientos ocupados")

    estacionamientos_dict = {}
    
    calles_ids = list(set(reg.idCalle for reg in db_item if reg.idCalle is not None))
    calles_bd = db.query(models.Calle).filter(models.Calle.idCalle.in_(calles_ids)).all()
    nombres_calles = {calle.idCalle: calle.nombreCalle for calle in calles_bd}

    for reg in db_item:
        key = (reg.idCalle, reg.numeroCalle)
        if key not in estacionamientos_dict:
            estacionamientos_dict[key] = {
                "idCalle": reg.idCalle,
                "Calle": nombres_calles.get(reg.idCalle, "Desconocida"),
                "NumeroCalle": reg.numeroCalle,
                "Detalles": []
            }
        
        estacionamientos_dict[key]["Detalles"].append({
            "idVehiculo": reg.idVehiculo,
            "FechaIngreso": reg.fechaHoraEntrada,
            "FechaSalida": reg.fechaHoraSalida
        })

    return list(estacionamientos_dict.values())

@app.get('/estacionamientos_disponibles', response_model=List[schemas.EstacionamientoDisponibleResponse])
def leer_estacionamientos_disponibles(item: schemas.ConsultaEstacionamientos, db: Session = Depends(get_db)):
    idCalle = item.idCalle
    numeroCalle = item.numeroCalle
    fechaHoraConsulta = item.fechaHoraConsulta

    if (idCalle == None and numeroCalle != None):
        raise HTTPException(status_code=400, detail="Si ingresa numero de calle debe ingresar tambien la calle")

    if idCalle != None:
        if not db.query(models.Calle).filter(models.Calle.idCalle == idCalle).first():
            raise HTTPException(status_code=404, detail="La calle consultada no existe")
    
    if numeroCalle != None and idCalle != None:
        if not db.query(models.Estacionamiento).filter(
            models.Estacionamiento.idCalle == idCalle, 
            models.Estacionamiento.numeroCalle == numeroCalle).first():
            raise HTTPException(status_code=404, detail="El estacionamiento consultado no existe")

    if fechaHoraConsulta == None:
        fechaHoraConsulta = datetime.now()

    query_est = db.query(models.Estacionamiento)
    if idCalle != None:
        query_est = query_est.filter(models.Estacionamiento.idCalle == idCalle)
    if numeroCalle != None:
        query_est = query_est.filter(models.Estacionamiento.numeroCalle == numeroCalle)
    
    todos_estacionamientos = query_est.all()

    filtrosBusqueda = [
        models.Registro.fechaHoraEntrada <= fechaHoraConsulta,
        models.Registro.fechaHoraSalida >= fechaHoraConsulta,
        models.Registro.anulado == False
    ]
    if idCalle != None:
        filtrosBusqueda.append(models.Registro.idCalle == idCalle)
    if numeroCalle != None:
        filtrosBusqueda.append(models.Registro.numeroCalle == numeroCalle)

    ocupados = db.query(models.Registro).filter(*filtrosBusqueda).all()
    set_ocupados = set((reg.idCalle, reg.numeroCalle) for reg in ocupados)

    disponibles = [est for est in todos_estacionamientos if (est.idCalle, est.numeroCalle) not in set_ocupados]

    if not disponibles:
        raise HTTPException(status_code=404, detail="No hay estacionamientos disponibles")

    calles_ids = list(set(est.idCalle for est in disponibles))
    calles_bd = db.query(models.Calle).filter(models.Calle.idCalle.in_(calles_ids)).all()
    nombres_calles = {calle.idCalle: calle.nombreCalle for calle in calles_bd}

    respuesta = []
    for est in disponibles:
        respuesta.append({
            "idCalle": est.idCalle,
            "Calle": nombres_calles.get(est.idCalle, "Desconocida"),
            "NumeroCalle": est.numeroCalle
        })

    return respuesta

@app.get('/estacionamientos_disponibles_por_rango', response_model=List[schemas.EstacionamientoDisponibleResponse])
def leer_estacionamientos_disponibles_por_rango(item: schemas.ConsultaEstacionamientosPorRango, db: Session = Depends(get_db)):
    idCalle = item.idCalle
    numeroCalle = item.numeroCalle
    fechaHoraConsulta = item.fechaHoraConsulta
    fechaHoraFinal = item.fechaHoraFinal

    if (idCalle == None and numeroCalle != None):
        raise HTTPException(status_code=400, detail="Si ingresa numero de calle debe ingresar tambien la calle")

    if idCalle != None:
        if not db.query(models.Calle).filter(models.Calle.idCalle == idCalle).first():
            raise HTTPException(status_code=404, detail="La calle consultada no existe")
    
    if numeroCalle != None and idCalle != None:
        if not db.query(models.Estacionamiento).filter(
            models.Estacionamiento.idCalle == idCalle, 
            models.Estacionamiento.numeroCalle == numeroCalle).first():
            raise HTTPException(status_code=404, detail="El estacionamiento consultado no existe")

    if fechaHoraConsulta == None:
        fechaHoraConsulta = datetime.now()
    if fechaHoraFinal == None:
        fechaHoraFinal = datetime.now()

    if fechaHoraFinal < fechaHoraConsulta:
        raise HTTPException(status_code=400, detail="La fecha de fin no puede ser menor a la fecha de inicio")

    query_est = db.query(models.Estacionamiento)
    if idCalle != None:
        query_est = query_est.filter(models.Estacionamiento.idCalle == idCalle)
    if numeroCalle != None:
        query_est = query_est.filter(models.Estacionamiento.numeroCalle == numeroCalle)
    
    todos_estacionamientos = query_est.all()

    filtrosBusqueda = [
        models.Registro.fechaHoraEntrada <= fechaHoraFinal,
        models.Registro.fechaHoraSalida >= fechaHoraConsulta,
        models.Registro.anulado == False
    ]
    if idCalle != None:
        filtrosBusqueda.append(models.Registro.idCalle == idCalle)
    if numeroCalle != None:
        filtrosBusqueda.append(models.Registro.numeroCalle == numeroCalle)

    ocupados = db.query(models.Registro).filter(*filtrosBusqueda).all()
    set_ocupados = set((reg.idCalle, reg.numeroCalle) for reg in ocupados)

    disponibles = [est for est in todos_estacionamientos if (est.idCalle, est.numeroCalle) not in set_ocupados]

    if not disponibles:
        raise HTTPException(status_code=404, detail="No hay estacionamientos disponibles")

    calles_ids = list(set(est.idCalle for est in disponibles))
    calles_bd = db.query(models.Calle).filter(models.Calle.idCalle.in_(calles_ids)).all()
    nombres_calles = {calle.idCalle: calle.nombreCalle for calle in calles_bd}

    respuesta = []
    for est in disponibles:
        respuesta.append({
            "idCalle": est.idCalle,
            "Calle": nombres_calles.get(est.idCalle, "Desconocida"),
            "NumeroCalle": est.numeroCalle
        })

    return respuesta