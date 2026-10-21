from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.usuario import UsuarioInput, UsuarioOutput, LoginInput, TokenOutput
from database_sqlalchemy import SessionLocal
from models_sqlalchemy import Usuario
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM, EXPIRACION_MINUTOS

router = APIRouter()

#dependencia que abre una sesión de base de datos por cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registro", response_model=UsuarioOutput, status_code=201)
def registrar_usuario(datos: UsuarioInput, db: Session = Depends(get_db)):

    #verificar si el username existe
    existente = db.query(Usuario).filter(Usuario.username == datos.username).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ese username ya está en uso")

    #hashear contraseña
    password_bytes = datos.password.encode("utf-8")
    hash_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hash_str = hash_bytes.decode("utf-8")

    #crear usuario y guardarlo
    nuevo_usuario = Usuario(username=datos.username, password_hash=hash_str)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  #una recarga para tener el id y el creado_en

    return nuevo_usuario
    

@router.post("/login", response_model=TokenOutput)
def login(datos: LoginInput, db: Session = Depends(get_db)):
    
    #buscar usuario
    usuario = db.query(Usuario).filter(Usuario.username == datos.username).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="credenciales inválidas")

    #verificar contraseña
    password_bytes = datos.password.encode("utf-8")
    hash_bytes = usuario.password_hash.encode("utf-8")

    if not bcrypt.checkpw(password_bytes, hash_bytes):
        raise HTTPException(status_code=401, detail= "credenciales inválidas")

    #generar JWT
    payload = {
        "user_id": usuario.id,
        "username": usuario.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)   

    return {"access_token": token, "token_type": "bearer"} 