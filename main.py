from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

Base = declarative_base()

SQLALCHEMY_DB = "postgresql+psycopg2://postgres:123@localhost:5432/utn"

engine = create_engine(SQLALCHEMY_DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ContactoBd(Base):
    __tablename__ = 'contactos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    direccion = Column(String(120))
    telefonos = Column(String(50))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas de la API

class ContactoSinId(BaseModel): 
    nombre: str
    direccion: Optional[str]
    telefonos: Optional[str]

class Contacto(ContactoSinId): 
    id: int


@app.get("/contactos")
def getAllContacts():
   db = SessionLocal()
   return db.query(ContactoBd).all()

@app.post("/contacto")
def addContact(c: ContactoSinId):
    db = SessionLocal()
    contacto_db =  ContactoBd()
    contacto_db.nombre = c.nombre
    contacto_db.direccion = c.direccion
    contacto_db.telefonos = c.telefonos

    db.add(contacto_db)
    db.commit()
    return {"code": "funciona"}


@app.delete("/contactos/{id}")
def deleteContacto(id: int):
    db = SessionLocal()
    cto = db.get(ContactoBd, id)
    if not cto:
        return {"code": "id no encontrado"}

    db.delete(cto)
    db.commit()
    return {"code": "funciona"}
    

"""class Persona(BaseModel):
    nombre: str
    apellido: str

persona1 = Persona(nombre="juan",apellido="perez")
persona2 = Persona(nombre="lionel",apellido="messi")

personas = [persona1,persona2]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/persona")
def get_persona():
    return personas
@app.get("/personas", response_model=List[Persona])
def get_personas():
    return personas

@app.get("/personas/{num}", response_model=Persona)
def get_persona(num: int):
    if num >= len(personas):
        raise HTTPException (status_code=404, detail="El numero no es valido")
    return personas[num]

@app.post("/persona")
def add_persona(p:Persona):
    personas.append(p)

@app.delete("/persona")
def delete_persona(p:Persona):
        personas.remove(p)
        """