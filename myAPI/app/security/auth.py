from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import HTTPException, status, Depends

## SEGURIDAD CON HTTP BASIC

security = HTTPBasic()

def verificarPeticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuarioAuthBool = secrets.compare_digest(credenciales.username, "Ricardo")
    contraAuthBool = secrets.compare_digest(credenciales.password,"123456")

    if not (usuarioAuthBool and contraAuthBool):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username