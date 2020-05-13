#------------------------------------------------------------------------------
# Decorator | Structural Design Pattern
#------------------------------------------------------------------------------
#
# The Decorator Pattern allows additional behaviors to be attached to an object
# at runtime by placing the object inside wrappers that contain new behavior.
#
# - Decorators provide a flexible alternative to subclassing when extending an
#   objects behavior.
# - Inheritance is typically static, meaning you cannot change the behavior of
#   an existing object at runtime. Extending a class can alter behavior, but
#   the behavior derives from an object's superclass.
# - Aggregation or Composition can be used instead of inheritance, where one
#   object has a reference to a helper object and delegates some work to it,
#   where substituting one helper object with another can happen at runtime,
#   and references to multiple objects can be held for various tasks.
# - Wrapper is an alias for Decorator. A Wrapper is an object that can be
#   linked with some target object. The wrapper contains the same set of
#   methods as the target and delegates all requests it receives to it. In
#   the process, the wrapper may intervene to perform some additional action
#   before or after it passes the request to the target
# - Decorators can wrap objects as any times as needed - stacking behaviors -
#   since both target objects and decorators follow the same interface.


#------------------------------------------------------------------------------
# Abstract Base Classes
# - 'Python decorators' could be used to officially declare these as abstract
#   base classes and/or abstract methods. These also wrap a class or class
#   method to produce runtime errors when subclasses do not implement what
#   the abstract base class insists be implemented.
# - To avoid differences in syntax for doing this between Python2 and Python3
#   we just avoid any such runtime enforcement since the class heirarchy in
#   this example is rather self evident.


class Component(object):
    """
    The base interface defines operations that can be altered by decorators.
    """
    def operation(self, *args):
        pass


class Decorator(Component):
    """
    Maintain a reference to a Component object and define an interface that
    conforms to Component's interface. The base Decorator class follows the
    same interface as the other components. The primary purpose of this class
    is to define the wrapping interface for all concrete decorators. The
    default implementation of the wrapping code might include a field for
    storing a wrapped component and the means to initialize it.
    """

    def __init__(self, component):
        self._component = component

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

    @property
    def component(self):
        """
        Convenience getter for the wrapped component.
        The decorator delegates all work to this component
        """
        return self._component

    def operation(self, *args):
        """
        The decorator applies some additional logic before and/or after calling
        the the logic of the component through its reference. Maintaining the
        component operation in a decorator base class method having the same
        signature allows subclasses to straighforwardly execute component logic
        as well as clients to call a decorated component as if it were the
        component itself.
        """
        return self._component.operation(*args)


#------------------------------------------------------------------------------
# Concrete Implementations
# - Concrete Components provide default implementations of the operations.
# - Concrete Decorators use their reference to the wrapped object to alter it.
#

class ConcreteComponent(Component):
    """
    There may be several variations of these classes.
    """

    def operation(self, *args):
        return "{}{}".format(self.__class__.__name__, args)


class ConcreteDecoratorAfter(Decorator):

    def operation(self, *args):
        """
        Concreate Decorators may call their superclass implementation of the
        operation, instead of invoking the operation on the component reference.
        This approach simplifies extension of decorator classes.
        """
        result = super(ConcreteDecoratorAfter, self).operation(*args)
        return "{}[{}]".format(self.__class__.__name__, result)


class ConcreteDecoratorBefore(Decorator):
    """
    Decorators can execute their behavior either before or after the call to a
    wrapped object.
    """

    def operation(self, *args):
        new_args = map(lambda x: '[{}]'.format(x), args)
        result = super(ConcreteDecoratorBefore, self).operation(*new_args)
        return "{}[{}]".format(self.__class__.__name__, result)


#------------------------------------------------------------------------------
# Client Code
# - The client code works with all objects using the Component interface. This
#   way it can stay independent of the concrete classes of components it works
#   with.

def client_code(component):
    """
    The client code works with all objects using the Component interface. This
    way it can stay independent of the concrete classes of components it works
    with.
    """
    print("RESULT: {}".format(component.operation('one', 'two')))


def main():

    """
    The client code can pass simple components to its functions...
    """
    simple = ConcreteComponent()
    print("Client: I've got a simple component:")
    client_code(simple)

    """
    ...as well as decorated components since they implement the same interface.
    """
    decorator1 = ConcreteDecoratorAfter(simple)
    print("Client: Now I've got a decorated component, running after:")
    client_code(decorator1)

    """
    Decorators can wrap simple components as well as other decorators thereby
    stacking the wrapped behavior
    """
    decorator2 = ConcreteDecoratorBefore(decorator1)
    print("Client: Stacked decorated components, running before and after:")
    client_code(decorator2)


#------------------------------------------------------------------------------


if __name__ == "__main__":
    main()


