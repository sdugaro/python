# https://python-patterns.guide/python/module-globals/
# https://python-patterns.guide/python/prebound-methods/
#
#------------------------------------------------------------------------------
# Prebound Method | Pythonic Global Object Creational Design Pattern
#------------------------------------------------------------------------------
# Offers callables at the top level of your module sharing state through a
# common object.
#
# - Offer several routines in the modules global namespace that need to share
#   state with each other at runtime. The random module provides routines
#   available in the modules global namespace like randrange() and choice()
#   that mirror the methods of a Random object. Behind the scenes these are
#   callables: methods that have been bound ahead of time to a single instance of
#   Random that the module itself has gone ahead and constructed.
# - Instantiate your class at the top level of your module
# - Assign it a private name prefixed with '_', no need for '__' as that infers
#   name mangling on instance variables being subclassed
# - Assign a bound copy of each of the objects methods to the global namespace
# - Instantiate a random number generator seed from an 'entropy pool' using
#   a system call to datetime
# - Take care not to instantiate an object at import time. This pattern is not
#   appropriate for a class whose constructor creates files, reads a database,
#   or could potentially introduce side effects, latency, or failures on import.
# - Best for instantiation of lightweight objects where the stateful behavior of
#   a class instance variable can be made available in the modules global level
# - Its almost always better to assign methods to global names explicitly

from datetime import datetime


class Random8(object):
    def __init__(self):
        self.set_seed(datetime.now().microsecond % 255 + 1)

    def set_seed(self, value):
        self.seed = value

    def random(self):
        self.seed, carry = divmod(self.seed, 2)
        if carry:
            self.seed ^= 0xb8
        return self.seed


_instance = Random8()
random = _instance.random
set_seed = _instance.set_seed

#------------------------------------------------------------------------------

if __name__ == "__main__":
    """ Use the modules global context to define prebound class methods. These
    act as convenient module level callable functions, which avoid the need for
    client code to instantiate an object before invoking its methods.
    """
    _instance.set_seed(88)
    print(_instance.random())
    _instance.set_seed(87)
    print(_instance.random())


