from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# definimos URL de la conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

# creamos el motor de la conexión
engine = create_engine(DATABASE_URL)

# creamos la gestión de sesiones
session_local = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

# creamos la base declarativa para los modelos
Base = declarative_base()

# funcion que trabajará con las peticiones
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

