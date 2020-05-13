# https://python-patterns.guide/gang-of-four/flyweight/

#------------------------------------------------------------------------------
# Flywieght | Structural Design Pattern
#------------------------------------------------------------------------------
# The flyweight pattern provides a way to decrease object count and save ram.
# Space is saved by using the same immutable object everywhere its used in a
# program, instead of a potentially massive number of unique object instances.
#
# - A perfect fit for Python that the language itself uses the pattern for
#   identifiers, integers, booleansand strings.
# - Strings are natural candidates for the flyweight pattern because they have
#   all three of the key properties of a flyweight object.
#   1) strings are immutable so they are safe to share.
#   2) strings carry no context about how its being used.
#   3) a strings value > its object identity (compared with == instead of is)
# - GOF describe these properties in terms of extrinsic and intrinsic and
#   refactoring to separate the two kinds of state.
# - GOF only imagined using a factory function for managing a collection of
#   flyweights, but Python moves the logic into a class's constructor instead.
# - Python bool has exactly two instances True and False, which are returned
#   by their class when passed an object to test for truthfulness: bool('')
# - Python integers [-5,256] are flyweights, created ahead of time by the
#   interpreter, returned when one of these integers are needed.
# - Pythons empty string and empty tuple are also common immutable flyweights.
# - The simplest flyweights are allocated ahead of time
# - Others use factories that to build flyweight data dynamically. A dynamic
#   data structure (dictionary) is needed to cache and retrieve flyweights.
# - Memory can still be exhausted if the number of possible values is very large
#   and a large number of unique values are still requested over a programs
#   lifetime. The weakref modules WeakValueDictionary could help with this.
# - GOF defines the flywieght pattern as using a factory function, but Python
#   provides another option: a class can implement the pattern right in its
#   constructor, just like bool() or int()


#------------------------------------------------------------------------------
# Statically allocating flyweights ahead of time

"""
A grading system might use flyweights for the grades themselves though not
particularly heavy. The compute method takes an extrinsic percentage and
returns the appropriately unique flyweight object
"""

_grades = [letter + suffix
           for letter in 'ABCD'
           for suffix in ('+', '', '-')] + ['F']


def compute_grade(percent):
    percent = max(59, min(99, percent))
    return _grades[(99 - percent) * 3 // 10]



#------------------------------------------------------------------------------
# Dynamically allocating flyweights on demand

"""
A combination factory flyweight akin to the aforemention python type methods.

Once a Grade object has been created, all further requests for it receive the
same object, so the instances dictionary doesn't continue to grow.

Don't define __init__ in a class whose __new__ might return an existing object.
Python always calls __init__ on the object it recieves back from __new__ as
long as the object is an instance of the class itself. __init__ might be useful
the first time a flyweight object is returned, but it would be redundant on
subsequnt occaisions when we return the already initialized object.
Instead, do the initialization inside __new__.

This hides the flyweight Pattern factory inside of __new__, however it can be
a bit unexpected to not actually get a new object instance from a constructor
when one would expect to: Grade(95). The client may or may not care, but if
so and explicit factory can be used.
"""


class Grade(object):
    _instances = {}

    def __repr__(self):
        return 'Grade {!r}'.format(self.letter)

    def __new__(cls, percent):
        percent = max(50, min(99, percent))
        letter = 'FDCBA'[(percent - 50) // 10]  # index char string for key

        # check our hash table to see if they flyweight was already created.
        self = cls._instances.get(letter)
        if self is None:
            # define this instance and cache a new immutable flyweight
            self = cls._instances[letter] = object.__new__(Grade)
            self.letter = letter
        return self


#------------------------------------------------------------------------------
# Client Code

def main():

    print("\nNative python flyweights:\n{}".format(50 * '-'))

    """
    Passing an 'extrinsic' argument to the bool() constructor will return one of
    two values, True or False. The argument could be an object of any type and
    bool will return a value that represents truthfulness or emptyness/zeroness
    depending on how you look at it.
    """

    print(">>> bool(0)\n{}".format(bool(0)))
    print(">>> bool('')\n{}".format(bool('')))
    print(">>> bool(12)\n{}".format(bool(12)))

    """
    Since the first 256 integers are flyweight objects, operations can be done
    on unique integer objects that also return unique integer objects using a single
    byte of memory where there could be hundreds instead
    """

    print(">>> 1 + 4 is 2 + 3\n{}".format(1 + 4 is 2 + 3))
    print(">>> 1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1 is 25\n{}".format(
        1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1 is 25))
    print(">>> 100 + 400 is 200 + 300\n{}".format(100 + 400 is 200 + 300))

    print(">>> str() is ''\n{}".format(str() is ''))
    print(">>> tuple([]) is ()\n{}".format(tuple([]) is ()))


    """ Statically defined flyweights """

    print("\nStatic flyweights:\n{}".format(50 * '-'))
    print(compute_grade(55))
    print(compute_grade(89))
    print(compute_grade(90))

    """ Dynamically defined flyweights """

    print("\nDynamic flyweights:\n{}".format(50 * '-'))
    print(Grade(55), Grade(85), Grade(95), Grade(100))
    print(len(Grade._instances))    # number of instances
    print(Grade(95) is Grade(100))  # ask for A two more times
    print(len(Grade._instances))    # number stayed the same?


if __name__ == "__main__":
    main()



