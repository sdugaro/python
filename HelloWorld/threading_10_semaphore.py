"""
A semaphore is one of the oldest synchronization primitives in the history
of computer science (Dijkstra); essentially a counter with certain properties
1. counting is atomic: there is a guarantee the os will not swap out
   a thread in the middle of incrementing or decrementing the counter.
   The internal counter is incremented when you call .release() and
   decremented when you call .acquire()
2. if a thread calls .acquire() when the counter is zero the thread will
   block until a different thread calls .release() at which point the
   counter increments to one.

A semaphore is a more advanced lock mechanism than a Lock, as it maintains
a counter rather than a lock flag, and it only blocks if more than a given
number of threads have attempted to hold the semaphore. Depending on how
the semaphore is initialized, multiple threads can access the same code
section simultaneously.

There are many cases we may want to allow more than one worker access to a
resource while still limiting the overall number of accesses. We might want
to use a semaphore in a situation where we need to support concurrent
connections/downloads or guard resources with limited capacity such as
a database server.

Here we create a ThreadPool class that tracks which threads are able to run
at any given moment. It simply holds the names of the active threads to show
that only the number of threads the Semaphore is initialized with will be
run concurrently. A real resource pool would allocate a connection or some
other value to the newly active thread.


https://greenteapress.com/wp/semaphores/

"""

import threading
import time
import logging

format = '%(asctime)s: (%(threadName)-9s) %(message)s'
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")


class ThreadPool(object):

    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)


def f(semaphore, pool):
    logging.debug('Waiting to join the pool')
    with semaphore:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        time.sleep(0.5)
        pool.makeInactive(name)

#------------------------------------------------------------------------------
# Client Code


def main():

    MAX_THREADS = 3
    pool = ThreadPool()
    s = threading.Semaphore(MAX_THREADS)

    for i in range(10):
        t = threading.Thread(target=f, name='thread_' + str(i), args=(s, pool))
        t.start()


if __name__ == '__main__':
    main()


