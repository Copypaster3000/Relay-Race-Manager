#athlete.py
#Drake Wheeler
#8/13/2024
#This file contains the athlete class, representing a runner in the race. The class stores the athlete's name, speed, and injury status. 
#It provides methods to manage and retrieve these attributes, ensuring that the athlete's data is accurately maintained throughout the race.


from errors import RedundancyError

class athlete:
    #constructor pass in name and running speed in mph
    def __init__(self, name = '', speed = -1):
        self._name = name #will hold the runners name
        self._speed = speed #this will be updated with the actual speed runners ran the last leg at and converted to flat speed
        self._injured = False #this will be set to true if the runner gets injured and can no longer run


    #returns the name of the athlete
    def get_name(self):
        return self._name

    #returns the runners current speed
    def get_speed(self):
        return self._speed 

    
    #updates the runners current speed, convert it to flat speed before passing it in
    #throw errors if speed passed in is less than or equal to zero
    def set_speed(self, speed):
        if(speed <= 0): 
            raise ValueError(f"Value Error. {self._name}'s speed was attempted to be set to less than or equal to zero, the speed has not been updated.")

        self._speed = speed


    #set injured data member with truth value passed in, throws RedundancyError is function call was unnecessary 
    def set_injury(self, injured):
        if(self._injured == injured):
            raise RedundancyError("Redundancy Error. Athlete's injured status was 'updated' to the value it already was.")

        self._injured = injured

    
    #returns whether or not athlete is injured
    def get_injury(self):
        return self._injured 


