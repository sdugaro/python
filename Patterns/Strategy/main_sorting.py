#------------------------------------------------------------------------------
# Strategy | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Strategy Pattern lets you define a family of algorithms, put each of
# them into a separate class, and make their objects interchangeable.
#
# - The Strategy pattern suggests that you take a class that does something
#   specific in a lot of different ways, and extract all of its algos into
#   separate classes called 'strategies'
# - Strategy lets the algorithm vary independently from clients that use it.
# - Poor software design manifests itself when simple bug fixes, new algos
#   or mild augmuentation of code creates a ripple effect among classes,
#   teams, and version control.
# - The context is independent of concrete strategies so you can add,
#   modifiy or remove algorithms withouth changing the code of the
#   context or the strategies.
# - The original class, called context, must have a field for storing a
#   reference to one of the strategires. The context delegates work to a
#   linked strategy object instead of executing on its own.
# - The context isnt responsible for selecting an appropriate algorithm
#   for the job, insead, the client passes the desired strategy to the
#   context. The context works with strategies through the same interface
#   which only exposes a single method for triggering the algorithm
#   encapsulated within the single strategy, but otherwise doesnt know
#   about the strategy itself.
# - If you only have a couple of algorithms that rarely change this pattern
#   may not be necessary given all the new classes an interfaces required.
#

import six
import abc


class Context(object):
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy):
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """

        self._strategy = strategy

    @property
    def strategy(self):
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def execute_strategy(self, data):
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """

        print("Context: Sorting data using the strategy (not sure how it'll do it)")
        result = self._strategy.do_algorithm(data)
        print(",".join(result))


@six.add_metaclass(abc.ABCMeta)
class Strategy():
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abc.abstractmethod
    def do_algorithm(self, data):
        pass


"""
Concrete Strategies implement the algorithm while following the base Strategy
interface. The interface makes them interchangeable in the Context.
"""


class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data):
        return sorted(data)


class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data):
        return reversed(sorted(data))


#------------------------------------------------------------------------------
# Client Code


def main():

    # The client code picks a concrete strategy and passes it to the context.
    # The client should be aware of the differences between strategies in order
    # to make the right choice.

    data = ["b", "a", "c", "e", "d"]

    context = Context(ConcreteStrategyA())
    print("Client: Strategy is set to normal sorting.")
    context.execute_strategy(data)

    print("Client: Strategy is set to reverse sorting.")
    context.strategy = ConcreteStrategyB()
    context.execute_strategy(data)


if __name__ == "__main__":
    main()


