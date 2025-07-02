FROM python:3.9-slim

WORKDIR /app

COPY consistent_hash.py .
COPY load_balancer.py .

RUN pip install flask requests

RUN apt-get update && apt-get install -y docker.io

CMD ["python", "load_balancer.py"]

