import pytest 
from services.personaje_service import PersonajeService
from repositories.personaje_repository import PersonajeRepository
from models.personaje import PersonajeInput

class RepositorioPersonajeFalso(PersonajeRepository):
    """Repositorio falso que no toca base de datos, usa un diccionario para simularlo para pruebas"""

    def __init__(self):
        #no se llama a super().__init__() porque no se busca una sesion real
        self.personajes = {} #id de personaje
        self.proximo_id = 1

    def listar_por_usuario(self, usuario_id):
        return [p for p in self.personajes.values() if p.usuario_id == usuario_id]

    def obtener_por_id_y_usuario(self, personaje_id, usuario_id):
        personaje = self.personajes.get(personaje_id)
        if personaje and personaje.usuario_id == usuario_id:
            return personaje
        return None

    def crear(self, nombre, hp, ataque, usuario_id):
        class PersonajeFalso:
            def __init__(self, id, nombre, hp, ataque, usuario_id):
                self.id = id
                self.nombre = nombre
                self.hp = hp
                self.ataque = ataque
                self.usuario_id = usuario_id

        nuevo = PersonajeFalso(self.proximo_id, nombre, hp, ataque, usuario_id)
        self.personajes[self.proximo_id] = nuevo
        self.proximo_id += 1
        return nuevo

    def actualizar(self, personaje, nombre, hp, ataque):
        personaje.nombre = nombre
        personaje.hp = hp
        personaje.ataque = ataque
        return personaje

    def borrar(self, personaje):
        del self.personajes[personaje.id]

#test para los personajes
def test_crear_personaje_exitoso():
    repo = RepositorioPersonajeFalso()
    service = PersonajeService(repo)

    datos = PersonajeInput(nombre="Kris", hp="90", ataque=10)
    nuevo = service.crear(datos, usuario_id=1)

    assert nuevo.nombre == "Kris"
    assert nuevo.hp == 90
    assert nuevo.usuario_id == 1
    assert nuevo.id == 1 #este es el primer personaje creado

def test_obtener_personaje_inexistente():
    repo = RepositorioPersonajeFalso()
    service = PersonajeService(repo)

    personaje = service.obtener(999, usuario_id=1)

    assert personaje is None

def test_obtener_personaje_de_otro_usuario():
    repo = RepositorioPersonajeFalso()
    service = PersonajeService(repo)

    datos = PersonajeInput(nombre="Kris", hp="90", ataque=10)    
    service.crear(datos, usuario_id=1) #personaje de usuario 1

    #intentar obtenerlo desde usuario 2
    personaje = service.obtener(1, usuario_id=2)

    assert personaje is None #no deberia verlo

def test_actualizar_personaje():
    repo = RepositorioPersonajeFalso()
    service = PersonajeService(repo)

    datos = PersonajeInput(nombre="Kris", hp="90", ataque=10)    
    service.crear(datos, usuario_id=1)

    datos_nuevos = PersonajeInput(nombre="Kris Cap. 2", hp="100", ataque=15)    
    actualizado = service.actualizar(1, datos_nuevos, usuario_id=1)

    assert actualizado.nombre == "Kris Cap. 2"
    assert actualizado.hp == 100
    assert actualizado.ataque == 15

def test_borrar_personaje():
    repo = RepositorioPersonajeFalso()
    service = PersonajeService(repo)

    datos = PersonajeInput(nombre="Kris", hp="90", ataque=10)    
    service.crear(datos, usuario_id=1)

    exito = service.borrar(1, usuario_id=1)

    assert exito is True

    #verificar que no existe
    personaje = service.obtener(1, usuario_id=1)
    assert personaje is None