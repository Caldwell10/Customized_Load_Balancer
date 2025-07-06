from load_balancer.consistent_hash import ConsistentHashMap
from collections import Counter

# Initialize
hash_map = ConsistentHashMap()

# Add servers
for sid in range(1, 4):
    hash_map.add_server(sid)

counts = Counter()
# Test request mapping
for request_id in range(10000):
    server = hash_map.get_server(request_id)
    counts[server] += 1

print("Server distribution for 10,000 requests:")
for server, count in sorted(counts.items()):
    print(f"Server {server}: {count} requests")

