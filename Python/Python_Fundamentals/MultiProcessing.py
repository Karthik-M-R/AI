import multiprocessing
import time

def heavy_math(name):
    print(f"Process {name} calculating...")
    # Simulates heavy CPU work
    count = 0
    for i in range(10**7):
        count += i
    print(f"Process {name} done!")

if __name__ == "__main__": 
    # ^ Multiprocessing MUST be inside this 'if' on Windows/macOS
    
    p1 = multiprocessing.Process(target=heavy_math, args=("2",))
    p2 = multiprocessing.Process(target=heavy_math, args=("1",))

    start_time = time.time()

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"Total time with Multiprocessing: {time.time() - start_time:.2f} seconds")
    