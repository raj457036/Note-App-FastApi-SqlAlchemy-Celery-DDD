import asyncio
import time

import httpx

url = "http://127.0.0.1:8000/api/v0/users/1e4d641d-4629-49ef-9e6d-a18d0339fdfb"


async def make_request():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            loop = asyncio.get_running_loop()
            start_time = loop.time()
            response = await client.get(url)
            end_time = loop.time()
            return (1, end_time - start_time, float(response.headers.get("X-Process-Time", 0.0)))
    except Exception as e:
        print("Exception: ", e)
        return (0, 0, 0)


async def main():
    success_count = 0
    failure_count = 0
    total_time = 0
    total_process_time = 0
    total_requests = 1000

    tasks = [make_request() for _ in range(total_requests)]
    start_time = time.time()  # Start measuring total time

    results = await asyncio.gather(*tasks)

    end_time = time.time()  # End measuring total time

    for success, time_taken, process_time in results:
        if success:
            success_count += 1
            total_process_time += process_time
            total_time += time_taken
        else:
            failure_count += 1

    requests_per_second = total_requests / (end_time - start_time)

    print(f"Success count: {success_count}")
    print(f"Failure count: {failure_count}")
    print(f"Average time taken per request: {total_time / total_requests}")
    print(f"Requests per second: {requests_per_second}")
    print(f"Total requests: {total_requests}")
    print(f"Total time: {end_time - start_time} seconds")
    print(f"Total process time: {total_process_time/total_requests}")


if __name__ == "__main__":
    asyncio.run(main())
