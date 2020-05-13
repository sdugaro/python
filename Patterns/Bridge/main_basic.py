#------------------------------------------------------------------------------
# Bridge | Structural Design Pattern
#------------------------------------------------------------------------------
# A Bridge Pattern is one in which a large class or set of closely related
# classes are split into two separate heirarchies - abstraction and
# implementation - which can be developed independently of each other.
#
# - This is an often employed solution to class explosion which tends to
#   manifest as derived class heirchies grow over time. Once a particular class
#   heirarchy has been designed, subclassing is the predominant way forward
#   until the codebase becomes unwieldly and intractable. At this point some
#   measure of re-orginization and/or re-factoring comes into play.
# - Class explosion is commonly found when classes derive in independent
#   dimensions, such that there is a combinatorial result. This is a clear
#   indicator of a division of closely related classes that the Bridge Pattern
#   works well with. This is also known as cartesian product complexity. 
# - Abstraction: is a high level control layer for some entity (interface). This
#   layer doesn't do any real work on its own, rather it delegates work to the
#   Implementation Layer (platform). For example, in most applications a GUI is
#   an abstraction while the implementation is the underlying API that the GUI
#   calls in response to user interactions. These can be extended independently
#   where the GUI is user/admin tailored and the API can support different
#   platforms (linux/windows/mac)
# - A Bridge would sit between a GUI and a multi platform framework that
#   provides the platform specific implementation details.
# - The abstraction object controls the appearance of the app, delegating the
#   actual work to the linked implementation object. Different implementations
#   are interchangeable as long as they follow a common interface.
# - GUI clases can be changed without touching the API related classes and
#   vice-versa, and further subclassing is now scaled down to something more
#   manageable.
# - A Bridge makes it easy to switch implementations at runtime.
# - In Python, a bridge isn't super popular because the language is not confined
#   to the rigid static inheritance structure of older compiled oop languages.


import six
import abc


class Abstraction:
    """
    The Abstraction defines the interface for the "control" part of the two
    class hierarchies. It maintains a reference to an object of the
    Implementation hierarchy and delegates all of the real work to this object.
    """

    def __init__(self, implementation):
        self.implementation = implementation

    def operation(self):
        result = "Abstraction: Base operation with:\n{}".format(
            self.implementation.operation_implementation())
        return result


class ExtendedAbstraction(Abstraction):
    """
    You can extend the Abstraction without changing the Implementation classes.
    """

    def operation(self):
        result = "ExtendedAbstraction: Extended operation with:\n{}".format(
            self.implementation.operation_implementation())
        return result


@six.add_metaclass(abc.ABCMeta)
class Implementation():
    """
    The Implementation defines the interface for all implementation classes. It
    doesn't have to match the Abstraction's interface. In fact, the two
    interfaces can be entirely different. Typically the Implementation interface
    provides only primitive operations, while the Abstraction defines higher-
    level operations based on those primitives.
    """

    @abc.abstractmethod
    def operation_implementation(self):
        pass


"""
Each Concrete Implementation corresponds to a specific platform and implements
the Implementation interface using that platform's API.
"""


class ConcreteImplementationA(Implementation):
    def operation_implementation(self):
        return "ConcreteImplementationA: Here's the result on the platform A."


class ConcreteImplementationB(Implementation):
    def operation_implementation(self):
        return "ConcreteImplementationB: Here's the result on the platform B."


#------------------------------------------------------------------------------
# Client Code

def client_code(abstraction):
    """
    Except for the initialization phase, where an Abstraction object gets linked
    with a specific Implementation object, the client code should only depend on
    the Abstraction class. This way the client code can support any abstraction-
    implementation combination.
    """

    print("{}\n".format(abstraction.operation()))


def main():
    """
    The client code should be able to work with any pre-configured 
    abstraction-implementation combination.
    """

    implementation = ConcreteImplementationA()
    abstraction = Abstraction(implementation)
    client_code(abstraction)

    implementation = ConcreteImplementationB()
    abstraction = ExtendedAbstraction(implementation)
    client_code(abstraction)


if __name__ == "__main__":
    main()
