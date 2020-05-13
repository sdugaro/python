# https://python-patterns.guide/gang-of-four/singleton/
#
#------------------------------------------------------------------------------
# Singleton | Creational Design Pattern
#------------------------------------------------------------------------------
# Python programmers never implement the Singleton Pattern, whose class forbids
# normal instantion and instead offers a class method that returns the singleton
# instance. Python is more elegant in that it lets a class continue to support
# the normal syntax for isntantiation via a custom __new__() constructor
# returning the singleton instance. A more Pythonic approach is to use the
# Global Object Pattern when your design forces you to offer global access to a
# singleton object
#
# Python was using the term 'singleton' before the "Singleton Pattern" was
# defined by the OO design pattern community.
# - a tuple of length 1 is called a singleton, akin to mathematics:
#   a set containing exactly 1 element
# - Modules are singletons because import only creates a single copy of each
#   module. Subsequent imports of the same name return th same module object
# - a singled is a class isntance that has been assigned a global name through
#   the Global Object Pattern (to share a global variable across modules). ie:
#   a global module namespace can store constants and mutable class instances
# - None and Ellipsis are examples of singleton objects in Python, named in
#   the __builtin__ module:: ie|python3] >>> type(Ellipsis)()
# - Prior to Python 2.4 there was no __new__() dunder; __init__() is always
#   called on the return value whether the object being returned is new or not.
#   __init__ is always called after __new__, so by not implementing __init__
#   only __new__() will be called. Use __new__ when you need to control the
#   CREATION of a new instance; its the first step in object creation responsible
#   for returning a new instance of your class. Use __init__ when you need to
#   control the  INITIALIZATION of a new instance; it does not return anything,
#   rather it is only responsible for initializing an instance after its been
#   created. Typically __new__ doesn't need to be overridden, unless you are
#   subclassing an immutable type like str, int, or tuple; use Factory instead.
# - Alternatively, raise an exception in __init__() to make normal object
#   instantiation impossible.


class Singleton(object):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            print('Creating the object for the first time')
            cls.__instance = super(Singleton, cls).__new__(cls)
            # Put any initialization here.
        return cls.__instance


#------------------------------------------------------------------------------

if __name__ == "__main__":

    s = Singleton()
    print(s)
    t = Singleton()
    print(t)
    assert s is t
    print("Are s & t singleton objects one and the same?", s is t)


