"""
A Barrier primitive can be used to keep a fixed number of threads in sync.
When creating a Barrier, the caller must specify how many threads will be
synchonizing on it. Each thread tries to pass a Barrier by calling the wait()
method which will block until all of the threads have made that call. As soon
as that happens, all the threads are released 'simultaneously'.
"""

import time
import random
import logging
import threading
from datetime import datetime

format = '%(asctime)s: (%(threadName)-9s) %(message)s'
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

PLAYERS = ["Lemieux", "Crosby", "Kessel", "Malkin", "Letang"]


def skate(barrier, players):
    barrier.wait()
    name = players.pop()
    time.sleep(random.randrange(2, 5))
    current_time = datetime.now().strftime("%H:%M:%S.%f")
    logging.debug("%s reached the finish line at: %s", name, current_time)


class Barrier:
    """
    In Py2k there is no threading.Barrier, so we implement our own
    N process Barrier using semaphores with the same interface.
    """
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.lock = threading.Semaphore(1)
        self.barrier = threading.Semaphore(0)

    def wait(self):
        """
        """
        self.lock.acquire()
        self.count += 1
        self.lock.release()
        if self.count == self.n:
            self.barrier.release()
        self.barrier.acquire()
        self.barrier.release()

#------------------------------------------------------------------------------
# Client Code


def main():

    threads = []
    try:  # Py3k
        barrier = threading.Barrier(len(PLAYERS))
    except AttributeError:  # not in Py2K, use our own
        barrier = Barrier(len(PLAYERS))

    logging.info("Skaters take your mark...")

    for i in range(len(PLAYERS)):
        threads.append(threading.Thread(target=skate, args=(barrier, PLAYERS)))
        logging.debug("Get set %s", PLAYERS[i])
        threads[-1].start()

    logging.debug("Go!")

    """ Block the Main thread until all threads finish """

    for thread in threads:
        thread.join()

    logging.debug('All skaters have crossed the finish line.')


if __name__ == '__main__':
    main()


