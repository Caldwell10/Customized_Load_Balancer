FROM docker:20.10.24-cli

WORKDIR /app

# Install Python, pip, Flask, requests, and curl
RUN apk add --no-cache python3 py3-pip curl && \
    pip3 install flask requests

COPY consistent_hash.py .
COPY load_balancer.py .

CMD ["python3", "load_balancer.py"]
