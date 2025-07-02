import asyncio
import httpx

async def fetch(client, url, idx):
    try:
        response = await client.get(url)
        print(f"Request {idx} -> Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Request {idx} failed: {e}")

async def main():
    url = "http://localhost:5000/home"
    num_requests = 20  # Number of concurrent requests

    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, url, i) for i in range(num_requests)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
