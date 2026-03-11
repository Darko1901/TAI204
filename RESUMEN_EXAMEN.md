# Resumen de Temas - FastAPI (Tecnologías de Internet)

## 1. Fundamentos de FastAPI y Swagger

FastAPI genera automáticamente documentación interactiva con **Swagger UI** (disponible en `/docs`) y **ReDoc** (en `/redoc`). Se configura al crear la instancia de la app:

```python
app = FastAPI(
    title="Mi Primer API",
    description="Ricardo Méndez",
    version="1.0"
)
```

- Swagger permite probar endpoints directamente desde el navegador.
- Los **tags** organizan los endpoints en secciones lógicas dentro de Swagger:

```python
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
```

- Los campos `example` y `description` de Pydantic se reflejan automáticamente en la documentación OpenAPI.

---

## 2. Verbos HTTP (métodos CRUD)

| Verbo | Uso típico | Ejemplo en el proyecto |
|-------|-----------|----------------------|
| **GET** | Leer/consultar recursos | `@app.get("/v1/usuarios/")` — listar usuarios |
| **POST** | Crear un nuevo recurso | `@app.post("/v1/usuarios/")` — agregar usuario |
| **PUT** | Reemplazar un recurso completo | `@app.put("/v1/usuarios/")` — actualizar usuario completo |
| **PATCH** | Actualizar parcialmente un recurso | `@app.patch("/v1/usuarios/")` — actualizar campos específicos |
| **DELETE** | Eliminar un recurso | `@app.delete("/v1/usuarios/{id}")` — eliminar usuario por ID |

### Diferencia entre PUT y PATCH

- **PUT**: Reemplaza el recurso completo. Si omites un campo, se pierde.
- **PATCH**: Solo actualiza los campos que envías, los demás se conservan.

---

## 3. Parámetros de ruta y query

### Parámetros de ruta (obligatorios)

Se definen entre llaves `{}` en la URL y como argumento de la función:

```python
@app.get("/v1/ParametroOb/{id}")
async def parametroObligatorio(id: int):
    return {"id recibido": id}
```

Se pueden tener múltiples parámetros de ruta:

```python
@app.post("/libros/registrarPrestamo/{nombre_libro}/{correo_usuario}")
```

### Parámetros query (opcionales)

Se definen como argumentos de la función con valor por defecto (usualmente `None`):

```python
from typing import Optional

@app.get("/v1/ParametroOp/")
async def parametroOpcional(id: Optional[int] = None):
    if id is not None:
        return {"id recibido": id}
    return {"mensaje": "No se recibió ID"}
```

Se envían en la URL como `?id=5`.

---

## 4. Validaciones con Pydantic

Pydantic permite definir modelos para validar automáticamente los datos del **request body**.

### Modelo básico con validaciones

```python
from pydantic import BaseModel, Field

class crearUsuario(BaseModel):
    id: int = Field(gt=0)
    Nombre: str = Field(min_length=3, max_length=50, example="Pepe pecas")
    Edad: int = Field(ge=1, le=125)
```

### Validadores principales de `Field()`

| Validador | Tipo | Descripción |
|-----------|------|-------------|
| `gt` | numérico | Mayor que (greater than) |
| `ge` | numérico | Mayor o igual que (greater or equal) |
| `lt` | numérico | Menor que (less than) |
| `le` | numérico | Mayor o igual que (less or equal) |
| `min_length` | string | Longitud mínima de la cadena |
| `max_length` | string | Longitud máxima de la cadena |
| `pattern` | string | Expresión regular que debe cumplir |
| `example` | cualquiera | Ejemplo que aparece en Swagger |
| `description` | cualquiera | Descripción que aparece en Swagger |

### Validación con regex (expresiones regulares)

```python
correo: str = Field(
    min_length=15,
    max_length=100,
    pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)
```

### Uso del modelo en un endpoint

```python
@app.post("/v1/usuarios/")
async def agregarUsuario(usuario: crearUsuario):
    # FastAPI automáticamente valida el body contra el modelo
    # Si no cumple las validaciones, retorna 422 Unprocessable Entity
    return {"mensaje": "Usuario creado", "datos": usuario}
```

---

## 5. Códigos de estado HTTP

```python
from fastapi import HTTPException, status

# Lanzar un error con código de estado específico
raise HTTPException(status_code=400, detail="El usuario no existe")
raise HTTPException(status_code=401, detail="Credenciales inválidas")
raise HTTPException(status_code=409, detail="Conflicto: recurso duplicado")
```

| Código | Significado | Uso en el proyecto |
|--------|------------|-------------------|
| **200** | OK | Respuesta exitosa (implícito) |
| **400** | Bad Request | ID duplicado, usuario no encontrado |
| **401** | Unauthorized | Credenciales inválidas, token expirado |
| **409** | Conflict | Recurso duplicado (préstamo ya existe) |
| **422** | Unprocessable Entity | Fallo de validación de Pydantic (automático) |

---

## 6. Autenticación con HTTPBasic

Esquema simple donde el cliente envía usuario y contraseña en cada petición (codificados en Base64 en el header `Authorization`).

```python
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
import secrets

security = HTTPBasic()

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def borrarUsuario(id: int, credenciales: HTTPBasicCredentials = Depends(security)):
    # Comparación segura de credenciales (evita timing attacks)
    usuario_correcto = secrets.compare_digest(credenciales.username, "Ricardo")
    contra_correcta = secrets.compare_digest(credenciales.password, "123456")

    if not (usuario_correcto and contra_correcta):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # ... lógica de eliminación
```

### Puntos clave:
- `HTTPBasic()` activa el diálogo de login en Swagger.
- `Depends(security)` inyecta las credenciales como dependencia.
- `secrets.compare_digest()` compara strings de forma segura contra **timing attacks** (a diferencia de `==`).

---

## 7. Autenticación con OAuth2 y JWT (el más complejo)

### Conceptos clave

- **OAuth2**: Protocolo/estándar de autorización. FastAPI usa `OAuth2PasswordBearer` para el flujo de "password grant".
- **JWT (JSON Web Token)**: Token firmado digitalmente que contiene información (claims) como el usuario (`sub`) y la expiración (`exp`).
- **Bearer Token**: El cliente envía el token en el header `Authorization: Bearer <token>`.

### Configuración

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "mi_clave_segura"    # Clave secreta para firmar tokens
ALGORITHM = "HS256"                # Algoritmo de firma
ACCESS_TOKEN_EXPIRE_MINUTES = 1    # Tiempo de expiración del token

oauth = OAuth2PasswordBearer(tokenUrl="token")
```

### Paso 1: Endpoint de login (generar token)

```python
def crearToken(datos: dict):
    datosToken = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datosToken.update({"exp": expiracion})
    token = jwt.encode(datosToken, SECRET_KEY, algorithm=ALGORITHM)
    return token

@app.post("/token", tags=['Autenticacion'])
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario_ok = secrets.compare_digest(form.username, "Ricardo")
    contra_ok = secrets.compare_digest(form.password, "123456")

    if not (usuario_ok and contra_ok):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crearToken(datos={"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}
```

### Paso 2: Verificar token (dependencia)

```python
def verificarToken(token: str = Depends(oauth)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
```

### Paso 3: Proteger endpoints

```python
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def borrarUsuario(id: int, usuarioAuth: str = Depends(verificarToken)):
    # usuarioAuth contiene el nombre de usuario extraído del token
    # Solo se ejecuta si el token es válido y no ha expirado
    ...
```

### Flujo completo:

1. El cliente hace `POST /token` con `username` y `password` (form-data).
2. El servidor valida credenciales y devuelve un JWT (`access_token`).
3. El cliente incluye el token en peticiones posteriores: `Authorization: Bearer <token>`.
4. `Depends(verificarToken)` decodifica el token, verifica firma y expiración.
5. Si el token es válido, se ejecuta el endpoint; si no, retorna 401.

### Estructura del JWT:

```
Header.Payload.Signature

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "Ricardo", "exp": 1709812345}
Signature: HMACSHA256(header + payload, SECRET_KEY)
```

- `sub` (subject): identifica al usuario.
- `exp` (expiration): timestamp Unix de expiración.

---

## 8. Inyección de Dependencias con `Depends()`

FastAPI usa `Depends()` para inyectar dependencias automáticamente en los endpoints:

```python
# La función security/verificarToken se ejecuta ANTES del endpoint
# Su resultado se pasa como argumento al endpoint
credenciales: HTTPBasicCredentials = Depends(security)      # HTTPBasic
usuarioAuth: str = Depends(verificarToken)                   # JWT
form: OAuth2PasswordRequestForm = Depends()                  # Form data de OAuth2
```

Esto permite reutilizar lógica de autenticación sin repetir código.

---

## 9. Async / Await

FastAPI soporta funciones asíncronas de forma nativa:

```python
import asyncio

@app.get("/HolaMundo", tags=['Asincronía'])
async def holaMundo():
    await asyncio.sleep(5)  # Simula una operación I/O sin bloquear el servidor
    return {"mensaje": "Hola Mundo"}
```

- `async def`: Define una función asíncrona (coroutine).
- `await`: Espera el resultado de una operación asíncrona sin bloquear otros requests.
- Útil para operaciones I/O: llamadas a APIs externas, consultas a BD, lectura de archivos.

---

## 10. Manejo de errores con HTTPException

```python
from fastapi import HTTPException

# Uso básico
raise HTTPException(status_code=400, detail="El usuario ya existe")

# Con autenticación
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales inválidas"
)
```

---

## 11. Integración Flask como cliente de FastAPI

En el proyecto se creó una app Flask que consume la API de FastAPI usando la librería `requests`:

```python
import requests

# Desde Flask, hacer peticiones a FastAPI
response = requests.get("http://127.0.0.1:8000/v1/usuarios/")
response = requests.post("http://127.0.0.1:8000/v1/usuarios/", json=datos)
response = requests.delete(f"http://127.0.0.1:8000/v1/usuarios/{id}")
```

Esto demuestra que FastAPI puede servir como **backend/microservicio** consumido por otras aplicaciones.

---

## Resumen rápido para repasar

| Tema | Lo esencial |
|------|-------------|
| **Swagger** | Se genera automático en `/docs`, se configura con `title`, `description`, `version`, `tags` |
| **Verbos HTTP** | GET (leer), POST (crear), PUT (reemplazar), PATCH (actualizar parcial), DELETE (eliminar) |
| **Pydantic** | `BaseModel` + `Field()` con `gt`, `ge`, `le`, `min_length`, `max_length`, `pattern` |
| **Path params** | `/{id}` en la ruta, obligatorios |
| **Query params** | `Optional[int] = None` en la función, van con `?clave=valor` |
| **HTTPBasic** | `HTTPBasic()` + `Depends()` + `secrets.compare_digest()` |
| **OAuth2 + JWT** | `OAuth2PasswordBearer` + `jose.jwt.encode/decode` + `Depends(verificarToken)` |
| **JWT claims** | `sub` (usuario), `exp` (expiración), firmado con `SECRET_KEY` y `HS256` |
| **HTTPException** | `raise HTTPException(status_code=400, detail="mensaje")` |
| **Depends()** | Inyección de dependencias: ejecuta funciones antes del endpoint |
| **Async/Await** | `async def` + `await` para operaciones no bloqueantes |
