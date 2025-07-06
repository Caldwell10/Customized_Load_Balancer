from flask import Flask, request, jsonify
import random, string, subprocess
from consistent_hash import ConsistentHashMap
import hashlib
from threading import Lock
import requests
import threading
import time

app = Flask(__name__)
ch_map = ConsistentHashMap(num_slots=512, virtual_servers=9)
N = 3  # default replicas
container_prefix = "Server"

# Track active containers
active_containers = {}

# Round Robin state
rr_index = 0
rr_lock = Lock()

def generate_hostname():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def spawn_container(server_id, hostname=None):
    if hostname is None:
        hostname = generate_hostname()
    print(f"[INFO] Spawning container: ServerID={server_id}, Hostname={hostname}")
    subprocess.run([
        "docker", "run", "--rm", "-d",
        "--name", hostname,
        "--network", "net1",
        "--network-alias", hostname,
        "-e", f"SERVER_ID={server_id}",
        "server_img"
    ])
    ch_map.add_server(server_id)
    active_containers[server_id] = hostname
    print(f"[INFO] Active containers after spawn: {active_containers}\n")
    return hostname

def remove_container(server_id):
    hostname = active_containers.get(server_id)
    if hostname:
        print(f"[INFO] Removing container: ServerID={server_id}, Hostname={hostname}")
        subprocess.run(["docker", "stop", hostname])
        subprocess.run(["docker", "rm", hostname])
        ch_map.remove_server(server_id)
        del active_containers[server_id]
        print(f"[INFO] Active containers after removal: {active_containers}\n")

# Heartbeat checker function
def heartbeat_checker(interval=5, timeout=2):
    while True:
        time.sleep(interval)
        for server_id, hostname in list(active_containers.items()):
            try:
                url = f"http://{hostname}:5001/heartbeat"
                res = requests.get(url, timeout=timeout)
                if res.status_code != 200:
                    raise Exception("Heartbeat failed")
            except Exception:
                print(f"[ALERT] Server {server_id} ({hostname}) failed heartbeat check. Removing and respawning...")
                remove_container(server_id)
                new_server_id = max(active_containers.keys(), default=0) + 1
                spawn_container(new_server_id)
                print(f"[INFO] Spawned new server with ID {new_server_id}")

@app.route("/rep", methods=["GET"])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(active_containers),
            "replicas": list(active_containers.values())
        },
        "status": "successful"
    }), 200

@app.route("/add", methods=["POST"])
def add_replicas():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Hostnames > instances", "status": "failure"}), 400
    for i in range(n):
        sid = max(active_containers.keys(), default=0) + 1
        hname = hostnames[i] if i < len(hostnames) else None
        spawn_container(sid, hname)
    return get_replicas()

@app.route("/rm", methods=["DELETE"])
def remove_replicas():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Hostnames > removable instances", "status": "failure"}), 400

    ids_to_remove = [sid for sid, h in active_containers.items() if h in hostnames]
    all_ids = list(active_containers.keys())
    extra = n - len(ids_to_remove)
    ids_to_remove += random.sample([sid for sid in all_ids if sid not in ids_to_remove], extra)

    for sid in ids_to_remove:
        remove_container(sid)
    return get_replicas()

def get_request_id(path):
    return int(hashlib.sha256(path.encode()).hexdigest(), 16) % (10**6)

def get_next_server_rr():
    global rr_index
    with rr_lock:
        if not active_containers:
            return None
        server_ids = sorted(active_containers.keys())
        server_id = server_ids[rr_index % len(server_ids)]
        rr_index += 1
        return server_id

def get_server_by_hash(path):
    rid = get_request_id(path)
    return ch_map.get_server(rid)

@app.route('/<path:endpoint>', methods=["GET"])
def proxy(endpoint):
    server_id = get_next_server_rr()
    hostname = active_containers.get(server_id)

    if not hostname:
        return jsonify({"message": "No server available", "status": "failure"}), 503

    try:
        url = f"http://{hostname}:5001/{endpoint}"

        if request.query_string:
            url = f"{url}?{request.query_string.decode()}"

        print(f"[INFO] Proxying to URL: {url}")
        res = requests.get(url)

        print(f"[DEBUG] Response status: {res.status_code}")
        print(f"[DEBUG] Response content: '{res.text}'")

        if not res.content.strip():
            return "", res.status_code

        try:
            return jsonify(res.json()), res.status_code
        except ValueError:
            return res.text, res.status_code

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to route request to {hostname}: {e}")
        return jsonify({"message": "Request exception occurred", "status": "failure"}), 400

if __name__ == "__main__":
    for sid in range(1, N+1):
        spawn_container(sid, f"Server{sid}")

    # Start heartbeat checker
    threading.Thread(target=heartbeat_checker, daemon=True).start()

    print("[INFO] Load balancer started on port 5001")
    app.run(host="0.0.0.0", port=5001)
