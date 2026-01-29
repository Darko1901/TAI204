# importaciones
from fastapi import FastAPI
import asyncio 

# instancias del servidor

app = FastAPI()

# endpoints
@app.get("/")
# SI vemos una async es porque habrá una peticion, una peticion siempre tiene que ir acompañada de un await
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"} # La clave es "mensaje" y el valor es "Bienvenido a..."

@app.get("/HolaMundo")
async def hola():
    await asyncio.sleep(5) # peticion, consultaBD, Archivo
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": "200"
        }
