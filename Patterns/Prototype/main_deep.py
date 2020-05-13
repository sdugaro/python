#------------------------------------------------------------------------------
# Prototype | Creational Design Pattern
#------------------------------------------------------------------------------
#
# Create a clone of a existing object so it can be modified independently of
# of the original object. The original object is left untouched so multiple
# clones can be made.
#
# - Python provides its own interface of Prototype via the copy.copy() and
#   copy.deepcopy() functions, so building a framework to implement this pattern
#   is by-en-large redundant.
# - Python's copy module is intended for use with mutable objects so they can
#   be cloned (ie. modify the clone without affecting the original).
# - when using the copy module it is important to be aware that copy.copy()
#   performs a Shallow Copy, meaning the children of the toplevel object
#   maintain their original references, while a copy.deepcopy() performs a
#   Deep Copy, meaning that children recursively get new references.
# - Depending on the complexity of the objects (ie whether or not they are
#   composed other objects) a copy.copy() or copy.deepcopy() should be used
#   judiciously. Note there is no difference between the two when it comes
#  to
#   immutable types (such as int, float, str, etc)
# - Pythons built-in mutable collections (list, dict, sets) can be shallow
#   copied by calling their factory functions on an existing collection. The
#   tuple() factory function also performs a shallow copy, even though tuples
#   are not mutalbe. However, tuple children can be mutable such as a tuple of
#   lists. Editing an mutalbe entry of a source or clones mutalbe children will
#   change the data in both objects since the child reference in a shallow copy
#   still point to original objects memory location. Note that dicts and sets
#   also have a .copy() method in their apis for performing a shallow copy.
# - clone = copy.deepcopy(prototype) leaves obj alone so clone can be mutated.
# - Any class that wants to implement custom copy operations should override
#   the __copy__ and __deepcopy__ dunder methods
# - Every object instance in Pytyhon has a __dict__ attribute for storing
#   attribute/value pairs set on the object instance. Instance variables set on
#   a class via __init__ or dynamically at runtime are maintained in the
#   __dict__ of the specific object instance. Class variables set once at class
#   definition time are set in the __dict__ of the Class definition object.
# - Since classes are first class callable objects in Python there are several
#   ways they can be invoked. Like the __dict__ dunder of attribute and value
#   mappings maintained in every object, the class definition is maintained
#   in an object's self.__class__ dunder. Internally, this allows a class
#   to reference its own class definition and invoke itself as a callable,
#   in other words, clone itself.


import copy
from pprint import pformat

#------------------------------------------------------------------------------


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point({},{})".format(self.x, self.y)


class Rectangle(object):
    def __init__(self, bottomleft, topright):
        self.bl = bottomleft
        self.tr = topright

    def __repr__(self):
        return "Rectangle({},{})".format(self.bl, self.tr)


class Circle(Point):
    def __init__(self, p, r):
        super(Circle, self).__init__(p.x, p.y)
        self.p = p
        self.r = r

    def __repr__(self):
        return "Circle({}, {})".format(self.p, self.r)



class SelfReference(object):
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def __repr__(self):
        return "SelfReference({})".format(self.parent)


class Composite:
    """ Composite class made up of various components """

    def __init__(self, id, obj_list, rectangle, circular_ref):
        self._id = id
        self._obj_list = obj_list
        self.rectangle = rectangle
        self._circular_ref = circular_ref

    def __copy__(self):
        """
        Implelement Shallow Copy. This method will be invoked when copy.copy()
        is called on this object, where the returned value is the shallow copy

        Every object's class definition is maintained in its self.__class__
        dunder, which is a callable that can be used to create and allocate
        new instances. We clone ourselves a new instance by calling our class
        definition with the current state of our member variables. In the event
        that any additional instance variables were set on this object at
        runtime, we can copy those by updating our new instance variable
        __dict__. dict.update() will add source dict key/value pairs to the
        target dict if they do not exists in the target.
        """

        print("My Instance Variable State:")
        print(pformat(self.__dict__, indent=5))

        # class definition requires args to instantiate (no defaults)
        new = self.__class__(
            self._id, self._obj_list, self.rectangle, self._circular_ref
        )
        print("Clone Initialized:")
        print(pformat(new.__dict__, indent=5))
        print("Adding Runtime Instance Attributes:")
        new.__dict__.update(self.__dict__)
        print(pformat(new.__dict__, indent=5))

        # The new object has a new list of objects but with references
        # to the same objects. Thats the same as a shallow copy.
        #new._obj_list = copy.copy(self._obj_list)
        #new._circular_ref = copy.copy(self._circular_ref)

        return new

    def __deepcopy__(self, memo={}):
        """
        Implement Deep Copy. This method will be invoked when copy.deepcopy()
        is called on this object, where the returned value is the deep copy.
        """
        new = self.__class__(
            self._id, self._obj_list, self.rectangle, self._circular_ref
        )
        new.__dict__.update(self.__dict__)

        # deepcopy provides new reference to child objects recursively.
        # it uses the interface dictionary argument memo to store logic
        # while recursing. This ensures circular references do not cause
        # infinite recursion.
        new._obj_list = copy.deepcopy(self._obj_list, memo)
        new._circular_ref = copy.deepcopy(self._circular_ref, memo)
        return new


def main_custom():

    rect = Rectangle(Point(0, 0), Point(5, 5))
    obj_list = [1, {1, 2, 3, 3}, [1, 2, 3, 3], (1, 2, 3, 3)]
    circular_ref = SelfReference()
    prototype = Composite(23, obj_list, rect, circular_ref)
    prototype.USER = "NEW ATTRIBUTE SET ON INSTANCE"
    circular_ref.set_parent(prototype)

    print(75 * '-')
    # The Composite prototype implements __copy__ which
    # overrides copy.copy() logic when passed to it
    shallow_clone = copy.copy(prototype)
    shallow_clone._obj_list.append("SHALLOW CLONE ADDED STRING")
    shallow_clone.rectangle.bl.x = -999.999
    print("Shallow Clone appened to its _obj_list:")
    print("Shallow Clone modified rectangle")
    print(pformat(shallow_clone.__dict__, indent=2))
    print("This AFFECTS the prototype._obj_list:")
    print(pformat(prototype.__dict__, indent=2))

    prototype._obj_list[1].add(4)
    prototype.rectangle.tr.y = 1e6
    print("Prototype added to its _obj_list set:")
    print("Prototype modified rectangle:")
    print(pformat(prototype.__dict__, indent=2))
    print("THIS AFFECTS the shallow_clone._obj_list:")
    print(pformat(shallow_clone.__dict__, indent=2))

    print("\n{:^60}: {}".format(
        "id(shallow_clone._circular_ref.parent)",
        id(shallow_clone._circular_ref.parent)))
    print("{:^60}: {}".format(
        "id(shallow_clone__circular_ref.parent._circular_ref.parent)",
        id(shallow_clone._circular_ref.parent._circular_ref.parent)))
    print("Shallow Circular Reference wont copy")

    print(75 * '-')
    # The Composite prototype implements __deepcopy__ which
    # overrides copy.deepcopy() logic when passed to it
    deep_clone = copy.deepcopy(prototype)
    deep_clone._obj_list.append("DEEP CLONE ADDED STRING")
    deep_clone.rectangle.bl.x = -999.999
    print("Deep Clone appened to its _obj_list:")
    print("Deep Clone modified rectangle:")
    print(pformat(deep_clone.__dict__, indent=2))
    print("This DOES NOT AFFECT the prototype._obj_list:")
    print(pformat(prototype.__dict__, indent=2))

    prototype._obj_list[2][-1] = 4444
    prototype.rectangle.tr.y = 1e6
    print("Prototype modified its _obj_list list:")
    print("Prototype modified rectangle:")
    print(pformat(prototype.__dict__, indent=2))
    print("This DOES NOT AFFECT the deep_clone._obj_list:")
    print(pformat(deep_clone.__dict__, indent=2))

    print("\n{:^60}: {}".format(
        "id(deep_clone._circular_ref.parent)",
        id(deep_clone._circular_ref.parent)))
    print("{:^60}: {}".format(
        "id(deep_clone._circular_ref.parent._circular_ref.parent)",
        id(deep_clone._circular_ref.parent._circular_ref.parent)))
    print("Deep Circular Reference shares reference/points to same object")


def main_basic():

    xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("\n{}\n{}".format(xs, 20 * '-'))
    ys = copy.copy(xs)
    zs = copy.deepcopy(xs)
    ts = tuple(xs)
    ts[0][1] = 'SHALLOW'
    xs.append(['a', 'b', 'c'])
    for i in (xs, ys, zs, ts):
        print i, i[0][1] is xs[0][1]

    xr = Rectangle(Point(0, 0), Point(5, 5))
    print("\n{}\n{}".format(xr, 20 * '-'))
    yr = copy.copy(xr)
    zr = copy.deepcopy(xr)
    xr.tr.x = "SHALLOW"
    zr.tr.y = 999
    for i in (xr, yr, zr):
        print i, i.tr.x is xr.tr.x


    xc = Circle(Point(1, 1), 1)
    print("\n{}\n{}".format(xc, 20 * '-'))
    yc = copy.copy(xc)
    zc = copy.deepcopy(xc)
    xc.r = 100            # does not modify yc.r!
    zc.r = 999
    for i in (xc, yc, zc):
        print i, i.r is xc.r

    p = Point(0, 0)
    p.x = 1
    p.y = 1
    p.r = 100

    print(dir(p))
    print(dir(Point))
    print("Point Instance __dict__", p.__dict__)   # mutable dict
    print("Point Class __dict__", Point.__dict__)  # immutable dict


    class C(object):
        """ Class with no instance variables """
        x = 4  # global class variable set once in C.__dict__

    c = C()
    c.y = 5    # dynamic instance variable
    print("Instance variable _dict__ for Class with no instance attributes", c.__dict__)
    class_x = [item for item in C.__dict__.items() if 'x' in item]
    print("Class variable x in Class.__dict__", class_x)


#------------------------------------------------------------------------------

if __name__ == "__main__":
    #main_basic()
    main_custom()


