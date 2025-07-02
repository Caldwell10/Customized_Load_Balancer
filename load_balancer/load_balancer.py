from flask import Flask, request, jsonify
import random, string, subprocess
from consistent_hash import ConsistentHashMap

app = Flask(__name__)
ch_map = ConsistentHashMap()
N = 3  # default replicas
container_prefix = "Server"

# Track active containers
active_containers = {}

def generate_hostname():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def spawn_container(server_id, hostname=None):
    if hostname is None:
        hostname = generate_hostname()
    subprocess.run([
        "docker", "run", "--rm", "-d",
        "--name", hostname,
        "--network", "customized_load_balancer_net1",
        "--network-alias", hostname,
        "-e", f"SERVER_ID={server_id}",
        "server_img"  # Build image from ./server/Dockerfile
    ])
    ch_map.add_server(server_id)
    active_containers[server_id] = hostname
    return hostname

def remove_container(server_id):
    hostname = active_containers.get(server_id)
    if hostname:
        subprocess.run(["docker", "stop", hostname])
        subprocess.run(["docker", "rm", hostname])
        ch_map.remove_server(server_id)
        del active_containers[server_id]

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

@app.route('/<path:endpoint>', methods=["GET"])
def proxy(endpoint):
    rid = random.randint(100000, 999999)
    server_id = ch_map.get_server(rid)
    hostname = active_containers.get(server_id)
    if not hostname:
        return jsonify({"message": "No server available", "status": "failure"}), 503
    try:
        import requests
        url = f"http://{hostname}:5050/{endpoint}"
        res = requests.get(url)
        return jsonify(res.json()), res.status_code
    except:
        return jsonify({"message": f"<Error> '/{endpoint}' endpoint does not exist", "status": "failure"}), 400

if __name__ == "__main__":
    for sid in range(1, N+1):
        spawn_container(sid, f"Server{sid}")
    app.run(host="0.0.0.0", port=5000)
