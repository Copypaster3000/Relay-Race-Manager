#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/14/2024
#This file holds the race leg class, it is the parent class of the core hierarchy.

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