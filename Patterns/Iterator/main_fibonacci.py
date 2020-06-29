#------------------------------------------------------------------------------
# Iterator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Iterator Pattern helps access the elements of a collection/class in
# sequential order without understanding the underlying class design.
#
# - In python, a generator object is a type of construct that can be iterated
#   over such as in a loop. A generator function is a function that returns such
#   an object (aka an iterator). Iterators can and often are infinite in nature
#   in that there will always be something 'next' that can be computed.
# - Pythons yeild statement is what distinguishes a typical function definition
#   from a generator function. The yeild statement returns a generator object
#   holding the data for the current iteration. The yeild statement permits one
#   to be memory efficient as only the data for the current iteration needs to
#   be provided -- as opposed to indexing into an entire data source. Following
#   the yeild statement some work can be done to compute what's yeilded next.
# - The fibonacci sequence is a classical use case of a generator as it is an
#   infinite sequence of integers. Conceptually simple as the next integer in
#   the sequence is simply the sum of the last two integers in the sequence.
# - While the codification is also simple, its important to note that computing
#   these integers toward infinity can hit integer overflow and memory limits,
#   so a means of exiting is needed, and provided by the python interpreter.


import time


def fibonacci():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b


#------------------------------------------------------------------------------
# Client Code

def main():

    g = fibonacci()

    try:
        for e in g:
            print(e)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Calculation stopped")


if __name__ == "__main__":
    main()
