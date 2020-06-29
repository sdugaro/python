#------------------------------------------------------------------------------
# Observer | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Observer Pattern lets you define a subscription mechanism to notify
# multiple objects about events that happen to the object being observed.
#
# - Objects are represented as observers that wait for an event to trigger.
# - An observer attaches to the subject once the specified event occurs.
# - When the event occurs the subject notifies the observers of the event.
# - This example is a threaded example where there is a producer thread
#   that obtains some data over time and when its ready, notifies other
#   worker threads to have at it (read only)
# - One can use threads by instantiating the Thread class in the threading
#   module, or create a custom thread by subclassing from Thread and
#   implementing the run() method to specify the work done in the thread.
# - Thread.start() must be called at most once per thread object. It
#   arranges for the object's run() method to be invoked in a separate
#   thread of control. Once a thread has been started, it is considered
#   alive and stops being alive when its run() method terminates either
#   normally by completing the block or by raising an unhandled exception.

import time
import logging
import threading

format = '%(asctime)s: (%(threadName)-9s) %(message)s'
logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")


class Downloader(threading.Thread):
    """
    Producer thread that retrieves data, cues it up, and when its done,
    notifies all other worker threads the data is ready so they can do
    something with it.
    """

    def __init__(self):
        """
        Lock is initialized in an unlocked state, then locked and
        released via the with statement.
        """
        self.data = []
        super(Downloader, self).__init__(name="Producer Thread")


    def run(self):
        logging.info('Downloading...')
        for i in range(1, 5):
            self.data.append(i)
            logging.info(self.data)
            time.sleep(2)

        logging.info('Done')


class Worker(threading.Thread):

    def __init__(self, name, subject):
        self.subject = subject
        super(Worker, self).__init__(name=name)

    def run(self):
        """
        By joining the Producer thread, Worker threads effectively
        subscribe to waiting until the Producer thread is finished
        doing its work. When it completes, all worker threads begin
        running in parallel to do something with the data that has
        been made available.
        """
        self.subject.join()

        for item in self.subject.data:
            logging.info(item)
            time.sleep(1)

        logging.info('Done')


#------------------------------------------------------------------------------
# Client Code


def main():

    """
    A producer thread beings downloading some data as soon as it is started,
    but it could take a minute. So this thread needs to block all other worker
    threads (observers) that are interested in the data until it is ready to
    be consumed.
    """
    p = Downloader()
    p.start()

    """
    Worker threads cue up, and are ready to run their logic on the data once
    the producer thread has finished its work.
    """
    t1 = Worker("Worker Thread 1", p)
    t1.start()

    t2 = Worker("Worker Thread 2", p)
    t2.start()

    t3 = Worker("Worker Thread 3", p)
    t3.start()


if __name__ == "__main__":
    main()
