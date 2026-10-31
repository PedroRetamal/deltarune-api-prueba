import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from config import SECRET_KEY, ALGORITHM, EXPIRACION_MINUTOS


class AuthService:
    
    def generar_token(self, usuario):
        """Genera un JWT a partir del objeto usuario."""
        payload = {
            "user_id": usuario.id,
            "username": usuario.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)   
    
        return {"access_token": token, "token_type": "bearer"} 
    
    def verificar_token(self, token: str):
        """Verifica un JWT y devuelve el payload. Lanza HTTPException si es inválido."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")