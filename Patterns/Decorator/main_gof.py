# https://python-patterns.guide/gang-of-four/decorator-pattern/

#------------------------------------------------------------------------------
# Decorator | Structural Design Pattern
#------------------------------------------------------------------------------
#
# The purpose of Decorator Pattern is to add, remove, or adjust the behaviors
# that the wrapped object would normally implement when its methods are called.
#
# - The Decorator Pattern can be easier to implement in a dynamic language like
#   Python thatn in static languages where it was first practiced.
# - Use it on the rare occaision when you need to adjust the behavior of an
#   object that you cant subclass, but can only wrap at runtime.
# - Python2.4 introduced the unrelated term decorator, which do transform and
#   wrap methods, but is really just syntactic sugar than it is code design.
#   https://www.python.org/dev/peps/pep-0318/#id70
# - A Decorator class is a form of the "Adapter Pattern"
# - A Decorator class implements the same interface as the object it wraps
# - A Decorator class delegate method calls to the object it wraps.
# - Commonly used to log method calls, peform cleanup around a method,
#   pre-process method arguments, post-process return values, forbid actions
#   that the wrapped object would normally allow.
# - You can only solve a problem with a subclass when your code is in charge of
#   creating objects in the first place. A decorator class allows you to
#   intercept construction (object creation).
# - A 'static wrapper' implementation is what would be more commonly found in
#   heavyweight statically typed languages like c++/java which is more inline
#   with the classic GOF implementation based around languages of that era.
#   This imposes that every method and attribute literally appear on the page
#   = Every method of the adapted class, getter/setter/deleter for every
#   attribute. Conceptually simply, but a lot of code to navigate.
# - Pythons object model is dynamic and supports the idea that an attribute
#   might disappear from an instance, hence the need for a deleter as well.



import logging
# use a module level logger to track module heirarchy
logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


#------------------------------------------------------------------------------
# Traditional Decorator Pattern implemented in Python - Noticably Verbose
#

"""
Suppose one library provides open python file objects and they need to be
passed to another library, but you want to log each time data is written.
Typically file objects are use to read() and write() and not much else.
But the file object has more than a dozen methods and offers 5 different
attributes.
"""

class WriteLoggingFile1(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    # We need to implement every file method and in the truly general case
    # would need a getter, setter, and deleter for every single attribute!

    def __enter__(self):
        return self._file.__enter__()

    def __exit__(self, *excinfo):
        return self._file.__exit__(*excinfo)

    def __iter__(self):
        return self._file.__iter__()

    def __next__(self):
        return self._file.__next__()

    def __repr__(self):
        return self._file.__repr__()

    def close(self):
        return self._file.close()

    @property
    def closed(self):
        return self._file.closed

    @closed.setter
    def closed(self, value):
        self._file.closed = value

    @closed.deleter
    def closed(self):
        del self._file.closed

    @property
    def encoding(self):
        return self._file.encoding

    @encoding.setter
    def encoding(self, value):
        self._file.encoding = value

    @encoding.deleter
    def encoding(self):
        del self._file.encoding

    @property
    def errors(self):
        return self._file.errors

    @errors.setter
    def errors(self, value):
        self._file.errors = value

    @errors.deleter
    def errors(self):
        del self._file.errors

    def fileno(self):
        return self._file.fileno()

    def flush(self):
        return self._file.flush()

    def isatty(self):
        return self._file.isatty()

    @property
    def mode(self):
        return self._file.mode

    @mode.setter
    def mode(self, value):
        self._file.mode = value

    @mode.deleter
    def mode(self):
        del self._file.mode

    @property
    def name(self):
        return self._file.name

    @name.setter
    def name(self, value):
        self._file.name = value

    @name.deleter
    def name(self):
        del self._file.name

    @property
    def newlines(self):
        return self._file.newlines

    @newlines.setter
    def newlines(self, value):
        self._file.newlines = value

    @newlines.deleter
    def newlines(self):
        del self._file.newlines

    def read(self, *args):
        return self._file.read(*args)

    def readinto(self, buffer):
        return self._file.readinto(buffer)

    def readline(self, *args):
        return self._file.readline(*args)

    def readlines(self, *args):
        return self._file.readlines(*args)

    def seek(self, *args):
        return self._file.seek(*args)

    def tell(self):
        return self._file.tell()

    def truncate(self, *args):
        return self._file.truncate(*args)

    # Finally, we reach the two methods that we actually want to specialize!
    # These log each time data is written:

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)

#------------------------------------------------------------------------------
# Minimal Tactical Wrapper Implementation - Ignore anything that unused.
#

"""
Previous example tackled the python file object as a general example of a class
that needed to be wrapped instead of studying how file objects work and finding
shortcuts
- file objects are implemented in c and dont permit deletion of their attributes
so all deleters can be omitted without consequence. the default behavior of a
property in the absenece of a deleter is to disallow deletion.
- all file attributes except mode are read-only and eraise AttributeError if
assigned to - the behavior if a property lacks a setter method.
- a minimal wrapper is a bit dangerous and can fail if its used in ways that
dont implement everything as needed.

A routine that seems so happy with a minimal wrapper like this can suddenly fail
later if rare circumstances make it dig into methods or attributes that you never
implemented because you never saw it use them. Even if you audit the library’s 
code and are sure it can never call any method besides write(), that could change
the next time you upgrade the library to a new version.


- the author needs to draw the line between the pedantry of wrapping every
possible method and the danger of not wrapping enough



"""

# Tactical version of Decorator Pattern:
# what if you read the code, and the only thing
# the library really needs is the write() method?
# just ignore everything else.

class WriteLoggingFile2(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)

#------------------------------------------------------------------------------
# Dynamic Wrapper Implementation - Intercept live attributes
#

"""
a common approach to the Decorator Pattern in Python.
Instead of trying to implement a method and preoperty for every method and
attribute on the wrapped object, and dynamic wrapper intercepts live attribute
accesses as the program executes and responds by trying to access the same
attribute on the wrapped object.

A Dynamic wrapper implements teh dunder methods __getattr__() __setattr__() and
if it wants to be feature complete __delattr__(). Each of them responds by
performing the equivalent operation on the wrapped object.

__getattr__() is only invoked for attributes that are in face missing on the
wrapper - the wrapper is free to offer real implementations of any methods or
properties it wants to intercept. edge cases: if the wrapped object is iterable
then the basic operations iter() and next() will fail on the wrapper unless the
wrapper also implements __iter__() and __next__(). iter() and next() examing and
objects class for under methods instead of hitting the object directly with
__getattr__()


there is a minimal performance penalty for every attribute access, but the
economy and readability outweighs the tradeoff of writing a static wrapper.

These also offer insulation against changes that might happen in the future to
the object being wrapped. If the object adds or removes and attribute or method,
this implementation would require no change to its code at all !!


"""

# Dynamic version of Decorator Pattern: intercept live attributes

class WriteLoggingFile3(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    # The two methods we actually want to specialize,
    # to log each occasion on which data is written.

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)

    # Two methods we don't actually want to intercept,
    # but iter() and next() will be upset without them.

    def __iter__(self):
        return self.__dict__['_file'].__iter__()

    def __next__(self):
        return self.__dict__['_file'].__next__()

    # Offer every other method and property dynamically.

    def __getattr__(self, name):
        return getattr(self.__dict__['_file'], name)

    def __setattr__(self, name, value):
        if name in ('_file', '_logger'):
            self.__dict__[name] = value
        else:
            setattr(self.__dict__['_file'], name, value)

    def __delattr__(self, name):
        delattr(self.__dict__['_file'], name)



"""
Pythons Introspection is "the downfall for the decorator pattern"
if the only operation you could perform on an object was attribute lookup
(statically through an identifier f.write or dynamically via getattr(f, attrname)
then a decorator would be foolproof.

if the code to which you pass the wrapper decides to look depper, all kind of
difference become appearent:
    ie the native file object is buttressed with many provate methods and
    attributes

??? dir() shows each of these implementations do not perfectly wrap as there may
be global privates and the like in a particular library...

therefore:

The Decorator Pattern in python support programming - but not metaprogramming
Code that is happy to simply access attributes will be happy to accept a
decorator Pattern wrapper instead. But code that induclges in introspection will
see the difference. ie. Python code that attempts to list and objects
attributes, examine __class__ or directly access __dict__ will see differences
between the object it expected and teh decorator given instead. Application code
should never do this however, they should only be necessary when implementing a
developer tool like a framework, test harness or debugger,


"""
#------------------------------------------------------------------------------
# Monkey Patch - Questionable or Not?
# 1) could monkey patch each object
#

"""
Take each object that needs decoration and install a new method dierctly on the
object, shadowing the offical method that remains on the class itself.
*** a function installed on a python object instance does NOT recieve an
automatic self argument. Instead it sees only the arguemetns with which it is
literally invoked.....
***



>>> def bind_write_method(logger):
...     # Does not work: will not receive `self` argument
...     def write_and_log(self, s):
...         self.write(s)
...         logger.debug('wrote %s bytes to %s', len(s), self._file)
...     return write_and_log


>>> f = open('/dev/null', 'w')
>>> f.write
<built-in method write ...>
>>> f.write = bind_write_method(getLogger())
>>> f.write('Hello, world.')
Traceback (most recent call last):
  ...
TypeError: write_and_log() missing 1 required positional argument: 's'


# instead do the binding yourself, by providing the object instance to the closure
that wraps the new method itself.


>>> def bind_write_method(self, logger):
...     def write_and_log(s):
...         write(s)
...         print('wrote {} bytes to {}'.format(len(s), self.name))
...     write = self.write
...     return write_and_log
>>> f = open('/dev/null', 'w')
>>> f.write = bind_write_method(f, getLogger())
>>> f.write('Hello, world.')
wrote 13 bytes to /dev/null

# lets you update the actino of a single method on a single object

"""

#------------------------------------------------------------------------------
# Client Code

def client_code(component):
    """
    The client code works with all objects using the Component interface. This
    way it can stay independent of the concrete classes of components it works
    with.
    """
    print("RESULT: {}".format(component.operation('one', 'two')))


def main():

    with open("yinyang.png", "rb") as fd:
        data = fd.read()

    file_object = open("yinyang_out.png", "wb")
    wlf = WriteLoggingFile1(file_object, LOGGER)
    wlf.write(data)




#------------------------------------------------------------------------------


if __name__ == "__main__":
    main()


