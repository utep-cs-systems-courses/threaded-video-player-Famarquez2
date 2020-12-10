import queue
from threading import Lock, Semaphore

class ThreadyQueue:
    def __init__(self, maxcount):
        self.base_q = queue.Queue()
        self.lock = Lock()
        self.empty = Semaphore(10)  # Allow ten frames at a time 
        self.not_empty = Semaphore(0)  # 
    
    def put(self, item):
        self.empty.acquire()
        self.lock.acquire()
        self.base_q.put(item)  # Makes sure that only one thread accesses the queue.
        self.lock.release()
        self.not_empty.release()

    def get(self):
        self.not_empty.acquire()
        self.lock.acquire()
        item = self.base_q.get()  # Deletes the first element of the list, transfers it into varibale.
        self.lock.release()
        self.empty.release()
        
        return item
