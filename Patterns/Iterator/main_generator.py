#------------------------------------------------------------------------------
# Iterator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Iterator Pattern provides a way to access the elements of aggregate
# objects sequentially without exposing its underlying representation.
#
# - An iterable is anything you are able to loop over
# - An iterator is the object that does the actual iterating
# - You can get an iterator from any iterable by calling the built-in iter
#   function on the iterable.
# - You can use the built-in next function on an iterator to get the next
#   item from it, which should raise a StopIteration exception if there are
#   no more items in the iterable.
# - Note that iterators are also iterables, and thier iterator is themselves.
# - Iterators allow you to make an iterable that computes items on the fly,
#   or iterate lazily, meaning they dont determine what the next item is
#   until asked which can save time and memory.
# - Typically Python programmers will create a generator when an iterator
#   is needed rather than implement an iterator the object oriented way.
#   There are 2 ways to make a generator object in Python: a generator
#   function and a generator expression. A "generator object" is an interator
#   whose type is generator. A "generator function" is a definition that
#   returns a generator object when called. A "generator expression" is a
#   comprehension syntax allowing you to create a generator object inline.
#   Generator Functions are distinguished from regular functions by their
#   use of one or more yeild statements. This means a generator object will
#   be returned from the function when called. That generator object can
#   be looped over until a yield statement is hit.
# - While you may encouter iterator classes, theres rarely a need to write
#   your own. Iterable classes however are common. These classes require an
#   __iter__() method which returns an iterator. Since generator functions
#   and expressions are an easy way to make an iterator, they cane be used
#   in and returned from an __iter__() method.
# - Generators are the typical way to make an Iterator in Python, much like
#   dictionaries are the typical way to make a mapping in Python, and
#   functions are the typical way to make a callable object in Python.


import sys
from itertools import repeat, count


class CountIterator:
    """
    A classically object oriented re-implementation of the itertools.count
    iterator. A class can override/implement various interfaces via dunders
    so as to return something tailored to the object. For the iter() and
    next() built-ins to return an iterator for a custom object, that objects
    class definition needs to implement __iter__() to return itself if
    its an iterator, as well as __next__() to return data appropriately
    via the iterator.
    """

    def __init__(self, start=0):
        """
        Initializer to define the number to start counting from
        """
        self.num = start

    def __str__(self):
        return "<My Custom Count Iterator>"

    def __len__(self):
        """
        In Py2k there is no way to represent Infinity as an integer.
        float('inf') also cannot be cast to an integer for return
        In Py3k, math.inf is available and the plain int type is unbounded.
        """
        return sys.maxint

    #------------------------------------------------------------------
    # Implementation of the interface that makes this class an iterator

    def __iter__(self):
        return self

    def next(self):
        """ Py2k """
        num = self.num
        self.num += 1
        return num

    def __next__(self):
        """ Py3k """
        num = self.num
        self.num += 1
        return num


class Point:
    """
    An iterable that provides x-y coordinates.
    When a Point object is created, an iterable is created (not an iterator)
    as it defines an __iter__ method which must return an iterator. An iterator
    is easily defined by a generator function. This allows our Point class to be
    iterated over.
    """
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __iter__(self):
        """
        a generator function that defines and returns a generator object
        """
        yield self.x
        yield self.y


#------------------------------------------------------------------------------
# Client Code


def main():

    """
    an iterable that returns 100 million of the same integer uses 64 Bytes
    """
    many_fours = repeat(4, times=100000000)
    print(sys.getsizeof(many_fours))

    """
    versus an equivalent list of the same integer which uses 800 MB of memory
    """
    list_fours = [4] * 100000000
    print(sys.getsizeof(list_fours))


    """
    save time and memory by only printing out the first line of a
    huge log file by iterating with next on the iterable file object
    This way data is read into memory one line at a time as opposed to
    readlines() which would store all lines in memory, and open the
    door to the possibility of running out of memory if the file is
    large enough.
    """
    print(next(open("email.txt")))

    """
    iterators can also be infinite
    """
    for n in count():
        print(n)
        if n > 50:
            print("Thats enough")
            break

    """
    Using the object oriented re-implementation of itertools.count.
    Various dunders for built-in functions that can be overridden
    by a class definition to provide an implementation meaningful
    to the object. Most standard library objects and data structures
    define these, and a custom class definition can as well.

    """
    numbers = [1, 2, 3]
    print(str(numbers), numbers.__str__())
    print(len(numbers), numbers.__len__())
    print(iter(numbers), numbers.__iter__)

    cnt_iter = CountIterator(10)  # an iterator returns itself.
    print(str(cnt_iter))
    print(len(cnt_iter))
    print(next(cnt_iter))
    print(next(cnt_iter))
    print(next(cnt_iter))

    for n in CountIterator(100):
        print(n)
        if n > 150:
            break

    """
    Python Generator Functions.
    Identified by a yield statement that returns a generator object.

    The itertools.count iterator implemented as a generator function in contrast
    to an object oriented iterator class implementation. Should you need to
    attach extra methods or attributes to your iterator object, using an
    iterator class will likely need to be used.

    Generator functions are akin to for loops that append to a list, where a
    yield statement is used in place of the append method.
    """

    def square_all(numbers):
        for n in numbers:
            yield n**2

    squares = square_all(numbers)
    print(type(squares), squares)
    # (<type 'generator'>, <generator object square_all at 0x7f1127562c80>)

    def count_it(start=0):
        num = start
        while True:
            yield num
            num += 1

    c = count_it(1000)
    print(next(c))
    print(next(c))
    print(next(c))

    for n in count_it():
        print(n)
        if n > 15:
            break


    """
    Python Generator Expressions.
    Similar to list comprehensions, but '()' used instead of '[]'

    While a list comprehensions provides a list, a generator expression provides
    a generator object.

    If you cant write a generator function in comprehension form then you cant
    create a generator expression to replace a generator function definition.
    Generator expressions are more succinct then they are flexible, and best
    used with simple filtering or mapping operations.
    """

    squares = (n**2 for n in numbers)
    print(type(squares), squares)
    #(<type 'generator'>, <generator object <genexpr> at 0x7f1127562cd0>)

    fd = open("email.txt")
    #lines = [line.rstrip('\n') for line in fd if line != '\n']
    lines = (line.rstrip('\n') for line in fd if line != '\n')
    print(type(lines))
    print(next(lines))
    print(next(lines))
    print(next(lines))


    """
    An Iterable Class defines an __iter__ method which returns an iterator.
    The iterator returned is a generator object, implemented in a generator
    function by using the yield statement. Note that an iterable object isn't
    only for data structures that can be looped over, such as a list. Iterable
    objects allow themselves to plug into the pythonic (syntactic) ecosystem.
    """

    p = Point(4, 5)
    x, y = P
    print(x, y)
    list(p)


#------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
