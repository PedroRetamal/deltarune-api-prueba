from sqlalchemy.orm import Session
from models_sqlalchemy import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_username(self, username: str):
        """Busca un usuario por su username, si no existe devuelve un None"""
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def crear(self, username: str, password_hash: str):
        """Crea usuario y lo guarda en la base """
        nuevo = Usuario(username=username, password_hash=password_hash)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo