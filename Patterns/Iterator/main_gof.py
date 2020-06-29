# https://python-patterns.guide/gang-of-four/iterator/

#------------------------------------------------------------------------------
# Iterator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Iterator Pattern proposes that the detail about how a data structure is
# traversed should be encapsulated by an 'iterator' object that from the
# outside, simply yeilds one item after another without exposing the internals
# of how the data structure is designed.
#
# - Python supports the Iterator Pattern at the most fundamental level available
#   to a programming language, so it is built into Pythons syntax.
# - The least expressive computer languages make no attempt to hide the inner
#   workings of their data structures, which means you have to generate the
#   integer indexes yourself. This interrupts the flow of programmer thought
#   with low-level data structure details. When code cant abstract away the
#   mechanics of iteration, it becomes more difficult to read and error prone.
# - Pythons for loop abstracts the Iterator Pattern so thoroughly that most
#   Python programmers are never even aware of the object design pattern it
#   enacts beneath the surface. The for loop performs repeated assignment,
#   running its indented block of code once for each item in the sequence its
#   iterating over. It is so concise and expressive that Python's
#   'comprehensions' evolved to create inline loops.
# - The traditional iterator pattern involves three objects: the container,
#   the containers internal logic which organizes items for traversal, and a
#   generic iterator object providing sequential access to the items. The
#   generic iterator should implement the same interface as all other iterators
#   rather than invent its own method calls for stepping through its items.
#   This ensures uniformity across iterators in the language so the programmer
#   does not need to learn a different api for each container.
# - Python provides a pair of builtins for iteration: iter() which takes a
#   container object as its argument and asks it to build and return a new
#   iterator object, where a TypeError will be raised if the argument isn't an
#   iterable container. next() which takes the iterator as its argument and
#   returns the next item from the container each time its called, raising a
#   StopIteration exception when there are no more objects to return.
# - The benefit of having the iterator as a separate object from the container
#   (as opposed to being managed by the container) is that multiple loops over
#   container can be performed at the same time. Its simply a pointer to
#   container data at any given point in time. This avoids concentric/nested
#   loops and supports multiple threads of control.
# - Python extends the traditional iterator pattern in that Python iterators
#   return themselves if passed to iter(); meaning iterators themselves can be
#   passed to for loops. This allows programs to switch between manual and
#   automatic iteration.
# - Python relegates its actual iteration object protocol to a pair of dunder
#   methods __iter__ and __next__. A class can plug into Pythons native
#   iteration mechansisms by implementing these. The container must offer
#   __iter__() that returns an iterator; making the container an 'iterable'.
#   Each iterator must offer a __next__() method to return the next item in
#   the container each time next() is called and raise StopIteration when there
#   are no further items. The iterator's __iter__() method should be able to
#   return itself. There is no requirement that the items returned by next be
#   stored or even exist until __next__() is called so storage in the container
#   may not be needed.
#


def parse_email(f):

    for line in f:
        envelope = line
        break

    headers = {}
    for line in f:
        if line == '\n':
            break
        name, value = line.split(':', 1)
        headers[name.strip()] = value.lstrip().rstrip('\n')

    body = []
    for line in f:
        if line.startswith('From'):
            break
        body.append(line)

    return envelope, headers, body


def parse_email_file(f):

    lines = list(f)
    it = iter(lines)

    for line in it:
        envelope = line
        break

    headers = {}
    for line in it:
        if line == '\n':
            break
        name, value = line.split(':', 1)
        headers[name.strip()] = value.lstrip().rstrip('\n')

    body = []
    for line in it:
        if line.startswith('From'):
            break
        body.append(line)

    return envelope, headers, body

#------------------------------------------------------------------------------
# Implementing and Iterable and an Iterator.
# Classes can implement the Iterator Pattern can plug into Pythons native
# iteration mechanisms for, iter() and next().


class OddNumbers(object):
    """
    An Iterable Object Implementation.
    A class/container that defines the __iter__ method which returns an
    iterator object makes the class/container an iterable.
    """

    def __init__(self, maximum):
        self.maximum = maximum

    def __iter__(self):
        return OddIterator(self)


class OddIterator(object):
    """
    An iterator implementation for the corresponsing iterable.
    The iterator must define next()/__next__() to return the next item from
    the container and raise the StopIteration exception when there is no next
    item to return. In the event that a user passes an iterator to a for loop
    instead of the underlying container, the iterator should also return an
    __iter__() method that simply returns itself.

    """

    def __init__(self, container):
        self.container = container
        self.n = -1

    def next(self):
        """ Py2k """
        self.n += 2
        if self.n > self.container.maximum:
            raise StopIteration
        return self.n

    def __next__(self):
        """ Py3k """
        self.n += 2
        if self.n > self.container.maximum:
            raise StopIteration
        return self.n

    def __iter__(self):
        return self


#------------------------------------------------------------------------------


def main():


    """
    A for loop is a repeated assigned statement, so it has the same flexibility
    as Pythons normal assignment operator in that you can upgrade from assigning
    a single name to unpacking a whole tuple, skipping a separate unpacking step
    """
    elements = [('H', 1.008), ('He', 4.003), ('Li', 6.94)]
    for tup in elements:
        symbol, weight = tup
        print(symbol, weight)

    # unpack in the for statement rather than iterating over tuples
    for symbol, weight in elements:
        print(symbol, weight)


    """
    A for loop can be coupled with a Python dictionary's item() method to easily
    visit each dictionary key and value withouth the expense of a key lookup at
    the top of each loop.
    """
    d = {'H': 1.008, 'He': 4.003, 'Li': 6.94}

    for symbol in d.keys():
        weight = d[symbol]
        print(symbol, weight)

    # unpack dictionary items in the for statement rather than dictionary access
    for symbol, weight in d.items():
        print(symbol, weight)

    [symbol for symbol, weight in d.items() if weight > 5]
    {symbol for symbol, weight in d.items() if weight > 5}
    {symbol: weight for symbol, weight in d.items() if weight > 5}
    list(symbol for symbol, weight in d.items() if weight > 5)

    """
    Using Pythons builtin iter() and next().
    Python iterators can be used in loops for manual or automatic control.
    They can be used to iterate over the underlying list in a file such that
    multiple loops can process the file without having to open it multiple
    times or have the file descriptor read from where it was last.
    """
    some_primes = [2, 3, 5, 7, 11, 13, 17, 19]

    it = iter(some_primes)
    while True:
        try:
            prime = next(it)
        except StopIteration:
            print("Prime List Exhausted")
            break
        else:
            print(prime)


    it = iter(some_primes)
    print(next(it))
    for prime in it:
        print(prime)
        break
    print(next(it))


    with open('email.txt') as f:
        #envelope, headers, body = parse_email(f)
        lines = list(f)

    it = iter(lines)
    envelope, headers, body = parse_email(it)
    print(headers['To'])
    print(len(body), 'lines')

    f = open('email.txt')
    envelope, headers, body = parse_email_file(f)
    print(headers['To'])
    print(len(body), 'lines')


    """
    By implementing __iter__ in the iterable container class as well as
    __iter__ and __next__ in the containers iterator class, the container can
    participate in Python's rich iteration ecosystem: for loops, iter()/next(),
    as well as comprehensions.
    """

    numbers = OddNumbers(7)
    for n in numbers:
        print(n)

    it = iter(OddNumbers(5))
    print(next(it))
    print(next(it))

    # iterate over the entire iterable into a list
    print(list(numbers))

    # iterate over the entire iterable using comprehension syntax
    print(set(n for n in numbers if n > 4))


#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
