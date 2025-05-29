# Usa una imagen oficial de Python como base
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto por donde la app escuchará (8000 para Django)
EXPOSE 8000

# Comando para correr el servidor de desarrollo de Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]

