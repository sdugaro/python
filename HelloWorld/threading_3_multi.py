
import logging
import threading
import time

"""
Example of creating multiple threads akin to a single thread.

A Thread object is instantiated with the function to be run and an argument list
to be passed to that function when the thread is started.

The program keeps a list of Thread objects so that it can wait for them later
using join(). Notice that multiple runs will produce different orderings. The
order in which threads are run is determined by the operating system and can be
hard to predict.

"""


def thread_function(name):
    logging.info("Thread {}: starting".format(name))
    for i in range(5):
        print(5 - i)
        time.sleep(1)
    logging.info("Thread {}: finished".format(name))


#------------------------------------------------------------------------------
# Client Code

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    threads = list()
    for index in range(3):
        logging.info("Main    : create and start thread {}.".format(index))
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread {}.".format(index))
        thread.join()
        logging.info("Main    : thread %d done", index)


if __name__ == "__main__":
    main()
