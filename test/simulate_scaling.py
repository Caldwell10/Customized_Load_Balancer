import matplotlib.pyplot as plt
from collections import Counter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'load_balancer')))

from consistent_hash import ConsistentHashMap

def simulate_scaling(min_servers=2, max_servers=6, num_requests=10000, batch_size=50):
    average_loads = []
    server_counts_list = []

    for n in range(min_servers, max_servers + 1):
        ch = ConsistentHashMap()
        for server_id in range(1, n + 1):
            ch.add_server(server_id)

        server_counts = Counter()

        total_batches = num_requests // batch_size
        request_id = 0

        for _ in range(total_batches):
            for _ in range(batch_size):
                server = ch.get_server(request_id)
                server_counts[server] += 1
                request_id += 1

        avg_load = sum(server_counts.values()) / len(server_counts)
        average_loads.append(avg_load)
        server_counts_list.append(server_counts)

        print(f"Servers: {n} -> Load Distribution: {dict(server_counts)}")

    return average_loads, server_counts_list

def plot_scaling(average_loads):
    servers = list(range(2, 7))
    plt.plot(servers, average_loads, marker='o', linestyle='-', color='green')
    plt.xlabel('Number of Servers (N)')
    plt.ylabel('Average Requests per Server')
    plt.title('Scalability of the Load Balancer with Batching')
    plt.grid(True)
    plt.savefig('Screenshots/scalability.png')
    plt.show()

if __name__ == "__main__":
    avg_loads, detailed_counts = simulate_scaling()
    plot_scaling(avg_loads)
    print("Scalability plot saved as scalability.png")

