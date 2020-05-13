# https://python-patterns.guide/gang-of-four/factory-method/
# https://realpython.com/factory-method-python/
#
#------------------------------------------------------------------------------
# Factory Method | Creational Design Pattern
#------------------------------------------------------------------------------
#
# The G.O.F Factory Method is not very Pythonic; originally designed for older
# programming languages where classes and functions are not first class objects
# and CANNOT be passed as parameters or stored as attributes like in Python.
# - a class cannot be a class attribute of another class
# - a function cannot be held as an instance of another class
# - no other callable can be dynamically defined and attatched at runtime
#
# It is common to create objects that in turn need to create objects.
#
# Dependency Injection:
# It's important to check of the class you're designing really needs to go
# around creating other objects. This pattern can be avoided if you know all
# the objects a class will need up front; a pattern used in many Python
# Libraries, such as json.load()
# - have the client pass an already open file object instead of supplying
#   a path for your implementation to open.
# - Efficiency: file has already been open, so use it without delay
# - Decoupling: library doesnt need to handle all parms accepted by open()
# - Flexibility: any subclass of a standard file object can be handled.
#
#------------------------------------------------------------------------------
# Object/Attribute Factory | Pythonic Creational Design Pattern
#------------------------------------------------------------------------------
# In general, this pattern has 4 major characteristics:
# 1. The Product Component : an interface describing what is to be created
# 2. The Creator Component : the factory that decides which concrete product
#       implementation is to be used given some parameter
# 3. The Client  Component : the application code that depends on an interface
#       to complete some task, requesting an implementation from the factory
# 4. Concrete Product Implementations: the business logic behind each product
#       that comes out of a factory
#
# - The class that needs to be created can be attached as an attribute on the
#   class that will be doing the creating. This takes advantage of the fact
#   that classes and functions are first-class objects in python.
# - Customize an object through its parameters instead of creating a new class
# - The creation method can be any kind of callable: bound method, class method
# - Parameters compose nicely: a dict can update/overwrite parm values
# - A toplevel Class Attribute can be overwritten to customize
#     class HttpConnection:
#         response_class = HttpRespsonse              # a class as an attribute
#         def get_response(self):
#             response = self.response_class(*args)
#
#     class MyHttpConnection(HttpConnection):
#         response_class = MyHttpResponse


import abc
import json
import xml.etree.ElementTree as ET


#------------------------------------------------------------------------------
# Simple Factory Pattern:
#   A class that has one creation method with a large conditional that chooses
#   which product class to instantiate and return based on a method parameter
#
# - A naive first implementation
# - Simple Factories usually dont have subclasses; extracting subclasses is a
#   step toward a Factory Method pattern
# - While the Simple Factory logic is well encapsulated, none of these methods
#   actually depend on the class instance variable self. This means each
#   component can be extracted into their own top level module function,
#   with the exception of the Client Component if its already in use.


class Song:

    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


class SongSerializer:

    def serialize(self, song, format):
        """ CLIENT COMPONENT:
        Application code that depends on an interface (product component).
        The interface is a *function* that takes a song and returns a string
        representation via various concrete interface implementations.
        """

        serializer = self._get_serializer(format)
        return serializer(song)

    def _get_serializer(self, format):
        """ CREATOR COMPONENT:
        Decides which concrete implementation to use.
        """

        if format == 'JSON':
            return self._serialize_to_json
        elif format == 'XML':
            return self._serialize_to_xml
        else:
            raise ValueError(format)

    def _serialize_to_json(self, song):
        """ CONCRETE PRODUCT COMPONENT 1
        Takes a Song object and returns a JSON string representation of it.
        """

        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return json.dumps(payload)

    def _serialize_to_xml(self, song):
        """ CONCRETE PRODUCT COMPONENT 2
        Takes a song object and returns an XML string representation of it.
        """

        song_element = ET.Element('song', attrib={'id': song.song_id})
        title = ET.SubElement(song_element, 'title')
        title.text = song.title
        artist = ET.SubElement(song_element, 'artist')
        artist.text = song.artist
        #return ET.tostring(song_element, encoding='unicode')
        return ET.tostring(song_element)


#------------------------------------------------------------------------------
# Factory Method Pattern:
# ----------------------
#
# S.O.L.I.D Implementation
#
# Single Responsibility Principle:
#    A class should have one and only one reason to change; it should only
#    have 1 job
#
# Open/Closed Principle:
#    Objects should be open for extention, but closed for modification
#
# Liskov Substitution Principle:
#    If q(x) is True about objects x of type T, then q(y) should be True
#    for objects y of type S where S is a subtype of T
#
# Interface Segregation Principle:
#    A client should never be forced to implement an interface that it doesnt
#    use; clients shouldn't be forced to depend on methods they dont use
#
# Dependency Inversion Principle:
#    Entities must depend on abstractions not concretions; the high level
#    module must not depend on the low level module (Decouple)
#
# - The naive implementation and Factory Method is largely decoupled below
# - The use of more classes judiciously allows them each to have a single job
# - The hard coded identifiers in SongSerializer.get_serializer were replaced
#   with a registry in SerializerFactory.get_serializer allowing it to remain
#   extensible but without modifying the internals of the function definition
# - Using an abstract base class for the Serializer Products ensures subclasses
#   have provided sufficient implementations than can be used interchangably.
# - new features can be introuced by adding new classes, as opposed to changing
#   existing ones


class SerializerFactory:

    def __init__(self):
        self._creators = {}

    def register_format(self, format, creator):
        self._creators[format] = creator

    def get_serializer(self, format):
        """ CREATOR COMPONENT
        Decides which concrete implementation to use.
        The classes that needs to be created (Serializer Products) can be
        attached as an attribute on the class that will be doing the creating.

        The hard coded product identifiers have been moved out of the factory
        so the factory itself doesnt need to be modified to add new products.
        """

        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


class ObjectSerializer:

    def serialize(self, serializable, format):
        """ CLIENT COMPONENT : application code that depends on an interface.
        The interface (product) are objects that take a song (or any other
        object that is serializable) and returns a string representation
        via various concrete interface implementations as requested.
        """

        serializer = factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.to_str()


class Product(object):
    """ PRODUCT COMPONENT:
    Define the interface of objects the Factory Method creates.
    This abstract base class describes how client code intends to interface
    with muliple concrete implementations that perform similar tasks.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start_object(self, object_name, object_id):
        pass

    @abc.abstractmethod
    def add_property(self, name, value):
        pass

    def to_str(self):
        pass


class JsonSerializer(Product):
    """ Concrete Product Implementation 1 """

    def __init__(self):
        self._current_object = None

    def start_object(self, object_name, object_id):
        self._current_object = {
            'id': object_id
        }

    def add_property(self, name, value):
        self._current_object[name] = value

    def to_str(self):
        return json.dumps(self._current_object)


class XmlSerializer(Product):
    """ Concrete Product Implementation 2 """

    def __init__(self):
        self._element = None

    def start_object(self, object_name, object_id):
        self._element = ET.Element(object_name, attrib={'id': object_id})

    def add_property(self, name, value):
        prop = ET.SubElement(self._element, name)
        prop.text = value

    def to_str(self):
        #return ET.tostring(self._element, encoding='unicode')
        return ET.tostring(self._element)


factory = SerializerFactory()
factory.register_format('JSON', JsonSerializer)
factory.register_format('XML', XmlSerializer)


class Serializable(object):
    """ Abstract Base Class for Objects that can be serialized
    Define an interface for objects that can be serialized to a string
    to allow our generic ObjectSerializer Client to operate on multiple
    subclasses that implement this interface
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def serialize(self, serializer):
        pass


class ASong(Serializable):
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist

    def serialize(self, serializer):
        serializer.start_object('song', self.song_id)
        serializer.add_property('title', self.title)
        serializer.add_property('artist', self.artist)


class AAlbum(Serializable):

    def __init__(self, album_id, title, artist, songs):
        self.id = album_id
        self.title = title
        self.artist = artist
        self.songs = songs

    def serialize(self, serializer):
        serializer.start_object('album', self.id)
        serializer.add_property('title', self.title)
        serializer.add_property('artist', self.artist)
        for i in range(len(self.songs)):
            serializer.add_property('song{}'.format(i), self.songs[i].title)


#------------------------------------------------------------------------------

if __name__ == "__main__":

    """ Factories hold an instance of a product, managing its interface """

    song = Song('1', 'Water of Love', 'Dire Straits')

    serializer = SongSerializer()
    print(serializer.serialize(song, "XML"))
    print(serializer.serialize(song, "JSON"))

    song1 = ASong('1', 'Water of Love', 'Dire Straits')
    song2 = ASong('2', 'Setting Me Up', 'Dire Straits')
    album = AAlbum('1', 'Dire Straights', 'Dire Straights', [song1, song2])
    serializer = ObjectSerializer()
    print(serializer.serialize(song1, "XML"))
    print(serializer.serialize(song2, "JSON"))
    print(serializer.serialize(album, "JSON"))
