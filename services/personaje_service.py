from repositories.personaje_repository import PersonajeRepository

class PersonajeService:
    def __init__(self, repositorio: PersonajeRepository):
        self.repo = repositorio

    def listar(self, usuario_id: int):
        """devuelve todos los personajes del usuario"""
        return self.repo.listar_por_usuario(usuario_id)

    def obtener(self, personaje_id: int, usuario_id: int):
        """busca un personaje y devuelve None si no existe o no es del usuario"""
        return self.repo.obtener_por_id_y_usuario(personaje_id, usuario_id)

    def crear(self, datos, usuario_id: int):
        """crea personaje usando los datos del modelo Pydantic"""
        return self.repo.crear(datos.nombre, datos.hp, datos.ataque, usuario_id)

    def actualizar(self, personaje_id: int, datos, usuario_id: int):
        """actualiza un personaje y devuelve None si no existe o no es del usuario"""
        personaje = self.repo.obtener_por_id_y_usuario(personaje_id, usuario_id)

        if not personaje:
            return None

        return self.repo.actualizar(personaje, datos.nombre, datos.hp, datos.ataque)

    def borrar(self, personaje_id: int, usuario_id: int):
        """borrar un personaje, devuelve True si lo borro y False si no existía"""
        personaje = self.repo.obtener_por_id_y_usuario(personaje_id, usuario_id)
        if not personaje:
            return False

        self.repo.borrar(personaje)

        return True