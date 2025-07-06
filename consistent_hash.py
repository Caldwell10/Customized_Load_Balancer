import hashlib

class ConsistentHashMap:
    def __init__(self, num_slots=512, virtual_servers=9, use_sha256=True):
        self.M = num_slots
        self.K = virtual_servers
        self.use_sha256 = use_sha256
        self.ring = dict()
        self.sorted_keys = []
        self.servers = set()

    def _hash_request(self, i):
        if self.use_sha256:
            # Use SHA256 for better distribution
            return int(hashlib.sha256(str(i).encode()).hexdigest(), 16) % self.M
        # Assignment formula
        return (i + (2 ** (i % 10)) + 17) % self.M

    def _hash_virtual(self, i, j):
        if self.use_sha256:
            return int(hashlib.sha256(f"{i}-{j}".encode()).hexdigest(), 16) % self.M
        return (i + j + (2 ** j) + 25) % self.M

    # ...rest of your class...