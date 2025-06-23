from load_balancer.consistent_hash import ConsistentHashMap

# Initialize
hash_map = ConsistentHashMap()

# Add servers
for sid in range(1,4):
    hash_map.add_server(sid)

# Test request mapping
print("Request ID -> Server Mapping")
for request_id in range(1000,1010):
    server = hash_map.get_server(request_id)
    print(f"Request {request_id} -> {server}")

