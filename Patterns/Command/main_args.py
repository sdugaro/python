#------------------------------------------------------------------------------
# Command | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Command Pattern adds a level of abstraction between actions where a
# command object is leveraged to invoke the actions.
#
# - The client creates a Command object that specifies a command to execute
#   with a list of arguments to that command.
# - The Command object is then invoked at a later point where the arguments
#   can be further varied or extended beyond those enforced at creation time.
# - The instance of the created Command object can be invoked as if it were a
#   function since we have made the object callable. An object in Python can
#   be make a callable by implementing the __call__ dunder in an object's
#   class definition.
#

import sys


def demo(a, b, c):
    """
    This function requires exactly 3 arguments.
    """
    print 'a:', a
    print 'b:', b
    print 'c:', c


class Command:

    def __init__(self, cmd, *args):
        """
        On creation of a Command instance, store the command to execute
        and any imparative positional arguments. Note that '*args' specifies
        that zero or more positional arguments are permitted to be passed
        to the Command constructor after requiring a first argument to be
        the name of the command to execute. 'args' is simply a variable that
        holds all the arguments in a tuple, which is cached for later use.
        """
        self._cmd = cmd
        self._args = args


    def __call__(self, *args):
        """
        Join he zero or more positional arguments specified at creation time
        with zero or more positional arguments specified at call time and
        then invoke the function specified at creation time with all specified
        arguments in order. The *-operator unpacks the tuple so the remaining
        argument list can be passed to a function programmatically.
        """
        all_args = self._args + args
        return self._cmd(*all_args)


#------------------------------------------------------------------------------
# Client Code

def main():

    """
    Use Pythons native dir command to list the contents of a specified module
    """
    cmd = Command(dir)
    try:  # Py3k
        print(cmd(builtins))
    except NameError:  # Py2k
        print(cmd(__builtins__))

    print(cmd(sys))

    """
    Create a command object to invoke the demo function with the first
    two arguments always the same, and the last one variable.
    """
    cmd = Command(demo, 1, 2)
    cmd(3)
    cmd(4)
    cmd(5)


if __name__ == "__main__":
    main()


