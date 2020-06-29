"""
The Producer-Consumer Problem is a classic example of a multi-process
synchronization problem (Dijkstra). The problem describes two processes
(the producer and consumer) who share a common fixed size buffer used
as a queue. The producer generates data to put into the buffer iteratively.
Simultaneously, the consumer removes data from the the queue. The problem
is such that the producer should not add data into the buffer if its full,
and the consumer should not remove data from the buffer if it is empty.

Here we have a producer program that needs to read messags from a (fake)
network and writes them to disk. The program listens for and accepts messages
as they come in, typically in bursts. Then we have a consumer program that
takes messages and write them to a (fake) database. In between the producer
and the consumer there will be a Pipeline that will be the part the changes
with respect to differnt synchronization objects.

The Pipeline object manages the 'stop' and 'go' signals between the consumer
and the producer threads such that a producer can set a message in the shared
resource (go) when the consumer is locked (stop), and the consumer can get a
message from a shared resource (go) when the producer is locked (stop). Should
messages be coming in bursts, the Pipeline has to throttle the messages to
hand off one at a time. First the consumer thread Lock is aquired to wait for
a message to be set. Once it is, the producer thread Lock is aquired to wait
for the set message to be recieved. Once it is, more data can be set, and get
interatively via this inter-process communication.

To be able to handle more than one message in the pipeline at a time, we
need a data structure for the pipeline that allows the number of messages
to grow and shrink as incoming data backs up from the producer. We use a
Queue object from Pythons standard libary instead of just a single variable
protected by a Lock. We also use a threading.Event to stop worker threads
instead of a SENTINEL message that the producer thread pushes into the
pipeline (when there is no more data to post) for the consumer thread to
break out of its process loop and end its function.
"""

import time
import random
import logging
import threading

try:  # Py3k
    import queue
except ImportError:  # Py2k
    import Queue as queue
    # Queue.Queue is an old style class which doesnt support many of the
    # features of new style classes such as super. super requires the
    # base class to derive from object and since it does not we need to
    # add it to the inheritance list for our custom Pipeline Queue.


def producer(pipeline, event):
    """ Producer Thread Function
    Pretend we're getting messages from the network and are posting them
    into a pipeline queue for consumption.
    """
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: {}".format(message))
        pipeline.set_message(message, "Producer")

    logging.info("Producer received EXIT event. Exiting.")


def consumer(pipeline, event):
    """ Consumer Thread Function
    Pretend we're saving a number in a database, after popping them off
    a pipeline queue. The consumer worker thread will loop until the
    event (signal to terminate) is set or until the pipeline queue has
    been emptied. If we don't check that the queue is empty before
    terminating we could lose some final messages or worse the producer
    could add messages to a full queue.
    """
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info("Consumer storing message: {} (queue size={})".format(
            message, pipeline.qsize()))

    logging.info("Consumer received EXIT event. Exiting.")


#class Pipeline(queue.Queue, object):
class Pipeline(queue.Queue):
    """
    Class to allow a message pipeline between producer and consumer.
    Represents a data buffer where the producer posts messages, and the
    consumer accepts them.
    """
    def __init__(self):
        """
        When a Queue is initialized with a maxsize, put() operations
        will block until there are fewer than maxsize elements. This means
        we do not need to manage Locks for race conditions in the message
        passing methods which now simply wrap the thread-safe Queue ops.
        """
        #super(Pipeline, self).__init__(maxsize=10)
        queue.Queue.__init__(self, maxsize=10)

    def get_message(self, name):
        logging.debug("{}:about to get message from queue".format(name))
        message = self.get()
        logging.debug("{}:got {} from queue".format(name, message))
        return message

    def set_message(self, message, name):
        logging.debug("{}:about to add {} to queue".format(name, message))
        self.put(message)
        logging.debug("{}:added {} to queue".format(name, message))

#------------------------------------------------------------------------------
# Client Code


def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG)

    threads = list()
    pipeline = Pipeline()
    event = threading.Event()

    t_producer = threading.Thread(target=producer, args=(pipeline, event,))
    t_consumer = threading.Thread(target=consumer, args=(pipeline, event,))

    threads.append(t_producer)
    threads.append(t_consumer)

    t_producer.start()
    t_consumer.start()

    """
    The main thread sleeps momentarily before issuing the exit event
    which causes the producer thread to terminate immediately (exit loop)
    and the consumer thread to exit its loop once the pipe queue is empty.
    """
    time.sleep(0.1)
    logging.info("{:>10}: about to set Event".format("Main"))
    event.set()

    for index, thread in enumerate(threads):
        thread.join()
        logging.info("{:>10}: thread {} done".format("Main", index))


if __name__ == "__main__":
    main()
