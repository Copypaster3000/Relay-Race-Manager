#flat.py
#Drake Wheeler
#8/13/2024
#This file contains the flat class, a subclass of race_leg. It represents flat race legs and includes attributes like traffic delays and water support. 
#The class provides methods to estimate and log the time required to complete these legs, considering the unique factors of flat terrain.

from errors import RedundancyError
from errors import MissingDataError
from race_leg import race_leg
import random

class flat(race_leg):
    #constructor
    def __init__(self, order = -1, distance = -1, traffic_delay = -1, water_support = False, type = 'Flat'):
        super().__init__(order, distance, type) 
        self._traffic_delay = traffic_delay
        self._water_support = water_support


    #overloaded string operator, returns class data members, throws MissingDataError if data member's still set to default value
    def __str__(self):
        water_status = "Yes" if self._water_support else "No"
        return (f"{super().__str__()},   Traffic delay: {self._traffic_delay} mins,   Water support: {water_status}")


    #displays the estimated time of the leg for the athlete to run
    def display_estimate(self, athlete):
        estimated_time = float(self.estimate_time(athlete))
        water_status = "Yes" if self._water_support else "No"

        print(f"Leg #{self._order},   Runner: {athlete.get_name()},   Distance: {self._distance} miles,   Type: {self._type},   Water Support: {water_status},   Est. leg time: {estimated_time} mins", end="")

        return estimated_time
    

    
    #randomizes flat leg stats appropriately, expects leg order to already be set upon instantiation
    #throws ValueError if order not already set
    def randomize(self):
        self._distance = round(random.uniform(3.0, 15.0), 1) #set leg distance randomly between 3 and 15 miles, rounded to 1 decimal
        if(random.randint(1, 5) == 1): self += random.randint(1, 15) #set's traffic delay randomly to 1-15 mins 1/5th of the time, uses classes overloaded += operator to do so
        else: 
            try:
                self.reset_traffic() #sets traffic delay to 0
            except ValueError as e:
                print(e) #displays error if traffic was already at 0

        try:
            if(random.randint(1, 2) == 1): self.update_water(True) #sets the trail to have water support half of the time
        except ValueError as e:
            print(e) #displays error if updated water function updates water support value to the same value it already was


        if(self._order == -1): 
                raise ValueError("Value Error. Flat's order data member was still set to the default value when it was randomized.")


    #pass in the athlete and the estimated time to finish the leg will be returned
    #this function cannot predict traffic delays
    def estimate_time(self, athlete):
        time = (self._distance / athlete.get_speed()) * 60 #sets the time in number of minutes base on runners speed and race leg distance

        if(self._water_support): #if there is water support
            time *= 0.9 #decrease time by 10%
        else: #if there is not water support
            time *= 1.1 #increase time by 10%

        return int(round(time)) #return estimated time rounded to an int


    #updates the athletes new running speed and returns the actual time the entire leg took 
    def log_actual_time(self, athlete):
        actual_time = float(input(f"\nEnter the time in minutes it actually took for {athlete.get_name()} to run leg {self._order}: "))

        #sets athletes new speed with actual time for running this leg, does not factor in time the athlete waited at the end of the leg
        #for the van from a traffic delay
        try:
            athlete.set_speed(self.calc_flat_speed(actual_time)) 
        except ValueError as e:
            print(e) #prints error if speed was attempted to be set to less then or equal to 0
        
        if(self._traffic_delay > 0): #if there was a traffic delay, add it to the time it took for the athlete to complete the leg
            actual_time += self._traffic_delay
            print(f"Uh oh! The van got caught in traffic. It took an addition {self._traffic_delay} minutes to reach the athlete after they finished their leg. This contributes to the overall race time.")

        return round(actual_time, 2) #returns time the entire leg took, until the next leg was able to start

    
    #pass in the time it took for the runner to run the leg, returns speed in mph
    def calc_flat_speed(self, time):
        return (self._distance / time) * 60 #calculates and return speed in mph

        
    #overloads the += operator to add time to traffic delay, throw ValueError if a negative number was attempted to be added to the traffic delay
    def __iadd__(self, delay):
        if(delay >= 0): self._traffic_delay += delay
        else: raise ValueError("Value Error. A negative number was attempted to be added to traffic delay using the += operator. Not allowed!")

        return self


    #updates whether or not the leg has water support (water support makes the estimate leg time faster), throws RedundancyError if the function call was redundant
    def update_water(self, water):
        if(water == self._water_support):
            raise RedundancyError("Redundancy Error. The water support function 'updated' water support to the same value it already was.")

        self._water_support = water


    #update resets the traffic delay to 0, throw RedundancyError if function call was redundant
    def reset_traffic(self):
        if(self._traffic_delay == 0): #if traffic delay is already 0 throw error
            raise RedundancyError("Redundancy Error. The traffic delay was already 0 minutes when it was reset.")
        
        self._traffic_delay = 0 #set traffic delay to 0

