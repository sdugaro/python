# https://python-patterns.guide/gang-of-four/abstract-factory/
# https://refactoring.guru/design-patterns/abstract-factory
#
#------------------------------------------------------------------------------
# Abstract Factory Method | Creational Design Pattern
#------------------------------------------------------------------------------
#
# Defines and interface for creating all distinct products but leaves the actual
# product creation to factory classes. Each factory type corresponds to a
# certain product variety, allowing entire product families to be created
# without specifying their concrete classes
#
# Factory := a function, method or class that produces objects, files, records
# Creation Method := a wrapper around a constructor call
# Static Creation Method := a creation method that can be called from a class
# Simple Factory Pattern := a class that has one creation method with a large
#   conditional that chooses which product class to instantiate and return
#   based on some method parameter.
# Factory Method Pattern := provides an inteface for creating objects and
#   allowing subclasses to alter the type of object that will be created;
#   common to see a base class with creation method and subclasses extend it.
# Abstract Factory Pattern := provides an interface for creating families of
#   related or dependend objects without specifying their concrete classes
#
# - Client Code calls the creation methods of a factory object (instead of
#   creating products directly with a constructor call)
# - Since a factory corresponds to a single product variant, all the products
#   you get from a factory will be compatiable with each other.
# - Client Code ONLY works with factories and products through their ABSTRACT
#   interfaces, so the same client code can work with different products.
# - Client Code is de-coupled from the concrete products.
# - Commonly used in Python libraries to extend and customize components
# - The pattern is identifiable by methods that return a factory object used
#   for creating specific sub components.
# - Traditionally a non-Pythonic pattern typically used in languages where
#   functions and classes are not first class objects. In Python a class or
#   factory function can be used when a library needs to create objects on
#   behalf of the client code.
# - A Pythonic approach would use a callable:= any object f that exectues code
#   using the syntax f(a,b,c). First-class:= a callable that can be passed as a
#   parameter, returned as a return value, or stored in a data structure. First
#   class callables offer a mechanism for implementing object factories:=
#   routines that build and return new objects. In Python types are callables.

import json
from decimal import Decimal  # Decimal is a callable
from abc import ABCMeta, abstractmethod

#------------------------------------------------------------------------------
# Traditional Abstract Factory Method Pattern Implementation in Python
# - handrolled, akin to older languages
# - no passing of callables or classes


#class AbstractFactory(metaclass=ABCMeta):  # Python3
class AbstractFactory:
    """
    Separate specifiction from implementation by creating an abstract base
    class. This creates a requirement that factory arguments adhere to this
    interface.
    """

    __metaclass__ = ABCMeta  # Python2

    @abstractmethod
    def build_sequence(self):
        pass

    @abstractmethod
    def build_number(self, string):
        pass


class Factory(AbstractFactory):
    def build_sequence(self):
        return []

    def build_number(self, string):
        return Decimal(string)


class Loader(object):

    @staticmethod
    def load(string, factory):
        sequence = factory.build_sequence()
        for substring in string.split(','):
            item = factory.build_number(substring)
            sequence.append(item)
        return sequence


#------------------------------------------------------------------------------
# Pythonic Approach using callable factories
# - json.load is a wrapper around json.JSONDecoder, its initialization method
#   stores the parse_float argument as an instance attribute defaulting to the
#   built in float type if not override is specified:
#
#    self.parse_float = parse_float or float
#

def build_decimal(string):
    """ Rudimentary Factory """
    return Decimal(string)


#------------------------------------------------------------------------------
# Multiple Factories Managing Product Families
# AbstractFactory: generally describes what products can be created: A & B
# ConcreteFactory1: defines an implementation that produces products A & B
# ConcreteFactory2: also produces products A & B, but slightly differently
#
# AbstractProductA: generally describes what product A is and its interface
# AbstractProductB: generally describes what product B is and its interface
# ConcreteProductA1|B1: ConcreteFactory1's implementation of A & B
# ConcreteProductA2|B2: ConcreteFactory2's implementation of A & B

DATA_FMT = "{:>7} [{:>5}] {:>7} [{:>8}]"

class AbstractFactory():
    """
    Declare an interface for operations that create abstract product
    objects.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_product_a(self):
        pass

    @abstractmethod
    def create_product_b(self):
        pass


class ConcreteFactory1(AbstractFactory):
    """
    Implement the operations to create concrete product objects.
    """

    def create_product_a(self):
        return ConcreteProductA1()

    def create_product_b(self):
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    """
    Implement the operations to create concrete product objects.
    """

    def create_product_a(self):
        return ConcreteProductA2()

    def create_product_b(self):
        return ConcreteProductB2()


class AbstractProductA():
    """
    Declare an interface that describes and can interact with Product A.
    Simply a schematic of A without any implementation or customization.
    Can provide some basic functionality that all factories can use when
    implementing/creating/customizing product A.
    """

    __metaclass__ = ABCMeta

    __i_am_a = "CHAIR"

    @abstractmethod
    def interface_a(self):
        pass

    @property
    def name(self):
        return AbstractProductA.__i_am_a


class ConcreteProductA1(AbstractProductA):
    """ Factory1's implementation of Product A.
    Based on the general Product A schematics (interface without implementation)
    """

    def interface_a(self):
        print(DATA_FMT.format("Product", "A", "Made at", "Factory1"))
        print(DATA_FMT.format("Is a", self.name, "Made in", "CHINA"))


class ConcreteProductA2(AbstractProductA):
    """ Factory2's implementation of Product A.
    Based on the general Product A schematics (interface without implementation)
    """

    def interface_a(self):
        print(DATA_FMT.format("Product", "A", "Made at", "Factory2"))
        print(DATA_FMT.format("Is a", self.name, "Made in", "MEXICO"))


class AbstractProductB():
    """
    Declare an interface that describes and can interact with Product B.
    Simply a schematic of A without any implementation or customization.
    Can provide some basic functionality that all factories can use when
    implementing/creating/customizing product B.
    """

    __metaclass__ = ABCMeta

    __i_am_a = "SOFA"

    @abstractmethod
    def interface_b(self):
        pass

    @property
    def name(self):
        return AbstractProductB.__i_am_a


class ConcreteProductB1(AbstractProductB):
    """ Factory1's implementation of Product B.
    Based on the general Product A schematics (interface without implementation)
    """

    def interface_b(self):
        print(DATA_FMT.format("Product", "B", "Made at", "Factory1"))
        print(DATA_FMT.format("Is a", self.name, "Made in", "CHINA"))


class ConcreteProductB2(AbstractProductB):
    """ Factory2's implementation of Product B.
    Based on the general Product A schematics (interface without implementation)
    """

    def interface_b(self):
        print(DATA_FMT.format("Product", "B", "Made at", "Factory2"))
        print(DATA_FMT.format("Is a", self.name, "Made in", "MEXICO"))


#------------------------------------------------------------------------------
# Client Code

if __name__ == "__main__":

    """
    Use a traditional Abstract Factory implementation in Pythoni
    to parse a string into Decimal objects.
    """

    f = Factory()
    result = Loader.load('1.23, 4.56', f)
    print(result)

    """ Convert a JSON number data type into a Python Decimal """

    text = '{"total": 9.61, "items": ["Americano", "Omelet"]}'
    print(json.loads(text, parse_float=build_decimal))
    print(json.loads(text, parse_float=Decimal))


    """ Deliver products A & B from all factories that make them """
    for factory in (ConcreteFactory1(), ConcreteFactory2()):
        product_a = factory.create_product_a()
        product_b = factory.create_product_b()
        product_a.interface_a()
        product_b.interface_b()


