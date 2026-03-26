from fastapi import HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crearUsuario
from app.security.auth import verificarPeticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)

# CONSULTAR USUARIOS DE NUESTRA TABLA FICTICIA   
@router.get("/")
async def consultaT(db:Session = Depends(get_db)):
    queryUsuarios = db.query(usuarioDB).all()
    return {"status":"200",
            "Numero de usuarios":len(queryUsuarios),
            "Usuarios":queryUsuarios}

# AGREGAR UN USUARIO A NUESTRA TABLA FICTICIA
@router.post("/")
async def agregarUsuario(usuarioP:crearUsuario, db:Session = Depends(get_db)):
    usuarioNuevo = usuarioDB(nombre= usuarioP.Nombre, edad=usuarioP.Edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    return{
        "mensaje":"Usuario agregado correctamente",
        "usuario":usuarioP,
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
