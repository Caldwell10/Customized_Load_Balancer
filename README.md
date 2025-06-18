
# Customized Load Balancer 

This project is part of a Distributed Systems assignment. It includes:
- A Dockerized HTTP server written with Flask
- A consistent hashing module to distribute requests
- Early testing and screenshots
- Port considerations due to system-level conflicts on macOS

---

## ✅ Task 1: Flask Server

### Features
- `/home` endpoint returns a JSON message with a unique server ID.
- `/heartbeat` endpoint confirms the server is alive with HTTP 200.

### Code
Server is implemented in `server.py`. Example response from `/home`:

```json
{
  "message": "Hello from Server: Unknown",
  "status": "successful"
}
```

> Server ID is passed via an environment variable (`SERVER_ID`) when running the container.

---

## 🐳 Dockerfile

The Flask server is containerized using the following Dockerfile:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY server.py .
RUN pip install flask
ENV SERVER_ID=1
CMD ["python", "server.py"]
```

---

## 🚀 Port Usage

**Note**: Port `5000` is required by the assignment, but on macOS it was already occupied by a system service (Control Center / AirPlay).  
✅ For local development, we used **port `5050`** temporarily:
```python
app.run(host='0.0.0.0', port=5050)
```

This will be reverted to `5000` before final testing in Ubuntu.

---

## 🧪 Screenshots

### `/home` endpoint
![Home Endpoint](Screenshots/home.png)

### `/heartbeat` endpoint
![Heartbeat Endpoint](Screenshots/heartbeat.png)

---

## ✅ Task 2: Consistent Hashing

Implemented in `hashing/consistent_hash.py`. Features:
- 512-slot consistent hash ring
- Each physical server has 9 virtual replicas
- Hashing functions as specified in the assignment:
  - Request: `H(i) = i + 2^i + 17`
  - Virtual server: `Φ(i, j) = i + j + 2^j + 25`
- Exponentiation is capped to prevent overflow:
  ```python
  def _hash_request(self, i):
      return (i + (2 ** (i % 10)) + 17) % 512
  ```

---

## 📂 Repository Structure (so far)
```
customizable-load-balancer/
├── Dockerfile
├── server.py
├── hashing/
│   └── consistent_hash.py
├── Screenshots/
│   ├── home.png
│   └── heartbeat.png
```

---
