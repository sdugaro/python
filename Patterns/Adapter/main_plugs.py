#------------------------------------------------------------------------------
# Adapter | Structural Design Pattern
#------------------------------------------------------------------------------
# An Adapter Pattern connects incompatible interfaces. It is categorized as
# structural design pattern as it combines the capability of two independent
# interfaces.
#
# - An adapter is a class that connects independent interfaces. It usually
#   implements a target interface with the logic needed to translate.
# - An adaptee is a class that needs to be wrapped and translated in some way;
#   it is the thing that needs to be adapted.
#


class EuropeanSocketInterface:
    """ Source Interface """
    def voltage(self):
        pass

    def live(self):
        pass

    def neutral(self):
        pass

    def earth(self):
        pass


class Socket(EuropeanSocketInterface):
    """ Adaptee Implementation """
    def voltage(self):
        return 230

    def live(self):
        return 1

    def neutral(self):
        return -1

    def earth(self):
        return 0


class USASocketInterface:
    """ Target Interface """
    def voltage(self):
        pass

    def live(self):
        pass

    def neutral(self):
        pass


class Adapter(USASocketInterface):
    """ Adapter Implementation

    Note that we hold a reference to the adaptee object in a class variable.
    This is so we can convert/adapt the necessary parts of the adaptee when
    requested by the client.
    """

    __socket = None

    def __init__(self, socket):
        self.__socket = socket

    def voltage(self):
        return 110

    def live(self):
        return self.__socket.live()

    def neutral(self):
        return self.__socket.neutral()


#------------------------------------------------------------------------------
# Client Code

class ElectricKettle:
    """ A North American Kettle expects to plug into a 110 volt socket to
    operate correctly. Otherwise it can fail to function or ruin the kettle.
    """
    __power = None

    def __init__(self, power):
        self.__power = power

    def boil(self):
        if self.__power.voltage() > 110:
            print "Kettle on fire!"
        elif self.__power.live() == 1 and self.__power.neutral() == -1:
            print "Coffee time!"
        else:
            print "No power."


def main():
    """
    An adapter is needed to plug a North American Kettle into a European socket.
    North American and European sockets are of different voltages and shapes,
    so plugging a North American appliance into a different socket requires an
    adapter - something that sits between the appliance and the socket. The
    kettle is what we need to work; whats needs an adapter -- a familar
    interface to plug into. The socket is what needs to be wrapped for the
    kettle to work -- what needs to be adapted (the adaptee)
    """

    socket = Socket()
    adapter = Adapter(socket)
    kettle = ElectricKettle(adapter)
    kettle.boil()


if __name__ == "__main__":
    main()


