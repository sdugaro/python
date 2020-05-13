#------------------------------------------------------------------------------
# Facade | Structural Design Pattern
#------------------------------------------------------------------------------
#
# The Facade Pattern provides a simple interface to the complex logic of one or
# several subsystems. The Facade delegates the client requests to the
# appropriate objects within the subsystem. The Facade is also responsible for
# managing their lifecycle. All of this shields the client from the undesired
# complexity of the subsystem.
#
# - A Facade provides a unified and simplified interface to a complex system of
#   classes, libraries or frameworks (sub system interfaces) helping decrease
#   the overall complexity of an application.
# - Dependencies can be moved into one place.
# - An entire library or framework rarely needs to be exposed, a Facade focuses
#   on creating an interface for only those parts of APIs its application uses.
# - Subsystem interfaces are not likely to look and feel the same; a facade can
#   bring uniformity to these differences in its own.
#


class Facade:
    """
    Know which subsystem classes are responsible for a request.
    Delegate client requests to appropriate subsystem objects.
    """

    def __init__(self, subsystem1=None, subsystem2=None):
        """
        Depending on the needs of the application a Facade can be initialized
        with subsystems, or fallthrough to create them itself.
        """
        self._subsystem_1 = subsystem1 or Subsystem1()
        self._subsystem_2 = subsystem2 or Subsystem2()

    def operation(self):
        """
        The facades methods are convenient shortcust to the sophisticated
        functionality of the substems. Clients do not need to know how to
        interface with the subsystems or how they interface with each other.
        """

        results = []
        results.append("Facade initializes subsystems:")
        results.append(self._subsystem_1.operation1())
        results.append(self._subsystem_2.operation1())
        results.append("Facade delegating to subsystems:")
        results.append(self._subsystem_1.operation2())
        results.append(self._subsystem_2.operation2())
        print("\n".join(results))


class Subsystem1:
    """
    To the subsystem, the Facade is just another client. Subsystems keep no
    references to the facade; they only handle requests from it.
    """

    def operation1(self):
        return "{} Ready ...".format(self.__class__.__name__)

    def operation2(self):
        return "{} Complete.".format(self.__class__.__name__)


class Subsystem2:
    """
    A different subsystem the facade works with simultaneously.
    The facade is also aware of this interfaces, which is uses even if the
    client provides a subsytem to the facade
    """

    def operation1(self):
        return "{} Ready ...".format(self.__class__.__name__)

    def operation2(self):
        return "{} Complete.".format(self.__class__.__name__)


#------------------------------------------------------------------------------
# Client Code

def main():
    facade = Facade()
    facade.operation()


if __name__ == "__main__":
    main()
