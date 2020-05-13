
import view

from model import Person

#------------------------------------------------------------------------------
# The controller module is the end user interface/API.
# - end user interacts with the controller (via start in main)
# - the controller interacts with the model (following end user commands/events)
# - the view returns the result of the request back to the end user
# The controller intermediates between the view and model


def __show_all():
    """ retrieve data from the Model and provide it to the View for display """
    people_in_db = Person.get_all()
    return view.show_all_view(people_in_db)


#------------------------------------------------------------------------------
# Public API

def start():
    """ interface with the end user to drive what the view returns """
    view.start_view()
    input = raw_input()
    if input == 'y':
        return __show_all()
    else:
        return view.end_view()

