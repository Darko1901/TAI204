import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

routerV = APIRouter(
    tags=["Inicio"]
)

# endpoints
@routerV.get("/")
# SI vemos una async es porque habrá una peticion, una peticion siempre tiene que ir acompañada de un await
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"} # La clave es "mensaje" y el valor es "Bienvenido a..."

@routerV.get("/HolaMundo")
async def hola():
    await asyncio.sleep(5) # peticion, consultaBD, Archivo
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": "200"
        }

# PARAMETRO OBLIGATORIO
@routerV.get("/v1/ParametroOb/{id}") # Con las llaves especificamos que el parametro es obligatorio
async def consultaUno(id:int):
    return {"mensaje":"Usuario encontrado",
            "usuario:":id,
            "status": "200"}

# PARAMETRO OPCIONAL
# requisitos: el endpoint debe de tener otro nombre porque son get, no necesita las llaves y la funcion debe de tener su propio nombre
@routerV.get("/v1/ParametroOp/") # Con las llaves especificamos que el parametro es obligatorio
async def consultarTodos(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"mensaje":"Usuario encontrado",
                       "usuario:": usuarioK,
                       "status": "200"}
        return{"mensaje": "usuario no encontrado",
               "status":"200"}
    else:
        return{"mensaje": "no se insertó ningún usuario para buscar",
               "status":"200"}


