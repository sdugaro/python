#------------------------------------------------------------------------------
# Chain Of Responsibility | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Chain Of Responsibility Pattern lets you pass requests along a chain of
# handlers. Upon recieving a request, each handler decides whether to process
# the requst of ignore it, passing it to the next handler in the chain.
#
#
# - A handler is defined in its own class with a single check method. All
#   handlers implement this method and call it along with with requests and any
#   data as arguments.
# - Handlers are linked by storing a reference to the next handler in the chain
#   where if a handler does not process a request they use the reference and the
#   incoming data in their own check method to pass the handling down the line.
# - Handlers could absorb the request and choose not to pass on the request
#   forward, or always pass it forward such that all handlers have an
#   opportunity to process the request in their own way.
# - Due to the dynamic nature of the chain, the client should be prepared to
#   handle various common scenarios:
#   1) the chain consists of a single link.
#   2) Some requests may not reach the end of the chain.
#   3) Some requests may reach the end of the chain unhandled.
#

import six
from abc import ABCMeta, abstractmethod


#------------------------------------------------------------------------------
# Abstract Base Classes


@six.add_metaclass(ABCMeta)
class Handler():
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented in a base handler class.
    """

    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


#------------------------------------------------------------------------------
# Concrete Handler Implementations


class MonkeyHandler(AbstractHandler):
    def handle(self, request):
        if request == "Banana":
            return "Monkey: I'll eat the {}".format(request)
        else:
            return super(MonkeyHandler, self).handle(request)


class SquirrelHandler(AbstractHandler):
    def handle(self, request):
        if request == "Nut":
            return "Squirrel: I'll eat the {}".format(request)
        else:
            return super(SquirrelHandler, self).handle(request)


class DogHandler(AbstractHandler):
    def handle(self, request):
        if request == "MeatBall":
            return "Dog: I'll eat the {}".format(request)
        else:
            return super(DogHandler, self).handle(request)


#------------------------------------------------------------------------------
# Client Code

def client_code(handler):
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """

    for food in ["Nut", "Banana", "Cup of coffee"]:
        print("\nClient: Who wants a {}?".format(food))

        result = handler.handle(food)

        if result:
            print("\t{}".format(result))
        else:
            print("\t{} was left untouched.".format(food))


def main():
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)

    """
    The client should be able to send a request to any handler, not just
    starting from the first one in the chain.
    """
    print("Chain: Monkey > Squirrel > Dog")
    client_code(monkey)
    print("\n")

    print("Subchain: Squirrel > Dog")
    client_code(squirrel)


if __name__ == "__main__":
    main()



