FROM python:3.9-slim

WORKDIR /app

COPY server.py .

RUN pip install flask

ENV SERVER_ID=1

CMD ["python", "server.py"]
