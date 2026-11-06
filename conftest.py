import os
import pytest 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from database_sqlalchemy import get_db
from models_sqlalchemy import Base
from sqlalchemy import text

#cargar variables de entorno
load_dotenv()

#url de la base de datos de testeo
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

#crear engine de test
engine_test = create_engine(DATABASE_URL_TEST)

#fábrica de sesiones para testear
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture que devuelve una sesión de base de datos de test, limpia todas las tablas antes de cada testeo
    """

    #crear tablas (en caso de que no existan)
    Base.metadata.create_all(bind=engine_test)

    #limpiar tablas antes del test, primero personajes y luego los usuarios por la foreign key
    with engine_test.connect() as conn:
        conn.execute(text("TRUNCATE TABLE personajes RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE usuarios RESTART IDENTITY CASCADE;"))
        conn.commit()

    #crear la sesión
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture que devuelve un TestClient de FastAPI sobrescribiendo la dependencia get_db para usar la base
    de datos de testeo
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    #sobrescribir la dependencia de la base de datos
    app.dependency_overrides[get_db] = override_get_db

    #crear el cliente de test
    with TestClient(app) as test_client:
        yield test_client

    #limpiar sobreescritura
    app.dependency_overrides.clear()