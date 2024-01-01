from pydantic import BaseModel

class ServiceBase(BaseModel):
    id: int
    password: str

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    class Config:
        orm_mode = True