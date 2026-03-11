from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, field_validator
from typing import Literal
import secrets
from datetime import datetime

app = FastAPI(
    title="Examen",
    description="Examen del segundo parcial",
)

# TABLA
turnos = [
    {"id": "1", "cliente": "Ricardo Mendez", "tipo_tramite": "deposito", "fecha_turno": "2026-03-15 10:00", "atendido": False},
    {"id": "2", "cliente": "Maria Garcia", "tipo_tramite": "retiro", "fecha_turno": "2026-03-15 11:30", "atendido": False},
]

class CrearTurno(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del turno")
    cliente: str = Field(..., min_length=8, max_length=50, example="Ricardo Méndez")
    tipo_tramite: Literal["deposito", "retiro", "consulta"] # -> Literal nos sirve para poder poner cualquiera de los tipos de trámite
    fecha_turno: str = Field(..., example="2026-03-15 10:00")

    @field_validator("fecha_turno")
    @classmethod
    def validar_fecha(cls, v):
        try:
            fecha = datetime.strptime(v, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use: YYYY-MM-DD HH:MM")

        if fecha <= datetime.now():
            raise ValueError("La fecha del turno debe de ser después del día de hoy")

        if fecha.hour < 9 or fecha.hour >= 15:
            raise ValueError("El turno debe estar entre las 9:00 y las 15:00")

        return v

security = HTTPBasic()

def verificarPeticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credenciales.username, "banco")
    contraAuth = secrets.compare_digest(credenciales.password, "2468")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username

# ENDPOINTS

@app.get("/", tags=["Inicio"])
async def prueba():
    return {
        "mensaje": "PRUEBA"
    }

# CONSULTAR TODOS LOS TURNOS
@app.get("/v1/turnos/", tags=["Turnos"])
async def consultarTurnos():
    return {
        "status": "200",
        "total": len(turnos),
        "turnos": turnos
    }

@app.get("/v1/turnos/{id}", tags=["Turnos"])
async def consultarTurnoPorId(id: str):
    for t in turnos:
        if t["id"] == id:
            return {
                "status": "200",
                "turno": t
            }
    raise HTTPException(
        status_code=400,
        detail="El turno que se desea buscar no existe"
    )

# CREAR TURNO
@app.post("/v1/turnos/", tags=["Turnos"])
async def crearTurno(turno: CrearTurno):
    for t in turnos:
        if t["id"] == str(turno.id):
            raise HTTPException(
                status_code=400,
                detail="El id del turno ya existe"
            )

    # Validar máximo 5 turnos por día por cliente
    fecha_nueva = datetime.strptime(turno.fecha_turno, "%Y-%m-%d %H:%M").date()
    turnos_del_cliente = [
        t for t in turnos
        if t["cliente"] == turno.cliente and
        datetime.strptime(t["fecha_turno"], "%Y-%m-%d %H:%M").date() == fecha_nueva
    ]
    if len(turnos_del_cliente) >= 5:
        raise HTTPException(
            status_code=400,
            detail=f"El cliente {turno.cliente} ya tiene 5 turnos para ese día"
        )

    turnos.append({
        "id": str(turno.id),
        "cliente": turno.cliente,
        "tipo_tramite": turno.tipo_tramite,
        "fecha_turno": turno.fecha_turno,
        "atendido": False
    })
    return {
        "mensaje": "Turno creado correctamente",
        "turno": turno,
        "status": "200"
    }

# MARCAR COMO ATENDIDO 
@app.patch("/v1/turnos/{id}/atendido", tags=["Turnos"])
async def marcarAtendido(id: str, usuarioAuth: str = Depends(verificarPeticion)):
    for t in turnos:
        if t["id"] == id:
            t["atendido"] = True
            return {
                "msj": f"Turno marcado como atendido por {usuarioAuth}",
                "turno": t,
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Turno no encontrado"
    )

# ELIMINAR TURNO 
@app.delete("/v1/turnos/{id}", tags=["Turnos"])
async def eliminarTurno(id: str, usuarioAuth: str = Depends(verificarPeticion)):
    for t in turnos:
        if t["id"] == id:
            turnos.remove(t)
            return {
                "msj": f"Turno eliminado por {usuarioAuth}",
                "turno": t,
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Turno no encontrado"
    )
