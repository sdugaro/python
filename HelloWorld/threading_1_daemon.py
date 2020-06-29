
import logging
import threading
import time

"""
In computer science, a daemon is a process that runs in the background.
In Pythons threading it has a more specific meaning: A daemon thread will shut
down immediately when the program exists. In other words, a daemon thread is a
process that runs in the background that shuts down automatically.

If a program is running Threads that are not daemons, then the program will wait
for those threads to complete before it terminates. Threads that are daemons
are just killed wherever they are in their compute when the program is exiting.

A Thread object is instantiated with the function to be run and an argument list
to be passed to that function when the thread is started.

Our thread function peels one argument off the argument list provided
and uses that as they name by which it is identified. Doing some compute is
earmarked with a proxy sleep method.

The Main thread

"""


def thread_function(name):
    logging.info("Thread {}: starting".format(name))
    time.sleep(2)
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
    #Py3K
    #x = threading.Thread(target=thread_function, args=(1,), daemon=True)
    #Py2K
    x = threading.Thread(target=thread_function, args=(1,))
    x.daemon = True

    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : thread started")
    # x.join()
    logging.info("Main    : I'm done; killing daemon thread")
    print(x)


if __name__ == "__main__":
    main()
