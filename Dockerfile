# Base image: lightweight Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Flask server code into the container
COPY server.py .

# Install Flask inside the container
RUN pip install flask

# Set a default environment variable
ENV SERVER_ID=1

# Run the Flask app
CMD ["python", "server.py"]
