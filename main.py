"""
día 3 ordenar archivos, se crea carpeta models y routers para separar todo
se crearon los __init__.py para que python sepa que sin archivos importables
"""

from fastapi import FastAPI
from routers import personajes, usuarios

#importar cors para aceptar peticiones de otros dominios
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#configuración cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #permitir cualquier origen (se restringe en producción)
    allow_credentials=True,
    allow_methods=["*"],  #permitir cualquier metodo, como post, get, patch, put, delete
    allow_headers=["*"]   #permitir cualquier header
)



# Registramos el router de personajes
# include_router le dice a FastAPI que use los endpoints de ese router.
# prefix="/personajes" pone el /personajes a todas las rutas del router
# tags=["personajes"] agrupa los endpoints bajo una etiqueta en /docs
app.include_router(personajes.router, prefix="/personajes", tags=["personajes"])

# registramos ahora los usuarios
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])

@app.get("/")
def root():
    return {"message": "hola mundo"}

@app.get("/saludo")
def saludo():
    return {"message": "hola deltarune"}