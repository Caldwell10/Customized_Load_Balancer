FROM python:3.9-slim

WORKDIR /app

COPY consistent_hash.py .
COPY load_balancer.py .

RUN pip install flask requests

CMD ["python", "load_balancer.py"]

# Install Docker CLI
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y docker-ce docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*
