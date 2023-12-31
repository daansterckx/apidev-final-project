from sqlalchemy.orm import Session

import models
import schemas


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    fake_hashed_password = client.password + "notreallyhashed"
    db_client = models.Client(email=client.email, hashed_password=fake_hashed_password)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client




