#------------------------------------------------------------------------------
# Iterator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Iterator Pattern allows sequential traversal through a complex data
# structure without exposing its internal details.
#
# - Common in Python Code; many frameworks and libraries use it to provide a
#   standard way to traverse their collections as client code might not have
#   direct access to the collections being traversed.
# - The pattern is recognizable by its naviation methods (next, previous, iter)

try:  # Py3k
    from collections.abc import Iterable, Iterator
except ImportError:  # Py2k
    from collections import Iterable, Iterator


"""
To create an iterator in Python, there are two abstract classes from the built-
in `collections` module - Iterable,Iterator. We need to implement the
`__iter__()` method in the iterated object (collection), and the `__next__ ()`
method in theiterator.
"""


class AlphabeticalOrderIterator(Iterator):
    """
    Concrete Iterators implement various traversal algorithms. These classes
    store the current traversal position at all times.
    """

    """
    `_position` attribute stores the current traversal position. An iterator may
    have a lot of other fields for storing iteration state, especially when it
    is supposed to work with a particular kind of collection.
    """
    _position = None

    """
    This attribute indicates the traversal direction.
    """
    _reverse = False

    def __init__(self, collection, reverse=False):
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """ Py3k
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value

    def next(self):
        """ Py2k
        The __next__() method must return the next item in the sequence. On
        reaching the end, and in subsequent calls, it must raise StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class WordsCollection(Iterable):
    """
    Concrete Collections provide one or several methods for retrieving fresh
    iterator instances, compatible with the collection class.
    """

    def __init__(self, collection=[]):
        self._collection = collection

    def __iter__(self):
        """
        The __iter__() method returns the iterator object itself, by default we
        return the iterator in ascending order.
        """
        return AlphabeticalOrderIterator(self._collection)

    def get_reverse_iterator(self):
        return AlphabeticalOrderIterator(self._collection, True)

    def add_item(self, item):
        self._collection.append(item)


#------------------------------------------------------------------------------
# Client Code

def main():

    # The client code may or may not know about the Concrete Iterator or
    # Collection classes, depending on the level of indirection you want to keep
    # in your program.
    collection = WordsCollection()
    collection.add_item("First")
    collection.add_item("Second")
    collection.add_item("Third")

    print("Straight traversal:")
    print("\n".join(collection))
    print("")

    print("Reverse traversal:")
    print("\n".join(collection.get_reverse_iterator()))


if __name__ == "__main__":
    main()
