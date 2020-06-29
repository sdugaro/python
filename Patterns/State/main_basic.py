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


class Context(object):
    """
    Define the interface of interest to clients. The client will provide
    the context a state object and then issue some request that it be
    handled.  The Context API will always be the same for the client, and
    the State API will always be the same for the context. This allows
    State objects to be switched out freely, while being operated on in
    a uniform manner. As a result states can scale while related changes
    to code cause minimal impact.
    """

    def __init__(self, state):
        """
    Maintain an instance of a ConcreteState subclass that defines the
    current state.

        """
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if isinstance(state, State):
            self._state = state

    def request(self):
        self._state.handle()


@six.add_metaclass(abc.ABCMeta)
class State:
    """
    Define an interface for encapsulating the behavior associated with a
    particular state of the Context.
    """

    @abc.abstractmethod
    def handle(self):
        pass


class ConcreteStateA(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def handle(self):
        print("{} handler Called".format(self.__class__.__name__))


class ConcreteStateB(State):
    """
    Implement a behavior associated with a state of the Context.
    """

    def handle(self):
        print("{} handler Called".format(self.__class__.__name__))

#------------------------------------------------------------------------------
# Client Code


def main():
    a = ConcreteStateA()
    b = ConcreteStateB()

    context = Context(a)
    context.request()
    context.state = b
    context.request()


if __name__ == "__main__":
    main()
