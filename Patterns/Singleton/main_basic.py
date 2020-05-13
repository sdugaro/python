#------------------------------------------------------------------------------
# Singleton | Creational Design Pattern
#------------------------------------------------------------------------------
# The Singleton Design Pattern ensures that a class has only 1 instance, while
# providing a global access point to this instance.
#
# It can be recognized by its static creation method, returning the cached
# instance
#
# Considered a 'Python Anti-Pattern' as it can be hard to refactor, rare that
# only 1 object will exist ofver a projects lifetime, can introduce unnecssary
# restrictions when a sole instance of a class is not actually required, hides
# dependencies, hard to subclass, and they introduces global state. INSTEAD,
# instantiate a single instance and propogate it as a parameter where needed.
#
# Note that comparisons with None should use the 'is' operator rather than '=='
# as it is faster and more predictable. The 'is' operator compares object
# identity, where there is only 1 None Object. Whereas, '==' compares object
# equivalence, which is defined from object to object, and can depend on the
# the exact type and ordering of the operands. This is especially true when
# comparing Singleton Objects


class Singleton:
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if Singleton.__instance is not None:
            raise Exception("An instance of the object exists. Use getInstance()")
        else:
            Singleton.__instance = self

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance is None:
            return Singleton()
        return Singleton.__instance


#------------------------------------------------------------------------------
# Observe that each object has the same memory location

if __name__ == "__main__":

    s = Singleton()
    print(s)

    s = Singleton.getInstance()
    print(s)

    s = Singleton.getInstance()
    print(s)

    t = Singleton.getInstance()
    print(t)

    u = Singleton()
    print(u)

