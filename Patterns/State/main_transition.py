#------------------------------------------------------------------------------
# State | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The State Pattern allows an object to alter its behavior when its internal
# state changes. The object will appear to change its class.
#
# - The State pattern is closely related to the idea of a Finite State Machine
# - At any given moment there is a finite number of states which a program or
#   object can be in. Within any unique state the program behaves differently,
#   and the program can be switched from one state to another instantaneously.
# - Depending on the current state the program may not be able to switch to
#   certain other states (Directed Graph).
# - The switching rules (aka Transitions) are finite and predetermined.
# - A state is usually just a set of values assigned to the objects fields.
# - State machines are usually implemented with lots of conditional operators
#   that select the appropriate behavior depending on the current state
#   of the object. This can become difficult to maintain and augment and
#   does not scale well. The State Pattern aims to help with this.
# - The State Pattern suggests that you create new classes for all possible
#   states of an object and extract all state specific behaviors into these
#   classes. Instead of implementing all behaviors on its own, the original
#   object - known as the context - stores a referene to one of the state
#   objects that represents its current state, and delegates all the state
#   related work to that object.
# - To transition the context to another state, replce the active state
#   object with another objects that represents the new state. This is only
#   possible if all state classes follow the same interface and the context
#   itself works with these objects through that interface.
# - In the State PAttern, the particular states may be aware of each other
#   and initiate transitions from one state to another.

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Context:
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state):
        self.transition_to(state)

    def transition_to(self, state):
        """
        The Context allows changing the State object at runtime.
        """

        print("{}: Transition to {}".format(
            self.__class__.__name__, type(state).__name__))
        self._state = state
        self._state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """

    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()


@six.add_metaclass(abc.ABCMeta)
class State(object):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abc.abstractmethod
    def handle1(self):
        pass

    @abc.abstractmethod
    def handle2(self):
        pass


class ConcreteStateA(State):
    """
    Concrete State implements various behaviors for the context state.
    """
    def handle1(self):
        print("{}: handling request1.".format(self.__class__.__name__))

        next_state = ConcreteStateB()
        print("+ Transitioning Context State to {}".format(next_state))
        self.context.transition_to(next_state)

    def handle2(self):
        print("{}: handling request2.".format(self.__class__.__name__))


class ConcreteStateB(State):
    """
    Concrete State implements various behaviors for the context state.
    """
    def handle1(self):
        print("{}: handling request1.".format(self.__class__.__name__))

    def handle2(self):
        print("{}: handling request2.".format(self.__class__.__name__))

        next_state = ConcreteStateA()
        print("+ Transitioning Context State to {}".format(next_state))
        self.context.transition_to(next_state)

#------------------------------------------------------------------------------
# Client Code


def main():

    initial_state = ConcreteStateA()
    context = Context(initial_state)
    context.request1()
    context.request2()


if __name__ == "__main__":
    main()
