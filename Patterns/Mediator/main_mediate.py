#------------------------------------------------------------------------------
# Mediator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Mediator Pattern reduces coupling between components of a program by
# making them communicate indirectly through a special mediator object.
#
# - The mediator object makes it easy to modify, extend and reuse individual
#   components because they are no longer dependent on many other classes.
# - The Mediator pattern suggests that there is no direct communication between
#   components that should be inddpendent of each other, rather the components
#   collaborate indirectly by calling a mediator object to redirect calls to
#   the appropriate components. In this way components are only coupled to a
#   single mediator class rather then dozens of their colleagues.
# - It is commonly seen when facilitating communication between gui components
#   and is analagous to the Controller in the Model/View/Controller Pattern.
# - Concrete Components implement functionality independent of other components
#   and of any mediators..

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Mediator:
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    @abc.abstractmethod
    def notify(self, sender, event):
        pass


class ConcreteMediator(Mediator):
    """
    The actual implementation of the Mediator used by the client.
    All logic related to which components are triggered in response to
    some event is managed herein.
    """
    def __init__(self, component1, component2):
        self._component1 = component1
        self._component1.mediator = self
        self._component2 = component2
        self._component2.mediator = self

    def notify(self, sender, event):
        print("{} notified by {}".format(self.__class__.__name__, sender))
        if event == "A":
            print("Mediator reacts on A and triggers following operations:")
            self._component2.do_c()
        elif event == "D":
            print("Mediator reacts on D and triggers following operations:")
            self._component1.do_b()
            self._component2.do_c()


class BaseComponent(object):
    """
    The Base Component provides the basic functionality of storing a mediator's
    instance inside component objects whether provided when the Component is
    constructed or at a later point via an assignment operator. The @property
    decorator provides the syntactic sugar for components to be able to get and
    set a mediator.
    """

    def __init__(self, mediator=None):
        self._mediator = mediator

    @property
    def mediator(self):
        return self._mediator

    @mediator.setter
    def mediator(self, mediator):
        self._mediator = mediator
        print("{} set mediator {}".format(self.__class__.__name__, mediator))


class Component1(BaseComponent):
    def do_a(self):
        print("Component 1 does A.")
        self.mediator.notify(self, "A")

    def do_b(self):
        print("Component 1 does B.")
        self.mediator.notify(self, "B")


class Component2(BaseComponent):
    def do_c(self):
        print("Component 2 does C.")
        self.mediator.notify(self, "C")

    def do_d(self):
        print("Component 2 does D.")
        self.mediator.notify(self, "D")


#------------------------------------------------------------------------------
# Client Code

def main():

    c1 = Component1()
    c2 = Component2()
    mediator = ConcreteMediator(c1, c2)

    print("\nClient triggers operation A.")
    c1.do_a()

    print("\nClient triggers operation D.")
    c2.do_d()


if __name__ == "__main__":
    main()
