from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
import os
import crud
import models
import schemas
from database import SessionLocal, engine
import hashlib
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class Token(BaseModel):
    access_token: str
    token_type: str

origins = [
    "https://frontendapidev.netlify.app/",  # Replace with the domain of your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate the username and password. Replace with your own logic.
    if form_data.username != "test" or form_data.password != "test":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate a token. Replace with your own logic.
    access_token = "test"
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/service/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service.id)
    if db_service:
        raise HTTPException(status_code=400, detail="Service ID already exists")
    return crud.create_service(db=db, service=service)

@app.put("/service/{service_id}")
def add_password(service_id: int, password: str = Query(...), db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return crud.update_service_password(db=db, service_id=service_id, password=hash_password(password))

@app.delete("/service/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    crud.delete_service(db=db, service_id=service_id)
    return {"message": "Service deleted successfully"}

@app.get("/service/{service_id}", response_model=schemas.Service)
def get_service(service_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@app.get("/service_id/{password}")
def get_service_id(password: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_service = crud.get_service_by_password(db, password)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"id": db_service.id}

@app.get("/service_password/{service_id}")
def get_service_password(service_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_service = crud.get_service_by_id(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"password": db_service.password}