from services.auth_service import AuthService
import jwt
import pytest
from fastapi import HTTPException
from config import SECRET_KEY, ALGORITHM

class UsuarioFalso:
    """objeto que imita a un usuario real para no depender de la base de datos"""
    def __init__(self, id, username):
        self.id = id
        self.username = username


def test_generar_token_contiene_datos():
    #preparar
    auth = AuthService()
    usuario = UsuarioFalso(id=42, username="pedro")

    #ejecutar
    resultado = auth.generar_token(usuario)

    #verificar
    assert "access_token" in resultado
    assert "token_type" in resultado
    assert resultado["token_type"] == "bearer"

    #decodificar el token y verificar contenido
    token = resultado["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["user_id"] == 42
    assert payload["username"] == "pedro"

def test_verificar_token_invalido():
    auth = AuthService()

    with pytest.raises(HTTPException) as error:
        auth.verificar_token("esto.no.es.un.token.valido")

    assert error.value.status_code == 401
    assert "Token inválido" in error.value.detail