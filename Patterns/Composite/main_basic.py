#------------------------------------------------------------------------------
# Composite | Structural Design Pattern
#------------------------------------------------------------------------------
#
# The Composite design pattern lets you compose objects into tree structures
# and then work with these structures as if they were individual objects.
#
# - tree structures are ideal for representing heirarchies in part or whole
# - clients treat individual objects and compositions of objects uniformly
# - actual objects are at the leaves of trees, compositions of objects are
#   at the branch roots, while the entire tree/object/package is the root.
# - methods are run recursively over the whole tree or a branch in order to
#   accumilate data in the traversal path.
#


import abc

#------------------------------------------------------------------------------


#class Component(metaclass=abc.ABCMeta):  # Py3k
class Component(object):
    """
    The base Component class declares common operations for both simple and
    complex objects of a composition. Parent accessors define the path for
    tree traversal, and specifying these through property decorators is a good
    way to protect and validate.
    """

    __metaclass__ = abc.ABCMeta  # Py2k

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def add(self, component):
        pass

    def remove(self, component):
        pass

    def is_composite(self):
        """
        Specify whether or not a tree node can have children. This is assumed
        False (inherited by Leaf nodes) unless implemented to return True.
        """
        return False

    @abc.abstractmethod
    def operation(self):
        """
        The @abstractmethod decorator insists that concrete subclasses provide
        and implementation of this method.
        """
        pass


class Leaf(Component):
    """
    Represent leaf objects in the composition tree. A leaf has no children.
    A Leaf defines behavior for primitive objects in the composition tree.
    Typically the leaf objects do the actual work or store some final data,
    as they are the end of the traversal path.
    """

    def operation(self):
        return "LEAF"


class Composite(Component):
    """
    Define behavior for components having children. Rather than allow for the
    base class to store child components and implement tree traversal logic we
    implement it here in tandem with accumilating results through each Composite
    and leaf operation(). Usually Composite objects delegate the actual work to
    their children.
    """

    def __init__(self):
        self._children = []

    def add(self, component):
        self._children.append(component)
        component.parent = self

    def remove(self, component):
        self._children.remove(component)
        component.parent = None

    def is_composite(self):
        return True

    def operation(self):
        """
        Depth First Search Traversal: each child runs its operation, and should
        that child be another Composite, its list of children operations are
        processed L->R.
        """

        results = []
        for child in self._children:
            results.append(child.operation())
        return "Branch({})".format('+'.join(results))


#------------------------------------------------------------------------------
# Client Code

def build_tree():
    """
    The tree structure needs to be built up before it can be traversed.
    """

    branch1 = Composite()
    branch1.add(Leaf())
    branch1.add(Leaf())

    branch2 = Composite()
    branch2.add(Leaf())
    branch2.add(Leaf())

    branch3 = Composite()
    branch3.add(Leaf())
    branch3.add(Leaf())

    branch4 = Composite()
    branch4.add(Leaf())
    branch4.add(Leaf())
    branch4.add(branch3)

    tree = Composite()
    tree.add(branch1)
    tree.add(branch2)
    tree.add(branch4)

    return tree


def main():

    root = build_tree()
    print(root.operation())


#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
