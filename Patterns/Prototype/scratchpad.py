

#class Employee:  # python 3
#    TypeError: must be type, not classobj
class Employee(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class SalaryEmployee(Employee):
    def __init__(self, id, name, weekly_salary):
        #super().__init__(id, name)  # python3
        #    super().__init__(id, name)
        #    TypeError: super() takes at least 1 argument (0 given)
        super(SalaryEmployee, self).__init__(id, name)  # python2
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyEmployee(Employee):
    def __init__(self, id, name, hours_worked, hour_rate):
        #super().__init__(id, name)  # python3
        #    super().__init__(id, name)
        #    TypeError: super() takes at least 1 argument (0 given)
        super(HourlyEmployee, self).__init__(id, name)  # python2
        self.hours_worked = hours_worked
        self.hour_rate = hour_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hour_rate


class CommissionEmployee(SalaryEmployee):
    def __init__(self, id, name, weekly_salary, commission):
        #super().__init__(id, name, weekly_salary)  # python3
        super(CommissionEmployee, self).__init__(id, name, weekly_salary)
        self.commission = commission

    def calculate_payroll(self):
        #fixed = super().calculate_payroll()  # python3
        fixed = super(CommissionEmployee, self).calculate_payroll()  # python2
        return fixed + self.commission


#------------------------------------------------------------------------------


# descriptors.py
class Verbose_attribute():
    """ implements the descriptor prototcol
    one instanciated as an attribute of a class it can be considered a descriptor
    as a descriptor, it has binding behavior when accessed using dot notation

    self is the instance fo the descriptor
    obj is the instance of the object your descriptor is attached to
    type is type of the object the descriptor is attached to

    __set__ doesnt have a type variable because you can only call __set__
    on the object. you can call __get__ on both the object and the class

    descriptors are instantiated just once per class: Every instacne of a class
    containing a descriptor shares that descriptor instance.
    """
    def __get__(self, obj, type=None):
        print("accessing the attribute to get the value")
        return 42

    def __set__(self, obj, value):
        print("accessing the attribute to set the value")
        # the recommended way to implement read only descriptors
        raise AttributeError("Cannot change the value")


class Foo():
    attribute1 = Verbose_attribute()


my_foo_object = Foo()
x = my_foo_object.attribute1
print(x)
x



class Foo2():
    """ Accomplishes the same thing, without implementing special dunders """
    def getter(self):
        print("accessing the attribute to get the value")
        return 42

    def setter(self, value):
        print("accessing the attribute to set the value")
        raise AttributeError("Cannot change the value")

    attribute1 = property(getter, setter)


my_foo_object = Foo2()
x = my_foo_object.attribute1
print(x)


class Foo3():
    """ Also the same thing, using property decorator syntactic sugar """
    @property
    def attribute1(self):
        print("accessing the attribute to get the value")
        return 42

    @attribute1.setter
    def attribute1(self, value):
        print("accessing the attribute to set the value")
        raise AttributeError("Cannot change the value")


my_foo_object = Foo3()
x = my_foo_object.attribute1
print(x)
# print my_foo_object.attribute1()


class Foo5():
    def __init__(self):
        self._spam = 0

    @property
    def spam(self):
        print("in the getter: ")
        return self._spam

    @spam.setter
    def spam(self, move):
        print("in the setter: ")
        self._spam = move + self._spam


f = Foo5()
print(f.spam)
print("----")
f.spam = 2
print("---set 2")
print(f.spam)
print("---")


class PayrollSystem:
    def calculate_payroll(self, employees):
        print('Calculating Payroll')
        print('===================')
        for employee in employees:
            #python3
            #print(f'Payroll for: {employee.id} - {employee.name}')
            #print(f'- Check amount: {employee.calculate_payroll()}')

            #python2
            print('Payroll for: {} - {}'.format(employee.id, employee.name))
            print('- Check amount: {}'.format(employee.calculate_payroll()))
            print('')


salary_employee = SalaryEmployee(1, 'John Smith', 1500)
hourly_employee = HourlyEmployee(2, 'Jane Doe', 40, 15)
commission_employee = CommissionEmployee(3, 'Kevin Bacon', 1000, 250)
payroll_system = PayrollSystem()

try:
    base = Employee(4, "Generic")
    print(base.name)
    print(base.name())
    base.name = "Generic_Employee"
    print(base.name())
    #base.id = 9999  # no setter
except Exception:
    pass

salary_employee = SalaryEmployee(1, 'John Smith', 1500)
hourly_employee = HourlyEmployee(2, 'Jane Doe', 40, 15)
commission_employee = CommissionEmployee(3, 'Kevin Bacon', 1000, 250)

payroll_system = PayrollSystem()
payroll_system.calculate_payroll([
    salary_employee,
    hourly_employee,
    commission_employee
])


print "------"


class Simple(object):  # new style, must inherit for property() in 2.7

    def __init__(self, var=5):
        # run variable check/set when instantiated if desired
        #self.__set_a(var)
        self.__any_private = var

    def __get_a(self):
        print("getting private variable 'a' (as far as the client knows it)")
        return self.__any_private

    def __set_a(self, var):
        print("setting private variable 'a' (as far as the client knows it)")
        self.__any_private = min(max(0, var), 100)

    a = property(__get_a, __set_a)


class Simple(object):

    def __init__(self, var=5):
        print("-- initializing with", var)
        #self.__any_private = var
        self.a = var  # THIS WILL CALL THE SETTERS VALIDATION CODE
        print("-- initializing done")

    @property
    def a(self):
        print("getting private variable 'a' (as far as the client knows it)")
        return self.__any_private

    @a.setter
    def a(self, var):
        print("setting private variable 'a' (as far as the client knows it)")
        self.__any_private = min(max(0, var), 100)


ref = Simple(-1)
print(ref.a)
ref.a = 7
print(ref.a)
#print ref.__any_private
# AttributeError: Simple instance has no attribute '__any_private'
print dir(ref)
print("Simple__any_private", ref._Simple__any_private)


#class Person: # with old style class setter will not work with property()
class Person(object):
    def __init__(self):
        self._protected_age = 0

    # function to get value of _age
    def get_age(self):
        print("getter method called")
        return self._protected_age

    # function to set value of _age
    def set_age(self, a):
        print("setter method called")
        if(a < 0):
            raise ValueError("Sorry, age cannot be a negative number")
        self._protected_age = a

    # function to delete _age attribute
    def del_age(self):
        del self._protected_age

    #  age is a property object that helps keep
    #  the access of private variables safe
    age = property(get_age, set_age, del_age)


#class Person: # with old style class setter will not work with property setter
class Person2(object):  # new style
    def __init__(self):
        self._protected_age = 0

    @property
    def age(self):
        print("getter method called")
        return self._protected_age

    @age.setter  # @method_name.setter | variable name could be anythign
    def age(self, a):
        print("setter method called", a)
        if(a < 0):
            raise ValueError("Sorry, age cannot be a negative number")
        self._protected_age = a

    @age.deleter
    def age(self):
        del self._protected_age


print("=====")
# client accesses the property object by name,  as if it were an instance
# variable, abstracting away the management of that variable inside
# the corresponding accessors

p = Person()
print dir(p)
print(p.age)
p.age = 10
print(p.age)
try:
    p.age = -1
except Exception:
    pass
print(p.age)

print("=====")



class Person(object):  # new style
    """
    initialize private variables dependent on an @property
    call the propery attribute in the constructor the same
    way as it would be by the client
    """
    def __init__(self, age=45):
        self.age = age

    @property  # only a getter, as value impiled by  @age.setter
    def kind(self):
        return self.__type

    @property  # get
    def age(self):
        print("getter method called")
        return self._protected_age

    @age.setter  # set explicit and implied instance variable
    def age(self, a):
        print("setter method called", a)

        assert isinstance(a, (int, float))
        if(a < 0):
            raise ValueError("Sorry, age cannot be a negative number")
        self._protected_age = a

        """ cant dict switch on ranges in python """
        if a > 0 and a < 2:
            self.__type = 'infant'
        elif a >= 2 and a < 4:
            self.__type = 'toddler'
        elif a >= 4 and a < 10:
            self.__type = 'child'
        elif a >= 10 and a < 12:
            self.__type = 'youth'
        elif a >= 12 and a < 20:
            self.__type = 'teen'
        elif a >= 20 and a < 65:
            self.__type = 'adult'
        else:
            self.__type = 'senior'


p = Person(44.5)
print(p.age)
print(p.kind)
p.age = 12
print(p.kind)
p.age = 121
print(p.kind)
try:
    p.age = "NOT A NUMBER"
except AssertionError as e:
    print("NAN", e)


print("=====")


class Sneaky(object):
    sneaky = True

    def __init__(self, sneaky=True, *args, **kwargs):
        super(Sneaky, self).__init__(*args, **kwargs)
        self.sneaky = sneaky

    def hide(self, light_level):
        return self.sneaky and light_level < 10


class Person(object):
    def __init__(self, human=True, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.human = human



class Thief(Sneaky, Person):
    def __init__(self, *args, **kwargs):
        super(Thief, self).__init__(*args, **kwargs)



t = Thief()
print(t.human)
print(Thief.mro())
# True

# unicode. add magic comment on first or second line
# parse unicode characters in a python source file
# -*- coding: utf-8 -*-
s = '\xe2\x99\xaf'
print(s)
s = u'\u2713'
print(s)




