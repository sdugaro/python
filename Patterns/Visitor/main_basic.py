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
#

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Element:
    """
    Define an Accept operation that takes a visitor as an argument.
    """

    @abc.abstractmethod
    def accept(self, visitor):
        pass


class ConcreteElementA(Element):
    """
    Implement an Accept operation that takes a visitor as an argument.
    """

    def accept(self, visitor):
        visitor.visit_concrete_element_a(self)


class ConcreteElementB(Element):
    """
    Implement an Accept operation that takes a visitor as an argument.
    """

    def accept(self, visitor):
        visitor.visit_concrete_element_b(self)


@six.add_metaclass(abc.ABCMeta)
class Visitor:
    """
    Declare a Visit operation for each class of ConcreteElement in the
    object structure. The operation's name and signature identifies the
    class that sends the Visit request to the visitor. That lets the
    visitor determine the concrete class of the element being visited.
    Then the visitor can access the element directly through its
    particular interface.
    """

    @abc.abstractmethod
    def visit_concrete_element_a(self, concrete_element_a):
        pass

    @abc.abstractmethod
    def visit_concrete_element_b(self, concrete_element_b):
        pass


class ConcreteVisitor1(Visitor):
    """
    Implement each operation declared by Visitor. Each operation
    implements a fragment of the algorithm defined for the corresponding
    class of object in the structure. ConcreteVisitor provides the
    context for the algorithm and stores its local state. This state
    often accumulates results during the traversal of the structure.
    """

    def visit_concrete_element_a(self, concrete_element_a):
        print("{} Visiting {}".format(
            self.__class__.__name__, concrete_element_a))

    def visit_concrete_element_b(self, concrete_element_b):
        print("{} Visiting {}".format(
            self.__class__.__name__, concrete_element_b))


class ConcreteVisitor2(Visitor):
    """
    Implement each operation declared by Visitor. Each operation
    implements a fragment of the algorithm defined for the corresponding
    class of object in the structure. ConcreteVisitor provides the
    context for the algorithm and stores its local state. This state
    often accumulates results during the traversal of the structure.
    """

    def visit_concrete_element_a(self, concrete_element_a):
        print("{} Visiting {}".format(
            self.__class__.__name__, concrete_element_a))

    def visit_concrete_element_b(self, concrete_element_b):
        print("{} Visiting {}".format(
            self.__class__.__name__, concrete_element_b))


#------------------------------------------------------------------------------
# Client Code

def main():
    visitor_1 = ConcreteVisitor1()
    visitor_2 = ConcreteVisitor2()

    concrete_element_a = ConcreteElementA()
    concrete_element_a.accept(visitor_1)
    concrete_element_a.accept(visitor_2)


if __name__ == "__main__":
    main()


