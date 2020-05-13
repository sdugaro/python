#------------------------------------------------------------------------------
# Decorator | Structural Design Pattern
#------------------------------------------------------------------------------
#
# The Decorator Pattern allows a user to add new functionality to an existing
# object dynamically without altering its structure, acting as a wrapper to an
# existing class.
#
# - A Decorator class wraps the original class while keeping its method
#    signatures intact.

"""
NB: The 'six' module /usr/lib/python2.7/site-packages/six.pyc is a native
Python2 / Python3 compatability library, providing utility functions for
smoothing over the differences between the two so Python code can be written
that is compatible in both versions. 2*3 = 6 https://six.readthedocs.io/

Notice the uniform differences in working with class inheritance.
Python2 class variable:  __metaclass__ = ABCMeta
Python3 metaclass inherit: Component(metaclass=abc.ABCMeta)
six     metaclass decorator: @six.add_metaclass(ABCMeta)

Python2: super(ClassName, self)
Python3: super()
six    : ClassName.

"""

import six
from abc import ABCMeta

#------------------------------------------------------------------------------
# Abstract Base Classes


@six.add_metaclass(ABCMeta)
class Abstract_Coffee(object):
    """
    Base Class interface defining operations that can be altered by decorators
    """

    def get_cost(self):
        pass

    def get_ingredients(self):
        pass

    def get_tax(self):
        return 0.1 * self.get_cost()


@six.add_metaclass(ABCMeta)
class Abstract_Coffee_Decorator(Abstract_Coffee):
    """
    Base Decorator interface inherits from the Base Class so it can call the
    methods defined in its interface. On initialization it expects to be passed
    an object that implements the base class interface, holding a reference to
    it so it can invoke the corresponding base class method when the method is
    called on the decorator. This provides an entry point to execute additional
    logic before and/or after calling the 'wrapped' logic.
    """

    def __init__(self, decorated_coffee):
        self.decorated_coffee = decorated_coffee

    def get_cost(self):
        return self.decorated_coffee.get_cost()

    def get_ingredients(self):
        return self.decorated_coffee.get_ingredients()


#------------------------------------------------------------------------------
# Concrete Implementations

class Coffee(Abstract_Coffee):

    def get_cost(self):
        return 1.00

    def get_ingredients(self):
        return 'coffee'


class Sugar(Abstract_Coffee_Decorator):

    def __init__(self, decorated_coffee):
        Abstract_Coffee_Decorator.__init__(self, decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost()

    def get_ingredients(self):
        return self.decorated_coffee.get_ingredients() + ', sugar'


class Milk(Abstract_Coffee_Decorator):

    def __init__(self, decorated_coffee):
        Abstract_Coffee_Decorator.__init__(self, decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 0.25

    def get_ingredients(self):
        return self.decorated_coffee.get_ingredients() + ', milk'


class Vanilla(Abstract_Coffee_Decorator):

    def __init__(self, decorated_coffee):
        Abstract_Coffee_Decorator.__init__(self, decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 0.75

    def get_ingredients(self):
        return self.decorated_coffee.get_ingredients() + ', vanilla'

#------------------------------------------------------------------------------


def main():

    myCoffee = Coffee()
    print('Ingredients: ' + myCoffee.get_ingredients() +
          '; Cost: ' + str(myCoffee.get_cost()) +
          '; Tax = ' + str(myCoffee.get_tax()))

    myCoffee = Milk(myCoffee)
    print('Ingredients: ' + myCoffee.get_ingredients() +
          '; Cost: ' + str(myCoffee.get_cost()) +
          '; Tax = ' + str(myCoffee.get_tax()))

    myCoffee = Vanilla(myCoffee)
    print('Ingredients: ' + myCoffee.get_ingredients() +
          '; Cost: ' + str(myCoffee.get_cost()) +
          '; Tax = ' + str(myCoffee.get_tax()))

    myCoffee = Sugar(myCoffee)
    print('Ingredients: ' + myCoffee.get_ingredients() +
          '; Cost: ' + str(myCoffee.get_cost()) +
          '; Tax = ' + str(myCoffee.get_tax()))

#------------------------------------------------------------------------------


if __name__ == "__main__":
    main()

