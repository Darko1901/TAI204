# importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind= engine)

# instancias del servidor

app = FastAPI(
    title = "Mi Primer API",
    description= "Ricardo Méndez",
    version= "1.0"
)

#Incluimos los routers que hicimos
app.include_router(usuarios.router)
app.include_router(varios.routerV)

