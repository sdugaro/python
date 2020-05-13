#------------------------------------------------------------------------------
# Factory Method | Creational Design Pattern
#------------------------------------------------------------------------------
# Allow a client to create various product classes without specifying the
# concrete classes directly, rather more generically through a creator method.
#
# - Minimizes much conditional handling code with a variety of products which
#   make code harder to read, understand and maintain, contrary to the
#   "Single Responsibility Principle" - a module, class or method should be
#   well defined such that it does one thing and has only 1 reason to change.
#   Lengthy conditionals usually have a common goal, so find a common interface.
#   In Python any object providing the desired methods implements an interface.
# - The Python Standard Library provides the abc module for formally defining
#   interfaces - a better approach for larger multi-developer applications.
#   The abc module works by marking methods of the base class and providing
#   implementations in concrete subclasses
# - The @abstractmethod decorator defines a method that is 'declared' by an
#   interface but isnt likely to do anything; the expectation being that the
#   method will be overridden by a concrete class implementation. This will
#   raise runtime errors when the @abstractmethod's are not overridden
# - Abstract Base Classes make it easy to define the structure of similar
#   factories who manage a similar interface for the products they create.
#

import abc


#------------------------------------------------------------------------------
# Creator Abstract Base Class and Concrete Creator Implementations

class Creator(object):
    """
    Declare the factory method, which returns an object of type Product.
    Creator may also define a default implementation of the factory
    method that returns a default ConcreteProduct object.
    Call the factory method to create a Product object.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.product = self._factory_method()

    @abc.abstractmethod
    def _factory_method(self):
        pass

    def operation(self):
        self.product.interface()


class CatCreator(Creator):
    """
    Override the factory method to return an instance of a ConcreteProduct1.
    """

    def _factory_method(self):
        return CatProduct()


class DogCreator(Creator):
    """
    Override the factory method to return an instance of a ConcreteProduct2.
    """

    def _factory_method(self):
        return DogProduct()

#------------------------------------------------------------------------------
# Product Abstract Base Class and Concrete Product Implementations


class Product(object):
    """
    Define the interface of objects the factory method creates.
    Implement this interface in concreate subclasses
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def interface(self):
        pass


class CatProduct(Product):

    def interface(self):
        print("I am a [{}]: Meow!".format(self.__class__.__name__))


class DogProduct(Product):

    def interface(self):
        print("I am a [{}]: Woof!".format(self.__class__.__name__))


#------------------------------------------------------------------------------

if __name__ == "__main__":

    """ Factories hold an instance of a product, managing its interface """
    cat = CatCreator()
    cat.operation()

    dog = DogCreator()
    dog.operation()
