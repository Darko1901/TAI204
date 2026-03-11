from fastapi import FastAPI, Depends, status, HTTPException
import secrets
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(
    title="Examen",
    description="Examen del segundo parcial"
)

security = HTTPBasic()

tablaClientes = [
    {"ID":"1","Nombre": "Ricardo"},
    {"ID":"2", "Nombre":"Diego"}
]

tablaTramites = [
    {"ID":"1", "descipcion":"deposito"},
    {"ID":"2", "descipcion":"retiro"},
    {"ID":"3", "descipcion":"consulta"},
]

tablaTurnos = [
    {"ID":"1", "id_tramite":"2","id_usuario":"1"},
    {"ID":"2", "id_tramite":"1","id_usuario":"1"}
]

@app.get("/examen/listarTurnos")
async def consultarTurnos():
    return{
        "status":"200",
        "turnos": "hola"
    }
@app.get("/examen/turnos/listarTurnos/{id}", tags=["CRUD_EXAMEN"])
async def consultarTurnoID(id:str):
    for turno in tablaTurnos:
        if turno["id"] == tablaTurnos("id"):
            return{
                "status":"200",
                "turno": turno
            }
    raise HTTPException(
        status_code= 400,
        detail="El turno que se desea buscar no existe"
    )

