"""
There are a number of ways to avoid or solve race conditions.

One way is to use a Python Lock to do some basic synchronization.
This allows only one thread at a time into the read-modify-write section
of the code, or the database value update per thread. In other languages
this is referred to as a mutex (MUTual EXclusion) which is what a Python
Lock does.

a Lock is an object that acts like a hall pass. Only one thread at a time
can have the Lock. Any other thread that wants the Lock must wait until the
owner of the Lock returns. The functions to do with are .acquire(the Lock)
and .release(the Lock). A Thread will call my_lock.aquire() to get the lock,
and if the lock is already held, a calling thread will wait until it is
released. Note that if one thread gets a Lock but never releases it, the
program will be stuck in something known as 'Deadlock'.

Pythons Lock also operas as a context manager, which means it can be used
in with statement, which will release it automatically when the with block
exits for any reason.

"""

import logging
import threading
import time

logging.getLogger().setLevel(logging.DEBUG)


class FakeDatabase:
    def __init__(self):
        """
        _lock is initialized in the unlocked state, then locked and released
        via the with statement. The thread that is running in the with context
        block will hold onto the Lock until it is finished updating the database. 
        This ensures all threads increment the database value sequentially.
        """
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("{:>10}: starting".format("Thread " + str(name)))
        logging.debug("{:>10}: about to lock".format("Thread " + str(name)))
        with self._lock:
            logging.debug("{:>10}: has the lock".format("Thread " + str(name)))
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("{:>10}: releasing the lock".format("Thread " + str(name)))

        logging.info("{:>10}: finished update".format("Thread " + str(name)))


#------------------------------------------------------------------------------
# Client Code

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    database = FakeDatabase()
    logging.info("Starting value is [{}].".format(database.value))

    # spin up two threads
    for index in range(2):
        logging.info("{:>10}: create and start thread {}.".format("Main", index))
        x = threading.Thread(target=database.locked_update, args=(index,))
        threads.append(x)
        x.start()

    # echo the computed update to the database
    logging.info("Ending value is [{}]".format(database.value))

    for index, thread in enumerate(threads):
        thread.join()
        logging.info("{:>10}: thread {} done".format("Main", index))
        logging.info("{:>10}: ending value is [{}]".format("Main", database.value))


if __name__ == "__main__":
    main()
