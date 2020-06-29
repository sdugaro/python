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
    Define the interface of interest to clients.
    Maintain a reference to a Strategy object.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def execute_strategy(self):
        self._strategy.algorithm_interface()


@six.add_metaclass(abc.ABCMeta)
class Strategy():
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    """

    @abc.abstractmethod
    def algorithm_interface(self):
        pass


class ConcreteStrategyA(Strategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    def algorithm_interface(self):
        print("2 + 2 = {}".format(4))


class ConcreteStrategyB(Strategy):
    """
    Implement the algorithm using the Strategy interface.
    """

    def algorithm_interface(self):
        print("2 * 2 = {}".format(4))

#------------------------------------------------------------------------------
# Client Code


def main():
    strategy_a = ConcreteStrategyA()
    strategy_b = ConcreteStrategyB()
    context = Context(strategy_a)
    context.execute_strategy()

    context.strategy = strategy_b
    context.execute_strategy()



if __name__ == "__main__":
    main()


