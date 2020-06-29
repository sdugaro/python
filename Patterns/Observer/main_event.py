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


import six
import abc
from random import randrange


@six.add_metaclass(abc.ABCMeta)
class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abc.abstractmethod
    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        pass

    @abc.abstractmethod
    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        pass

    @abc.abstractmethod
    def notify(self):
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state information and notifies registered
    observers when the state changes. For simplicity, the state in maintained
    in a single variable.

    The Subject has a list of subscribers (observers). For simplicity,
    subscribers are maintained in a queue but they could be stored more
    categorically in such as by event or type.

    """

    _state = None
    _observers = []

    def attach(self, observer):
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer):
        print("Subject: {} no longer subscribed".format(observer))
        self._observers.remove(observer)

    def notify(self):
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self):
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """

        print("\nSubject: I'm doing something important.")
        self._state = randrange(0, 10)

        print("Subject: My state has just changed to: {}".format(self._state))
        self.notify()


@six.add_metaclass(abc.ABCMeta)
class Observer:
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abc.abstractmethod
    def update(self, subject):
        """
        Receive update from subject.
        """
        pass


class ConcreteObserverA(Observer):
    """
    Concrete Observers react to certain updates issued by the Subject
    they have subscribed to. This observer takes interest in Subject
    events less than 5.
    """
    def update(self, subject):
        if subject._state < 5:
            print("ConcreteObserverA: Reacted to the event")


class ConcreteObserverB(Observer):
    """
    Concrete Observers react to certain updates issued by the Subject
    they have subscribed to. This observer takes interest in any Subject
    events that are not 1.
    """
    def update(self, subject):
        if subject._state == 0 or subject._state >= 2:
            print("ConcreteObserverB: Reacted to the event")


#------------------------------------------------------------------------------
# Client Code


def main():

    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_a)

    subject.some_business_logic()


if __name__ == "__main__":
    main()
