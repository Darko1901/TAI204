from pydantic import BaseModel, Field

##MODELO DE VALIDACION PYDANTIC
class crearUsuario(BaseModel):
    id: int = Field(...,gt=0,description="Identificador de usuario")
    Nombre: str = Field(..., min_length=3, max_length=50, example="Pepe pecas")
    Edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 y 125")


