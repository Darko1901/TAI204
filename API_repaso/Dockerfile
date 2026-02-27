# Importar la imagen
FROM python:3.12-slim

# Creamos la carpeta de trabajo del contenedor
# En este caso es app, porque ahi es donde esta nuestra apy y todos los archivos
# con los que trabajara el contenedor
WORKDIR /app

# Copiamos los requerimientos del servidor
COPY requirements.txt .

# Instalar los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el codigo de la api o de nuestro proyecto
COPY ./app .

# Exponemos el puerto con el que trabajará el contenedor
EXPOSE 5002

# Comando para ejecutar el servidor
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","5002","--reload"]

