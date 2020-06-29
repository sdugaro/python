#------------------------------------------------------------------------------
# Memento | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Mememto Pattern lets you save and restore an object's internal state
# without revealing the details of its implementation.
#
# - A memento does not compromise the internal strucure of the object it works
#   with nor the data maintained inside its snapshots.


import six
import abc

from datetime import datetime
from random import sample
from string import digits as NUMBERS
from string import ascii_letters as LETTERS


@six.add_metaclass(abc.ABCMeta)
class Memento:
    """
    The Memento interface provides a way to retrieve the memento's metadata,
    such as creation date or name. However, it doesn't expose the Originator's
    state.
    """

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_date(self):
        pass


class ConcreteMemento(Memento):
    def __init__(self, state):
        self._state = state
        self._date = str(datetime.now())[:19]

    def get_state(self):
        """
        The Originator uses this method when restoring its state.
        """
        return self._state

    def get_name(self):
        """
        The rest of the methods are used by the Caretaker to display metadata.
        """
        return "{} / {}...".format(self._date, self._state[0:9])

    def get_date(self):
        return self._date



class Originator():
    """
    The Originator holds some important state that may change over time.
    It also defines a method for saving the state inside a memento and
    another method for restoring the state from it.

    For the sake of simplicity, state is stored in a single variable.
    """

    _state = None

    def __init__(self, state):
        self._state = state
        print("{}: My initial state is: {}".format(
            self.__class__.__name__, self._state))

    def do_something(self):
        """
        The Originator's business logic may affect its internal state.
        Therefore, the client should backup the state before launching methods
        of the business logic via the save() method.
        """

        print("{}: I'm doing something important.".format(
            self.__class__.__name__))
        self._state = self._generate_random_string(30)

        print("{}: and my state has changed to: {}".format(
            self.__class__.__name__, self._state))

    def _generate_random_string(self, length=10):
        return "".join(sample(ascii_letters, length))

    def save(self):
        """
        Saves the current state inside a memento.
        """

        return ConcreteMemento(self._state)

    def restore(self, memento):
        """
        Restores the Originator's state from a memento object.
        """

        self._state = memento.get_state()
        print("{}: My state has changed to: {}".format(
            self.__class__.__name__, self._state))


class Caretaker():
    """
    The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
    doesn't have access to the originator's state, stored inside the memento.
    It works with all mementos via the base Memento interface.
    """

    def __init__(self, originator):
        self._mementos = []
        self._originator = originator

    def backup(self):
        print("\nCaretaker: Saving Originator's state...")
        self._mementos.append(self._originator.save())

    def undo(self):
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print("{}: Restoring state to: {}".format(
            self.__class__.__name__, memento.get_name()))

        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def show_history(self):
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento.get_name())


#------------------------------------------------------------------------------
# Client Code


def main():
    originator = Originator("Super-duper-super-puper-super.")
    caretaker = Caretaker(originator)

    caretaker.backup()
    originator.do_something()

    caretaker.backup()
    originator.do_something()

    caretaker.backup()
    originator.do_something()

    print()
    caretaker.show_history()

    print("\nClient: Now, let's rollback!\n")
    caretaker.undo()

    print("\nClient: Once more!\n")
    caretaker.undo()


if __name__ == "__main__":
    main()
