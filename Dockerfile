# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia archivos necesarios
COPY . .

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto de FastAPI
EXPOSE 8001

# Comando para iniciar FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]
