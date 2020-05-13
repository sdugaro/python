#------------------------------------------------------------------------------
# Facade | Structural Design Pattern
#------------------------------------------------------------------------------
#
# A Facade provides a unified interface to a set of interfaces in a subsystem
# It defines a higher-level interface and delegates to subsystems accordingly.
#
#

import random
from time import sleep


#------------------------------------------------------------------------------
# Subsystem Classes
# - prefixed with '_' to identify as Components, akin to protected member vars

class _IgnitionSystem(object):

    @staticmethod
    def produce_spark():
        return True if random.random() > 0.5 else False


class _Engine(object):

    def __init__(self):
        self._revsper_minute = 0

    def turnon(self):
        self._revsper_minute = 2000

    def turnoff(self):
        self._revsper_minute = 0


class _FuelTank(object):

    def __init__(self, level=30):
        self._level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level


class _DashBoardLight(object):

    def __init__(self, is_on=False):
        self._is_on = is_on

    def __str__(self):
        return self.__class__.__name__

    @property
    def is_on(self):
        return self._is_on

    @is_on.setter
    def is_on(self, status):
        self._is_on = status

    def status_check(self):
        if self._is_on:
            print("{}: ON".format(str(self)))
        else:
            print("{}: OFF".format(str(self)))


class _HandBrakeLight(_DashBoardLight):
    pass


class _FogLampLight(_DashBoardLight):
    pass


class _Dashboard(object):

    def __init__(self):
        self._lights = {"handbreak": _HandBrakeLight(), "fog": _FogLampLight()}

    def show(self):
        for light in self._lights.values():
            light.status_check()


#------------------------------------------------------------------------------
# Facade

class Car(object):
    """
    The Composite Class that assembles components into a subsystem and then
    delgates client requests to its components appropriately.
    """

    def __init__(self):
        self._ignition_system = _IgnitionSystem()
        self._engine = _Engine()
        self._fuel_tank = _FuelTank()
        self._dashboard = _Dashboard()

    @property
    def km_per_litre(self):
        return 17.0

    def consume_fuel(self, km):
        litres = min(self._fuel_tank.level, km / self.km_per_litre)
        self._fuel_tank.level -= litres

    def start(self, tries=10):
        print("\nStarting...")
        self._dashboard.show()

        count = 0
        while count < tries:
            spark = self._ignition_system.produce_spark()
            if spark:
                print("Engine Started[{}/{}]".format(count, tries))
                self._engine.turnon()
                return

            print("Attempt [{}/{}] Did Not Start".format(count, tries))
            count += 1
            sleep(1)

        print("Can't start. Faulty ignition system")

    def has_enough_fuel(self, km, km_per_litre):
        litres_needed = km / km_per_litre
        if self._fuel_tank.level > litres_needed:
            return True
        else:
            return False

    def drive(self, km=100):
        print("\n")
        if self._engine._revsper_minute > 0:
            while self.has_enough_fuel(km, self.km_per_litre):
                self.consume_fuel(km)
                print("Drove {}km".format(km))
                print("{:.2f}l of fuel still left".format(self._fuel_tank.level))
        else:
            print("Can't drive. The Engine is turned off!")

    def park(self):
        print("\nParking...")
        self._dashboard._lights["handbreak"].is_on = True
        self._dashboard.show()
        self._engine.turnoff()

    def switch_fog_lights(self, status):
        print("\nSwitching {} fog lights...".format(status))
        boolean = True if status == "ON" else False
        self._dashboard._lights["fog"].is_on = boolean
        self._dashboard.show()

    def fill_up_tank(self):
        print("\nFuel tank filled up!")
        self._fuel_tank.level = 100


#------------------------------------------------------------------------------
# Client Code

def main():

    car = Car()
    car.start()
    car.drive()
    car.switch_fog_lights("ON")
    car.switch_fog_lights("OFF")
    car.park()
    car.fill_up_tank()
    car.drive()
    car.start()
    car.drive()


if __name__ == "__main__":
    main()

