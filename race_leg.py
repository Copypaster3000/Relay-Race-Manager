#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/14/2024
#This file contains the race_leg class, which is the base class for representing a leg of a race. It holds essential information about the race leg, 
#such as its order, distance, and type. The class provides methods to access these details and ensures that all required data is correctly set before use.

from errors import MissingDataError

class race_leg:
    def __init__(self, order = -1, distance = -1, type = ""):
        self._order = order
        self._distance = distance
        self._type = type


    #returns the race legs order
    def get_order(self):
        return self._order


    #overloaded string operator, returns data members, throws MissingDataError is a data member is still set to default value
    def __str__(self):
        if(self._order == -1 or self._distance == -1 or self._type == ""): #if there is data that is still at default value, throw error
            raise MissingDataError("Missing Data Error. Data displayed with __str__ is still at a default value.")

        return (f"Leg #{self._order},   Distance: {self._distance} miles,   Type: {self._type}")