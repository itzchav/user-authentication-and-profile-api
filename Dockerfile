FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"]
