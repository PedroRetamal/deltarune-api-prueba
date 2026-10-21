from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database_sqlalchemy import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(67), nullable=False)
    creado_en = Column(TIMESTAMP, server_default=func.now())

    #Relación: un usuario tiene muchos personajes
    personajes = relationship("Personaje", back_populates="usuario")


class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    hp = Column(Integer, nullable=False)
    ataque = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"),nullable=False)
    creado_en = Column(TIMESTAMP, server_default=func.now())

    #Relacion inversa
    usuario = relationship("Usuario", back_populates="personajes")