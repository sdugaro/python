import time
import random
import logging
import threading

try:  # Py3k
    import queue
except ImportError:  # Py2k
    import Queue as queue


def producer(q, event):
    """ Producer thread generates and queues data"""
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: {}".format(message))
        q.put(message)

    logging.info("Producer received EXIT event. Exiting.")


def consumer(q, event):
    """ Consumer thread pulls data off the queue and echos it """
    while not event.is_set() or not q.empty():
        message = q.get()
        logging.info("Consumer storing message: {} (queue size={})".format(
            message, q.qsize()))

    logging.info("Consumer received EXIT event. Exiting.")


#------------------------------------------------------------------------------
# Client Code


def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG)

    threads = list()
    pipeline = queue.Queue(maxsize=10)
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
