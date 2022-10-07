from multiprocessing.spawn import get_preparation_data
import random
from datawarehouse.service import BaseService

# I am aware that this isnt actually maxint, its an example.
MAX_INT = 999999999

# The ExampleService class houses all the methods and logic required to service the example routes.
class ExampleService(BaseService):

    # this is a constructor for the class. You'd write a constructor if you wanted to setup some initial variables or state.
    # Its actually optional to have a constructor for classes in python, but its nice to have.
    def __init__(seed=None):
        if seed:
            random.seed(seed)

    # this just returns a random integer.
    @classmethod
    def getRandomInt(self, min=0, max=MAX_INT):
        return random.randint(min, max)

    # Very inefficient method of getting a random even integer, but it stands to show how a service will contain the logic.
    # you wouldnt have this logic inside the controller file (though this code is short) because we keep the controller file as slim as possible.
    @classmethod
    def getRandomEvenInt(self, min=0, max=MAX_INT):
        x = 1
        while x % 2 != 0:
            x = self.get_random_int(min, max)

        return x
