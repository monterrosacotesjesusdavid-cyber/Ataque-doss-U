FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["locust", "--headless", "--users", "500", "--spawn-rate", "50", "--run-time", "24h", "--host", "https://siginv.uniguajira.edu.co", "-f", "locustfile.py"]
