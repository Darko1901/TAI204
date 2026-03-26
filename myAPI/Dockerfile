#Importamos la imagen basada en una version ligera de python
FROM python:3.12-slim

#Creamos carpeta de trabajo del contenedor
WORKDIR /app

#Copiamos los requerimientos del servidor
COPY requirements.txt .

# Instalando los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo de API
COPY ./app .

# Exponer el puerto con el que trabajará el contenedor
EXPOSE 5000

# Comando de ejecucion FASTAPI
CMD ["uvicorn","app.main:app","--reload","--host","0.0.0.0","--port","5000"]


