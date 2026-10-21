from pydantic import BaseModel

class PersonajeInput(BaseModel):
    nombre: str
    hp: int
    ataque: int

class PersonajeOutput(BaseModel):
    id: int
    nombre: str
    hp: int
    ataque: int