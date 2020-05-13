from model import Person

#------------------------------------------------------------------------------
# The View is responsible for representing the Model data back to the end user
# - the controller directs the view to respond based on input from the end user
# - in other words, the controller triggers an update to the view
# Since the View's job is to represents the Model's data to the user, naturally
# it should have access to the Model's API. The controller provides additional
# information about how the end user is expecting to see the Model's data


#------------------------------------------------------------------------------
# Public API - expected to be used by the controller

def show_all_view(person_list):
    """ Return the number and people in the controller provided data """
    message = 'Our DB has [{}] users:'.format(len(person_list))
    print(message)
    for person in person_list:
        print(person.name())


def start_view():
    print 'Model/View/Controller - Basic Example'
    print 'Do you want to see everyone in my db?[y/n]'


def end_view():
    print 'Goodbye!'
