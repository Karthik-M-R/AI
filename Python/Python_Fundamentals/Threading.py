import threading
import time

def task(name, delay):
    print(f"Task {name} starting (waiting {delay}s)...")
    time.sleep(delay) # Simulates a network request or "waiting"
    print(f"Task {name} finished!")

# Creating threads
t1 = threading.Thread(target=task, args=("A", 2))
t2 = threading.Thread(target=task, args=("B", 2))

start_time = time.time()

t1.start()
t2.start()

# .join() tells the main program: "Wait for these to finish before moving on"
t1.join()
t2.join()

print(f"Total time with Threading: {time.time() - start_time:.2f} seconds")
# Output: ~2 seconds (They waited at the same time!)