from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import os
import crud
import models
import schemas
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/service/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service.id)
    if db_service:
        raise HTTPException(status_code=400, detail="Service ID already exists")
    return crud.create_service(db=db, service=service)

@app.put("/service/{service_id}")
def add_password(service_id: int, password: str, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return crud.update_service_password(db=db, service_id=service_id, password=password)

@app.delete("/service/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    crud.delete_service(db=db, service_id=service_id)
    return {"message": "Service deleted successfully"}

@app.get("/service/{service_id}", response_model=schemas.Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@app.get("/service_id/{password}")
def get_service_id(password: str, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_password(db, password=password)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"id": db_service.id}

@app.get("/service_password/{service_id}")
def get_service_password(service_id: int, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"password": db_service.password}