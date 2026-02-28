from multiprocessing import Process, Value, Lock

def add_order(shared_count, lock):
    with lock: # Chef A "locks" the board so Chef B can't touch it yet
        shared_count.value += 1 

if __name__ == "__main__":
    # 'i' means integer, 0 is the starting value
    orders = Value('i', 0)
    lock = Lock()
    
    p1 = Process(target=add_order, args=(orders, lock))
    p2 = Process(target=add_order, args=(orders, lock))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    print(orders.value) # Should be 2