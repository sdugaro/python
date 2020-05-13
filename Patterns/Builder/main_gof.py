# https://python-patterns.guide/gang-of-four/builder/

#------------------------------------------------------------------------------
# Builder | Creational Design Pattern
#------------------------------------------------------------------------------
# Compose complex objects from simple objects algorithmically
#
# - Builder is largely used for what the GOF considered a secondary benefit,
#   convenience. Client code stays simple even while directing the creation of
#   elaborate object hierarchies. The caller is exempt from needing to manually
#   instantiate each objecte or understand how the objects fit together.
# - Rigid use of the pattern is rare in Python in so far as the client doesn't
#   always need a reference to be returned from a Builder or Director; libraries
#   are often designed to be used directly.
#

# reference to the product (plot) holding the data

import numpy as NP
import matplotlib.image as IMG
import matplotlib.pyplot as PLT

#------------------------------------------------------------------------------


class Director():

    @staticmethod
    def plot_sin(min, max, step):

        x = NP.arange(min, max, step)
        PLT.plot(x, NP.sin(x))
        PLT.gcf()  # get current figure
        PLT.show()


#------------------------------------------------------------------------------
# Client Code - the client wants to plot a function

def main():

    """
    The matplotlib interface lets the caller build a simple plot with just a
    line of code, and save an image of a plot with just a line of code. The
    interface has hidden from the caller many complex objects that had to be
    created for matplotlib to represent a simple plot. matplotlib allows
    customization via keyword arguments and hides all the details of how
    plots are represented as objects.
    """

    """ client asks builder (library) to build a plot """
    x = NP.arange(-6.2, 6.2, 0.1)
    PLT.plot(x, NP.sin(x))

    """ client asks builder for a reference to the plot product """
    plot = PLT.gcf()          # get current figure
    plot.savefig('sine.png')  # client saves the reference to disk
    #PLT.savefig('sine.png')  # or could have asked builder to do it

    """ now the client displays a persistent reference of the plot """
    img = IMG.imread('sine.png')
    imgplot = PLT.imshow(img)
    PLT.show()

    """
    The client can use a Director, or do what the director does itself.
    """
    Director.plot_sin(-6, 6, 1)


if __name__ == "__main__":
    main()


