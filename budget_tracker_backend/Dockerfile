FROM python:3.12.3

RUN apt-get update && apt install netcat-traditional

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY budget_tracker_backend /app/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"] 