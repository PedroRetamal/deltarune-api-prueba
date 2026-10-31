from sqlalchemy.orm import Session
from models_sqlalchemy import Personaje

class PersonajeRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_usuario(self, usuario_id: int):
        """devuelve una lista con los personajes del usuario"""
        return self.db.query(Personaje).filter(Personaje.usuario_id == usuario_id).all()

    def obtener_por_id_y_usuario(self, personaje_id: int, usuario_id: int):
        """busca un personaje por su id, pero solo si pertenece al usuario"""
        personaje = self.db.query(Personaje).filter(Personaje.id == personaje_id, Personaje.usuario_id == usuario_id).first()

        if not personaje:
            return None

        return personaje

    def crear(self, nombre: str, hp: int, ataque: int, usuario_id: int):
        """crea personaje y lo guarda en la base de datos"""
        nuevo = Personaje(
                nombre= nombre,
                hp= hp,
                ataque= ataque,
                usuario_id=usuario_id
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo


    def actualizar(self, personaje, nombre: str, hp: int, ataque: int):
        """actualiza los datos de un personaje que ya existe"""
        personaje.nombre = nombre
        personaje.hp = hp
        personaje.ataque = ataque
    
        self.db.commit()
        self.db.refresh(personaje)
    
        return personaje

    def borrar(self, personaje):
        """borra un personaje de la base de datos"""
        self.db.delete(personaje)
        self.db.commit()