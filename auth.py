from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config import SECRET_KEY, ALGORITHM
from services.auth_service import AuthService

#esto le dice a fastApi que espere un token bearer en el header
security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials #el token sin la palabra bearer
    auth_service = AuthService()

    return auth_service.verificar_token(token)