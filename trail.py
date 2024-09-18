#Drake Wheeler
#8/13/2024
#This file defines the trail class, another subclass of race_leg. It represents a trail leg of a race, including attributes such as difficulty, and the possibility of injuries 
#like twisted ankles or bear attacks. The class includes methods to estimate and log the time required for this type of race leg.



from errors import MissingDataError
from errors import RedundancyError
from athlete import athlete
from race_leg import race_leg
import random

class trail(race_leg):
    #constructor
    def __init__(self, order = -1, distance = -1, difficulty = -1, twists_ankle = False, bear_attack = False, type = 'Trail'):
        super().__init__(order, distance, type)
        self._difficulty = difficulty
        self._twists_ankle = twists_ankle
        self._bear_attack = bear_attack


    
    #overloaded string operator, returns class data members, throws MissingDataError is there is data that is still at default value
    def __str__(self):
        twist = "Yes" if self._twists_ankle else "No"
        bear = "Yes" if self._bear_attack else "No"

        return (f"{super().__str__()},   Difficulty: {self.check_difficulty()},   Twists ankle: {twist},   Bear attack: {bear}")

    
    #this function randomizes the trail stats in appropriate ranges
    #it is expected the order of this leg will already be set upon the objects instantiation 
    #throws MissingDataError if order not already set
    def randomize(self):
        self._distance = round(random.uniform(3.0, 15.0), 1) #set leg distance randomly between 3 and 15 miles, rounded to 1 decimal
        self._difficulty = random.randint(1, 3) #set difficulty randomly to 1, 2, or 3
        if(random.randint(1, 30) == 1): self._twist_ankle = True #sets trail to twist ankle 1/30th of the time
        if(random.randint(1, 100) == 1): self._bear_attack = True #sets a bear attack to occur on leg 1/100th of the time

        if(self._order == -1): 
                raise MissingDataError("Missing Data Error. A race leg did not have it's order set already when it was randomized")


    #displays the estimated time of the leg for the athlete to run
    def display_estimate(self, athlete):
        estimated_time = float(self.estimate_time(athlete))

        print(f"Leg #{self._order},   Runner: {athlete.get_name()},   Distance: {self._distance} miles,   Type: {self._type},   Difficulty: {self.check_difficulty()},   Est. leg time: {estimated_time} mins", end="")

        return estimated_time

    
    #pass in the athlete and the estimated time to finish the leg will be returned
    #this function cannot predict the future like twisted ankles or bear attacks!
    def estimate_time(self, athlete):
        time = (self._distance / athlete.get_speed()) * 60 #set time with the number of minutes based on runners speed and race leg distance

        if(self._difficulty == 2): time *= 1.2 #increase estimated time based on difficulty
        if(self._difficulty == 3): time *= 1.5

        return int(round(time)) #returns estimated time rounded to an int


    #this function logs the actual time it took the runner. It gets the time the user says it took the runner to finish the leg, then it tells the user
    #if the runner ran into any accidents on the trail and adds those to the runners leg time. This function updates the runners speed and returns the 
    #time it actually took the runner to complete this leg, this function also sets the athlete's injury status to injured if the trail did injure them
    def log_actual_time(self, athlete):
        actual_time = float(input(f"\nEnter the time in minutes it actually took for {athlete.get_name()} to run leg #{self._order}: "))

        #sets athlete new speed with their calculated flat speed based on their actual time for this leg
        #does not factor in trail issues so that the runners speed remains accurate for future estimations
        try:
            athlete.set_speed(self.calc_flat_speed(actual_time)) 
        except ValueError as e:
            print(e) #prints error if speed was attempted to be set to less then or equal to 0

        if(self._twists_ankle):
            print(f"{athlete.get_name()} twisted their ankle during this leg which added 20% to their time.")
            actual_time *= 1.2 #increases the runners time if they twisted their ankle

        if(self._bear_attack):
            print(f"{athlete.get_name()} was attacked by a bear! Luckily they escaped but it made their time take twice as long!")
            actual_time *= 2  #increases the runners time if they were attacked by a bear

        if(self._twists_ankle or self._bear_attack): 
            print(f"{athlete.get_name()} is now injured and will not be able to run the rest of the race. They will now be skipped over.")
            athlete.set_injury(True)

        return round(actual_time, 2) #returns time the entire leg took, until the next leg was able to start


    #pass in the runners actual time in minutes enter from the user and this will return their updated current flat speed
    #by reverse calculating the same way the estimated time was given
    def calc_flat_speed(self, time):
        if(self._difficulty == 2): adjusted_time = time / 1.2
        elif(self._difficulty == 3): adjusted_time = time / 1.5
        else: adjusted_time = time

        flat_speed = (self._distance / adjusted_time) * 60

        return round(flat_speed, 2)


    #updates whether this trail section gets the runner eaten by a bear or not, throw RedundancyError if function call was redundant
    def update_bear_meal(self, eaten):
        if(self._bear_attack == eaten):
            raise RedundancyError("Redundancy Error. Trail's bear attack status was 'updated' to the value it already was.")

        self._bear_attack = eaten #set eaten by bear stat with value passed in


    #updates whether this trail section twist the runner's ankle, throws RedundancyError is function call was redundant
    def update_twist_ankle(self, twist):
        if(self._twists_ankle == twist):
            raise RedundancyError("Redundancy Error. Trail's twits ankle stats was 'updated' to the value it already was.")

        self._twists_ankle = twist #set twists ankle stat with value passed in


    #displays the trails difficulty to the user, returns the difficulty rating
    def check_difficulty(self):
        if(self._difficulty == -1): return("No difficulty level has been logged")
        elif(self._difficulty == 1): return("Easy")
        elif(self._difficulty == 2): return("Medium")
        elif(self._difficulty == 3): return("Hard")
        else: return("The difficulty is set to something invalid")





