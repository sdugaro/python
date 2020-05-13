# https://python-patterns.guide/gang-of-four/composite/

#------------------------------------------------------------------------------
# Composite | Structural Design Pattern
#------------------------------------------------------------------------------
#
# The Composite design pattern suggests that whenever you design container
# objects (composites) that colelct and organize content objects (leafs) you
# will simplify many operations if you give container objects AND content
# objects a shared set of methods. This supports as many operations as possible
# without the caller having to care whether they have been passed an individual
# content object or an entire container.
#
# - The Composite Pattern as its classically defined, has a superclass for
#   creating or enforcing symmetry between objects via inheritance such that
#   the flow of logic between object types is not dependent on if statements.
# - The benefits of the symmetry that the Composite Pattern creates between
#   containers and their contents only accrues if the symmetry allows for the
#   objects to be interchangeable.
# - Many statically typed languages impose that two different classes are only
#   interchangeable if they are subclasses of a parent class that implements
#   the methods they have in common.
# - Other statically typed languages require that two different classes conform
#   to an interface declaring exactly which methods they implmenent in common.
# - In Python, which is dynamically typed, these approaches are supported but
#   not enforced. This allows for the creation of symmetry among concentric
#   objects heirarchies to be reimagined. For instance, on the other side of
#   the spectrum, by leveraging duck typing.
# - Structural typing is a static typing system that determines type
#   compatibility by a type's structure at compile time. Duck typing exists
#   in dynamically typed systems where type compatibility is determined by only
#   the part of a types structure that is accessed at runtime. Again, python
#   supports structural typing through annotations, but it is not enforced.
# - In Python, objects can duck-type the interface, and then rely on tests to
#   help maintain symmetries between containers and contents. We dont really
#   need to use abstract base classes, inheritance, or explicit interfaces.
#   These formal design choices can benefit large sclae projects involving
#   multiple developers in order to make class dependency a bit more clear.
#   The idea behind duck typing is "if walks like a duck, talks like a duck,
#   and looks like a duck, then its probably a duck" resonates simply by the
#   fact that you can write a program to accomplish the same goals a bit more
#   loosely depending on the language. For instance Python does not have and
#   explicity interface keyword to enforce that all methods of the interface
#   need to be implemented; the class either implements some or all of the
#   methods in the 'conceptual interface' and does the work when called upon or
#   it doesnt. Its at that point when we can ascertain if an object is a duck.
# - Easier to ask for forgiveness than permission (EAFP): This common Python
#   coding style assumes the existence of valid keys or attributes and catches
#   exceptions if the assumption proves false. This clean and fast style is
#   characterized by the presence of many try and except statements. With duck
#   typing we neither ask for permission or forgiveness.

import copy

#------------------------------------------------------------------------------

"""
NB: that in Py2k, not inheriting from object will create an 'old-style' class
which up until Python2.1, was the only flavour available. The concept of an
'old-style' class is unrelated to the concept of type: If x is an instance of an
'old-style' class, then x.__class__ degignates teh class of x, but type(x) is
always <type 'instance'>. This means all old style instances, independent of
their class, are implemented with a single built-in type called instance.

A 'new-style' class is simply a user defined type, introduced in Python2.2 to
unify classes and types (providing a new unified object model with a full meta
model): If x is an instance of a 'new-style' class then x__class__ is the same
as type(x). This allowed for a number of immediate benefits like the ability to
subclass most built-in types, make use of descriptors and properties, and
better support multiple inheritance.

In Py2k, classes are 'old-style' by default, and made 'new-style' by explicitly
inheriting from the 'top-level type' "object": MyNewStyleClass(object). To
engage the 'new(er)-style' language features of Python, classes must ultimately
inherit from "object",  Hence 'everything in Python is an object'.

In Py3k, classes implicily inherit from "object" and need not be explicit.

Here we do not make use of the new(er) style language features as the focus is
on a less restrictive implementation, and so intentionally avoid inheriting from
the 'top-level object type'.
"""


class Content:
    """
    Represent leaf objects in the composition tree. A leaf has no children.
    A Leaf defines behavior for primitive objects in the composition tree.
    Typically the leaf objects do the actual work or store some final data,
    as they are the end of the traversal path.
    """

    def __init__(self, name):
        self._name = name
        self._level = 0
        self._parent = None

    def __repr__(self):
        return "Content({}):{}".format(self._name, self._level)

    def _levelup(self):
        """
        _protected method implementation required to terminate recursion at leaf
        nodes of the tree. looks like a duck.
        """
        return

    #--------------------------------------------------------------------------

    def operation(self):
        """ implement the required part of the conceptual interface """
        fmt = '{}|- {} \033[32m*\033[0m'
        print(fmt.format('|  ' * self._level, self._name))
        # Payload some data


class Container:
    """
    Duck typing allows us to set parents
            # basic type checking can still be enforced without
            # structural typing impositions via annotations or other.
    """

    def __init__(self, name, children=[]):
        self._name = name
        self._level = 0
        self._parent = None
        self._children = []
        #print self._name, self._children, "<<< Initialized"

    def __repr__(self):
        return "Container({}):{}".format(self._name, self._level)

    def _levelup(self):
        """
        _protected implies other classes can implement this method in their
        interface for inter-object communication, without formal theory or
        language syntax. Walk like a duck, talk like a duck. A dunder defined
        method gets name-mangled to include the class name to prevent this as
        a __private method or variable implies exclusivity to the class.
        """
        for c in self._children:
            c._level = self._level + 1
            c._levelup()

    #--------------------------------------------------------------------------
    def viz(self):
        """
        Recursively print the the contents of this Branch for debugging. Note
        that we can avoid implementing viz() in Content because we are aware
        this implementation considers it a leaf which wont recurse any further.
        The Container generalizes this by leveraging the built-in hasattr()
        method to consider any object that does not implement viz() to be a
        terminator. We can assert that only objects we know of have been added
        as our children, so it is safe to assume that we will only be recursing
        on Container objects through this one and only implementatino of viz().
        """
        print('{}{}'.format('-' * self._level, repr(self)))
        for c in self._children:
            if hasattr(c, 'viz'):
                c.viz()
            else:
                print("{}{}".format("-" * c._level, repr(c)))

    def add(self, obj):
        assert isinstance(obj, (Container, Content)), (
            "[{}] is an unexpected type".format(obj))

        if obj in self._children:
            print("[{}] is already a child. Skipping.".format(obj._name))
            return

        if obj._parent is not None:
            print("[{}] already parented. Replicating heirarchy".format(obj._name))
            obj = copy.deepcopy(obj)

        self._children.append(obj)
        obj._parent = self
        self._levelup()
        #print self._children, "<---- added"

    def remove(self, obj):
        self._children.remove(obj)
        obj._parent = None  # kill reference for garbage collection

    def operation(self):
        print('{}|- {}'.format('|  ' * self._level, self._name))
        for child in self._children:
            child.operation()


#------------------------------------------------------------------------------
# Client Code

def build_tree():
    """
    The tree structure needs to be built up before it can be traversed.
    This example provides a clear metaphor for the Composite Pattern where
    content can be organized neatly in a box that can be packaged with other
    boxes of content.
    """

    drill = Content("Drill")
    screws = Content("Screws")
    branch1 = Container("Drill Box")
    branch1.add(drill)
    branch1.add(screws)

    branch2 = Container("Hammer Box")
    branch2.add(Content("Hammer"))
    branch2.add(Content("Nails"))
    branch2.viz()

    branch3 = Container("Paint Brush Box")
    branch3.add(Content("Roller"))
    branch3.add(Content("Roller Brush"))
    branch3.add(Content('1" Brush'))
    branch3.add(Content('2" Brush'))

    branch4 = Container("Paint Box")
    branch4.add(Content("Primer"))
    branch4.add(Content("Paint"))
    branch4.add(branch3)
    branch4.viz()

    tree = Container("Tool Box")
    tree.add(branch1)
    tree.add(branch2)
    tree.add(branch2)  # duplicate; already added, skipped
    tree.add(branch3)  # already has a parent, copied with new id
    tree.add(branch4)

    tree._children[3].remove(branch3)  # moved brush box up from paint box

    return tree


def main():

    root = build_tree()
    root.operation()


#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
