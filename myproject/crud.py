from sqlalchemy.orm import Session
import models, schemas

def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_service_by_password(db: Session, password: str):
    return db.query(models.Service).filter(models.Service.password == password).first()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(id=service.id, password=service.password)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service_password(db: Session, service_id: int, password: str):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        return None
    db_service.password = password
    db.commit()
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service is None:
        return None
    db.delete(db_service)
    db.commit()
    return db_service
