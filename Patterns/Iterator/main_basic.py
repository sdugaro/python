#------------------------------------------------------------------------------
# Iterator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Iterator Pattern provides a way to access the elements of aggregate
# objects sequentially without exposing its underlying representation.
#
# - An iterable is anything that can be looped over.
# - An iterator is the object that does the actual iterating.
# - You can get an iterator from any iterable by calling the built-in iter
#   function on the iterable.
# - You can use the built-in next function on an iterator to get the next
#   item from it, which should raise a StopIteration exception if there are
#   no more items in the iterable.

try:  # Py3k
    from collections.abc import Iterable, Iterator
except ImportError:  # Py2k
    from collections import Iterable, Iterator


class ConcreteIterable(Iterable):
    """
    Implement the iterable containerIterator creation interface to return an instance of
    the proper ConcreteIterator.
    """

    def __init__(self):
        self._data = ["Hello", "World", "How", "Are", "You?"]

    def __iter__(self):
        return ConcreteIterator(self)


class ConcreteIterator(Iterator):
    """
    Implement the Iterator interface.
    """

    def __init__(self, concrete_iterable):
        self._iterable = concrete_iterable
        self._index = 0

    def __next__(self):
        """ Py3k """
        try:
            data = self._iterable._data[self._index]
            self._index += 1
            return data
        except IndexError:
            raise StopIteration

    def next(self):
        """ Py2k """
        try:
            data = self._iterable._data[self._index]
            self._index += 1
            return data
        except IndexError:
            raise StopIteration

#------------------------------------------------------------------------------
# Client Code


def main():
    container = ConcreteIterable()
    for data in container:
        print(data)
    print("\n")

    it = ConcreteIterator(container)
    print("{} {}!".format(next(it), next(it)))


if __name__ == "__main__":
    main()
