FROM python:3.9-slim

WORKDIR /app

COPY consistent_hash.py .
COPY load_balancer.py .

RUN pip install flask requests

CMD ["python", "load_balancer.py"]


