from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#url de conexión usando el drives psycopg
DATABASE_URL = "postgresql+psycopg://postgres:Animania@localhost:5432/deltarune_db"

#engine es la conexión a la base
engine = create_engine(DATABASE_URL)

#sessionLocal es una "fábrica" de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base es la clase padre de todos los modelos
Base = declarative_base()