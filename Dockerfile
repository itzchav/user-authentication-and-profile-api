# Usa una imagen oficial ligera de Python
FROM python:3.11-slim

# Variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . .

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto que usará Gunicorn
EXPOSE 8000

# Comando que ejecuta migraciones y arranca Gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]
