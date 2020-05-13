from controller import start

#------------------------------------------------------------------------------
# Model View Controller Design Pattern
#------------------------------------------------------------------------------
# The MVC design pattern separates the data, presentation and business logic
# of a programs architecture into 3 predominant modules.
#
# Model: consists of pure application logic to interact with the data source
# View: formats data for presentation to the user
# Controller: intermediary between view and model.
#
# User -> Drives -> Controller
# Controller -> Queries -> Model
# Model -> Updates -> View
# View -> Shows -> User

if __name__ == "__main__":

    """ Main end-user entry point to start the controller via its API """
    start()

