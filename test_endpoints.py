def test_flujo_completo_usuario_y_personaje(client):
    """
    Test del flujo completo:
    1. Registro de usuario
    2. Login y obtención de token
    3. crear un personaje (depende de que haya un token)
    4. listar personaje y verificar que el personaje salga
    """

    #1. registro de usuario
    respuesta = client.post("/usuarios/registro", json={
        "username": "pedro",
        "password": "password123"
    })
    assert respuesta.status_code == 201
    assert respuesta.json()["username"] == "pedro"

    #2. Login y obtención de token
    respuesta = client.post("/usuarios/login", json={
        "username": "pedro",
        "password": "password123"
    })
    assert respuesta.status_code == 200
    token = respuesta.json()["access_token"]
    assert token is not None

    #3. Crear personaje
    respuesta = client.post(
        "/personajes",
        json={"nombre": "Kris", "hp": 90, "ataque":10},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert respuesta.status_code == 201
    personaje = respuesta.json()
    assert personaje["nombre"] == "Kris"
    assert personaje["hp"] == 90
    assert personaje["ataque"] == 10

    #4. listar personajes
    respuesta = client.get(
        "/personajes",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["usuario_actual"] == "pedro"
    assert len(datos["personajes"]) == 1
    assert datos["personajes"][0]["nombre"] == "Kris"


def test_crud_completo_personajes(client):
    """Test del CRUD completo de personajes: crear, leer, actualizar y borrar"""
    #registrar usuario y obtener token
    client.post("/usuarios/registro", json={"username": "kris", "password": "password123"})
    respuesta = client.post("/usuarios/login", json={"username": "kris", "password": "password123"})
    token = respuesta.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    #crear personaje
    respuesta = client.post("/personajes", json={"nombre": "Susie", "hp": 120, "ataque": 14}, headers= headers)
    assert respuesta.status_code == 201
    personaje_id = respuesta.json()["id"]

    #obtener personaje
    respuesta = client.get(f"/personajes/{personaje_id}", headers=headers)
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Susie"
    assert respuesta.json()["hp"] == 120
    assert respuesta.json()["ataque"] == 14

    #actualizar personaje
    respuesta = client.put(
        f"/personajes/{personaje_id}",
        json={"nombre": "Susie chapter 2", "hp": 150, "ataque": 20},
        headers=headers
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["hp"] == 150

    #borrar personaje
    respuesta = client.delete(f"/personajes/{personaje_id}", headers=headers)
    assert respuesta.status_code == 204

    #verificar que ya no existe
    respuesta = client.get(f"/personajes/{personaje_id}", headers=headers)
    assert respuesta.status_code == 404

def test_errores_autenticacion(client):
    """Test de errores: registro duplicado y login con contraseña incorrecta"""
    #Registrar un usuario
    client.post("/usuarios/registro", json={"username": "kris", "password": "password123"})

    #registro duplicado
    respuesta = client.post("/usuarios/registro", json={"username": "kris", "password": "otrapassword"})
    assert respuesta.status_code == 400

    #login con contraseña incorrecta
    respuesta = client.post("/usuarios/login", json={"username": "kris", "password": "wrong"})
    assert respuesta.status_code == 401

def test_aislamiento_entre_usuarios(client):
    """Test de que un usuario no puede ver los personajes de otro"""
    #usuario 1
    client.post("/usuarios/registro", json={"username": "kris", "password": "password123"})
    respuesta = client.post("/usuarios/login", json={"username": "kris", "password": "password123"})
    token_kris = respuesta.json()["access_token"]

    #usuario 1 crea personaje
    respuesta = client.post(
        "/personajes",
        json={"nombre": "Kris", "hp": 90, "ataque": 10},
        headers={"Authorization": f"Bearer {token_kris}"}
    )
    personaje_id = respuesta.json()["id"]

    #usuario 2
    client.post("/usuarios/registro", json={"username": "susie", "password": "password123"})
    respuesta = client.post("/usuarios/login", json={"username": "susie", "password": "password123"})
    token_susie = respuesta.json()["access_token"]

    #usuario 2 intenta ver el personaje de usuario 1
    respuesta = client.get(
        f"/personajes/{personaje_id}",
        headers={"Authorization": f"Bearer {token_susie}"}
    )
    assert respuesta.status_code == 404
