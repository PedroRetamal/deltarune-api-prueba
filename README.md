# Deltarune API

API REST para gestionar personajes de Deltarune.

## Tecnologías

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (autenticación)

## Endpoints principales

### Usuarios
- `POST /usuarios/registro` - Registrar usuario
- `POST /usuarios/login` - Iniciar sesión (devuelve JWT)

### Personajes (requieren autenticación)
- `GET /personajes` - Listar personajes del usuario
- `POST /personajes` - Crear personaje
- `PUT /personajes/{id}` - Actualizar personaje
- `DELETE /personajes/{id}` - Borrar personaje

## Autor

Pedro Retamal