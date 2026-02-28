import threading
import time

def standard_worker():
    print("Non-Daemon: Starting important work...")
    time.sleep(5)
    print("Non-Daemon: Important work FINISHED!") # This WILL print

def background_support():
    while True:
        print("Daemon: Just cleaning up in the background...")# if deamon false then this runs infinitely
        time.sleep(1)

# Creating the threads
t1 = threading.Thread(target=standard_worker)
t2 = threading.Thread(target=background_support, daemon=True) # Set as Daemon

t1.start()
t2.start()

print("Main Thread: My job is done. Waiting for Non-Daemons...")
# The program will wait 5 seconds for t1, but as soon as t1 finishes,
# it will KILL t2 immediately and exit.