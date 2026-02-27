from fastapi import FastAPI,status,HTTPException
import asyncio
from pydantic import BaseModel,Field

## Instancias del servidor

app = FastAPI(
    title="API Biblioteca",
    description="API para la gestión de los libros y préstamos de una biblioteca"
)

### TABLA CON REGISTROS DE EJEMPLO
tabla_libros = [
    {"id":"1", "nombre":"El jugador", "anio":"1890", "num_paginas":"200", "estado":"Disponible"},
    {"id":"2", "nombre":"Noches Blancas", "anio":"1895", "num_paginas":"125", "estado":"Prestado"},
]
tabla_usuarios = [
    {"id":"1", "nombre":"Ricardo","correo":"holaRichie1901@gmail.com"},
    {"id":"2", "nombre":"Artemio","correo":"holaArti69@gmail.com"}
]
tabla_prestamos = [
    {"id":"1","libro":"Noches Blancas","correo_usuario":"holaArti69@gmail.com"}
]

## CLASE para lo de pydantic
class crearLibro(BaseModel):
    id: int = Field(...,gt=0,description="Identificador del libro")
    Nombre: str = Field(...,min_length=2, max_length=100,example="La rata con thinner")
    Anio: int = Field(...,ge=1450, le=2026, description="Año del libro")
    Num_pags: int = Field(..., gt=1, example="300")
    Estado: str = Field(...,min_length=5, max_length=30, description="Estado en el que se encuentra el libro")

class crearUsuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificador del usuario")
    Nombre: str = Field(...,min_length=3, max_length=50, example="Ana")
    correo: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', min_length=15, max_length=100)


## ENDPOINTS
@app.get("/libros/consultar/", tags=["CRUD_libros"])
async def consultarLibros():
    return{
        "status":"200",
        "Registros":len(tabla_libros),
        "Libros": tabla_libros
    }
# Consultar prestamos
@app.get("/prestamos/consultar/", tags=["CRUD_libros"])
async def consultarPrestamos():
    return{
        "status":"200",
        "Registros":len(tabla_prestamos),
        "Prestamos":tabla_prestamos
    }
# Agregar un libro, aquí sí usamos la clase de crearLibro
@app.post("/libros/agregar/", tags=["CRUD_libros"])
async def agregarLibro(libro:crearLibro):
    for i in tabla_libros:
        if i["id"] == str(libro.id):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    tabla_libros.append(libro)
    return{
        "mensaje": "Libro agregado",
        "libro": libro,
        "status": "200"
    }
# Buscar un libro por su nombre
@app.get("/libros/buscarPorNombre/{nombre}", tags=["CRUD_libros"])
async def buscarLibroPorNombre(nombre:str):
    for lbr in tabla_libros:
        if lbr["nombre"].lower() == nombre.lower():
            return{
                "status":"200",
                "mensaje":"libro encontrado",
                "libro": lbr
            }
    raise HTTPException(
        status_code=400,
        detail="El libro que se desea buscar no está registrado"
    )

# marcar el libro como devuelto
@app.put("/libros/marcarDevuelto/{nombre}", tags=["CRUD_libros"])
async def marcarLibroComoDevuelto(nombre:str):
    for lbr in tabla_libros:
        if lbr["nombre"].lower() == nombre.lower():
            lbr["estado"] = "devuelto"
            return{
                "status":"200",
                "mwnsaje": "Libro marcado como devuelto",
                "libro": lbr
            }
    raise HTTPException(
        status_code=409,
        detail="El libro que se desea buscar no está registrado"
    )

# Registrar el prestamo de un libro a un usuario
@app.post("/libros/registrarPrestamo/{nombre_libro}/{correo_usuario}", tags=["CRUD_libros"])
async def registrarPrestamoUsuario(libro:str, correo:str):
    for i in tabla_libros:
        if i["nombre"].lower() == libro.lower():
            if i["estado"].lower() != "disponible":
                raise HTTPException(
                    status_code=400,
                    detail="El libro no está disponible para préstamo"
                )
            for j in tabla_usuarios:
                if j["correo"].lower() == correo.lower():
                    # Aqui se valida que no exista un prestamo con el mismo usuario y mismo libro
                    for prestamo in tabla_prestamos:
                        if prestamo["libro"].lower() == libro.lower():
                            raise HTTPException(
                                status_code=409,
                                detail="El usuario ya tiene este libro en préstamo"
                            )
                    # Registramos el prestamo
                    tabla_prestamos.append(
                        {
                        "libro": libro,
                        "correo_usuario": correo
                        }
                    )
                    i["estado"] = "Prestado"
                    return{
                        "status":"200",
                        "mensaje":"Prestamo registrado"
                    }
            raise HTTPException(
                status_code=400,
                detail="El usuario no existe"
            )
    raise HTTPException(
        status_code=400,
        detail="El libro no existe"
    )

# Eliminar el registro de un prestamo
@app.delete("/libros/eliminarPrestamo/{id}", tags=["CRUD_libros"])
async def eliminarPrestamo(id:str):
    for pre in tabla_prestamos:
        if pre["id"] == id:
            tabla_prestamos.remove(pre)
            return {
                "status":"200",
                "registro":pre,
                "mensaje":"Registro eliminado"
            }
    raise HTTPException(
        status_code=400,
        detail="El registro que se desea buscar no existe"
    )