#------------------------------------------------------------------------------
# Command | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Command Pattern turns a request into a standalone object containing all
# information about the request. This transformation lets you parametrize
# methods with different requests, delay or queue a requests execution, and
# support undoable oprations.
#
# - Good software design is often based on the principle of separation of
#   concearns which results in breaking an app into layers. For instance
#   a layer for a gui and another layer for the business logic, where a gui
#   object calls a method of a business logic object with some arguments.
#   This process is usally described as one object sending another object
#   a request.
# - The command pattern suggests that gui objects shouldn't send requests
#   directly, rather all the request details should be extracted into a
#   separate command class with a single method that triggers the request.
# - Command objects serve as links between various gui and business logic
#   objects. The gui object doesnt need to know what business logic object
#   will recieve the request or what the business logic is, it just triggers
#   the command which handles all the details.
# - The Command object maintains a standard and simple interface, usually
#   just a single execution method that takes no parameters. This interface
#   lets you use carious command with the same request sending and avoid
#   coupling it to concrete classes of commands. This makes it easy to
#   change the senders behavior at runtime by switching the command objects
#   that are linked to the sender.
# - When dealing with parameters, the command object should either be
#   pre-configured with this data or be capable of retrieving it.
# - This pattern is common in Python code; typically used as an alternative
#   for callbacks connecting ui elements to actions, queuing tasks, and
#   tracking operation history.
# - The pattern is recognizable by methods in a sender object that invokes
#   methods in a reciever object encapsulated by a command object limited
#   to specific actions.
#

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Command:
    """
    The Command interface declares a method for executing a command.
    """

    @abc.abstractmethod
    def execute(self):
        pass


class SimpleCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, payload):
        self._payload = payload

    def execute(self):
        print("{}: I can print ({})".format(self.__class__.__name__, self._payload))


class ComplexCommand(Command):
    """
    Some commands can delegate more complex operations to other objects,
    called "receivers."
    """

    def __init__(self, receiver, a, b):
        """
        Complex commands can accept one or several receiver objects along with
        any context data via the constructor.
        """

        self._receiver = receiver
        self._a = a
        self._b = b

    def execute(self):
        """
        Commands can delegate to any methods of a receiver.
        """

        print("ComplexCommand: Complex stuff should be done by a receiver object")
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)


class Receiver:
    """
    The Receiver classes contain some important business logic. They know how to
    perform all kinds of operations, associated with carrying out a request. In
    fact, any class may serve as a Receiver.
    """

    def do_something(self, a):
        print("\n{}: Working on ({})".format(self.__class__.__name__, a))

    def do_something_else(self, b):
        print("\n{}: Also working on ({})".format(self.__class__.__name__, b))


class Invoker:
    """
    The Invoker is associated with one or several commands.
    It sends a request to the command(s) provided to it, knowing its execute()
    method can be called as it has been defined in its interface.
    """

    _on_start = None
    _on_finish = None

    """
    Initialize commands.
    """

    def set_on_start(self, command):
        self._on_start = command

    def set_on_finish(self, command):
        self._on_finish = command

    def do_something_important(self):
        """
        The Invoker does not depend on concrete command or receiver classes.
        The Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        print("Invoker: Does anybody want something done before I begin?")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("Invoker: ...doing something really important...")

        print("Invoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


#------------------------------------------------------------------------------

def main():
    """
    The client code can parameterize an invoker with any commands.
    """

    invoker = Invoker()
    invoker.set_on_start(SimpleCommand("Say Hi!"))

    receiver = Receiver()
    invoker.set_on_finish(ComplexCommand(receiver, "Send mail", "Save report"))

    invoker.do_something_important()


if __name__ == "__main__":
    main()

