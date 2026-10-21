from pydantic import BaseModel, Field, field_validator
from datetime import datetime

#lo que mete el usuario
class UsuarioInput(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Solo letras, números y guión bajo"
    )
    password: str = Field(
        min_length=8,
        max_length=72,
        description="Entre 8 y 72 caracteres"
    )

    #validación personalizada de que no haya espacios
    @field_validator("username")
    @classmethod
    def username_sin_espacios(cls, valor:str) -> str:
        if " " in valor:
            raise ValueError("El username no puede contener espacios")
        return valor

#lo que sale para ver (sin contraseña porque el cliente no necesita ver esa información)
class UsuarioOutput(BaseModel):
    id: int
    username: str
    creado_en: datetime

#lo que mete el usuario al login
class LoginInput(BaseModel):
    username: str
    password: str

#el token
class TokenOutput(BaseModel):
    access_token: str
    token_type: str
