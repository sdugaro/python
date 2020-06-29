"""
A Timer is a way to schedule a function to be called after a certain amount
of time has passed. A timer starts its work after a delay and can be cancelled
at any point within that delay time period.

Timers are started, as with all threads, by calling their start() method.
The timer can be stopped before its action has begun by calling cancel().
"""

import time
import threading
import logging

format = '%(asctime)s: (%(threadName)-9s) %(message)s'
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")


def f():
    logging.debug('thread function running')
    return

#------------------------------------------------------------------------------
# Client Code


def main():

    t1 = threading.Timer(5, f)
    t1.setName('Timer Thread 1')
    t2 = threading.Timer(5, f)
    t2.setName('Timer Thread 2')

    logging.debug('starting timers...')
    t1.start()
    t2.start()

    logging.debug('waiting before canceling "%s"', t2.getName())
    time.sleep(2)

    logging.debug('canceling "%s"', t2.getName())
    print('before t2.cancel(). t2.is_alive() = {}'.format(t2.is_alive()))
    t2.cancel()
    time.sleep(2)
    print('after t2.cancel(). t2.is_alive() = {}'.format(t2.is_alive()))


    """
    Block the Main thread until the thread(s) whose join() method
    is called terminates normally, through an unhandled exception,
    or until the optional timeout provided to the join method
    """

    t1.join()
    t2.join()

    logging.debug('done')


if __name__ == '__main__':
    main()


