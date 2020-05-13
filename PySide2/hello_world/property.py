"""
Simple Property Getter/Setter/Deleter Example

@property decorator allows properties to be defined without calling
the property() function manually. A decorator is a function that
receives another function as an argument allowing the behavior of
the funtion to be extended without actually modifying the function.

@property is a built-in decorator to define a method property in a
class to get a method attribute. @[property-name].setter is used to
set a property value, and @[property-name].deleter supports deletion
of a property with the del keyword.



> python
from property import Person
>>> p=Person()
>>> p.name='Steve'  ## Setter
>>> p.name          ## Getter
Steve
>>> del p.name      ## Deleter
Deleting..
>>> p.name
Traceback (most recent call last):
>>> p

"""

#------------------------------------------------------------------------------
# C++/Java control access to class resources by public private protected
# keywords. Python doesnt have a mechanism that restricts access to any
# instance variable or method, but prescribes a convention of prefixing
# private (__) and protected (_) members with underscores to emulate it.
# They can still be accessed, but doing so in your api suggests that a
# responsible programmer should refrain from accessing them.

""" PUBLIC INSTANCE  ATTRIBUTES
Can access these attributes an modify their values freely

> python
>>> from property import EmployeePublic
>>> e = EmployeePublic("Steve",50000)
>>> e.salary
50000
>>> e.salary = 10000
>>> e.salary
10000
"""


class EmployeePublic:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


""" PROTECTED INSTANCE ATTRIBUTES
Can access these attributes an modify their values but its use at the
toplevel of the class interface/API is frowned upon as they are intended
to be used internally by subclasses

> python
>>> from property import EmployeeProtected
>>> e = EmployeeProtected("Steve",50000)
>>> e._salary
50000
>>> e._salary = 10000
>>> e._salary
10000
"""


class EmployeeProtected:
    def __init__(self, name, salary):
        self._name = name
        self._salary = salary


""" PRIVATE INSTANCE ATTRIBUTES
Python performs NAME MANGLING on PRIVATE variables:
ie. every member with __ will be changed to _object._class__variable

This makes it harder still to access and modify member variables and values

>>> from property import EmployeePrivate
>>> p = EmployeePrivate("Steve",50000)
>>> p.__salary
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: EmployeePrivate instance has no attribute '__salary'
>>> p.__dict__
{'_EmployeePrivate__salary': 50000, '_EmployeePrivate__name': 'Steve'}
>>> p._EmployeePrivate__salary
50000
>>> p._EmployeePrivate__salary = 10000
>>> p._EmployeePrivate__salary
10000
"""


class EmployeePrivate:
    def __init__(self, name, salary):
        self.__name = name
        self.__salary = salary


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Traditional object oriented languages like C++/Java use properties in a class
# to encapsulate data, including getter and setter methods to access the
# encapsulated data -- which has access controlled.
# Having to write out the entire get/set methods every time you need to access
# properties is tedious, so it would be great if the get/set functions were
# called implicitly when accessing an attribute as they are with Java/C#
#
# This CAN be done using the built-in property() function: which provides an
# interface wrapping the get/set/delete functions to be called into an object
#   prop = property(getter, setter, deleter, docstring)
#
# This also ensures that the private attribute name is mangled
#
# NOTE:You must inherit from object in order for this work
#------------------------------------------------------------------------------

""" ENCAPSUALTED GETTER/SETTER PROPERTIES
> python
# NB: reloading a particular Class from a module
>>> import property
>>> reload(property)
<module 'property' from 'property.py'>
>>> from property import PersonProperty

>>> from property import PersonProperty
>>> p = PersonProperty()
>>> p.name
getname() called
''
>>> p.name = "Steve"
setname() called
>>> p.name
getname() called
'Steve'
>>> p.__dict__
{'_PersonProperty__name': 'Steve'}
>>> del p.name
delname() called
>>> p.name
getname() called
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "property.py", line 143, in getname
    return self.__name
AttributeError: 'PersonProperty' object has no attribute '_PersonProperty__name'
"""


class PersonProperty(object):
    def __init__(self, name=''):
        self.__name = name

    def getname(self):
        print('getname() called')
        return self.__name

    def setname(self, name):
        print('setname() called')
        self.__name = name

    def delname(self):
        print('delname() called')
        del self.__name

    name = property(getname, setname, delname, "I'm the 'name' property")


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# A Property decorator allows us to define properties without calling the
# property() function. IN GENERAL, a decorator is a function that recieves
# another function as an argument, so it can be extended without modifying it.
# Since functions are first-order objects in python, they can be passed as
# arguments to other functions and be returned from another function. functions
# can also be nested within other functions (inner functions like Java) and
# all of this combines to wrap a function into what is known as a decorator
#------------------------------------------------------------------------------


""" DEOCRATOR GETTER/SETTER Overloading

>>> from property import Person
>>> p = Person()
>>> p.name
Getting...
''
>>> p.name="Steve"
Setting...
>>> p.name
Getting...
'Steve'
>>> del p.name
Deleting...
>>> p.name
Getting...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "property.py", line 201, in name
    return self.__name
AttributeError: 'Person' object has no attribute '_Person__name'
"""


class Person(object):
    def __init__(self, name=''):
        self.__name = name

    @property
    def name(self):
        print('Getting...')
        return self.__name

    @name.setter
    def name(self, value):
        print('Setting...')
        self.__name = value

    @name.deleter
    def name(self):
        print('Deleting...')
        del self.__name


""" CLASS METHOD DECORATOR
@classmethod can be applied on any method of a class.
This will allow us to call a method using the CLASS NAME instead of
the object -- tho you still can call it using an object.

The CLASS of the object instance is implicity passed as the first
 argument INSTEAD of self (the object instance).

A CLASS METHOD CANNOT MODIFY object INSTANCE STATE
(that would require a reference to self). HOWEVER,
A CLASS METHOD _CAN_ MODIFY CLASS STATE
(class variables that apply across all instances of the class)

> python
>>> from property import Car
>>> c1 = Car()
>>> c2 = Car()
>>> Car.num_cars()
Total Cars: 2
>>> c1.num_cars()
Total Cars: 2

"""


class Car(object):
    totalObjects = 0

    def __init__(self):
        Car.totalObjects = Car.totalObjects + 1

    @classmethod
    def num_cars(cls):
        print("Executing class method on {}".format(cls))
        print("Total Objects: ", cls.totalObjects)


""" STATIC METHOD DECORATOR
A Static method does NOT recieve any reference arguments whether it
is called by an instance of a class or the class itself. We can call
the method using the class name instead of the object or from an
object instance itself, but NO DATA is shared across instances.
Its just a regular function that can  accept regular arguments.

Note:
A STATIC METHOD CANNOT MODIFY object INSTANCE STATE __NOR__ can
A STATIC METHOD CANNOT MODIFY  CLASS STATE

They are primarily used as a way to namespace functions into a
class - for logical grouping/orginization - return enumarations
or constants, or perform some calculation given its arguments.

ANY INSTANCE OR THE CLASS IS FREE TO MODIFY the class variable
directly, just not via methods - except for a classmethod


>>> from property import Truck
>>> t1 = Truck()
>>> t2 = Truck()
>>> Truck.num_trucks()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "property.py", line 307, in num_trucks
    >>> t1 = Trucks(7)
NameError: global name 'totalObjects' is not defined
>>>

>>> from property import Trucks
>>> Trucks.__dict__
dict_proxy({'__dict__': <attribute '__dict__' of 'Trucks' objects>,
'__module__': 'property',
'_num_protected': 0,
'wheel_area': <staticmethod object at 0x7ff5af4e27c0>,
'_Trucks__num_private': 0,
'__weakref__': <attribute '__weakref__' of 'Trucks' objects>,
'num_public': 0,
'__init__': <function __init__ at 0x7ff5af53ef50>,
'__doc__': ' Class variables are mutable constants
'})
>>>
>>> Trucks.wheel_area(10)
('Total Wheel Area: ', 62.830000000000005)
>>> Trucks.num_public
0
>>> t1 = Trucks(7)
>>> t1.num_public
7
>>> t1._num_protected
70
>>> t1._Trucks__num_private
700
>>> t2 = Trucks(5)
>>> t2.num_public
5
>>> t1.num_public
50
>>> t1._Trucks__num_private
500

"""


class Truck(object):
    # class variable cant be modified by static methods
    # they go out of scope to those methods, not global
    totalObjects = 0

    def __init__(self):
        Truck.totalObjects = Car.totalObjects + 1

    @staticmethod
    def num_trucks():
        print ("Total Objects: ", totalObjects)


class Trucks(object):
    """ Class variables are mutable constants """
    num_public = 0
    _num_protected = 0
    __num_private = 0

    def __init__(self, num):
        Trucks.num_public = num
        Trucks._num_protected = num * 10
        Trucks.__num_private = num * 100

    @staticmethod
    def wheel_area(radius):
        print("Total Wheel Area: ", 2 * 3.1415 * radius)





