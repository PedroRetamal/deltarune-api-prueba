from pydantic import BaseModel
from datetime import datetime

class PersonajeInput(BaseModel):
    nombre: str
    hp: int
    ataque: int

class PersonajeOutput(BaseModel):
    id: int
    nombre: str
    hp: int
    ataque: int
    creado_en: datetime