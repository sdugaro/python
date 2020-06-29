#------------------------------------------------------------------------------
# Visitor | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Visitor Pattern allows you to separate algorithms from the objects on
# which they operate.
#
# - Visitor lets you define a new operation without changing the classes of
#   the elements on which it operates.
# - The Visitor Pattern lets you add 'external' operations wo a whole class
#   heirarchy without changing the existing code of these classes.
# - The Visitor Pattern suggests that you place the new behavior into a
#   separate class called 'Visitor' instead of trying to integrate it into
#   existing classes. The original object that had to perform the behavior
#   is now passed to one of the visitors methods as an argument, providing
#   the method access to all necessary data contained within the object.
# - The Visitor Pattern uses a technice called 'Double Dispatch' which helps
#   to execute the proper method on an object without conditionals. Instead
#   of letting the client select a proper version of the method to call,
#   this choice is delegated to objects passed to the Visitor as an argument.
#   Since the objects know their own classes, they will be able to pick a
#   proper method on the Visitor less awkwardly. These objects 'accept' a
#   visitor and tell it what visiting method should be executed.
# - The Visitor class presents its interface of what it can run, and
#   the concrete elements implement an 'accept' method for the client with
#   a visitor argument to pre-define which of the visitor methods it will
#   run when it accepts a visitor.
# - The elements have full access to their own attributes so know better
#   what arguments should be fed to visitor functions than any external
#   class would. Visitor objects, once accepted, are likely to lack the
#   necessary access to the private fields and methods of the elements
#   they are working with.
# - While the Visitor can offer an api that tailors to specific elements
#   so that the element uses the one tailored for it providing itself as
#   the argument, this can be more flexible. Should the Visitor provide
#   its methods more generically, Concrete Components can call the same
#   visitor methods with the added responsibility that they offer up their
#   data to the generic visitor method argument list.
# - You can experience the biggest benefit of the Visitor pattern when using
#   it with a complex object structure, such as a Composite tree. In this case
#   it might be helpful to store some intermediate state of the algorithm
#   while executing visitor's methods over various objects of the structure.
# - The Visitor Pattern uses a technique called 'Double Dispatch' which helps
#   to execute the proper method on an object without conditionals. Instead
#   of letting the client select a proper version of the method to call,
#   this choice is delegated to objects passed to the Visitor as an argument.
#   Since the objects know their own classes, they will be able to pick a
#   proper method on the Visitor less awkwardly. These objects 'accept' a
#   visitor and tell it what visiting method should be executed.
#

"""
Double Dispatch allows using dynamic binding alongside overloaded
methods. Say a base class has a method overridden by multiple subclasses,
the only way to know which method is being called is to run the program
and check the class of an object passed to the method. All we know for
sure is that the object will have an implementation of the method.
This is known as 'late or dynamic binding'. Suppose Shape is a base
class and Circle is a subclass

class Visitor:
    def visit(shape): ...
    def visit(circle): ...

class Shape:
    def accept(visitor):
        visitor.visit(self)

class Circle:
    def accept(visitor):
        visitor.visit(self)

"""


import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Component:
    """
    The Component interface declares an `accept` method that should take the
    base visitor interface as an argument.
    """

    @abc.abstractmethod
    def accept(self, visitor):
        pass


class ConcreteComponentA(Component):
    """
    Each Concrete Component must implement the `accept` method in such a way
    that it calls the visitor's method corresponding to the component's class.
    """

    def accept(self, visitor):
        """
        Note that we're calling `visit_concrete_component_a`, which matches the
        current class name. This way we let the visitor know the class of the
        component it works with.
        """

        visitor.visit_concrete_component_a(self)

    def exclusive_method_of_concrete_component_a(self):
        """
        Concrete Components may have special methods that don't exist in their
        base class or interface. The Visitor is still able to use these methods
        since it's aware of the component's concrete class.
        """

        return "A [Some ConcreteComponent A Logic]"


class ConcreteComponentB(Component):
    """
    Same here: visit_concrete_component_b is fed a ConcreteComponentB as an arg
    """

    def accept(self, visitor):
        visitor.visit_concrete_component_b(self)

    def special_method_of_concrete_component_b(self):
        return "B [Some ConcreteComponent B Logic]"


@six.add_metaclass(abc.ABCMeta)
class Visitor:
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """

    @abc.abstractmethod
    def visit_concrete_component_a(self, element):
        pass

    @abc.abstractmethod
    def visit_concrete_component_b(self, element):
        pass


class ConcreteVisitor1(Visitor):
    """
    Concrete Visitors implement several versions of the same algorithm,
    which can work with all concrete component classes. This implies that
    the algorithm recievies variation in its arguments from the elements
    themselves as they encapsulate their own data.
    """
    def visit_concrete_component_a(self, element):
        print("{} executing {} method:\n {}".format(
            self.__class__.__name__, type(element),
            element.exclusive_method_of_concrete_component_a()))

    def visit_concrete_component_b(self, element):
        print("{} executing {} method:\n {}".format(
            self.__class__.__name__, type(element),
            element.special_method_of_concrete_component_b()))


class ConcreteVisitor2(Visitor):
    def visit_concrete_component_a(self, element):
        print("{} executing {} method:\n {}".format(
            self.__class__.__name__, type(element),
            element.exclusive_method_of_concrete_component_a()))

    def visit_concrete_component_b(self, element):
        print("{} executing {} method:\n {}".format(
            self.__class__.__name__, type(element),
            element.special_method_of_concrete_component_b()))


#------------------------------------------------------------------------------
# Client Code

def client_code(components, visitor):
    """
    The client code can run visitor operations over any set of elements without
    figuring out their concrete classes. The accept operation directs a call to
    the appropriate operation in the visitor object.
    """

    print("Client passing visitor {} to all components.".format(type(visitor)))
    for component in components:
        component.accept(visitor)
    print("All components visited.\n")


def main():
    components = [ConcreteComponentA(), ConcreteComponentB()]

    print("The client code works with all visitors via the base Visitor interface.")
    visitor1 = ConcreteVisitor1()
    client_code(components, visitor1)

    print("It allows the same client code to work with different types of visitors:")
    visitor2 = ConcreteVisitor2()
    client_code(components, visitor2)


if __name__ == "__main__":
    main()


