# https://python-patterns.guide/gang-of-four/singleton/
# https://python-patterns.guide/python/module-globals/
#
# The Singleton Pattern is a poor fit for a language like python that lacks the
# concepts of new, private, protected and a compilation stage. __new__ was
# introduced in Python2.4 to support different patterns but has DRAWBACKS:
# - hard to read compared to the Pythonic Global Object Pattern where a mutable
#   object simply lives at the top level of a modules namespace.
# - Calls to a Singleton() class without some hint in the classname is not
#   explicit to end users who on the surface would expect a new instance
# - a global object allows for other instance of the class to be created, which
#   is useful when testing a class in mulitple ways; If there are no additional
#   instances possible one might need to monkey patch or subclass and override.
#   A pattern one needs to work around is a pattern that should be avoided.
#
# The Global Object Pattern leverages off of the fact that every Python module
# is a separate namespce (essential for making a language tractable: a focus
# on the module variables in front of you). Python parses the outerlevel of
# each module as normal code and executes each toplevel statement as the module
# is imported. A class instance that has been assigned a global name in this way
# is considered to be a "Singleton".
#
#------------------------------------------------------------------------------
# Constant | Pythonic Global Object Creational Design Pattern
#------------------------------------------------------------------------------
# A module instantiates an object at import time and assigns it a name in the
# modules global scope.
#
# - Common across the Standard Library
#     January = 1                                        # calendar.py
#     SSL_HANDSHAKE_TIMEOUT = 60.0                       # asyncio.constants.py
#     all_errors = (Error, OSError, EOFError)            # ftplib.py
#     windows_locale = { 0x0436: "af_ZA", ... }          # locale.py
#     _EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc) # datetime.py
#     _blocking_errnos = { 1, 2, 3, 3 , 2, 1 }           # socket.py mutable set
#     # set([1, 2, 3])
#     DIGITS = frozenset('12345678900987654321')         # sre_parse.py (regex)
#     # frozenset(['1', '0', '3', '2', '5', '4', '7', '6', '9', '8'])
# - Mutable, meaning the names can be reassigned or deleted after import
#     import calendar
#     del calendar.January
# - Constants in the sense that the objects themselves are immutable (prims)
# - Leverage name mangling if desired: _MangledClass__mangled = 23
# - Often introduced as a refactoring: documenting a recurring values meaning
#   and organizing a readable 'jump-to definition' at the top of the module
#   where the value can be easily changed and propogated in one place
# - Computation at import time
#     COPY_BUFSIZE = 1024*1024 if _WINDOWS else 16*1024  # shutil.py
# - Dunder Constants are typically set by the Python itself; special runtime
#     __name__, __author__ , __file__, __version__, __all__
# - immutable compiled expressions at a small compute hit for every import
#     HAS_UTF8 = re.compile(b'[\x80-\xff]')              # json/encoder.py
# - Mutable global objects. environ object populates data that can be edited
#   at runtime. Various threads and routines can coordinate access to a process
#   wide resource, whose change is immediately visible elsewhere in the program.
#   Commonly seen with Loggers. Write code that accepts arguments and returns
#   computed values.
#     import os, itertools
#     os.environ['TERM'] = 'xterm'
#     _process_counter = iterools.count(1)
# - Dont get carried away: errors at import time are far more serious than
#   errors at runtime. these errors are happen before the applications main
#   try/except clock. Best for global objects to wait until they are first
#   called before opening files or doing time consuming work.
#

DATA = []
JSON_FILE = "db1.txt"


def get_data(clear=False):
    """ Read some data, filter, and present
    the json module has global re's that get compiled, taking a time hit
    when imported the first time, but subsequently cached. We do not do
    any heavy lifting in the global scope directly, only when requested:
    here via main or by any other client of this api.
    """
    import json
    global DATA

    with open(JSON_FILE, "r") as fd:
        data = json.load(fd)

    if clear:
        DATA = []  # local variable overrides global without keyword

    for item in data:
        DATA.append((item['first_name'], item['last_name']))

    print(DATA)


#------------------------------------------------------------------------------

if __name__ == "__main__":
    """ Read some data into a singleton (uniquely named global object) using
    a mutably defined filename to define where to read data from. Do this
    potentially heavy operation on globals only when requested at runtime not
    during module impport time.
    """
    get_data()
    JSON_FILE = "db2.txt"
    get_data()
    JSON_FILE = "db3.txt"
    get_data(clear=True)

