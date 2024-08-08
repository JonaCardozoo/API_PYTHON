from typing import List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()


class Persona(BaseModel):
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