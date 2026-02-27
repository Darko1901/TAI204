# importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio 
from typing import Optional
from pydantic import BaseModel,Field

# instancias del servidor

app = FastAPI(
    title = "Mi Primer API",
    description= "Ricardo Méndez",
    version= "1.0"
)

# TABLA FICTICIA
usuarios = [
    {"id":"1", "nombre":"Diego", "edad":"21"},
    {"id":"2", "nombre":"Diego2", "edad":"22"},
    {"id":"3", "nombre":"Diego3", "edad":"23"}
]

class crearUsuario(BaseModel):
    id: int = Field(...,gt=0,description="Identificador de usuario")
    Nombre: str = Field(..., min_length=3, max_length=50, example="Pepe pecas")
    Edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 y 125")



# endpoints
@app.get("/", tags=['Inicio'])
# SI vemos una async es porque habrá una peticion, una peticion siempre tiene que ir acompañada de un await
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"} # La clave es "mensaje" y el valor es "Bienvenido a..."

@app.get("/HolaMundo", tags=['Asincronía'])
async def hola():
    await asyncio.sleep(5) # peticion, consultaBD, Archivo
    return {
        "mensaje": "Hola Mundo FastAPI",
        "status": "200"
        }


# PARAMETRO OBLIGATORIO
@app.get("/v1/ParametroOb/{id}", tags=['Paramétro Obligatorio']) # Con las llaves especificamos que el parametro es obligatorio
async def consultaUno(id:int):
    return {"mensaje":"Usuario encontrado",
            "usuario:":id,
            "status": "200"}

# PARAMETRO OPCIONAL
# requisitos: el endpoint debe de tener otro nombre porque son get, no necesita las llaves y la funcion debe de tener su propio nombre
@app.get("/v1/ParametroOp/", tags=['Paramétro Opcional']) # Con las llaves especificamos que el parametro es obligatorio
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

# CONSULTAR USUARIOS DE NUESTRA TABLA FICTICIA   
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return {"status":"200",
            "Numero de usuarios":len(usuarios),
            "Usuarios":usuarios}

# AGREGAR UN USUARIO A NUESTRA TABLA FICTICIA
@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def agregarUsuario(usuario:crearUsuario):
    for usr in usuarios:
        if usr["id"] == str(usuario.id):
            raise HTTPException(
                status_code= 400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado correctamente",
        "usuario":usuario,
        "status":"200"
    }

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminarUsuario(id:str):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "msj":"Usuario eliminado",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code= 400,
        detail="El usuario que se desea eliminar no existe"
    )

@app.patch("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizarUsuario(usuario:crearUsuario):
    for usr in usuarios:
        if usr["id"] == str(usuario.id):
            usr["nombre"] = usuario.Nombre
            usr["edad"] = str(usuario.Edad)
            return{
                "msj":"Usuario actualizado",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code= 400,
        detail="El id no existe"
    )

@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizarUsuario2(usuario:crearUsuario):
    for usr in usuarios:
        if usr["id"] == str(usuario.Edad):
            usr["nombre"] = usuario.Nombre
            usr["edad"] = str(usuario.Edad)
            return{
                "msj":"Usuario actualizado",
                "usuario":usr,
                "status":"200"
            }
