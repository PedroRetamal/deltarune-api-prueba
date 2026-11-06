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