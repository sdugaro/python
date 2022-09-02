import random
import heapq
from pprint import pformat

DEBUG = False
#-------------------------------------------------------------------------------

def dataGenerator(n, data_type="dict" ):
    """
    Generate a stream of random priority items for dev/test
    n (int):
        number of data items to generate
    data_type (str = 'dict' | 'tuple' | 'list':
        the data structure to return the items in
    """
    commands = ["one", "two", "three", "four", "five"]

    for i in range(n):
        if data_type == 'tuple':
            yield (random.randint(0,10) , f"command_{random.choice(commands)}")
        elif data_type == 'list':
            yield [random.randint(0,10) , f"command_{random.choice(commands)}"]
        else:
            yield {random.randint(0,10) : f"command_{random.choice(commands)}"}

#-------------------------------------------------------------------------------
# quick play with heapq from https://docs.python.org/3/library/heapq.html 

if DEBUG:
    data = [x for x in dataGenerator(7, "tuple")]
    print(data)

    heapq.heapify(data)
    print(data)

    next = heapq.heappop(data)
    while next:
        try:
            print(next)
            next = heapq.heappop(data)
        except IndexError:
            next = None

#-------------------------------------------------------------------------------

class SimplePriorityQueue():
    """
    While binary heaps are best for priority queues and the python standard lib
    has one https://docs.python.org/3/library/heapq.html we will implement a 
    priority queue with a simple fixed length array based on the assumption that
    there are 10 priorities. It is easy to envision a fixed list where each
    element is a list of work items which are appended in the same order in they
    are received. We could use a double ended queue (deque) which would allow us
    to pop off the front of the work item list, but we will use native lists and
    maintain a reverse order so they are easy to pop off the back.

    NB: PY3K now implicitly inherits the obect base class
    """

    def __init__(self):
        """
        Initialize the data structure to hold priorty work items.
        NB: Could have defined as a __private class variable
        NB: Could have maintained a dictionary with priorities as keys
        """
        self.q = [[] for i in range(11)]


    def add(self, item):
        """
        Insert item into the queue given its priority

        item (dict):
            an item to insert into the priority queue of the form
            {int priority: str command} where priority is [0,10]
        returns:
            None
        """
        if type(item) is not dict or len(item) != 1:
            raise TypeError("Expected {int: command}")

        try:
            data = tuple(item.items())
            priority, command = data[0]
            self.q[priority].insert(0, (priority,command))

        except IndexError:
            info = "It seems your priorities are out of bounds.\n"
            info+= "Sorry, but I can only add priorities [0-10]"
            print(info)

        except ValueError:
            info = "It seems you are trying to use a non-integer priority.\n"
            info+= f"Sorry, but I cant add {item}"
            print(info)


    def pop(self):
        """
        Remove and return the item with highest priority from the queue,
        where the highest priority is 0 and the lowest is 10

        returns:
            a work item command, optionally as a tuple with priority
        """

        item = None
        for i in range(11):

            if not self.q[i]:
                continue

            register = self.q[i]
            item = register.pop()
            break

        return item

#-------------------------------------------------------------------------------

class SimplerPriorityQueue():
    """
    Same idea, but leveraging the fact that the incoming data stream are
    dictionaries, we can maintain the priorities as keys. Sparsernot as
    obvious as a list of lists in terms of conceptualizing Also without
    so many comments for legibility and given inline validation.
    """

    def __init__(self):

        self.q = {}

    def add(self, item):
        if type(item) is not dict or len(item) != 1:
            raise TypeError("Expected {int: command}")

        priority, command = tuple(item.items())[0]
        if type(priority) is not int or priority not in range(11):
            raise TypeError("Expected integer priority in [0,10]")

        if priority in self.q:
            self.q[priority].insert(0,command)
        else:
            self.q[priority] = [command]

    def pop(self):

        item = None
        for i in sorted(self.q.keys()):

            register = self.q.get(i)
            if not register:
                continue

            item = (i, register.pop())
            break

        return item

#-------------------------------------------------------------------------------
# Demonstrate the functionality of our Simple(r)PriorityQueue:
# 1. show the random items being added
# 2. show the populated data structure
# 3. retrieve data in priority order
#
# SimplerPriorityQueue Adding {7: 'command_one'}
# SimplerPriorityQueue Adding {10: 'command_three'}
# SimplerPriorityQueue Adding {0: 'command_three'}
# SimplerPriorityQueue Adding {0: 'command_five'}
# SimplerPriorityQueue Adding {7: 'command_three'}
# SimplerPriorityQueue Adding {9: 'command_one'}
# SimplerPriorityQueue Adding {2: 'command_three'}
#
# {0: ['command_five', 'command_three'],
#  2: ['command_three'],
#  7: ['command_three', 'command_one'],
#  9: ['command_one'],
#  10: ['command_three']}
#
# (0, 'command_three')
# (0, 'command_five')
# (2, 'command_three')
# (7, 'command_one')
# (7, 'command_three')
# (9, 'command_one')
# (10, 'command_three')
# 

data = [x for x in dataGenerator(7)]
if DEBUG: print(data)


#PQ = SimplePriorityQueue()
PQ = SimplerPriorityQueue()
for x in dataGenerator(17):
    print(f"{PQ.__class__.__name__} Adding {x}")
    PQ.add(x)

print('\n', pformat(PQ.q), '\n')

item = PQ.pop()
while item:
    print(item)
    item = PQ.pop()
