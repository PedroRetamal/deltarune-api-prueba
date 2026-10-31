import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from repositories.usuario_repository import UsuarioRepository
from config import SECRET_KEY, ALGORITHM, EXPIRACION_MINUTOS
from services.auth_service import AuthService

class UsuarioService:
    def __init__(self, repositorio: UsuarioRepository, auth_service: AuthService):
        self.repo = repositorio
        self.auth_service = auth_service

    def registrar(self, username: str, password: str):
        """Registra usuario, lanza ValueError si el username ya existe"""
        #verificar que existe
        existente = self.repo.obtener_por_username(username)
        if existente:
            raise ValueError("Ese username ya está en uso")

        #hashear contraseña
        password_bytes = password.encode("utf-8")
        hash_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        hash_str = hash_bytes.decode("utf-8")

        #guardar en base de datos
        return self.repo.crear(username, hash_str)

    def verificar_credenciales(self, username: str, password: str):
        """verifica usuario y contraseña, devuelve usuario si son correctas y None si no"""
        usuario = self.repo.obtener_por_username(username)
        if not usuario:
            return None

        password_bytes = password.encode("utf-8")
        hash_bytes = usuario.password_hash.encode("utf-8")

        if not bcrypt.checkpw(password_bytes, hash_bytes):
            return None

        return usuario

    def login (self, username: str, password: str):
        """verifica credenciales, si son correctas genera un JWT"""
        #verificar credenciales
        usuario = self.verificar_credenciales(username, password)
        if not usuario:
            return None

        #generar JWT
        return self.auth_service.generar_token(usuario)