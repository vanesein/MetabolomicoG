#import threading
#import time
#
#exitFlag = 0
#
#class myThread (threading.Thread):
#    def __init__(self, threadID, name, counter):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#        self.name = name
#        self.counter = counter
#    def run(self):
#        print ("Starting " + self.name)
#        print_time(self.name, self.counter, 5)
#        print ("Exiting " + self.name)
#
#def print_time(threadName, delay, counter):
#    while counter:
#        if exitFlag:
#            threadName.exit()
#        time.sleep(delay)
#        print ("%s: %s" % (threadName, time.ctime(time.time())))
#        counter -= 1
#
## Create new threads
#thread1 = myThread(1, "Thread-1", 1)
#thread2 = myThread(2, "Thread-2", 2)
#
## Start new Threads
#thread1.start()
#thread2.start()
#thread1.join()
#thread2.join()
#print ("Exiting Main Thread")

###from multiprocessing.dummy import Pool as ThreadPool
###
###def squareNumber(n):
###    return n ** 2
###
#### function to be mapped over
###def calculateParallel(numbers, threads=4):
###    pool = ThreadPool(threads)
###    results = pool.map(squareNumber, numbers)
###    pool.close()
###    pool.join()
###    return results
###
###if __name__ == "__main__":
###    numbers = [1, 2, 3, 4, 5]
###    squaredNumbers = calculateParallel(numbers, 8)
###    for n in squaredNumbers:
###        print(n)


import threading
from queue import Queue
import time

# lock to serialize console output
lock = threading.Lock()

def do_work(a, b, c):
    #time.sleep(.1) # pretend to do some lengthy work.
    # Make sure the whole print completes or threads can mix up output in one line.
    with lock:
        print(threading.current_thread().name,a,b,c)

# The worker thread pulls an item from the queue and processes it
def worker(a):
    while True:
        items = q.get()
        do_work(items[0], items[1], items[2])
        q.task_done()

# Create the queue and thread pool.
q = Queue()
for i in range(4):
     t = threading.Thread(target=worker, args=(q,))
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()

# stuff work items on the queue (in this case, just a number).
start = time.perf_counter()
for item in range(20):
    q.put((item, item+1, item+5))

q.join()       # block until all tasks are done

# "Work" took .1 seconds per task.
# 20 tasks serially would be 2 seconds.
# With 4 threads should be about .5 seconds (contrived because non-CPU intensive "work")
print('time:',time.perf_counter() - start)