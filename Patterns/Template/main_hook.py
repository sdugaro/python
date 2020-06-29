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
# - Another optional step would be a hook. A hook has an empty body. Usually
#   hooks are placed before and after crucial steps of algorithms to provide
#   subclasses with additional extension points for an algorithm.
# - Each building step can be slightly changed to make the end result
#   somewhat different from another clients implementation.

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class AbstractBaseClass:
    """
    The Abstract Class defines a template method that contains a skeleton of
    some algorithm, usually composed of calls to abstract primitive methods.

    Concrete subclasses should implement these operations, but leave the
    template method itself intact.
    """

    def template_method(self):
        """
        The template method defines the skeleton of an algorithm.
        """

        self.base_operation1()
        self.required_operation4()
        self.base_operation2()
        self.hook1()
        self.required_operation5()
        self.base_operation3()
        self.hook2()

    # These operations already have implementations.

    def base_operation1(self):
        print("AbstractBaseClass(1): I am doing the bulk of the work.")

    def base_operation2(self):
        print("AbstractBaseClass(2): Subclasses can override some operations")

    def base_operation3(self):
        print("AbstractBaseClass(3): I can provide default implementations.")

    # These operations have to be implemented in subclasses.

    @abc.abstractmethod
    def required_operation4(self):
        pass

    @abc.abstractmethod
    def required_operation5(self):
        pass

    # These are "hooks." Subclasses may override them, but it's not mandatory
    # since the hooks already have default (but empty) implementation. Hooks
    # provide additional extension points in some crucial places of the
    # algorithm.

    def hook1(self):
        pass

    def hook2(self):
        pass


class ConcreteClass1(AbstractBaseClass):
    """
    Concrete classes must implement all abstract operations of the base class.
    They can also override some default operations with a custom implementation.
    """

    def required_operation4(self):
        print("{}: Implemented Operation4".format(self.__class__.__name__))

    def required_operation5(self):
        print("{}: Implemented Operation5".format(self.__class__.__name__))

    def base_operation2(self):
        print("{}: Overrode Default Operation2".format(self.__class__.__name__))


class ConcreteClass2(AbstractBaseClass):
    """
    Usually, concrete classes will override a subset of base class operations.
    Abstract method definitions in the base class force subclasses to provide
    an implementation to the interface. Since there are hooks being called
    in the template_method, a subclass can inject logic at those points to
    tailor the steps of the algorithm.
    """

    def required_operation4(self):
        print("{}: Implemented Operation4".format(self.__class__.__name__))

    def required_operation5(self):
        print("{}: Implemented Operation5".format(self.__class__.__name__))

    def hook1(self):
        print("{}: Overrode Hook1".format(self.__class__.__name__))


#------------------------------------------------------------------------------
# Client Code

def client_code(liskov):
    """
    The client code calls the template method to execute the algorithm. Client
    code does not have to know the concrete class of an object it works with, as
    long as it works with objects through the interface of their base class.
    """

    print("Client about to run Algorithm of argument object {}".format(liskov))
    liskov.template_method()
    print("{} algorithm finished.\n".format(liskov))


def main():
    client_code(ConcreteClass1())
    client_code(ConcreteClass2())


if __name__ == "__main__":
    main()


