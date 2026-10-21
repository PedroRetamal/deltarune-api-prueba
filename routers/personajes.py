# se quitaron los /personajes de los endpoints porque se puso como prefix en main.py

#los endpoint deben ir de más específico a más generico

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.personaje import PersonajeInput, PersonajeOutput
from models_sqlalchemy import Personaje as PersonajeDB
from database_sqlalchemy import SessionLocal
from auth import verificar_token  #importar la verificación del token

router = APIRouter()

#dependencia que abre una sesión de base de datos por cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




#saludar personajes con una mejor forma de verificar que el personaje exista, adaptado al CRUD de hoy sabado
@router.get("/{personaje_id}/saludo")
def saludar_personaje(
    personaje_id: int,
    usuario: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    personaje = db.query(PersonajeDB).filter(
        PersonajeDB.id == personaje_id,
        PersonajeDB.usuario_id == usuario["user_id"]
    ).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    return {"mensaje": f"¡Hola, {personaje.nombre}!"}



# obtener personaje por id (Esto es el READ de CRUD tambien, la R)
@router.get("/{personaje_id}", response_model=PersonajeOutput)
def obtener_personaje(
    personaje_id: int, 
    usuario: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    personaje = db.query(PersonajeDB).filter(
        PersonajeDB.id == personaje_id,
        PersonajeDB.usuario_id == usuario["user_id"]
    ).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    return personaje
    

#actualizar personaje (esto es el U de CRUD), se parchea todo al ser put, si quisiera cambiar solo 1 valor sería patch
@router.put("/{personaje_id}", response_model=PersonajeOutput)
def actualizar_personaje(
    personaje_id: int, 
    datos: PersonajeInput, 
    usuario: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    personaje = db.query(PersonajeDB).filter(
        PersonajeDB.id == personaje_id,
        PersonajeDB.usuario_id == usuario["user_id"]
    ).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    personaje.nombre = datos.nombre
    personaje.hp = datos.hp
    personaje.ataque = datos.ataque

    db.commit()
    db.refresh(personaje)

    return personaje


#borrar personaje, esto es la D de CRUD
@router.delete("/{personaje_id}", status_code=204)
def borrar_personaje(
    personaje_id: int, 
    usuario: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):

    personaje = db.query(PersonajeDB).filter(
        PersonajeDB.id == personaje_id,
        PersonajeDB.usuario_id == usuario["user_id"]
    ).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    db.delete(personaje)
    db.commit()


# listar todos los personajes (Este es el READ de CRUD , la R)
@router.get("")
def listar_personajes(
    usuario: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    personajes = db.query(PersonajeDB).filter(
        PersonajeDB.usuario_id == usuario["user_id"]
    ).all()

    return {
        "usuario_actual": usuario["username"],
        "personajes": personajes
    }
# crear personaje con POST (este es el CREATE del CRUD, osea la C)
@router.post("", response_model=PersonajeOutput, status_code=201)
def crear_personaje(
    datos: PersonajeInput, 
    usuario: dict = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    nuevo = PersonajeDB(
        nombre=datos.nombre,
        hp=datos.hp,
        ataque=datos.ataque,
        usuario_id=usuario["user_id"]
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo