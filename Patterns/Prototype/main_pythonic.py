#------------------------------------------------------------------------------
# Prototype | Creational Design Pattern
#------------------------------------------------------------------------------
#
# Copy existing objects without making your code dependent on their classes
# An instance of a prototype specifies the kinds of objects to create, and new
# objects are created by copying the prototype. This helps hide the complexity
# of the instances being created, allowing clones to be modified independently.
#
# - No need to derive off of object since this class is not meant to be
#   extendable; any attempt to do so will result in a TypeError (python2)
# - The interpreter name mangles dunder-prefixed instance and class members
#   which makes them Pythonically 'private' without the need for a keyword
# - We dont need an initialize() method as in the Static Factory example as
#   that happens in the __init__ constructor, where initialization of an
#   object typically happens in Python. The object creation constructor is
#   actually __new__, but a need to override this method is rarely seen.
# - We also replace the static factory methods for obtaining a particular
#   prototype in favor of a more flexible factory creation method.
# - Choosing to not implement this Factory as a static class means there
#   can be more than one instance of this factory, which might be desirable
#   if there were reason to slightly augment Prototype factories. In other
#   words, the common suggestion that a Factory be a Singleton is not
#   imposed, really boiling down to how the client code interacts with
#   a PrototypeFactory interface
# - Conceptually, a class variable should be more performant that an instance
#   variable since it is initialized once (when the class is defined) while
#   an instance variable is initialized every time a new instance is created.
#   However in practice, this is largely negligible. A timeit test over 10
#   Billion instantiations would show about a 1 second difference. A factory
#   is unlikely to see more than a single instantiation depending on how
#   configurable it is. This factory merely composes a fixed number of
#   prototypes, which are instantiated once per factory.
# - A Factory Method typically has some kind of identifer argument that is
#   used as a switch to  return the appropriate.
# - Method Overloading (polymorphism where multiple methods have the same name
#   but different arguments) is not supported in Python. Other languages do
#   this at compile via a lookup table. Python is a dynamically typed language,
#   where everything is an object, including classes and  methods and every
#   object attribute of a class must have a unique name. Similar logic can be
#   inferred from the arguments based on thier type at runtime.
# - Method Overriding (Polymorphism) is however supported via inheritance.

import copy

#------------------------------------------------------------------------------


class Prototype(object):

    def __init__(self, type_, value, user=None):
        """
        __private member variables get name-mangled to hinder access
        _protected member variables implement accessors as needed as they are
          a developersince convention to make certain variables less accessable
        public member variables are get/set directly given that they can also
        be added dynamically at runtime.
         """
        self.__id = type_
        self._value = value
        self.user = user

    def clone(self):
        return copy.copy(self)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class Type1(Prototype):

    def __init__(self, number):
        super(Type1, self).__init__("Type1", number)


class Type2(Prototype):

    def __init__(self, number):
        super(Type2, self).__init__("Type2", number)


class PrototypeFactoryError(Exception):
    """ Base class for PrototypeFactory Errors """
    pass


class NoSuchPrototypeError(PrototypeFactoryError):
    """ Raised when a requested prototype does not exist """
    pass


class PrototypeFactory:
    """
    The Prototype Factory manages the creation of prototype clones.

    Various Prototype configurations are defined in the factory's constructor
    and locked away in an auto name-mangled private variable so as to prevent
    the Prototype from edits. This ensures each new clone will be the same.
    """

    def __init__(self):
        self.__prototypes = {
            1: [Type1(1), Type1(2)],
            2: [Type2(1), Type2(2)]
        }

    def clonePrototype(self, type_, variant=0):
        """
        creation method to serve up a copy of a predefined prototype.

        Note its fine to give a local variable the same name as an argument;
        it will have its own reference and not modify the callers value.
        This can be confirmed using id() in an interpreter.
        """

        if isinstance(type_, str):
            digits = set(''.join(i for i in type_ if i.isdigit()))
            type_ = int(digits.pop())

        if isinstance(variant, str):
            digits = set(''.join(i for i in variant if i.isdigit()))
            variant = int(digits.pop())

        try:
            prototype = self.__prototypes[type_][variant]
        except (KeyError, IndexError):
            prototype = None

        if prototype is None:
            raise NoSuchPrototypeError
        return prototype


def main():

    """
    Instantiate a Prototype Factory
    """
    factory = PrototypeFactory()

    """ instantiate, edit and work with Prototype clones not """
    t10 = factory.clonePrototype(1, 0)
    print("Type1|Config1 Cloned:", t10, t10.get_value())
    t10.set_value(7)
    print("Type1|Config1 Edited:", t10, t10.get_value())
    t10 = factory.clonePrototype("Type1", "Value1")
    print("Type1|Config1  Reset:", t10, t10.get_value())
    # we have a fresh clone with a new memory location, which is the reference
    # now held in the original variable name. The original reference to the
    # original clone gets garbage collected since nothing else is using it.

    try:
        del t10
        print("Type1|Config1 Deleted:", t10)
    except Exception as e:
        print(e)
        print("Clone was deleted; Re-Cloning...")
        t10 = factory.clonePrototype(1) # 0 by default 

    clones = [t10]
    clones.append(factory.clonePrototype(1, 1))
    clones.append(factory.clonePrototype(2, 0))
    clones.append(factory.clonePrototype(2, 1))

    print("Working With Prototype Clones:")
    for c in clones:
        print(c, c.get_value())


#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

