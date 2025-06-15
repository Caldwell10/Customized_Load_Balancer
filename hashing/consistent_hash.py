import math
import bisect

class ConsistentHashMap:
    def __init__(self, num_slots =512, virtual_servers=9):
        self.M =num_slots
        self.K = virtual_servers
        self.ring = dict()  # slot: server_id
        self.sorted_keys = []  # sorted slot numbers into an list
        self.servers = set()

    def _hash_request(self, request_id):
        return (request_id + 2**request_id+17) % self.M

    def _hash_virtual(self,server_id, replica_id):
        return(server_id**2 + replica_id + 2**replica_id+25) % self.M

    def add_server(self, server_id):
        if server_id in self.servers:
            return
        self.servers.add(server_id) # track this server

        for j in range(self.K): # for each virtual replica
            slot =self._hash_virtual(server_id, j)
            # If slot is taken, apply linear probing
            while slot in self.ring:
                slot = (slot + 1) % self.M # move to the next slot circularly

            self.ring[slot] = server_id #assign this slot to server
            bisect.insort(self.ring[slot], server_id) # insert into sorted slot list


        def remove_server(self, server_id):
            self.servers.discard(server_id)
            slots_to_remove = [slot for slot,sid in self.ring.items() if sid == server_id]
            for slot in slots_to_remove:
                del self.ring[slot]
                self.sorted_keys.remove(slot)

        def get_server(self, request_id):
            slot = self._hash_request(request_id)
            idx = bisect.bisect_left(self.sorted_keys, slot)
            if idx == len(self.sorted_keys):
                idx = 0
            return self.ring[self.sorted_keys[idx]]





