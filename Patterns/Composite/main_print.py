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

import copy

#------------------------------------------------------------------------------


class Node(object):
    """
    The base class representing a node in a tree heirarchy. A Node in a tree
    heirarchy can be a branch (container) which has children or a leaf that
    has no children (but some specific content). Defining the child-management
    operations in the base class abstracts the logic away from concrete
    subclasses where traversal code is supported, but does not overcrowd the
    subclass with its own (possibly redundant) implementation. A base traversal
    implementation can still be overridden by a subclass if it needs to behave
    differently, which is likely the case for leaf nodes in a tree structure.
    """

    def __init__(self, name, children=[]):
        self._level = 0
        self._name = name
        self._parent = None
        self._children = set()   # does not maintain insertion order

        for child in children:
            # while we could print and continue, lets raise and stop
            assert isinstance(child, Node), (
                '[{}] is not of type Node'.format(child))
            self._children.add(child)
            self._levelup()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        assert isinstance(parent, Node), (
            '[{}] is not of type Node'.format(parent))
        self._parent = parent

    def _levelup(self):
        for c in self._children:
            c._level = self._level + 1
            c._levelup()

    def add(self, node):
        self._children.add(node)

    def remove(self, node):
        """ if node isnt a Node, it wont be found in our children list """
        self._children.discard(node)
        pass

    def is_branch(self):
        return False

    def operation(self):
        """ Default behavior of the operation defined in the base class """

        print('{}|- {}'.format('|  ' * self._level, self._name))
        for child in self._children:
            child.operation()


class Content(Node):
    """
    Represent leaf objects in the composition tree. A leaf has no children.
    A Leaf defines behavior for primitive objects in the composition tree.
    Typically the leaf objects do the heavy lifting such as loading payload
    data into memory that isnt required until that heavier data is actually
    needed or requested.
    """

    def __init__(self, name):
        super(Content, self).__init__(name, children=[])

    def operation(self):
        """ Override the default operation behavior for this subclass
        """
        fmt = '{}|- {} \033[32m*\033[0m'
        print(fmt.format('|  ' * self._level, self._name))
        # Payload some data


class Container(Node):
    """
    The container can contain some lightweight meta data to be accumilated
    as opposed to the Content which will hold some heavier payload data,
    such as geometry caches, images, etc.. This means very little memory
    overhead is needed to navigate the heirarchy and delegate the final
    operations further down the tree. (viz usd)
    """

    def __init__(self, name, children=[]):
        super(Container, self).__init__(name, children)

    def add(self, component):
        assert isinstance(component, Node), (
            '[{}] is not of type Node'.format(component))

        if component in self._children:
            print("[{}] is already a child. Skipping.".format(component._name))
            return

        if component.parent is not None:
            print("[{}] already parented. Replicating heirarchy".format(component._name))
            component = copy.deepcopy(component)

        super(Container, self).add(component)
        component.parent = self
        self._levelup()

    def remove(self, component):
        component.parent = None  # garbage collect if no other ref to object
        super(Container, self).remove(component)

    def is_branch(self):
        return True


#------------------------------------------------------------------------------
# Client Code

def build_tree():
    """
    The tree structure needs to be built up before it can be traversed.
    This example provides a clear metaphor for the Composite Pattern where
    content can be organized neatly in a box that can be packaged with other
    boxes of content.
    """

    branch1 = Container("Drill Box")
    branch1.add(Content("Drill"))
    branch1.add(Content("Screws"))

    branch2 = Container("Hammer Box")
    branch2.add(Content("Hammer"))
    branch2.add(Content("Nails"))

    branch3 = Container("Paint Brush Box")
    branch3.add(Content("Roller"))
    branch3.add(Content("Roller Brush"))
    branch3.add(Content('1" Brush'))
    branch3.add(Content('2" Brush'))

    branch4 = Container("Paint Box")
    branch4.add(Content("Primer"))
    branch4.add(Content("Paint"))
    branch4.add(branch3)

    tree = Container("Tool Box")
    tree.add(branch1)
    tree.add(branch2)
    tree.add(branch2)  # duplicate; already added, skipped
    tree.add(branch3)  # already has a parent, copied
    tree.add(branch4)

    return tree


def build_tree2():
    """
    Inline tree build via initializer, using the baseclass.
    This would not be possible with @abstractmethod enforcement
    """

    tree = Node("Root", [
        Node("Node 1", [
            Node("Node 1.1", [
                Node("Node 1.1.1", [
                    Node("Node 1.1.1.1"),
                    Node("Node 1.1.1.2"),
                ]),
            ]),
            Node("Node 1.2"),
            Node("Node 1.3", [
                Node("Node 1.3.1")
            ]),
            Node("Node 1.4", [
                Node("Node 1.4.1"),
                Node("Node 1.4.2", [
                    Node("Node 1.4.2.1"),
                    Node("Node 1.4.2.2", [
                        Node("Node 1.4.2.2.1"),
                    ]),
                ]),
            ]),
        ]),
        Node("Node 2", [
            Node("Node 2.1"),
            Node("Node 2.2"),
        ]),
        Node("Node 3"),
    ])

    return tree


def main():

    print("\033[32mBuilding Tree....\033[0m")
    #root = build_tree2()
    root = build_tree()
    print("\033[32mDone.\033[0m")
    root.operation()


#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
