import asyncio
import httpx

async def fetch(client, url, idx):
    try:
        response = await client.get(url)
        print(f"Request {idx} -> Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Request {idx} failed: {e}")

async def run_batch(start_idx, batch_size, url):
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, url, i) for i in range(start_idx, start_idx + batch_size)]
        await asyncio.gather(*tasks)

async def main():
    url = "http://localhost:5000/home"
    total_requests = 10000
    batch_size = 50

    for start_idx in range(0, total_requests, batch_size):
        print(f"\n--- Starting batch {start_idx // batch_size + 1} ---\n")
        await run_batch(start_idx, batch_size, url)

if __name__ == "__main__":
    asyncio.run(main())
