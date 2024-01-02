from sqlalchemy import Column, Integer, String
from database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)