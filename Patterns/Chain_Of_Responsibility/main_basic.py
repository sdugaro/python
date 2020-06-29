#------------------------------------------------------------------------------
# Chain Of Responsibility | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Chain Of Responsibility Pattern avoids coupling the sender of a request
# with a receiver by giving mulitiple objects a change to handle the request.
#
# - The receiving objects are chained by defining a reference to a successor
#   and a common request handler to invoke on each object.
# - Each concrete handler object inherits from a base handler abstract class
#   where the successor link is managed for all derived concrete classes.
# - In each common requst handler method, a conditional check is performed.
#   Should it fail, the request and data is passed to the sucessor via the
#   same handler method defined in the base class.
#

import six
import abc
import random

"""
Note that in Python3.4+ one can simply inherit from abc.ABC as it is a wrapper
for abc.ABCMeta that will implicitly define the metaclass. This is easier to
read and more familiar to statically typed languages. For now we use the six
module to support both Py2k and Py3k -- which would take the keyword argument
metaclass=abc.ABCMeta where one would commonly expect to provide a base class.
"""


@six.add_metaclass(abc.ABCMeta)
class Handler():
    """
    Define an interface for handling requests and implement the successor link
    """

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def _can_handle(self, *args):
        pass

    @abc.abstractmethod
    def handle_request(self, *args):
        pass


class ConcreteHandler1(Handler):
    """
    Implement the handler abstract methods defining how to check if a request
    can be processed and how to handle the request if so. Otherwise forward
    the request onto the successor so long as one has been defined.
    """

    def _can_handle(self, *args):
        return random.choice([True, False])

    def handle_request(self, *args):
        if self._can_handle(*args):
            print("{} from {}".format(' '.join(args), self.__class__.__name__))
        elif self._successor is not None:
            self._successor.handle_request(*args)


class ConcreteHandler2(Handler):
    """
    Implement the handler abstract methods defining how to check if a request
    can be processed and how to handle the request if so. Otherwise forward
    the request onto the successor so long as one has been defined.
    """

    def _can_handle(self, *args):
        return random.choice([False, True])

    def handle_request(self, *args):
        if self._can_handle(*args):
            print("{} from {}".format(' '.join(args), self.__class__.__name__))
        elif self._successor is not None:
            self._successor.handle_request(*args)


#------------------------------------------------------------------------------
# Client Code


def main():
    """ Create the handlers and define their chain sequence """
    concrete_handler_1 = ConcreteHandler1()  # no successor
    concrete_handler_2 = ConcreteHandler2(concrete_handler_1)

    """ Invoke the request for handling """
    concrete_handler_2.handle_request("Hello World")


if __name__ == "__main__":
    main()
