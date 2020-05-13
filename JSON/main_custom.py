import json
import traceback


#------------------------------------------------------------------------------
# Custom Complex Number implementation


class Complex(object):
    def __init__(self, real, imag=0.0):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real,
                       self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real,
                       self.imag - other.imag)

    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag,
                       self.imag * other.real + self.real * other.imag)

    def __div__(self, other):
        sr, si, rr, ri = self.real, self.imag, other.real, other.imag
        r = float(rr**2 + ri**2)
        return Complex((sr * rr + si * ri) / r, (si * rr - sr * ri) / r)

    def __abs__(self):
        return sqrt(self.real**2 + self.imag**2)

    def __neg__(self):   # defines -c (c is Complex)
        return Complex(-self.real, -self.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '(%g, %g)' % (self.real, self.imag)

    def __repr__(self):
        return 'Complex' + str(self)

    def __pow__(self, power):
        raise NotImplementedError(
            'self**power is not yet impl. for Complex'
        )


#------------------------------------------------------------------------------
# Python has native built-in complex number support via the complex class
# Serialize a complex object into a tuple which is natively supported by JSON

# via a default function passed as an argument to json.dump()

def encode_complex(z):
    if isinstance(z, complex):
        return (z.real, z.imag)
    else:
        type_name = z.__class__.__name__
        f_error = "Object of type '{}' is not JSON serializable".format(type_name)
        raise TypeError(f_error)


# by subclassing JSONEncoder, and overriding its default() method

class ComplexEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, complex):
            return (z.real, z.imag)
        else:
            #return super().default(z)   # python3
            return super(ComplexEncoder, self).default(z)


#------------------------------------------------------------------------------
# Deserialize json data using metadata to intuit the constructor

def decode_complex(dct):
    if "__complex__" in dct:
        return complex(dct["real"], dct["imag"])
    return dct


class ComplexDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        print("->", dct)
        if "__complex__" in dct:
            return complex(dct["real"], dct["imag"])
        return dct


#------------------------------------------------------------------------------
# main use cases and data

z1 = 9 + 5j
z2 = complex(9, 6)
z3 = Complex(9, 7)


try:  # JSON cant serialize objects natively
    print(json.dumps(z1))
    print(json.dumps(z2))
    print(json.jumps(z3))

except Exception as e:
    print(e)


try:  # to encode the objects into a native JSON list
    print(json.dumps(z1, default=encode_complex))
    print(json.dumps(z2, cls=ComplexEncoder))

    encoder = ComplexEncoder()
    print(encoder.encode(z1))

    print(json.dumps(z3, cls=ComplexEncoder))

except Exception as e:
    print(e)


# JSON structured data in Python; Note the use of native Python types
z1_json = [
    {
        "__complex__": True,
        "real": 42,
        "imag": 36
    },
    {
        "__complex__": True,
        "real": 64,
        "imag": 11
    }
]

try:  # to decode objects from a string and from a file
    print(" SERIALIZING", z1_json)
    with open("export_complex.json", "w") as fd:
        json.dump(z1_json, fd)

    with open("export_complex.json", "r") as fd:
        data = json.load(fd, object_hook=decode_complex)
    print("DESERIALIZED", data)

except Exception as e:
    print(e)


# String Representation of a json file; note the JSON literal true
# as opposed to the Python literal True. Indentation not important.
z2_json = """
[
  {
    "__complex__": true,
    "real": 42,
    "imag": 36
  },
  {
    "__complex__": true,
    "real": 64,
    "imag": 11
  }
]
"""


try:  # to decode string representation of a file
    print("  SERIALIZED", z2_json)
    data = json.loads(z2_json, cls=ComplexDecoder)
    print("DESERIALIZED", data)

except Exception as e:
    print(e)


#------------------------------------------------------------------------------
# Custom classes should leverage __repr__() to serialize their
# objects to a string representation of their constructor which
# can have eval() called on, which invokes the constructor to
# create a new instance of the class. Complex does this
# >>> z1 = 5+8j
# >>> z1
# (5+8j)
# >>> repr(z1)
# '(5+8j)'
# >>> z2 = eval(repr(z1))
# >>> z1 == z2
# True
# >>> repr(z2)
# '(5+8j)'


print(75 * '=')
print z3  # prints Complex.__str__()
print("Complex Object: z", z3)  # prints Complex.__repr__()
print("repr(z):", repr(z3))     # string repr of Complex
print("eval(repr(z)):", eval(repr(z3)))  # an object constructed from repr
print("z == eval(repr(z)?:", z3 == eval(repr(z3)))  # Complex.__eq__()


complex_nums = [z1, z2, z3, Complex(1, 2), Complex(3, 4), Complex(5.6, 7.8)]


class MyComplexEncoder(json.JSONEncoder):
    """ Encode Each element in the list using a constructor """
    def default(self, z):
        if isinstance(z, Complex):
            return repr(z)
        elif isinstance(z, complex):
            return "Complex({}, {})".format(z.real, z.imag)
        else:
            return super(MyComplexEncoder, self).default(z)


class MyComplexDecoder(json.JSONDecoder):
    """ Decode the list by invoking the constructor on each element """
    def decode(self, obj):
        print(" DECODING... {}\n {}".format(type(obj), obj))
        reconstructed = [eval(x) for x in eval(obj)]
        return reconstructed


def sum_my_complex_objects(lst_Complex):
    print("SUMMING COMPLEX OBJECTS...")
    z = Complex(0)
    for c in lst_Complex:
        z = z + c
    print("{} + {}i\n".format(z.real, z.imag))


try:
    line = 75 * '-'
    print("MY COMPLEX RAW:\n{}\n{}".format(complex_nums, line))
    print("MY COMPLEX SERIALIZED TO STRING:")
    complex_json = json.dumps(complex_nums, cls=MyComplexEncoder, indent=8)
    print("{}\n{}".format(complex_json, line))

    print("DESERIALIZING MY COMPLEX FROM STRING:")
    decoder = MyComplexDecoder()
    data = decoder.decode(complex_json)
    print(data)
    sum_my_complex_objects(data)


    file = "export_custom.json"
    with open(file, "w") as fd:
        json.dump(complex_nums, fd, cls=MyComplexEncoder)
    print("MY COMPLEX SERIALIZED TO DISK: {}\n{}".format(file, line))

    print("DESERIALIZING MY COMPLEX FROM DISK:")
    with open(file, "r") as fd:
        data = json.load(fd, cls=MyComplexDecoder)
    print(data)
    sum_my_complex_objects(data)


except Exception as e:
    print("\033[1;31m{}\033[0m".format(e))
    print(traceback.format_exc(e))

