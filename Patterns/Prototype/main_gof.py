#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://python-patterns.guide/gang-of-four/prototype/
# https://www.python.org/dev/peps/pep-0263/

#------------------------------------------------------------------------------
# Prototype | Creational Design Pattern
#------------------------------------------------------------------------------
#
# A mechanism by which a caller provides a framework with a menu of classes
# to instantiate when the user, or other runtime source of dynamic requests
# selects a class from a menu of choices. A Framework is supplied with a menu
# of classes that need to be instantiated with pre-specified arguments.
#
# - Building such a framework isn't necessary in a language that supports first
#   class functions and classes. There are many pythonic alternatives.
# - Python offers several possible mechanisms for supplying a framework with
#   classes to instantiate and the arguments we want them intantiated with.
# - The choices in Python for implementing a Prototype pattern are numerous
#   because classes and functions are first class objects, eligible to be
#   passed as arguments and stored in data structures like any other objects.
#   This could include supplying a (cls, args, kwargs) for each prototype key
#   value, where the framework would call cls(*args, **kwargs)
# - In Python lists, tuples and dicts can be applied to functions as arguments
# - GOF did not have the facilities afforded to Python programmers. Thye were
#   only armed with polymorphism and the method call, and developed pattern
#   structures around those early OOP languages and theory. Hence factory
#   classes emerged to remember a particular list of arguments and supply
#   those arguments when a particular object was asked for. This simply isnt
#   as convenient as the mechanisms available in the Python language.
# - The prototype pattern "made it much easier for the GOF to accmplish
#   'parametrized object creation' using underpowered Object Orient languages
#   that were popular LAST CENTURY" - haha.
# - If none of the classes need to be constructed with arguments there
#   wouldn't be a need for a Prototype pattern.
# - In general, the intent of the Prototype Pattern is to avoid the need
#   to have one factory for every class in play.
# - This sourcefile uses NON-ASCII ♯ and ♭ characters which will be a problem
#   for the python parser when interpreting the file unless a 'magic comment'
#   is placed in the first or second line of the file as above. The 'shebang'
#   in any executable script specifies the scripts ability to be executed as if
#   it were a standalone executable in a terminal or when double clicked in a
#   file manager. This means that once the file is chmoded as an exeucable we
#   would no longer need to preceed the source file script in a terminal with
#   the program needed to interpret it (ie.% python). Since python installations
#   on different linux platforms can be in different places or virtual envs,
#   unlike /usr/bin/env, we env to launch whatever python program is defined by
#   the environment for interpretation of this sourcefile when executed.
#
# Some Piano Nomenclature:
# - There are 7 Note names (C, D, E ,F, G, A, B) in an octave
# - Middle C is refered to as C4, the C in the middle of the keyboard
# - A standard piano has 7 octaves C1-C7, often with an additional C8 key
# - A Dotted note holds its beat for its measure plus half of its measure
# - A Sharp is a half step/key up/right, a Flat is a half step/key dn/left
# - A ledger signature describes how many notes/beats in a measure (ie 3/4)
# - The duration a note is played for is recognized by its symbol called:
#
# English Note    American Note    Length(beats)  Measure (fraction of a whole)
#------------------------------------------------------------------------------
# semibreve       whole (measure)       4         1 = (4/4) (1)
# dotted minum    dotted half           3      1.33 = (4/3) (3/4 -> 0.75)
# minim           half (measure)        2         2 = (4/2) (1/2 -> 2)
# crotchet        quarter (measure)     1         4 = (4/1) (1/4 -> 4)
# quaver          eighth (measure)     1/2        8 = (4/(1/2)) (1/8 -> 8)
# semiquaver      sixteenth (measure)  1/4       16 = (4/(1/4)) (1/16 -> 16)


class Note(object):

    __measure = 4
    __fractions = {
        1: ('semibreve', 'whole', u'\u1D15D'),
        2: ('minum', 'half', u'\u1D15E'),
        4: ('crotchet', 'quarter', '♩'),
        8: ('quaver', 'eighth', '♪'),
        16: ('semiquaver', 'sixteenth', u'\u1D160'),
    }
    # private class variables set at class definition time for all instances

    def __init__(self, name='C', fraction=4, octave=4):
        """
        Middle C Crotchet (quarter note measure) by default

        Use the @property.setters self.name attribute to invoke the decorator
        logic that manages the corresponding private variables. In these
        wrappers we compute/set any additional private variables that are
        implicitly dependent on them, but hidden to the client. Failing do
        do so will fail to set the implicitly dependent variables.
        """
        # property attributes
        self.name = name
        self.octave = octave
        self.fraction = fraction
        # protected inherited instance variables
        self._step = ''
        self._dotted = ''
        #print ("__init__'d", name, self.__class__.__name__)

    def __repr__(self):
        """
        A string representation that can be used for serialization
        such that when deserialized the note can be reconstructed
        """
        pass

    def __str__(self):
        note = "{:>10} Note: {}{}{}".format(
            self.__measure_type,
            self.__name,
            self._step,
            self._dotted
        )
        return note

    @property
    def fraction(self):
        return self.__fraction

    @fraction.setter
    def fraction(self, fraction):
        self.__fraction = int(fraction)

        self.__beats = self.__fraction * self.__measure
        self.__note_type = self.__fractions[self.__fraction][0]
        self.__measure_type = self.__fractions[self.__fraction][1]

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name.upper()

    @property
    def octave(self):
        return self.__octave

    @octave.setter
    def octave(self, octave):
        self.__octave = int(octave)

    def clone(self, name=None, fraction=None, octave=None):
        name = (name, self.__name)[name is None]
        octave = (octave, self.__octave)[octave is None]
        fraction = (fraction, self.__fraction)[fraction is None]
        return type(self)(name, fraction, octave)
        # vs return Note(name, fraction, octave)


class Sharp(Note):
    """ A ♯ Note: up half a step

    Unicode characters can be used in this source file provided we define a
    'magic comment' in the first or second line of this file. Otherwise the
    explicit encoding would have to be used, determinable from pasting in a
    unicode character from a resource such as `https://copychar.cc/` into an
    interpreter or by defining unicode string for the character.
    >>> s = '😍'
    >>> s
    '\xf0\x9f\x98\x8d'
    >>> s = u'\u266F'
    >>> print(s)
    ♯
    """
    def __init__(self, *args, **kwargs):
        super(Sharp, self).__init__(*args, **kwargs)
        self._step = "♯"  # parse as unicode per magic comment


class Flat(Note):
    """ A ♭ Note: down half a step

    Note that member variables that we wish to inherit and make use of Liskov
    Substitution in base class methods should be protected with a single dunder
    prefix and not made private with a dunder prefex. Derived classes will not
    have access to Base class private variables without name-mangling trickery
    that explicity references the name-mangled name. ie: self._Base__private

    """
    def __init__(self, *args, **kwargs):
        super(Flat, self).__init__(*args, **kwargs)
        #self._Note__step = "♭"
        self._step = "♭"


class Dotted(Note):
    """
    A note that extends its measure by half
    ie. a dotted minum is 2 beats + half(2 beats) = 3 beats
    ie. a dotted quaver is 2 beat + half(1 beat) = 1.5 beats
    """
    def __init__(self, *args, **kwargs):
        super(Dotted, self).__init__(*args, **kwargs)
        self._Note__beats = self._Note__beats + 0.5 * self._Note__beats
        #self._dotted u'\u00B7'    # utf-16
        self._dotted = '\xC2\xB7'  # utf-8
        #self._dotted = '.'        # ascii


class DottedSharp(Dotted, Sharp):
    """ A Note that is both Sharp and Dotted

    This is a an example of multiple inheritance, which starts to allude to the
    problem of class explosion. Attributes as simple as those we are using here
    could really just be additional initialization parameters, but as this was
    intended to provide an overall implementation reference for OOP theory in
    Python, this continues to support our implementation.
    """

    def __init__(self, *args, **kwargs):
        super(DottedSharp, self).__init__(*args, **kwargs)


class DottedFlat(Dotted, Flat):
    """ A Note that is both Flat and Dotted

    When multiple inheritance is in play, so is the 'method resolution order'
    that defines the order in which the mulitple base class's initialization
    methods are invoked.

    [<class '__main__.DottedFlat'>, <class '__main__.Dotted'>, <class
    '__main__.Flat'>, <class '__main__.Note'>, <type 'object'>]
    """
    def __init__(self, *args, **kwargs):
        super(DottedFlat, self).__init__(*args, **kwargs)
        #print(DottedFlat.mro())


#------------------------------------------------------------------------------
# Dedicated GOF Style Prototype Factory Frameworks
#------------------------------------------------------------------------------

class NoteFactory1:

    def __init__(self):
        """
        Initialize all the prototypes as instance variables when the factory
        is instantiated. Class variables are initialized once at class
        definition time, while instance variables are created each time the
        class is instantiated. Defining prototypes as class variables
        instantiate prototypes at runtime, which could slow bootstrapping and
        make it harder to debug, depending on the class. Therefore in Python,
        initializing objects as instance variables is the better option,
        reseriving class varible instantiation for primitive constants.

        No other pythonic implementation here depends on the copy module so it
        is only imported here.
        """

        import copy

        __prototypes = {
            'whole': Note(1),
            'half': Note(2),
            'quarter': Note(4),
            'eighth': Note(8),
            'sixteenth': Note(16),
            'sharp': Sharp,
            'flat': Flat,
            'dotted': Dotted,
        }


    def clonePrototype(self, key):
        """
        We dont return a reference to the prototype as that could be modified
        and compromise the integrity of our prototype for future clones.

        Notice that this factory method is most similar to the GOF legacy
        language implementation as prototypes are instantiated when the factory
        is first initialized following object construction.
        """
        try:
            prototype = self.__prototypes['key']
        except KeyError:
            err = "Our factory does not have any [{}]. Try\n[{}]"
            raise Exception(err.format(key, self.__prototypes.keys()))

        return copy.copy(prototype)


class NoteFactory2:

    def __init__(self):
        """
        We dont actually need to instantiate the prototypes into memory when the
        factory is initialized as in the legacy language GOF implementation. We
        can instead leverage off of classes and functions being first class
        objects in Python. Here, only the prototype class definition (ie recipie
        or template) is maintained along with an argument list, taking up next
        to no memory when the factory is instantiated, especially when the
        reference to each class definition is the same, with the same address.

        This is similar in concept to the argv list provided by a shell to a
        command line script. Tuples are used to disallow the __prototype values
        to be overwritten as lists are mutable in Python and tuples are not.
        """
        __prototypes = {
            'whole': (Note, 1),
            'half': (Note, 2),
            'quarter': (Note, 4),
            'eighth': (Note, 8),
            'sixteenth': (Note, 16),
            'sharp': (Sharp, ),
            'flat': (Flat, ),
            'dotted': (Dotted, ),
        }


    def clonePrototype(self, key):
        """
        Now the factory method "framework" simply constructs a new instance of
        a prototype when requested by invoking the class definition along with
        its argument initialization list. Pythonic operators make it easy to
        peel off the first element as the class/function to invoke and unpack
        the rest of the list as arguments.
        """
        try:
            proto = self.__prototypes['key']
        except KeyError:
            err = "Our factory does not have any [{}]. Try\n[{}]"
            raise Exception(err.format(key, self.__prototypes.keys()))

        return proto[0](*proto[1:])


class NoteFactory3:

    def __init__(self):
        """
        Instead of operating on a single list in the factory construction
        method, we could further employ Python language features to make the
        class instantiation more explicit by using a slightly better data
        structure to separate the class definition from its argument list.
        """
        __prototypes = {
            'whole': (Note, (1,)),
            'half': (Note, (2,)),
            'quarter': (Note, (4,)),
            'eighth': (Note, (8,)),
            'sixteenth': (Note, (16,)),
            'sharp': (Sharp, ()),
            'flat': (Flat, ()),
            'dotted': (Dotted, ()),
        }


    def clonePrototype(self, key):
        """
        Now just invoke the definition using its unpacked argument list,
        simply returning an instance object from the class definition.
        """
        try:
            proto_cls, proto_args = self.__prototypes['key']
        except KeyError:
            err = "Our factory does not have any [{}]. Try\n[{}]"
            raise Exception(err.format(key, self.__prototypes.keys()))

        return proto_cls(*proto_args)


class NoteFactory4:

    def __init__(self):
        """
        This idea can also be representd by Pythons partial() objects, which
        package together a callable with positional and keyword arguments that
        are supplied at a later point when the partial object itself is called.

        Its good practice to not import anything that isnt being used by the
        program. So we avoid importing the partial module at the toplevel,
        deferring the import to when its actually in play -- during the first
        instantiation of this particular NoteFactory Class.

        Defining partial arguments positionally enforces the default 'C'
        argument to be explicit and therefore self documenting.
        """
        from functools import partial

        __prototypes = {
            'whole': partial(Note, fraction=1),   # keyword args: implicit 'C'
            'half': partial(Note, faction=2),
            'quarter': Note,                      # Middle C4 by default
            'eighth': partial(Note, 'C', 8),      # positionl args: explicit
            'sixteenth': partial(Note, 'C', 16),
            'sharp': Sharp,
            'flat': Flat,
            'dotted': Dotted,
        }


    def clonePrototype(self, key):
        """
        Now simply invoke the partial callable to return an instance.
        We choose to return None, rather than raise an exception; the client can
        check if the request produced a result, which might be preferred usage.
        """
        try:
            return self.__prototypes['key']()
        except KeyError:
            return None


#------------------------------------------------------------------------------
# Pythonic Factory
#------------------------------------------------------------------------------
# Rather than implementing a dedicated Factory Class to manage prototype
# instances as suggested by the legacy language GOF pattern, we can leverage
# off Python language features further and implement a factory as dictionary
# directly. The object instantiation is done via a lambda expression which
# creates a callable such that the Prototypes are not instantiated into memory
# until the key values are requested. Obviously a dictionary is a data
# structure and can't do the cloning of a prototype, so by pushing the clone
# method into the prototype base class, the objects themselves manage that.

def main_dict_factory():

    """
    Prototypes are 'C4' notes of different measures, and C4-Sharp, C4-Flat,
    C4-Dotted quarter notes, all initialized by the prototype class definition
    by default. Keyword arguments are used for clarity and illustration, and
    only providing the class definition without any arguments will instantiate
    the prototype with its defaults as a class definition is also a callable.
    """

    note_factory = {
        'whole': lambda: Note(fraction=1),
        'half': lambda: Note(fraction=2),
        'quarter': lambda: Note(fraction=4),
        'eighth': lambda: Note(fraction=8),
        'sixteenth': lambda: Note(fraction=16),
        'flat': Flat,
        'sharp': Sharp,
        'dotted': Dotted,
        'dot_flat': DottedFlat,
        'dot_sharp': DottedSharp,
    }


    """
    The GOF Prototye pattern tries to help the client from having to
    instantiate from the Prototype classes directly, where prototypes are
    instantiated once by a factory, then reused and cloned through its
    interface. In that implementation the prototypes themselves did not
    manage the cloning, whereas in this implementation they can, so it is
    arguable whether a factory data structure is even needed for any purpose
    other than predefining the notes all in one place and being more explicit
    about the what the note prototype is by labeling them using dictionary keys.
    """
    n1 = Note()                    # Middle C Crotchet by default
    n2 = Note(fraction=8)          # Middle C Quaver
    n3 = Note('D')                 # Middle D Crotchet
    n4 = Note('E')
    n4 = Note('F')
    n5 = Note('G')
    n6 = Note('A')
    n7 = Note('E', fraction=2)     # Minum (half note - 2 beats)
    n8 = Note('F', fraction=2)
    n9 = Note('C', octave=5)       # High C
    n10 = Flat('B', fraction=8)    # B flat Quaver
    n11 = Dotted('F', fraction=2)  # Dotted Minum (3 beats)

    n0 = Note()         # quarter note C4 by default
    n0.fraction = 1     # to whole note via @property.setter
    n0.name = 'b'
    print(n10)
    print(n11)

    """
    Alternatively, the client asks the note_factory data structure for the
    callables and then invokes them to get an instance. The prototype in this
    sense is 'partially assembled' in some sense, which doesnt take up as much
    memory as actual object instances would; while all the light-weight
    prototypes can be stored, only those that actually need to be used need to
    be instantiated.

    A few original clones are all that is needed to mutate into as many new
    instance variations as desired, and for the most part, from any clone.
    """
    c = note_factory['quarter']()
    c_ = note_factory['eighth']()
    cc = note_factory['half']()
    ccc = note_factory['dotted']()
    c_flat = note_factory['flat']()
    c_sharp = note_factory['sharp']()
    ccc_flat = note_factory['dot_flat']()
    ccc_sharp = note_factory['dot_sharp']()

    print(c)
    print(c_)
    print(cc)
    print(ccc)
    print(c_flat)
    print(c_sharp)
    print(ccc_flat)
    print(ccc_sharp)

    d = c.clone('d')
    e = c.clone('e')
    f = c.clone('f')
    g = c.clone('g')
    a = c.clone('a')
    C = c.clone(octave=5)

    ff = cc.clone('f')
    ee = ff.clone('e')
    fff = ccc.clone('f')

    b_flat = c_flat.clone('b', 8)
    fff_sharp = ccc_sharp.clone('f', 16)
    print(b_flat)

    for n in (c, d, e, fff_sharp, g, a, b_flat, C):
        print n


def main():

    c = Note()
    C = c.clone(octave=5)
    c_ = c.clone(fraction=8)
    cc = c.clone(fraction=2)

    d = c.clone('d')
    e = c.clone('e')
    f = c.clone('f')
    g = c.clone('g')
    a = c.clone('a')

    ee = e.clone(fraction=2)
    ff = ee.clone('f')

    fff = Dotted('f', 2)
    b_flat = Flat('b')

    happy_birthday = (
        c_, c_, d, c, f, ee,
        c_, c_, d, c, g, ff,
        c_, c_, C, a, f, e, d,
        b_flat, b_flat, a, f, g, fff
    )

    print("Happy Birthday To You")
    for note in happy_birthday:
        print(note)


#------------------------------------------------------------------------------

if __name__ == "__main__":
    #main_dict_factory()
    main()


