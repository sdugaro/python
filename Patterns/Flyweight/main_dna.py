#------------------------------------------------------------------------------
# Flywieght | Structural Design Pattern
#------------------------------------------------------------------------------
# The flyweight pattern provides a way to decrease object count. A predominant
# feature of flyweight objects is that they are immutable; they cannot be
# modified once they have been constructed.
#
# - Dictionaries are commonly used to store reference objects in a Factory.
# - The __new__ dunder method is the creation method (constructor) in Python.
#   It is called prior to __init__ whenever a class is instantiated to create
#   an object. It is a static method, whose method signature requires that it
#   be passed the class that needs to be instantiated. The Python interpreter
#   provides this parameter at instantiation time for custom creation methods
#   to be implemented. It also passes forward the arguments to the constructor
#   provided by the caller. If the parent object class is not called via super
#   or object.__new__ then it is a complete creation override and __init__
#   wont be called.
# - __new__ will return the id() of the newly created object, which can be
#   used to check object equivalence with the 'is' operator
#

#------------------------------------------------------------------------------


class ComplexGenetics(object):
    """ Flyweight Class
    The flyweight stores the large common portion of all the objects
    (the intrinsic state). The extrinsic state is the part of the object
    that makes the object unique/distinguishes it from other objects.
    The extrinsic data is passed in as an argument to the Flyweight.
    This restores the full identity of each object, where objects are
    otherwise 99% the same, saving memory on duplicate data.
    """

    def __init__(self):
        pass

    def genes(self, gene_code):
        """
        The extrinsic arugment joins the common cached data to complete
        the full data profile of the object
        """

        return "ComplexPattern[%s]MassiveData" % (gene_code)


class Families(object):
    """ Flyweigh Factory
    Here our factory is designed to actually create new objects when the
    Families class constructor is called, However it will do a quick check
    to see if it has already created and cached the object. If so, the
    cached flyweight object is returned. One starts to appreciate the
    Pattern when each of these objects consumes a lot of memory and there
    are a lot of them (as in DNA). Analysis can therefore be done as needed
    without loaded all object data memory up front.
    """

    family = {}

    def __new__(cls, name, family_id):
        try:
            id = cls.family[family_id]
        except KeyError:
            id = object.__new__(cls)
            cls.family[family_id] = id
        return id

    def set_genetic_info(self, genetic_info):
        cg = ComplexGenetics()
        self.genetic_info = cg.genes(genetic_info)

    def get_genetic_info(self):
        return (self.genetic_info)

#------------------------------------------------------------------------------
# Client Code


def main():

    family_objects = []
    data = (('a', 1, 'ATAG'), ('a', 2, 'AAGT'), ('b', 1, 'ATAG'))

    for i in data:
        # get the 'majority' of an objects state for a particular family
        obj = Families(i[0], i[1])
        # procedurally complete the object with the extrinsic state
        obj.set_genetic_info(i[2])
        # only use the objects data we need
        family_objects.append(obj)

    for i in family_objects:
        print "id = " + str(id(i))
        print i.get_genetic_info()

    print("We are unlikely to be able to decode a massive string to compare.")
    print("However, the object id tells us we are dealing with the same object.")


#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
