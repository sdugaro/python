"""
There are a number of ways to avoid or solve race conditions.

The Producer-Consumer Problem is a classic example of a multi-process
synchronization problem (Dijkstra). The problem describes two processes
(the producer and consumer) who share a common fixed size buffer used
as a queue. The producer generates data to put into the buffer iteratively.
Simultaneously, the consumer removes data from the the queue. The problem
is such that the producer should not add data into the buffer if its full,
and the consumer should not remove data from the buffer if it is empty.

The solution is for the producer to go to sleep if the buffer is full, and
wait for the consumer to notify the producer when it removes data so the
producer can start to full the buffer again. Conversely, if the buffer is
empty, the consumer goes to sleep and is notified by the producer when
it puts data into the buffer so the consumer can again empty the buffer.
This encapsulates the idea of inter-process communication, typically
using semaphores, where an inadequate solution can result in deadlock,
where both processes are waiting to be awakened. A semaphore is a variable
used to control access to a common resource shared by multiple processes
in a concurrent system.

Here we have a producer program that needs to read messags from a (fake)
network and writes them to disk. The program listens for and accepts messages
as they come in, typically in bursts. Then we have a consumer program that
takes messages and write them to a (fake) database. In between the producer
and the consumer there will be a Pipeline that will be the part the changes
with respect to differnt synchronization objects.

By definition, a Sentinel is a kind of 'observer' or guard. In this context,
a Sentinel provides semaphore isolation via flow control over concurrent
threads. It is implemented with here with Pythons Lock primitive.

Note that this implementation does not solve the producer-consumer problem
in general because it only allows a single value into the pipeline at a
a time. This means when the producer gets a burst of messages it will have
nowhere to put them and will have to wait before continuing. Throttling the
incoming bursts of data to only let one trickle in at a time can create a
backlog and unnecessary latency.

"""

import random
import logging
import threading

SENTINEL = object()


def producer(pipeline):
    """ Producer Thread Function
    Pretend we're getting messages from the network, and feed those
    into a pipeline (buffer). For illustration, a message is generated
    as a random number, which is added to a buffer for consumption,
    and when the burst of messages is complete, a sentinel is sent
    into the pipeline to signal that consumption should stop.
    """
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: {}".format(message))
        pipeline.set_message(message, "Producer")

    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL, "Producer")


def consumer(pipeline):
    """ Consumer Thread Function
    Pretend we're saving a number in a database, after reading messages
    from the pipeline (buffer). For illustration the number is just
    echoed to the shell. Should we encounter a sentinel message that
    signals us to stop and terminate the thread (go to sleep).
    """
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: {}".format(message))


class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer.
    Represents a data buffer where the producer posts messages, and the
    consumer accepts them.
    """
    def __init__(self):
        """
        message: the shared rsource storing the message to pass
        producer_lock: restricts access to the message by the producer thread
        consumer_lock: restricts access to the message by the consumer thread

        When a pipeline object is instantiated, the consumer Lock is aquired.
        This is the appropriate starting state: allow the producer thread to
        add a new message, while the consumer thread waits until a message is
        present. Once a thread is aquired, subsequent attempts to aquire it
        block.
        """
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()  # set a 'stop light' for the consumer

    def get_message(self, name):
        """
        The consumer calls this to call aquire on the .consumer_lock in order
        to make the consumer wait until a message is ready. Once the consumer
        has aquired the lock, copy the value from .message locally and then
        release the .producer_lock to allow the producer to insert the next
        message into the pipeline (buffer). Once the consumer releases() the
        .producer_lock via get_message() the producer is able to set the
        message and change the value of the shared resource (the message
        value). This is why it is important to store a local copy before
        releasing the lock and return the value of the local copy of the
        shared resource (pre .producer_lock.release). Simply returning the
        value of self.message could create a race condition in the time
        between releasing the producer_lock (which permits the producer
        thread to set the message) and returning the value of the shared
        resource (self.message).
        """
        logging.debug("{}:about to acquire getlock".format(name))
        self.consumer_lock.acquire()
        logging.debug("{}:have getlock".format(name))
        message = self.message
        logging.debug("{}:about to release setlock".format(name))
        self.producer_lock.release()
        logging.debug("{}:setlock released".format(name))
        return message

    def set_message(self, message, name):
        """
        The flip side of the transaction. The procuder calls this with some
        message to set once it aquires the .producer_lock. Once it has set
        the message into the shared resource (self.message) the .consumer_lock
        is released to allow the consumer to read the value. In short, data is
        only set by this pipeline on behalf of the producer once a 'green light'
        has been given by the consumer via get_message (or by this pipeline
        on initialization) via the aquired consumer_lock. Effectively this
        states that 'the consumer will wait and not get any messages so that
        the producer can set the buffer data without a race condition'.
        """
        logging.debug("{}:about to acquire setlock".format(name))
        self.producer_lock.acquire()
        logging.debug("{}:have setlock".format(name))
        self.message = message
        logging.debug("{}:about to release getlock".format(name))
        self.consumer_lock.release()
        logging.debug("{}:getlock released".format(name))

#------------------------------------------------------------------------------
# Client Code


def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    threads = list()
    pipeline = Pipeline()
    t_producer = threading.Thread(target=producer, args=(pipeline,))
    t_consumer = threading.Thread(target=consumer, args=(pipeline,))

    threads.append(t_producer)
    threads.append(t_consumer)

    t_producer.start()
    t_consumer.start()

    for index, thread in enumerate(threads):
        thread.join()
        logging.info("{:>10}: thread {} done".format("Main", index))


if __name__ == "__main__":
    main()
