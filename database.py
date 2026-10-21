import psycopg

# Datos de conexión (en el futuro esto va en .env)
DB_CONFIG = {
    "dbname": "deltarune_db",
    "user": "postgres",
    "password": "Animania",   # ← reemplaza con tu contraseña real
    "host": "localhost",
    "port": "5432"
}

def obtener_conexion():
    """Devuelve una conexión nueva a PostgreSQL."""
    return psycopg.connect(**DB_CONFIG)