# importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios

# instancias del servidor

app = FastAPI(
    title = "Mi Primer API",
    description= "Ricardo Méndez",
    version= "1.0"
)

#Incluimos los routers que hicimos
app.include_router(usuarios.router)
app.include_router(varios.routerV)

