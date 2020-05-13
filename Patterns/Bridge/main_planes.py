#------------------------------------------------------------------------------
# Bridge | Structural Design Pattern
#------------------------------------------------------------------------------
# A Bridge Pattern is a standard practice which splits the abstraction from
# the interface in order to prevent cartesian product complexity explosion.
#
# - The Bridge pattern favors composition over inheritance, since depending on
#   the problem, inheritance can lead to a superfluous combination of derived
#   classes to attain appropriate coverage.
# - This is illustrated in the following example of airplanes where organizing
#   the various types between Military/Commercial + Cargo/Passenger via
#   inheritance would result in 4 classes MilitaryCargo, MilitaryPassenger,
#   CommercialCargo, CommercialPassenger. Then adding a single new
#   distinguishing feature such as Short/Long Haul suddenly results in 8
#   classes. This grows explonentially, 2^n for each level.
# - Instead, create one class for each of the types in different categories.
#   Military/Commercial can be grouped into a Plane type parent class, and
#   Cargo/Passenger can be grouped into a Carrier type parent class. Then a
#   bridge pattern provides the architectural structure that connects the two
#   parent class groupings. This is done by simply passing one of the parent
#   class objects as a parameter to the constructor of the other parent class.
# - The parent base class defines the abstract creation methods which the child
#   classes inherit and implement.


""" Cargo/Passenger Carriers """


class Carrier:
    def carry_military(self, items):
        pass

    def carry_commercial(self, items):
        pass


class Cargo(Carrier):
    def carry_military(self, items):
        print("The plane carries {} military cargo goods".format(items))

    def carry_commercial(self, items):
        print("The plane carries {} commercial cargo goods".format(items))


class Passenger(Carrier):
    def carry_military(self, passengers):
        print("The plane carries {} military passengers".format(passengers))

    def carry_commercial(self, passengers):
        print("The plane carries {} commercial passengers".format(passengers))


"""
Military/Commercial Planes - initalized with a Carrier

NB: The Py2k super() syntax is backwards compatible in Py3k. Whereas just
calling super() without arguments as you would in Py3k will raise a TypeError
in Py2k requiring arguments. In order to use super in Py2k, the parent base
classes must inherit from object, which is implicit in Py3k, otherwise a
"TypeError: must be type, not classobj" will be raised.
"""


class Plane(object):
    def __init__(self, Carrier):
        self.carrier = Carrier

    def display_description(self):
        pass

    def add_objects(self):
        pass


class Commercial(Plane):
    def __init__(self, Carrier, objects):
        super(Commercial, self).__init__(Carrier)
        self.objects = objects

    def display_description(self):
        self.carrier.carry_commercial(self.objects)

    def add_objects(self, new_objects):
        self.objects += new_objects


class Military(Plane):
    def __init__(self, Carrier, objects):
        super(Military, self).__init__(Carrier)
        self.objects = objects

    def display_description(self):
        self.carrier.carry_military(self.objects)

    def add_objects(self, new_objects):
        self.objects += new_objects


#------------------------------------------------------------------------------
# Client Code

def main():

    cargo = Cargo()
    passenger = Passenger()

    """
    Bridge Miltary and Cargo Classes.  Passing the Military class a Cargo
    instance defines the notion of a Military Cargo Plane through composition.
    """
    military1 = Military(cargo, 100)
    military1.display_description()
    military1.add_objects(25)
    military1.display_description()

    """
    Bridge Miltary and Passenger Classes.
    This defines the notion of a Military Passenger Plane through composition.
    """
    military2 = Military(passenger, 250)
    military2.display_description()
    military2.add_objects(10)
    military2.display_description()

    """
    Bridge Commercial and Passenger Classes.
    This defines the notion of a Commercial Passenger Plane via composition.
    """
    commercial1 = Commercial(passenger, 400)
    commercial1.display_description()
    commercial1.add_objects(50)
    commercial1.display_description()

    """
    Bridge Commercial and Cargo Classes.
    This defines the notion of a Commercial Cargeo Plane via composition.
    """
    commercial2 = Commercial(cargo, 150)
    commercial2.display_description()
    commercial2.add_objects(15)
    commercial2.display_description()


if __name__ == "__main__":
    main()


