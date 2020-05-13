import json
import datetime

from pprint import pformat
from dateutil import parser
from collections import OrderedDict

#------------------------------------------------------------------------------
# Insert and leverage meta data into the JSON serialization/deserialization
# Consider the convenience of Pythons __repr__() as it relates to being able
# to 'stringify' and reconstruct custom classes
#
# Use object_hook to deserialize the string representation of date for JSON
# back into a native python object.
#
# Use object_pairs_hook to preserve the order of the JSON datastructure on
# disk as it is read back in, since by default the python dictionary loaded
# by JSON will not preserve order
#
# NOTE: the difference between data types pushed
# object_pairs_hook (recieves a list a list of tuples)
# >>>>> [(u'_type', u'datetime'), (u'value', u'2020-01-19 15:07:38')]
# used to initialize the defined Callable
# (ie OrderedDict can be constructed with tuple arguments )
# >>> d = OrderedDict([(u'_type', u'datetime'), (u'value', u'2020-01-19 15:07:38')])
# >>> d
# >>> '_type' in d
# True
# while object_hook (recieves a dictionary).
# object_hook is NOT invoked if the object_pairs_hook is set



def object_pairs_hook(obj):
    print "||>>", obj
    obj_pair = OrderedDict(obj)
    if '_type' in obj_pair:  # discard the meta data on load
        if obj_pair['_type'] == 'datetime':
            return parser.parse(obj_pair['value'])
    return obj_pair


class RoundTripEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                "_type": "datetime",
                "value": obj.strftime("{} {}".format(
                    self.DATE_FORMAT, self.TIME_FORMAT
                ))
            }
        return super(RoundTripEncoder, self).default(obj)



class RoundTripDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self,
                                  object_hook=self.object_hook,
                                  object_pairs_hook=self.object_pairs_hook,
                                  #object_pairs_hook=OrderedDict,
                                  *args, **kwargs)

    # data pairs from the JSON files structure are provided in recursive order
    # so they can be processed and returned in the same order seen on disk.
    # Here we can reconstruct any objects that were serialized as strings back
    # into the python objects from which they came as if they were native types.
    # Having found the meta data we were looking for we can discard it, and
    # simply return a newly constructed instance of the object.
    def object_pairs_hook(self, obj):
        print ">>>>", obj
        obj_pair = OrderedDict(obj)  # convert list of tuples to ordered dict
        if '_type' in obj_pair:      # discard the meta data, returning only object
            if obj_pair['_type'] == 'datetime':
                return parser.parse(obj_pair['value'])
        return obj_pair

    # not called if object_pairs_hook set. recieves pairwise dict
    def object_hook(self, obj):
        print "-->>", obj
        if '_type' not in obj:
            return obj
        _type = obj['_type']
        if _type == 'datetime':
            return parser.parse(obj['value'])
        return obj


#------------------------------------------------------------------------------
# Populate a data dictionary with python datetime objects
# NOTE: order is not maintained in the dictionary, so JSON data isn't either


data  = {
    "id": 45,
    "male": True,
    "name": "Steve Dugaro",
    "occupation": ["Software Engineer", "Technical Director"]
}
data = OrderedDict(data)  # dict order above not guaranteed, but now it is

dt = datetime.datetime.now()
for m in range(0, 12):
    key = "dt{}".format(m + 1)
    #data.update({key: dt.replace(month=m + 1)})
    data[key] = dt.replace(month=m + 1)

line = 75 * '-'
print("PYTHON DATA:\n{0}".format(line))
print(pformat(data))
print(" SERIALIZED IN MEMORY STRING:\n{0}".format(line))
print(json.dumps(data, cls=RoundTripEncoder, indent=2))

fname = "export_date.json"
print("SERIALIZING TO DISK\n{0}".format(line))
print("| ordered datetime objects encoded as strings (see file): {}".format(fname))
with open(fname, "w") as fd:
    # export objects in 'reconstructable' format using native JSON literals
    # data is exported EXACTLY AS represented in the python dictionary
    json.dump(data, fd, cls=RoundTripEncoder)

print("\n{1}\nDESERIALIZING FROM DISK: {0}\n{1}".format(fname, line))
with open(fname, "r") as fd:
    data = json.load(fd, cls=RoundTripDecoder)
    #data = json.load(fd, cls=RoundTripDecoder, object_pairs_hook=object_pairs_hook)


print "{1}\nRAW LOADED DATA:\n{0}\n{1}".format(data, line)
print("USING DESERIALIZED OBJECTS | setting year to 1999:")
for k, v in data.items():
    print(k, v),
    if isinstance(v, datetime.datetime):
        print(v.replace(year=1999))
