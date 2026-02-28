"""

THE ASYNCIO & AIOHTTP MASTERCLASS

Covers: Event Loops, Coroutines, Await, and Concurrent Web Requests.


To understand asyncio, think of it like a Busy Restaurant.

The Event Loop: This is the manager who coordinates everything.

The Waiter (Single Thread): He doesn't stand at a table waiting for customers to chew. He takes an order, sends it to the kitchen, and immediately moves to the next table.

await: This is the waiter saying, "I'm going to go do other things; call me when the food is ready."

aiohttp: This is a specialized tool for the waiter to handle many "orders" (web requests) at once without getting confused.

"""

import asyncio
import aiohttp # Note: You may need to 'pip install aiohttp'
import time

# 1. THE COROUTINE (The 'Async' Function)
# Using 'async def' creates a coroutine. It doesn't run immediately;
# it returns a coroutine object that the Event Loop manages.
async def fetch_data(id, delay):
    print(f"Request {id}: Starting (will take {delay}s)...")
    
    # 2. THE AWAIT KEYWORD
    # 'await' tells the Event Loop: "I am waiting for I/O (like a website). 
    # You can go run other functions while I wait."
    await asyncio.sleep(delay) 
    
    print(f"Request {id}: Finished!")
    return f"Data {id}"

# 3. AIOHTTP (Async Web Requests)
# Standard 'requests' is blocking (stops the whole program). 
# 'aiohttp' is non-blocking (the waiter keeps moving).
async def fetch_url(session, url):
    # 'async with' ensures the connection is closed properly after the task
    async with session.get(url) as response:
        status = response.status
        # We 'await' the result because reading the website body takes time (I/O)
        text = await response.text()
        print(f"Fetched {url} - Status: {status}")
        return len(text)

# 4. THE MAIN EVENT LOOP COORDINATOR
async def main():
    print("--- Starting Async Tasks ---")
    start_time = time.time()

    # --- Scenario A: Simple Concurrent Tasks ---
    # asyncio.gather runs multiple coroutines at the same time
    task_results = await asyncio.gather(
        fetch_data(1, 3),
        fetch_data(2, 1),
        fetch_data(3, 2)
    )
    print(f"Task Results: {task_results}")

    # --- Scenario B: Real Web Requests with AIOHTTP ---
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://www.github.com"
    ]
    
    # ClientSession is like a browser instance; we reuse it for efficiency
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        # Run all web requests in parallel
        pages_sizes = await asyncio.gather(*tasks)
        print(f"Page Sizes: {pages_sizes}")

    end_time = time.time()
    print(f"--- All finished in {end_time - start_time:.2f} seconds ---")

# 5. RUNNING THE EVENT LOOP
# This is the entry point. It starts the 'Manager' (Event Loop).
if __name__ == "__main__":
    # asyncio.run() creates the loop, runs the main function, and closes the loop.
    asyncio.run(main())

"""
SUMMARY OF TERMS:
- Event Loop: The 'brain' that decides which paused function to wake up next.
- Coroutine: A function defined with 'async def'.
- await: The pause button. It yields control back to the loop.
- asyncio.gather: The 'Start All' button for multiple tasks.
"""