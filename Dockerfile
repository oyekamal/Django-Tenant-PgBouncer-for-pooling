FROM python:3.9

WORKDIR /app

# Install netcat for health check
RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
