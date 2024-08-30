#steep.py
#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/13/2024
#This file contains the steep class, which is a specialized subclass of race_leg. It represents a steep leg of a race, including additional attributes such as elevation gain, 
#elevation loss, and the chance of a runner slipping. The class provides methods to estimate and log the time required to complete this challenging segment.ved from race leg. It represents steep race legs.


from errors import MissingDataError
from errors import RedundancyError
from athlete import athlete
from race_leg import race_leg
import random

class steep(race_leg):
    #constructor
    def __init__(self, order = -1, distance = -1, elevation_gain = -1, elevation_loss = -1, slip = False, type = 'Steep'):
       super().__init__(order, distance, type)
       self._elevation_gain = elevation_gain
       self._elevation_loss = elevation_loss
       self._slip = slip


    #overloaded string operator, returns class details, throws MissingDataError if there's data displayed that is still set to default value
    def __str__(self):
        slip_status = "Yes" if self._slip else "No"
        return (f"{super().__str__()},   Elevation gain: {self._elevation_gain}ft,   Elevation loss: {self._elevation_loss}ft,   Slip: {slip_status}")


    #randomize trail stats appropriately 
    #expects trail leg order to already be set upon instantiation, throws MissingDataError if order not already set
    def randomize(self):
        self._distance = round(random.uniform(3.0, 15.0), 1) #set leg distance randomly between 3 and 15 miles, rounded to 1 decimal
        self._elevation_gain = int(random.uniform(0, 2000)) #sets elevation gain randomly between 0 and 2000
        self._elevation_loss = int(random.uniform(0, 2000)) #sets elevation loss randomly between 0 and 2000
        if(random.randint(1, 4) == 1): self._slip = True #sets trail to cause runner to slip 1/4th of the time

        if(self._order == -1): 
                raise MissingDataError("Missing Data Error. A steep leg did not have it's order set already when it was randomized.")


    #displays the estimated time of the leg for the athlete to run
    def display_estimate(self, athlete):
        estimated_time = float(self.estimate_time(athlete))

        print(f"Leg #{self._order},   Runner: {athlete.get_name()},   Distance: {self._distance} miles,   Type: {self._type},   Elevation gain: {self._elevation_gain}ft,   Elevation loss: {self._elevation_loss}ft,   Est. leg time: {estimated_time} mins", end="")

        return estimated_time


    #returns the estimated time to complete this leg, pass in the athlete running this leg
    #the estimate cannot predict if the runner will slip during this race leg
    def estimate_time(self, athlete):
        time = (self._distance / athlete.get_speed()) * 60 #sets time with miles to complete leg based on distance and runners mph speed
        
        time *= (1 + (self.calc_ave_incline() / 10)) #adjusts time for average incline of the race leg

        return int(round(time)) #returns the estimated time rounded to an int


    #get the actual time it took the athlete to complete the race leg from user, uses that to calc athlete's new flat speed and updates it
    #then returns the athlete's leg time including any additional time due to issues on the leg
    def log_actual_time(self, athlete):
        actual_time = float(input(f"\nEnter the time in minutes it actually took for {athlete.get_name()} to run leg #{self._order}: "))

        #sets athlete new speed with their calculated flat speed based on their actual time for this leg
        try:
            athlete.set_speed(self.calc_flat_speed(actual_time)) 
        except ValueError as e:
            print(e) #prints error if speed was attempted to be set to less then or equal to 0

        #if this race leg caused the runner to slip...
        if(self._slip):
            print(f"{athlete.get_name()} slipped while running this leg, it added an additional 5 minutes to their actual time.")
            print("They did not become injured they will stay in the race.")
            actual_time += 5

        return actual_time #returns the time runner ran this leg in
        

    #this calculates the athletes flat speed base on the steep trail they ran
    def calc_flat_speed(self, time):
        #undo the incline adjustment
        adjusted_time = time / (1 + (self.calc_ave_incline() / 10))
        #convert back to hours
        adjusted_time /= 60
        #calculate flat speed in mph
        flat_speed = self._distance / adjusted_time

        return round(flat_speed, 2) #return speed rounded to 2 decimal points


    #returns the total elevation change from start to finish of the leg, returns 0 is there is bad data used to calc elevation change
    def calc_elevation_change(self):
        if(self._elevation_gain < 0 or self._elevation_loss < 0): return 0 

        return self._elevation_gain - self._elevation_loss


    #returns the incline rounded to 2 decimal places
    def calc_ave_incline(self):
        if(self._elevation_gain < 0 or self._elevation_loss < 0): return 0 #set it to throw error if bad input
        return round((self.calc_elevation_change() / (self._distance * 5280)) * 100, 2)


    #updates whether the trail causes the runner to slip (which adds to their estimated time on the leg), throw RedundancyError if function call was redundant
    def update_slip(self, slip):
        if(self._slip == slip):
            raise RedundancyError("Redundancy Error. A steep object's slip status was 'updated' to the value it already was.")

        self._slip = slip

