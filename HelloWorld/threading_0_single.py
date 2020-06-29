
import logging
import threading
import time

"""
Example of creating a single thread, starting it, and waiting for it to finish.

A Thread object is instantiated with the function to be run and an argument list
to be passed to that function when the thread is started.

Our thread function peels one argument off the argument list provided
and uses that as they name by which it is identified. Doing some compute is
earmarked with a proxy sleep method.

The Main thread completes its task, and waits for the thread to finish its
work before ending the program.

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
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : thread started")
    # x.join()
    logging.info("Main    : I'm done; waiting for thread to finish.")
    print(x)


if __name__ == "__main__":
    main()
