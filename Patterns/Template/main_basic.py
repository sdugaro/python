#------------------------------------------------------------------------------
# Template | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Template Pattern defines the skeleton of an algorithm in the superclass
# but lets subclasses override specific steps of the algorithm without changing
# its structure.
#
# - The Template Pattern helps eliminate code duplication leaving algorithm
#   structure intact.
# - The Template Pattern suggests that you break down an algorithm into a
#   series of steps, turn these steps into methods and put a series of calls
#   to these methods inside a single "Template Method"
# - The steps may either be abstract or have some default implementation.
# - To use the algorithm, the client should provide its own subclass,
#   implement all abstract steps, and override some of the optional ones
#   if thier default implementation needs to differ.

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class AbstractClass:
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    """

    def template_method(self):
        """
        Implement a template method defining the skeleton of an algorithm.
        The template method calls primitive operations as well as operations
        defined in AbstractClass or those of other objects.
        """
        self._primitive_operation_1()
        self._primitive_operation_2()
        self._primitive_operation_3()

    @abc.abstractmethod
    def _primitive_operation_1(self):
        pass

    @abc.abstractmethod
    def _primitive_operation_2(self):
        pass

    @abc.abstractmethod
    def _primitive_operation_3(self):
        pass


class ConcreteClass(AbstractClass):
    """
    Implement the primitive operations to carry out
    subclass-specific steps of the algorithm.
    """

    def _primitive_operation_1(self):
        print("Build Foundation")

    def _primitive_operation_2(self):
        print("Build Walls")

    def _primitive_operation_3(self):
        print("Build Roof")

#------------------------------------------------------------------------------
# Client Code


def main():
    concrete_class = ConcreteClass()
    concrete_class.template_method()


if __name__ == "__main__":
    main()


