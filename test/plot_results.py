import matplotlib.pyplot as plt
from collections import Counter

# Read the results from the file
server_counts = Counter()

with open('results.txt', 'r') as f:
    for line in f:
        if "Hello from Server:" in line:
            server_id = line.split("Hello from Server:")[1].split("'")[0].strip()
            server_counts[server_id] += 1

# Plot
servers = list(server_counts.keys())
requests = list(server_counts.values())

plt.bar(servers, requests, color='skyblue')
plt.xlabel('Server ID')
plt.ylabel('Number of Requests')
plt.title('Load Distribution Across Servers')

# Save the plot
plt.savefig('load_distribution.png')
print("Plot saved as load_distribution.png")
