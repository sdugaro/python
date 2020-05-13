# https://python-patterns.guide/python/module-globals/
# https://python-patterns.guide/python/sentinel-object/
#
#------------------------------------------------------------------------------
# Sentinel Object | Pythonic Global Object Creational Design Pattern
#------------------------------------------------------------------------------
# A sentinel object() can be used to indicate missing or unspecified data.
# Patterns are needed for cases where object attributes or whole objects go
# missing or are not available, so as to distinguish useful data from
# placeholders that indicate data is absent.
#
# - Sentinal := a guard whose job is to stand and keep watch
# - A sentinal value is a value similar to other return values that has a
#   special meaning agreed upon ahead of time; a default initializer.
# - Using an empty string as an initilizer allows one to continue to use string
#   operatons on the object disregarding issues of exisistence or type
# - Every name in Python either doesn't exist, or exists and refers to an
#   object. You can remove a name or assign a new object to it - Python offers
#   no other alternatives. Behind the scenes, each name in python is a pointer
#   that stores the address of the object to which it refers with a counter for
#   garbage collection. Even a name pointing to None contains a valid address.
#   At the lowest level this name is a C pointer holding the address of an
#   object, but C, unlike Python  makes no gurantee a pointer holds the address
#   of a valid object; it could point to 0 or NULL (the sentinel value). When
#   NULL is not checked before being used, a program will segfault.
# - None and False are objects with non-zero adresses, but other "Null Objects"
#   can be defined to represent a blank or non-existent value.
# - Avoid having to constantly check if an object is None before invoking
#   methods on it by replacing None iwth an object specifically designed to
#   represent the idea of "No One"


from datetime import datetime


SENTINEL = object()


class NoManager(object):
    name = 'No Manager'


class Person(object):
    #def __init__(self, name, manager=SENTINEL):
    def __init__(self, name, manager=NoManager):
        self.__name = name
        self.__manager = manager

        # inefficient to hold a unique memory location for each instance
        #self.__manager = NoManager() if manager is None else manager

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def manager(self):
        #if self.__manager is SENTINEL:
        #   return "NOBODY"
        return self.__manager.name

    @manager.setter
    def manager(self, name):
        self.__manager.name = name


EMPLOYEE_DATA = "EMPLOYEE [{:>15}] MANAGER [{:<15}]"

#------------------------------------------------------------------------------

if __name__ == "__main__":

    """ Define some employees with or without managers.
    Display all employees and their managers with uniform iteration.
    """

    gm = Person("Mario Lemieux")
    coach = Person("Dan Bylsma", gm)
    p1 = Person("Sidney Crosby", coach)
    p2 = Person("Evengy Malkin", coach)
    p3 = Person("Kris Letang", coach)
    p4 = Person("Phil Kessel", coach)
    employees = [gm, coach, p1, p2, p3, p4]

    date = datetime(2014, 6, 6, 12, 12)
    print(date)
    for e in employees:
        print(EMPLOYEE_DATA.format(e.name, e.manager))

    date = datetime(2015, 12, 12, 6, 6)
    coach.name = "Mike Sullivan"  # change of management
    print(date)
    for e in employees:
        print(EMPLOYEE_DATA.format(e.name, e.manager))

    date = datetime(2019, 6, 29, 8, 1)
    employees.remove(p4)

    date = datetime(2020, 02, 24, 1, 1)
    employees.append(Person("Patrick Marleau", coach))
    print(date)
    for e in employees:
        print(EMPLOYEE_DATA.format(e.name, e.manager))



