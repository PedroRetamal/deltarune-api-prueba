from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.usuario import UsuarioInput, UsuarioOutput, LoginInput, TokenOutput
from database_sqlalchemy import SessionLocal
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService
from services.auth_service import AuthService
from models_sqlalchemy import Usuario


router = APIRouter()

#dependencia que abre una sesión de base de datos por cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#registro
@router.post("/registro", response_model=UsuarioOutput, status_code=201)
def registrar_usuario(datos: UsuarioInput, db: Session = Depends(get_db)):

    #crear las capas
    repo = UsuarioRepository(db)
    auth_service = AuthService()
    service = UsuarioService(repo, auth_service)

    #llamar al servicio y manejar las excepciones
    try:
        nuevo_usuario = service.registrar(datos.username, datos.password)
    except ValueError as error:
        #el servicio lanzó un valueError (username duplicado), asi que convertimos a HTTP
        raise HTTPException(status_code=400, detail=str(error))

    return nuevo_usuario
    

@router.post("/login", response_model=TokenOutput)
def login(datos: LoginInput, db: Session = Depends(get_db)):
    
    #crear capas
    repo = UsuarioRepository(db)
    auth_service = AuthService()
    service = UsuarioService(repo, auth_service)


    #llamar al servicio
    resultado = service.login(datos.username, datos.password)

    #si el servicio devuelve none es porque las credenciales son inválidas
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return resultado