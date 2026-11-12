import os
from sqlalchemy import create_engine
from models_sqlalchemy import Base
from dotenv import load_dotenv

load_dotenv()

#docker pasa esta variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está definida")

print("conectando a la base de datos para crear tablas")
engine = create_engine(DATABASE_URL)

#crear las tablas
Base.metadata.create_all(bind=engine)

print("tablas creadas correctamente")