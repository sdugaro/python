#------------------------------------------------------------------------------
# Mediator | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Mediator Pattern lets you reduce chaotic dependencies between objects.
# It restricts direct communication between objects and forces them to
# collaborate via a mediator object.
#
# - The mediator object encapsulates how a set of objects interact.
# - The Mediator pattern promotes loose coupling by preventing objects from
#   referring to each other explicitly, and allows their interaction to be
#   varied and managed in a central location.
# - Each colleague knows who the mediator is, and the mediator knows about
#   all colleagues in play.


class Mediator:
    """
    Implement cooperative behavior by coordinating Colleague objects.
    The mediator object knows and maintains all colleagues.
    """

    def __init__(self):
        self._colleagues = (Colleague1(self), Colleague2(self))

    def mediate(self):
        print("Introduce yourselves:")
        for c in self._colleagues:
            print(c.__class__.__name__)



class Colleague1:
    """
    Each colleague knows its Mediator object, and communicates with
    the mediator when it would have otherwise communicated directly
    with another colleague.
    """

    def __init__(self, mediator):
        self._mediator = mediator


class Colleague2:
    """
    Each colleague knows its Mediator object, and communicates with
    the mediator when it would have otherwise communicated directly
    with another colleague.
    """

    def __init__(self, mediator):
        self._mediator = mediator


#------------------------------------------------------------------------------
# Client Code

def main():
    mediator = Mediator()
    mediator.mediate()


if __name__ == "__main__":
    main()
