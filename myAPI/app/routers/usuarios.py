from fastapi import HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crearUsuario
from app.security.auth import verificarPeticion

router = APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)

# CONSULTAR USUARIOS DE NUESTRA TABLA FICTICIA   
@router.get("/")
async def consultaT():
    return {"status":"200",
            "Numero de usuarios":len(usuarios),
            "Usuarios":usuarios}

# AGREGAR UN USUARIO A NUESTRA TABLA FICTICIA
@router.post("/")
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

@router.delete("/{id}")
async def eliminarUsuario(id:str, usuarioAuth:str=Depends(verificarPeticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "msj": f"Usuario eliminado por {usuarioAuth}",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code= 400,
        detail="El usuario que se desea eliminar no existe"
    )

@router.patch("/{id}")
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

@router.put("/{id}")
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
