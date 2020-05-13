#------------------------------------------------------------------------------
# Flywieght | Structural Design Pattern
#------------------------------------------------------------------------------
# The Flyweight (or Cache)  Pattern allows you to fit more objects into ram by
# sharing common parts of state between multiple objects isntead of keeping all
# the data in each object.
#
# - They Flyweight Pattern is sometimes known as the Cache Pattern.
# - The constant data of an objects is commonly called the intrinsic state,
#   it lives within the object, other objects can read it but not change it.
# - The rest of an object's state, often altered by other objects from the
#   outside is called the extrinsic state.
# - The flyweight pattern suggests to stop storing the extrinsic state inside
#   the object, instead pass the state to the specific methods that rely on it.
# - When only the instrisic state stays within the object, it can be reused in
#   different contexts, which tends to reduce the number of objects needed.
# - In most cases, the extrinsic state gets moved to the container object which
#   aggregates objects before applying the flyweight pattern. Alternatively, a
#   separate context class would store the extrinsic state along with a
#   reference to the lfywieght object.
# - The most memory consuming fields are moved to a few flyweight objects, such
#   that hundreds of small contextual objects can resuse a single heavy
#   flyweight object instead of hundres of copies of the data.
# - Immutability is important. Since the same flyweight object can be used in
#   different contexts, you have to make sure its state cant be modified; a
#   flyweight objcet should initialize its state just once, and not expose any
#   public fields or setters to other objects.
# - A Flyweight factory can be used to provide access to various flyweights,
#   perhaps managing a cache pool.
# - If your program doesnt deal with a shortage of RAM this pattern may be
#   superfluous.


import json

#------------------------------------------------------------------------------


class Flyweight():
    """
    The Flyweight stores a common portion of the state (also called intrinsic
    state) that belongs to multiple real business entities. The Flyweight
    accepts the rest of the state (extrinsic state, unique for each entity)
    via its method parameters.
    """

    def __init__(self, shared_state):
        self._shared_state = shared_state

    def operation(self, unique_state):
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print("Flyweight: Displaying shared ({s}) "
              "and unique ({u}) state.\n".format(s=s, u=u))


class FlyweightFactory():
    """
    The Flyweight Factory creates and manages the Flyweight objects. It ensures
    that flyweights are shared correctly. When the client requests a flyweight,
    the factory either returns an existing instance or creates a new one, if it
    doesn't exist yet.
    """

    _flyweights = {}  # class attribute dictionary

    def __init__(self, initial_flyweights):
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = Flyweight(state)

    def get_key(self, state):
        """
        Returns a Flyweight's string hash for a given state.
        This is just an underscore delimited string of each record
        """
        return "_".join(sorted(state))

    def get_flyweight(self, shared_state):
        """
        Returns an existing Flyweight with a given state or creates a new one.
        """

        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            print("FlyweightFactory: Can't find a flyweight, "
                  "creating new one [{}].".format(key))
            self._flyweights[key] = Flyweight(shared_state)
        else:
            print("FlyweightFactory: Reusing existing flyweight"
                  "[{}].".format(key))

        return self._flyweights[key]

    def list_flyweights(self):
        count = len(self._flyweights)
        result = '\n'.join(map(str, self._flyweights.keys()))
        print("FlyweightFactory: I have {c} flyweights:"
              "\n{r}".format(c=count, r=result))


#------------------------------------------------------------------------------
# Client Code

def add_car_to_police_database(factory, plates, owner, brand, model, color):
    """
    The client code either stores or calculates extrinsic state and passes it
    to the flyweight's methods.
    """
    print("\nClient: Adding a car to database.")
    flyweight = factory.get_flyweight([brand, model, color])
    flyweight.operation([plates, owner])


def main():
    """
    The client code usually creates a bunch of pre-populated flyweights in the
    initialization stage of the application.
    """

    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])

    factory.list_flyweights()

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "M5", "red")

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "X1", "red")

    factory.list_flyweights()


if __name__ == "__main__":
    main()



