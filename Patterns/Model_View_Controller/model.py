import json

#------------------------------------------------------------------------------
# The Model consists of pure application logic, such as
# - interfacing with a database
# - storing/filtering/maintaining relevant data in memory
# - providing and interface to the data for View & Controller


class Person(object):
    JSONFILE = "db.txt"

    def __init__(self, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name

    def name(self):
        """ return the full Person name """
        return ("{} {}".format(self.first_name, self.last_name))

    @classmethod
    def get_all(self):
        """ Poll the database for people names.
        Return a list of Person Objects for which an interface is provided.
        """

        with open(self.JSONFILE, "r") as database:
            json_list = json.load(database)


        result = []
        for item in json_list:
            person = Person(item['first_name'], item['last_name'])
            result.append(person)
        return result



