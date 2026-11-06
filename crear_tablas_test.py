"""
Script para crear las tablas en la base de datos de testeo, se ejecuta cuando la base de datos está vacía

"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models_sqlalchemy import Base

#cargar las variables de entorno
load_dotenv()

#obtener la URL de test
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

#crear el engine de test
engine_test = create_engine(DATABASE_URL_TEST)

#crear todas las tablas definidas en los modelos
print("Crando tablas en la base de datos de testeo")
Base.metadata.create_all(engine_test)
print("Tablas creadas con éxito")