# Deltarune API

API REST para gestionar personajes de Deltarune, construida con FastAPI, PostgreSQL y autenticación JWT.

## Tecnologías

- **Backend:** FastAPI, Python 3.12
- **Base de Datos:** PostgreSQL, SQLAlchemy (ORM)
- **Seguridad:** JWT (JSON Web Tokens), Bcrypt
- **Infraestructura:** Docker, Docker Compose

## Endpoints principales

### Usuarios
- `POST /usuarios/registro` - Registrar un nuevo usuario
- `POST /usuarios/login` - Iniciar sesión (devuelve un token JWT)

### Personajes (requieren autenticación)
- `GET /personajes` - Listar los personajes del usuario autenticado
- `POST /personajes` - Crear un nuevo personaje
- `PUT /personajes/{id}` - Actualizar un personaje existente
- `DELETE /personajes/{id}` - Eliminar un personaje

## Cómo ejecutar el proyecto (con Docker)

1. Clona el repositorio:
   ```bash
   git clone https://github.com/PedroRetamal/deltarune-api-prueba.git
   cd deltarune-api-prueba
   ```

2. Crea un archivo `.env` basándote en el archivo `.env.example` (y completa las variables con tus credenciales):
   ```bash
   cp .env.example .env
   ```

3. Levanta los contenedores:
   ```bash
   docker compose up --build -d
   ```

4. Accede a la documentación interactiva de la API:
   Abre tu navegador en `http://127.0.0.1:8001/docs`
