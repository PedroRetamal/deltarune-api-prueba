# Imagen base: Python 3.12 en Debian 12 (bookworm), versión slim
FROM python:3.12-slim-bookworm

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto 8000 (donde corre FastAPI)
EXPOSE 8000

# Comando que se ejecuta al iniciar el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]