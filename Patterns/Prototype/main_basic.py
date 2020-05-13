#------------------------------------------------------------------------------
# Prototype | Creational Design Pattern
#------------------------------------------------------------------------------
#
# Copy existing objects without making your code dependent on their classes
# An instance of a prototype specifies the kinds of objects to create, and new
# objects are created by copying the prototype. This helps hide the complexity
# of the instances being created, allowing clones to be modified independently.
#
# - Since have to know an objects class to create a duplicate, your code
#    becomes dependent on that class; you cant just copy values from an instance
#    of an object and have an exact copy since some object fields can be private
#    and are not visible from outside of the object itself.
# - Prototype objects can produce full copies since objects of the same class
#    have access to each others private fields.
# - All prototype classses should have a common interface that makes it possible
#    to copy objects, even if their concrete classes are unknown.
# - Create a new object of the same class, then go through all the fields and
#    of the original object and copy over their values (C++ copy constructor)
# - The Prototype delegates the cloning process to the actual objects being cloned.
# - An object that supports cloning is called a Prototype, and cloning is an
#    alternative to subclassing when objects have hundreds of configurations.
# - After creating and configuring a large set of objects, and you need an
#    object thats the same as one that has been configured, the prototype gets
#    cloned instead of having to construct a new object from scratch.
#
# In Python, assignment statements do not copy objects, they instead create a
# reference (pointer to an source objects address), and a reference may not be
# enough: ie modify a copy, not the original (Shallow Copy vs Deep Copy)
# Shallow Copy: constructs a new compound object, then inserts references
#    to the objects found in the original to whatever extent is possible.
# - a change to the source WILL be reflected in the copy
# - copy.copy()
# Deep Copy: constructs a new compound objects, then recursively inserts
#    copies of the objects found in the original.
# - a change to the source WILL NOT be relrected in the cloned object
# - copy.deepcopy()

import copy

#------------------------------------------------------------------------------


class Prototype:

    _type = None
    _value = None

    def clone(self):
        pass

    def getType(self):
        return self._type

    def get_value(self):
        return self._value


class Type1(Prototype):

    def __init__(self, number):
        self._type = "Type1"
        self._value = number

    def clone(self):
        return copy.copy(self)


class Type2(Prototype):

    """ Concrete prototype. """

    def __init__(self, number):
        self._type = "Type2"
        self._value = number

    def clone(self):
        return copy.copy(self)


class PrototypeFactory:

    """ Manages prototypes.
    Static factory that encapsulates prototype initialization/configuration
    allowing these configurations to be instantiated as a starting point by
    cloning them
    """

    # private class variable: # name mangled to _PrototypeFactory__type*
    __type1Value1 = None
    __type1Value2 = None
    __type2Value1 = None
    __type2Value2 = None

    @staticmethod
    def initialize():
        PrototypeFactory.__type1Value1 = Type1(1)
        PrototypeFactory.__type1Value2 = Type1(2)
        PrototypeFactory.__type2Value1 = Type2(1)
        PrototypeFactory.__type2Value2 = Type2(2)

    @staticmethod
    def get_type1_1():
        return PrototypeFactory.__type1Value1.clone()

    @staticmethod
    def get_type1_2():
        return PrototypeFactory.__type1Value2.clone()

    @staticmethod
    def get_type2_1():
        return PrototypeFactory.__type2Value1.clone()

    @staticmethod
    def get_type2_2():
        return PrototypeFactory.__type2Value2.clone()


def main():

    """
    Define various Prototypes and configurations so we have a unique ground
    truth for each of them in memory. The client doesn't need to care what
    the particulars are with respect to creating the objects as the Factory
    takes care of that upon initialization - making object creation trivial.

    A nicer Factory Method implementation might pass parameters to a single
    method such as .get_prototype('type1','variation1') or the like.
    However, this example tries to replicate the original GOF implementation,
    with a comparable structure in Python, albeit not very Pythonic.
    """
    PrototypeFactory.initialize()

    """ instantiate, edit and work with Prototype clones not """
    t11 = PrototypeFactory.get_type1_1()
    print("Type1|Config1 Cloned:", t11, t11.get_value())
    t11._value = 7
    print("Type1|Config1 Edited:", t11, t11.get_value())
    t11 = PrototypeFactory.get_type1_1()
    print("Type1|Config1  Reset:", t11, t11.get_value())
    # we have a fresh clone with a new memory location, which is the reference
    # now held in the original variable name. The original reference to the
    # original clone gets garbage collected since nothing else is using it.

    try:
        del t11
        print("Type1|Config1 Deleted:", t11)
    except Exception as e:
        print(e)
        print("Clone was deleted; Re-Cloning...")
        t11 = PrototypeFactory.get_type1_1()


    clones = [t11]
    clones.append(PrototypeFactory.get_type1_2())
    clones.append(PrototypeFactory.get_type2_1())
    clones.append(PrototypeFactory.get_type2_2())

    print("Working With Prototype Clones:")
    for c in clones:
        print(c, c.get_value())


#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

