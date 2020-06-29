
import logging
import threading
import time

"""
Example of creating multiple threads using a ThreadPoolExecutor.

This is an easier way to start up a group of threads than threading_multi.py

* Requires Python3.2+ for concurrent.futures *

"""

import concurrent.futures


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
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")


    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))


if __name__ == "__main__":
    main()
