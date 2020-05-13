#------------------------------------------------------------------------------
# Adapter | Structural Design Pattern
#------------------------------------------------------------------------------
# An Adapter Pattern allows objects with incompatible interfaces collaborate.
# It is a wrapper between two objects, catching calls for one object and
# transforming them to a format and interface recognizable by the second.
#
# - Data is commonly maintained in formats such as csc, xml, json, yaml which
#   all have different interfaces around the data, so it is common to need
#   adapters that move the raw data between different interfaces or libraries.
# - Adapters hide the conversion complexity happening behind the scenes, such
#   that the wrapped object istn even aware of the adapter.
# - Beyond data conversion, adapters can help objects with different interfaces
#   collaborate. The adapter gets an interface, compatible with one object, the
#   object uses this interface to call the adapters methods, and upon receiving
#   the call, the adapter passes the requests to another object but in a format
#   and order the second object expects.
# - 2-Way adapters are common to convert calls in both directions.
# - Adapters permit the reuse of several existing subclasses that lack some
#   common functionality that cannot be added to the superclass.
#


class Target():
    """
    The Target defines the domain-specific interface used by the client code.
    """

    def request(self):
        return "Target: The default target's behavior."


class Adaptee:
    """
    The Adaptee contains some useful behavior, but its interface is incompatible
    with the existing client code. The Adaptee needs some adaptation before the
    client code can use it.
    """

    def specific_request(self):
        return ".eetpadA eht fo roivaheb laicepS"


class Adapter(Target):
    """
    The Adapter makes the Adaptee's interface compatible with the Target's
    interface.
    """

    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        result = self.adaptee.specific_request()[::-1]
        return "Adapter: (TRANSLATED) {}".format(result)


#------------------------------------------------------------------------------
# Client Code

def client_code(target):
    """
    The client code supports all classes that follow the Target interface.
    """

    print("{}".format(target.request()))


def main():

    target = Target()
    print("\nClient: I work with Target objects via the request() method:")
    client_code(target)

    adaptee = Adaptee()
    print("\nClient: With the Adaptee class, I have to use a different")
    print("method specific_request(), and cannot interpret the result")
    print("Adaptee: {}".format(adaptee.specific_request()))

    adapter = Adapter(adaptee)
    print("\nClient: Wrapping Adaptee with an adapter works as expected")
    client_code(adapter)


if __name__ == "__main__":
    main()

