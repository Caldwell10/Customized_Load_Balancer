import asyncio
import httpx
from collections import Counter

open("results.txt", "w").close()

# Global Counter to track distribution
server_counter = Counter()

async def fetch(client, url, idx):
    try:
        response = await client.get(url)
        data = response.json()
        server_message = data.get("message", "")

        # Extract server ID
        if "Hello from Server:" in server_message:
            server_id = server_message.split("Hello from Server:")[1].strip()

            # Track this server
            server_counter[server_id] += 1

            # Also write to file for backup
            with open("results.txt", "a") as f:
                f.write(f"Request {idx} -> Server: {server_id}\n")

            print(f"Request {idx} -> Server: {server_id}")
        else:
            print(f"Request {idx} -> Unexpected response: {data}")

    except Exception as e:
        print(f"Request {idx} failed: {e}")

async def run_batch(start_idx, batch_size, url):
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch(client, f"{url}?req={i}", i)
            for i in range(start_idx, start_idx + batch_size)
        ]
        await asyncio.gather(*tasks)

async def main():
    url = "http://localhost:5001/home"
    total_requests = 10000
    batch_size = 50

    for start_idx in range(0, total_requests, batch_size):
        print(f"\n--- Starting batch {start_idx // batch_size + 1} ---\n")
        await run_batch(start_idx, batch_size, url)

    # Print summary at the end
    print("\n=== Load Distribution Summary ===")
    for server, count in server_counter.items():
        print(f"Server {server}: {count} requests")

if __name__ == "__main__":
    asyncio.run(main())
