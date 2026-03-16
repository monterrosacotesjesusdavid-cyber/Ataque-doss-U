FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["locust", "--headless", "--users", "100", "--spawn-rate", "10", "--run-time", "24h", "--host", "https://190.131.213.202", "--csv", "logs/resultados", "-f", "locustfile.py"]
