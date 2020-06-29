#------------------------------------------------------------------------------
# Observer | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Observer Pattern lets you define a subscription mechanism to notify
# multiple objects about events that happen to the object being observed.
#
# - A one-to-many dependency is created between objects so that when one
#   object changes state, all its dependents are notified and updated
#   automatically.
# - The Chain of Responsibility, Comand, Mediator and Observer patterns
#   address various ways of connecting senders and recievers of requests.
#   Chain of Responsibility passes a request along a dynamic chain of potential
#   recievers until one handles it.
#   Command establishes unidirectional links between senders and receivers.
#   Mediator eliminates direct links between senders and receivers forcing them
#   to communicate indirectly via a mediator object
#   Observer lets receivers dynamically subscribe and unsubscribe from
#   receiving requests from the sender.
# - Note that with Py2k we must inherit from object in order to make use
#   of property descriptors and method overloading.


import six
import abc
import random


@six.add_metaclass(abc.ABCMeta)
class Observer(object):
    """
    Define a base interface for objects to respond to when notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        self._subject = subject
        print("{} set subject {}".format(self.__class__.__name__, subject))


class ConcreteObserver1(Observer):
    """
    Implement how an observer will update in response to subject events.
    For example, store state that stays consistent with the subject's.
    """

    def update(self, arg):
        print("{} Notified of Subject state Change [{}]:".format(
            self.__class__.__name__, arg))

        self._observer_state = arg
        print("-> Synched State [{}]".format(self._observer_state))


class ConcreteObserver2(Observer):
    """
    Implement how an observer will update in response to subject events.
    For example, store state that stays consistent with the subject's.
    """

    def update(self, arg):
        print("{} Notified of Subject state Change [{}]:".format(
            self.__class__.__name__, arg))

        random.seed(arg)
        self._observer_state = random.randint(1, 100)
        print("-> Seeded Random Integer [{:>3}]".format(self._observer_state))


class Subject(object):
    """
    A Subject (aka Publisher) is an object that has some interesting state.
    It needs to know its observers. Any number of Observer objects may observe
    a subject. The subject sends a notification to its observers when its
    state changes.
    """

    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer.subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer.subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)

    @property
    def subject_state(self):
        return self._subject_state

    @subject_state.setter
    def subject_state(self, arg):
        """
        When a subjects state has changed, notify all registered observers
        """
        self._subject_state = arg
        self._notify()


#------------------------------------------------------------------------------
# Client Code


def main():

    observer1 = ConcreteObserver1()
    observer2 = ConcreteObserver2()

    subject = Subject()
    subject.attach(observer1)
    subject.attach(observer2)

    print("\nSubject is Changing State:")
    subject.subject_state = 123
    subject.subject_state = 456

    subject.detach(observer1)
    print("\nSubject detached {}".format(observer1))
    subject.subject_state = 789
    subject.subject_state = 123


if __name__ == "__main__":
    main()
