from multiprocessing import Process, Queue

def cook_task(q):
    q.put("Salad is ready!") # Putting the "dish" in the window

if __name__ == "__main__":
    q = Queue()
    p = Process(target=cook_task, args=(q,))
    p.start()
    
    print(q.get()) # Main process picks up the "dish"