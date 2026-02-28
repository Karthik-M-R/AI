'''We use run_in_executor to run that blocking function in a separate thread, 
allowing the Event Loop to stay responsive.'''

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def blocking_work(n):
    # This represents a library that isn't async-friendly (e.g., requests, cv2, pandas)
    time.sleep(2) 
    return f"Finished heavy work {n}"

async def main():
    loop = asyncio.get_running_loop()
    
    print("--- Starting Main Loop ---")

    # 1. We create a 'pool' of workers
    with ThreadPoolExecutor() as pool:
        
        # 2. We schedule the blocking work in the executor
        # Syntax: run_in_executor(executor, function, *args)
        # Note: We pass the function name, NOT function_name()
        task1 = loop.run_in_executor(pool, blocking_work, 1)
        task2 = loop.run_in_executor(pool, blocking_work, 2)

        # 3. While those run in threads, we can still do async stuff!
        print("Main loop is still alive and serving other tasks...")
        await asyncio.gather(
            asyncio.sleep(1),
            asyncio.sleep(1)
        )
        print("Asyncio tasks finished while threads were still working.")

        # 4. Now we wait for the results from the threads
        result1 = await task1
        result2 = await task2
        print(f"Results from threads: {result1}, {result2}")

if __name__ == "__main__":  
    asyncio.run(main())


    # if __name__ == "__main__" ensures that certain code runs only when the file is 
    # executed directly, not when imported as a module.