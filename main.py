from fastapi import FastAPI, Depends, HTTPException, status  
from sqlalchemy.orm import Session 
from typing import List, Optional, Annotated
from database import engine, SessionLocal, get_db
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
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
@app.get('/calles', response_model=List[schemas.CalleResponse])
def leer_calles(db: Session = Depends(get_db)):
    items = db.query(models.Calle).all()
    return items
@app.get('/calles/{id}', response_model=schemas.CalleResponse)
def leer_calle(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Calle).filter(models.Calle.idCalle == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Calle no encontrada")
    return item
@app.put('/calles/{id}', response_model=schemas.CalleResponse)
def actualizar_calle(id: int, item: schemas.CalleUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Calle).filter(models.Calle.idCalle == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Calle no encontrada")
    
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item
@app.delete('/calles/{id}', response_model=schemas.CalleResponse)
def eliminar_calle(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Calle).filter(models.Calle.idCalle == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Calle no encontrada")
    
    db.delete(item)
    db.commit()
    return item