#------------------------------------------------------------------------------
# Factory Method | Creational Design Pattern
#------------------------------------------------------------------------------
# The Factory Method Design Pattern provides an interface for creating objects
# in a superclass, but allows subclasses to alter the type of objects that
# will be created.
#
# - Lets a class defer instantiation to its subclasses
# - Replaces direct object construction with calls to a special creator method
# - Objects returned by a factory method are commonly called "products"
# - The factory is recognizable by creator methods which instantiate objects
#   from concrete product classes, returning objects of an abstract type.
# - All products should follow the same interface, where the methods make sense
#   in every product. A common base class is convenient and instructive but
#   isnt absolutely necessary; each product must provide an implementation
# - A module can contain a standalone factory method, avoiding the need to
#   instantiate an object of the Creator/Factory class


#------------------------------------------------------------------------------
# Factory Products

class Button(object):
    """
    The Product base class.
    Defines an interface for all objects created by the Factory.
    All subclasses (concrete products) must implement this interface,
    overriding thier distinguishing attributes.
    """
    html = ""

    def get_html(self):
        return self.html


class Image(Button):
    html = "<img></img>"


class Input(Button):
    html = "<input></input>"


class Flash(Button):
    html = "<obj></obj>"


#------------------------------------------------------------------------------
# Factory Creators

def factory_button(b_type):
    """
    Module level 'Factory Method' implementation.
    Fine for simple examples but can be less flexible when requirements change
    """
    targetclass = b_type.capitalize()
    return globals()[targetclass]()


class ButtonFactory():
    """
    The Creator class
    Returns an object of a specified Product class
    """

    def create_button(self, b_type):
        """ The 'Factory Method' in the 'Creator' class"""
        targetclass = b_type.capitalize()
        return globals()[targetclass]()


""" Moudule level pre-bound Factory Method """
_button_factory = ButtonFactory()
create_button = _button_factory.create_button


#------------------------------------------------------------------------------


if __name__ == "__main__":

    buttons = ['image', 'input', 'flash']

    print("Creating Buttons with module level factory method:")
    for b in buttons:
        print(factory_button(b).get_html())

    print("Creating Buttons with ButtonFactory instance:")
    factory = ButtonFactory()
    for b in buttons:
        print(factory.create_button(b).get_html())

    print("Creating Buttons with module level pre-bound ButtonFactory method:")
    for b in buttons:
        print(create_button(b).get_html())

