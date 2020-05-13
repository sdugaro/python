#------------------------------------------------------------------------------
# Proxy | Structural Design Pattern
#------------------------------------------------------------------------------
#
# A Proxy Pattern lets you provide an object that acts a s a substitute for a
# real service object used by a client. A Proxy receives client requests, does
# some work and the passes teh request to the service object.
#
# - The proxy object will have the same interface as a service, which makes it
#   interchangeable with a real service object when passed to a client.
# - While similar to the Facade Pattern in that both buffer a complex entity
#   and initialize them, a Proxy will have the same interface as its service
#   object which makes them interchangeable.
# - While similar to the Decorator Pattern in that both are built on the
#   composition of objects that work is delegated to, A Proxy will manage the
#   life cycle of its service object, while the composition of decorators is
#   managed by the client.
#


import six
import abc

#------------------------------------------------------------------------------


@six.add_metaclass(abc.ABCMeta)
class Subject():
    """
    The Subject interface declares common operations for both RealSubject and
    the Proxy. As long as the client works with RealSubject using this
    interface, you'll be able to pass it a proxy instead of a real subject.
    """

    @abc.abstractmethod
    def request(self):
        pass


class RealSubject(Subject):
    """
    The RealSubject contains some core business logic. Usually, RealSubjects are
    capable of doing some useful work which may also be very slow or sensitive -
    e.g. correcting input data. A Proxy can solve these issues without any
    changes to the RealSubject's code.
    """

    def request(self):
        print("RealSubject: Handling request.")


class Proxy(Subject):
    """
    The Proxy has an interface identical to the RealSubject.
    """

    def __init__(self, real_subject):
        self._real_subject = real_subject

    def request(self):
        """
        The most common applications of the Proxy pattern are lazy loading,
        caching, controlling the access, logging, etc. A Proxy can perform one
        of these things and then, depending on the result, pass the execution to
        the same method in a linked RealSubject object.
        """

        if self.check_access():
            self._real_subject.request()
            self.log_access()

    def check_access(self):
        print("Proxy: Checking access prior to firing a real request.")
        return True

    def log_access(self):
        print("Proxy: Logging the time of request.")


#------------------------------------------------------------------------------

def client_code(subject):
    """
    The client code is supposed to work with all objects (both subjects and
    proxies) via the Subject interface in order to support both real subjects
    and proxies. In real life, however, clients mostly work with their real
    subjects directly. In this case, to implement the pattern more easily, you
    can extend your proxy from the real subject's class.
    """

    # ...

    subject.request()

    # ...


def main():
    print("Client: Executing the client code with a real subject:")
    real_subject = RealSubject()
    client_code(real_subject)

    print("")

    print("Client: Executing the same client code with a proxy:")
    proxy = Proxy(real_subject)
    client_code(proxy)


if __name__ == "__main__":
    main()
