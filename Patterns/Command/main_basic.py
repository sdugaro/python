#------------------------------------------------------------------------------
# Command | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Command Pattern encapsulates a request as an object, thereby allowing you
# to parameterize clients with different requests.
#
# - In essence, a Command object manages the linkage between one object and the
#   business logic in another object such that neither object needs to care
#   about or depend on one anothers apis.
# - This creates a clear separation of concearns such that the logic of each
#   object can be developed independently without affecting the other.
# - When an object needs to have a request fulfilled, it trusts that through
#   the fixed api of the Command interface, that request will be executed.
# - The client code configures the actions and wraps them in commands to be
#   executed by some other object when required.
# - The six module permits compatability between Py2k and Py3k when working with
#   the abc (abstract base class) module.
# - The Command abstract base class defines and interface that needs to be
#   implemented by a concrete Command class invoked by client code.


import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Command:
    """
    Declare an interface for executing an operation.
    """

    def __init__(self, receiver):
        self._receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass


class ConcreteCommand(Command):
    """
    Define a binding between a Receiver object and an action.
    Implement execute() by invoking the appropriate action
    on the encapsulated reciever object.
    """

    def execute(self):
        self._receiver.action()


class Receiver:
    """
    Know how to perform the operations associated with carrying out a
    request. Any class may serve as a Receiver.
    """

    def __init__(self, *args):
        self._args = args

    def action(self):
        print("{}: Executing Action {}".format(
            self.__class__.__name__,
            self._args))


class Invoker:
    """
    Ask the command to carry out the request.
    """

    def __init__(self):
        self._commands = []

    def store_command(self, command):
        self._commands.append(command)

    def execute_commands(self):
        for command in self._commands:
            command.execute()


#------------------------------------------------------------------------------
# Client Code


def main():
    receiver1 = Receiver("Hello", "World")
    reciever2 = Receiver("The", "Quick", "Brown", "Fox",
                         "Jumps", "Over", "The", "Lazy", "Dog")

    command1 = ConcreteCommand(receiver1)
    command2 = ConcreteCommand(reciever2)

    invoker = Invoker()
    invoker.store_command(command1)
    invoker.store_command(command2)
    invoker.execute_commands()


if __name__ == "__main__":
    main()
