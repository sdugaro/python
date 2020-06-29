
import logging
import threading
import time

"""
Race conditions can occur when two or more threads access a shared piece of
data or resource.

Here we write a class that updates a (fake) database. The database stores
a single number: 'value' which is the shared data on which we will see a
race condition. An update is meant to get 'value' from the database, do
some computation with it (add 1 and sleep), and then write the result back
to the database's value.

Each thread will have their own 'local_copy' of the database value while
doing some compute and writing the data back. In the time that thread one
is spun up and doing its compute, thread two spins up to read the same
initial value from the database as thread 1. Since an 'update' increments
the value by 1, each thread will increment from zero to one and not account
for the fact that two update operations occurred.

The standard library provides some primitives to prevent race conditions
from happening.

"""

class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info("{:>10}: starting".format("Thread " + str(name)))
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
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
        x = threading.Thread(target=database.update, args=(index,))
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
