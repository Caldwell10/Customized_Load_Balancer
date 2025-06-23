import bisect

class ConsistentHashMap:
    def __init__(self, num_slots=512, virtual_servers=9):
        self.M = num_slots
        self.K = virtual_servers
        self.ring = dict()
        self.sorted_keys = []
        self.servers = set()

    def _hash_request(self, i):
        return (i + (2 ** (i % 10)) + 17) % self.M

    def _hash_virtual(self, i, j):
        return (i + j + (2 ** j) + 25) % self.M

    def add_server(self, server_id):
        if server_id in self.servers:
            return
        self.servers.add(server_id)
        for j in range(self.K):
            slot = self._hash_virtual(server_id, j)
            while slot in self.ring:
                slot = (slot + 1) % self.M
            self.ring[slot] = server_id
            bisect.insort(self.sorted_keys, slot)

    def remove_server(self, server_id):
        self.servers.discard(server_id)
        slots_to_remove = [slot for slot, sid in self.ring.items() if sid == server_id]
        for slot in slots_to_remove:
            del self.ring[slot]
            self.sorted_keys.remove(slot)

    def get_server(self, request_id):
        slot = self._hash_request(request_id)
        idx = bisect.bisect_left(self.sorted_keys, slot)
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]
