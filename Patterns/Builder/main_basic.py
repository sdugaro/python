#------------------------------------------------------------------------------
# Builder | Creational Design Pattern
#------------------------------------------------------------------------------
# Compose complex objects from simple objects algorithmically
#
# - A builder class assembles a final object via a step by step procedure
# - Decouples the construction of an object from its representation
# - Provides more control and editing over the construction process
# - Different types and representations of an object can be created from the
#   same constructino code.
# - A Director class defines the order in which to execute the build steps.
#   This is a good place to orginize reusable construction routines and hide
#   the details of Product construction from the client.
#   This hides the details of Product Construction from the client code
# - A Builder provides the discrete implementation of the build steps.
# - Client Code can call the build steps directly rather than use a Director,
#   but would otherwise simply associate a Builder with a Director, launch the
#   construction with the director and get the result from the builder
#

#------------------------------------------------------------------------------
# The product and the sum of its parts


class Vehicle:
    """ The Product to be built """
    def __init__(self):
        self.__seats = list()
        self.__wheels = list()
        self.__engine = None
        self.__body = None

    def set_body(self, body):
        self.__body = body

    def set_wheel(self, wheel):
        self.__wheels.append(wheel)

    def set_engine(self, engine):
        self.__engine = engine

    def set_seat(self, seat):
        self.__seats.append(seat)

    def specifications(self):

        total__seats = sum(s.num for s in self.__seats)

        data_fmt = "{:>11}: {:>11}\n"
        data_str = data_fmt.format('Body', self.__body.shape)
        data_str += data_fmt.format('Engine', self.__engine.horsepower)
        data_str += data_fmt.format('Seats', total__seats)
        data_str += data_fmt.format('Tire Size', self.__wheels[0].size)
        return data_str


class Wheel:

    def __init__(self, size):
        self.size = size


class Engine:

    def __init__(self, horsepower):
        self.horsepower = horsepower


class Body:

    def __init__(self, shape):
        self.shape = shape


class Seat(object):  # new style: inherit from object to use super
    def __init__(self, fabric, type_='Single'):
        self.num = 3 if type_ == 'Bench' else 1

        self.shape = type_
        self.fabric = fabric


class BikeSeat(Seat):
    def __init__(self, fabric):
        super(BikeSeat, self).__init__(fabric, 'Bicycle')


#------------------------------------------------------------------------------
# Abstract and Concrete Builders

class Builder:
    """
    Interface describing the build steps, or different parts of the Product
    """

    def reset(self, *args, **kwargs):
        pass

    def set_body(self):
        pass

    def set_engine(self):
        pass

    def set_wheels(self, num, size):
        pass

    def set_seats(self, num, fabric):
        pass

    def get_product(self):
        pass


class VehicleBuilder(Builder):
    """
    A Concrete Builder class providing specific implementations of the build
    steps. There may be many Builders, each with thier own implementation or
    'way of doing things'. Ultimately the Builder puts together the product
    at the discretion of the Director until the director asks for it, at which
    point building has ended until the Director asks for
    """

    def reset(self):
        self.__product = Vehicle()

    def get_product(self):
        product = self.__product
        self.reset()
        return product

    def set_body(self, type_):
        body = Body(type_)
        self.__product.set_body(body)

    def set_engine(self, horsepower):
        engine = Engine(horsepower)
        self.__product.set_engine(engine)

    def set_wheels(self, num, size):
        wheel = Wheel(size)
        for i in range(num):
            self.__product.set_wheel(wheel)

    def set_seats(self, num, fabric):

        assert num > 0 and num < 7

        count = 0
        while count < num:
            if count < 2:
                seat = Seat(fabric)
                count += 1
            elif count < 5:
                seat = Seat(fabric, 'Bench')
                count += 3
            elif count < 7:
                seat = Seat(fabric, 'Compact')
                count += 1
            self.__product.set_seat(seat)


class BikeBuilder(Builder):
    """
    Another Concrete Builder class, specializing in bicycles.
    Notice in Python, unlike other languages, the entire builder interface does
    not need to be implemented, particularly when the abc module is not in play
    to enforce abstract base class interface implementation. A bicycle is still
    a vehicle, however as certain assumptions can be made implicitly this builder
    doesnt have to implement as many methods and can provide additional ones.
    """

    def reset(self, electric=False):
        self.__product = Vehicle()

        if electric:
            engine = Engine('electric')
            self.__product.set_engine(engine)

    def get_product(self):
        product = self.__product
        self.reset()
        return product

    def set_body(self, type_):
        body = Body(type_)
        self.__product.set_body(body)

        wheel = Wheel(18)
        for i in range(2):
            self.__product.set_wheel(wheel)

    def set_seat(self, fabric):
        seat = BikeSeat(fabric)
        self.__product.set_seat(seat)


#------------------------------------------------------------------------------
# A Director works with a Builder (introduced to him by the Client) who has
# knowledge of building Product components. The Director is like a project
# manager who organizes the timing, assembly and delivery of the Product.

class Director:

    def __init__(self, builder=None):
        self.__builder = builder

    def set_builder(self, builder):
        self.__builder = builder

    def construct_car(self):

        self.__builder.reset()
        self.__builder.set_body('sedan')
        self.__builder.set_wheels(4, 22)
        self.__builder.set_engine('400cc')
        self.__builder.set_seats(5, 'leather')

        return self.__builder.get_product()

    def construct_van(self):
        self.__builder.reset()
        self.__builder.set_body('transport')
        self.__builder.set_engine('800cc')
        self.__builder.set_seats(8, 'cloth')
        self.__builder.set_wheels(4, 40)

        return self.__builder.get_product()

    def construct_motorcycle(self):
        self.__builder.reset()
        self.__builder.set_body('motocross')
        self.__builder.set_seats(1, 'vinyl')
        self.__builder.set_engine('250cc')
        self.__builder.set_wheels(2, 44)

        return self.__builder.get_product()

    def construct_bicycle(self):
        self.__builder.reset(electric=True)
        self.__builder.set_body('mountain')
        self.__builder.set_seat('leather')

        return self.__builder.get_product()


#------------------------------------------------------------------------------
# Client Code - the client wants a car.
# He doesnt know how to build car parts or how to put car parts together.
# However, he knows a Builder who can make car parts and a Mechanic that
# knows how to assemble car parts into a car. He introduces the Mechanic
# to his resource for car parts, and gets the final car product from the
# Mechanic once complete.

def main():

    line = 45 * '-'
    director = Director()
    builder = VehicleBuilder()

    print("I want a Car\n{}".format(line))
    director.set_builder(builder)
    vehicle = director.construct_car()
    print(vehicle.specifications())

    print("I want a Motorcycle\n{}".format(line))
    director.set_builder(builder)
    vehicle = director.construct_motorcycle()
    print(vehicle.specifications())

    print("Actually, I meant an Electric Bike\n{}".format(line))

    builder = BikeBuilder()
    director.set_builder(builder)
    vehicle = director.construct_bicycle()
    print(vehicle.specifications())


if __name__ == "__main__":
    main()


