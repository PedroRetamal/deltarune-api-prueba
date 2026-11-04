import os
import psycopg
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

def obtener_conexion():
    """Devuelve una conexión nueva a PostgreSQL usando las variables de entorno."""
    return psycopg.connect(os.getenv("DATABASE_URL_PSYCOPG"))