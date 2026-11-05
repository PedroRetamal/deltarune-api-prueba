import pytest
from services.usuario_service import UsuarioService
from services.auth_service import AuthService
from repositories.usuario_repository import UsuarioRepository

class RepositorioUsuarioFalso(UsuarioRepository):
    """Repositorio falso que no toca la base de datos"""

    def __init__(self):
        #no se llama a super().__init__() porque no se busca crear una sesion real
        self.usuarios = {}

    def obtener_por_username(self, username):
        return self.usuarios.get(username)

    def crear(self, username, password_hash):
        #calcular el id usando el diccionario del repositorio self.usuarios
        nuevo_id = len(self.usuarios) + 1
        nuevo = UsuarioFalso(nuevo_id, username, password_hash)
        self.usuarios[username] = nuevo
        return nuevo

class UsuarioFalso:
    """objeto que imita a usuario real con los atributos necesarios"""
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash


def test_registrar_usuario_exitoso():
    #preparar test
    repo = RepositorioUsuarioFalso()
    auth = AuthService()
    service = UsuarioService(repo, auth)

    #ejecutar con registro hardcodeado
    resultado = service.registrar("pedro","password123")

    #verificar
    assert resultado.username == "pedro"
    assert "password123" not in resultado.password_hash #la contraseña no debe estar en texto plano

    assert resultado.password_hash.startswith("$2b$") #debe ser un hash de bcrypt


def test_registrar_usuario_duplicado():
    #preparar test
    repo = RepositorioUsuarioFalso()
    auth = AuthService()
    service = UsuarioService(repo, auth)

    #registrar al primer usuario
    service.registrar("pedro","password123")

    #ejecutar y verificar que el segundo de ValueError
    with pytest.raises(ValueError) as error:
        service.registrar("pedro", "otra_password")

    assert "ya está en uso" in str(error.value)

def test_verificar_credenciales_correctas():
    repo = RepositorioUsuarioFalso()
    auth = AuthService()
    service = UsuarioService(repo, auth)

    #registrar usuario
    service.registrar("pedro", "password123")

    #ejecutar
    usuario = service.verificar_credenciales("pedro", "password123")

    #verificar
    assert usuario is not None
    assert usuario.username == "pedro"

def test_verificar_credenciales_incorrectas():
    repo = RepositorioUsuarioFalso()
    auth = AuthService()
    service = UsuarioService(repo, auth)

    service.registrar("pedro", "password123")

    usuario = service.verificar_credenciales("pedro", "otra_password")

    #verificar
    assert usuario is None

def test_verificar_credenciales_usuario_inexistente():
    repo = RepositorioUsuarioFalso()
    auth = AuthService()
    service = UsuarioService(repo, auth)

    #no registrar nada

    usuario = service.verificar_credenciales("no_existe", "password123")

    assert usuario is None