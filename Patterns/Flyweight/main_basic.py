#------------------------------------------------------------------------------
# Flywieght | Structural Design Pattern
#------------------------------------------------------------------------------
# The flyweight pattern allows you to fit more objects into ram by sharing
# common parts of state between multiple objects isntead of keeping all the
# data in each object. Programs can support vast numbers of objects by keeping
# their memory consumption low since data shared by objects is cached.
#
# - They Flyweight Pattern is sometimes known as the Cache Pattern.
# - The constant data of an objects is commonly called the intrinsic state,
#   it lives within the object, other objects can read it but not change it.
# - The rest of an object's state, often altered by other objects from the
#   outside is called the extrinsic state.
# - The flyweight pattern suggests to stop storing the extrinsic state inside
#   the object, instead pass the state to the specific methods that rely on it.
# - When only the instrisic state stays within the object, it can be reused in
#   different contexts, which tends to reduce the number of objects needed.
# - In most cases, the extrinsic state gets moved to the container object which
#   aggregates objects before applying the flyweight pattern. Alternatively, a
#   separate context class would store the extrinsic state along with a
#   reference to the lfywieght object.
# - The most memory consuming fields are moved to a few flyweight objects, such
#   that many small contextual objects can resuse a single heavy flyweight
#   object instead of many copies of the data.
# - Immutability is important. Since the same flyweight object can be used in
#   different contexts, you have to make sure its state cant be modified
# - A flyweight objcet should initialize its state just once, and not expose
#   any public fields or setters to other objects.
# - A Flyweight factory can be used to provide access to various flyweights,
#   perhaps managing a cache pool.
# - If your program isn't RAM heavy this pattern may be superfluous.


import abc
import six

from random import randint


#------------------------------------------------------------------------------

class FlyweightFactory:
    """
    Create and manage flyweight objects and ensure they are shared properly.
    When a client requests a flyweight, the FlyweightFactory object supplies
    an existing instance from a cachepool or creates one, if none for the pool.
    """

    def __init__(self):
        self._flyweights = {}

    def get_flyweight(self, key):
        try:
            flyweight = self._flyweights[key]
        except KeyError:
            flyweight = ConcreteFlyweight(key, randint(1, 99))
            self._flyweights[key] = flyweight
        return flyweight


#------------------------------------------------------------------------------

@six.add_metaclass(abc.ABCMeta)
#class Flyweight(metaclass=abc.ABCMeta):
class Flyweight():
    """
    Declare an interface through which flyweights can receive and act on
    extrinsic state. Note that the shared intrinsic state is initialized once
    and no setters or public attributes exist.
    """

    def __init__(self, one_time_intrinsic):
        self._intrinsic_state = one_time_intrinsic

    @abc.abstractmethod
    def operation(self, extrinsic_state):
        pass


class ConcreteFlyweight(Flyweight):
    """
    Implement the Flyweight interface and add storage for intrinsic state.
    A ConcreteFlyweight object must be sharable. Any state it stores must be
    independent of the ConcreteFlyweight object's context.
    """

    def __init__(self, name, state):
        self._name = name
        self._intrinsic_state = state

    def operation(self, extrinsic_state):

        result = extrinsic_state + self._intrinsic_state
        print("FlyWeight[{}|{}] + extrinsic arg[{}] = {}".format(
            self._name, self._intrinsic_state,
            extrinsic_state, result))


#------------------------------------------------------------------------------

def main():
    flyweight_factory = FlyweightFactory()
    concrete_flyweight = flyweight_factory.get_flyweight("key")
    concrete_flyweight.operation(100)

    concrete_flyweight = flyweight_factory.get_flyweight("one")
    concrete_flyweight.operation(10000)

    concrete_flyweight = flyweight_factory.get_flyweight("key")
    concrete_flyweight.operation(1000000)


if __name__ == "__main__":
    main()
