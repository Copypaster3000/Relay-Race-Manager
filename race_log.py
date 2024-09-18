#race_log.py
#Drake Wheeler
#8/13/2024
#This file defines the race_log class, which manages the overall race, including the athletes and the 2-3 tree that organizes the race legs. 
#It includes methods to create, display, and track the progress of the race, as well as handle various race events and outcomes.

from athlete import athlete
from two_three_tree import two_three_tree
from steep import steep
from flat import flat
from trail import trail

class race_log:
    #constructor
    def __init__(self):
        self._athletes = [] #initialize a list that will holds athletes
        self._injured_athletes = [] #initializes list that will hold injured athletes
        self._healthy_athletes = 0 #holds the number of healthy athletes
        self._completed = True #mark false if the team couldn't complete the race
        self._tree = two_three_tree() #initialize 2-3 tree object that will hold race legs
        self._accumulated_time = 0 #time in minutes spent racing so far
        self._estimated_time = 0 #the estimated time the entire race will take
        self._current_leg = 0 #the leg of the race currently being run
        self._total_legs = 0 #total number of legs in the race


    #creates a randomized race with the number of legs that is passed in, returns true for success or false for error
    def create_race(self):
        print("The race will be randomly generated there are three possible different race leg types. Each leg will be between 3 and 15 miles.")
        print(f"Flat legs have a 50% chance of having water support and a 20% change of having the van get in a traffic delay between 1-15 minutes.")
        print("Traffic delays cannot be predicted ahead of time. Steep legs have an elevation gain and loss between 0 and 2000 feet. They can also cause")
        print("a runner to slip which adds 5 minutes to their time but you can only find out if the runner slipped after the leg. Trail legs have a difficulty")
        print(f"from easy to hard. A runner can also twists their ankle or be attacked by a bear which increases there time by 20% and 50%, these events also")
        print("injure the athlete and take them out for the rest of the race and cannot be predicted before the runner runs the leg. A trail leg twists the")
        print("runners ankle 1/30th of the time and causes a bear attack 1/100th of the time.")
        #store number of race legs from user
        legs = int(input("\nThe race will be randomly generated with appropriate stats. Enter the number of legs you want in your race: "))

        self._total_legs = legs #set total legs data member

        if not self._tree.create_tree(legs): print("Error. There are no race legs in the tree after they were created.")


    #displays all the details of each race leg in order, return true for success, or false for error
    def display_race_details(self):
        if not self._tree.display_all_details(): print("There are no race legs in the tree after they were created.")


    #create the athletes that will be running the race from user input, returns True for success, or False for error
    def create_athletes(self):
        self._healthy_athletes = int(input("\nEnter the number of athletes on your team for this race as an integer: "))
        print("Enter the athletes in the order you want them to run the race in rotation.")

        for i in range(1, self._healthy_athletes + 1): #for each athlete the user wants to create
            name = input(f"\nEnter the name of the runner #{i}: ") #get athletes name from user
            speed = float(input(f"Enter {name}'s flat ground running speed in mph: ")) #get athletes speed from user
            while(speed <= 0): #if the speed entered is invalid
                speed = float(input("The athlete's speed must be greater than 0, enter again:")) #prompt user for new valid speed

            new_athlete = athlete(name, speed) #creates a new athlete object with the details gotten from user
            self._athletes.append(new_athlete) #adds athlete object to the race_log's athletes list

    

    #displays the pre-race estimates
    def estimate_race(self):
        print("\nEst. time: is the estimated time in minutes it will take the runner to complete that leg. Est. start: is the estimated time")
        print("in hours and minutes from the start of the race that the leg will start. So use that time to estimate when then van will need")
        print("to be at the start of that leg to exchange runners. Below is the layout for the race, who is running which leg, the know details")
        print("about the legs and the time estimates.\n")

        for i in range(1, self._total_legs + 1): #for every leg in the race
            leg_time = float(self._tree.display_pre_race_estimate(i, self._athletes[(i - 1) % self._healthy_athletes])) #get estimated time it will take the runner to complete the leg and display all leg stats
            hours = int(self._estimated_time // 60)
            mins = int(self._estimated_time % 60)
            print(f",   Est. start: {hours}:{mins:02d}") #print the estimated start time for this leg in hours and mins from when the leg first started
            self._estimated_time += leg_time #add this legs estimated time to the accumulated estimated time


    #use while the race is going on to track the athlete's leg times, get stats on the leg's they are running and get the estimates for when to be at the start 
    #of the next leg
    def conduct_race(self):
        print("\nAfter each runner runs their leg, enter their actual time completing the leg. This will be used to accurately predict their leg times")
        print("going forward, each estimated leg time as the race goes on is calculated with the latest updated info. After entering the runners leg time")
        print("you will be notified if any issue occurred during that leg which added time to the leg or injured the runner. Any injured runners will be")
        print("taken out of the rotation of runners.")
        print("\nThe race has now begun! Use the estimated leg time to know when the van needs to be at the end of the leg to exchange runners.")

        for i in range(1, self._total_legs + 1): #for every leg in the race
            if(self._healthy_athletes <= 0): #if the team has no more uninjured runners and they didn't complete the last leg
                self._completed = False
                print("Oh no! You have no more healthy athletes on your team, they are all injured. Your team is unable to complete the race.")
                return #exit the function

            hours = int(self._accumulated_time // 60) #store hours from accumulated time that is in minutes
            mins = int(self._accumulated_time % 60) #store minutes 
            print(f"\nTime elapsed since race started: {hours}:{mins:02d}")
            self._tree.display_pre_race_estimate(i, self._athletes[(i - 1) % self._healthy_athletes]) #display the stats for this leg, including the estimated time it will take the runner to complete it
            self._accumulated_time += self._tree.log_time(i, self._athletes[(i - 1) % self._healthy_athletes])  #get the actual time it took the runner to complete the leg, update the runners speed and inform users of any issues that happened on the leg

            if(self._athletes[(i - 1) % self._healthy_athletes].get_injury()): #if the athlete was injured on the leg they just ran
                self._injured_athletes.append(self._athletes[(i - 1) % self._healthy_athletes]) #put that athlete on the injured list
                del self._injured_athletes[(i - 1) % self._healthy_athletes] #remove athlete from healthy athlete list
                self._healthy_athletes -= 1 #subtract 1 from the humber of healthy athletes


    #summarizes the race after it is completed
    def race_summary(self):
        if self._completed is not True:  #if the team did not complete the race
            print("\nI guess these race legs were to treacherous for your athletes. Recruit some tougher runners for next time!")
            return
        
        estimate_hours = int(self._estimated_time // 60) 
        estimate_mins = int(self._estimated_time % 60)
        actual_hours = int(self._accumulated_time // 60)
        actual_mins = int(self._accumulated_time % 60)

        print("\nWell done finishing the race!")
        print(f"It was initially estimated that your team would complete the race in {estimate_hours}:{estimate_mins}.")
        print(f"You actually completed the race in {actual_hours}:{actual_mins}")
            

    #this function allows the user to clearly test all the functionality of the 2-3 tree
    def use_23_functionality(self):
        choice = 0

        print("\nHere are some things you can do to test the functionality of the 2-3 tree which was used to store all the race legs.")
        while choice is not 4:
            print("\n1) Insert")
            print("2) Retrieve a race leg object from the tree (and then display it)")
            print("3) Display all the details of all race legs in order")
            print("4) Exit program")
            choice = int(input("Enter your choice from the menu as an integer: "))

            if(choice == 1):
                self.user_insert()
            elif(choice == 2):
                order = int(input("\nEnter the leg number of the leg you would like to retrieve: "))
                leg = self._tree.retrieve(order)
                if(order is False):
                    print("There is no race leg with that leg number in the tree.")
                else:
                    print(leg)
            elif(choice == 3):
                self._tree.display_all_details()


    #inserts a leg object into the 2-3 tree with user input
    def user_insert(self):
        leg_type = int(input("\nEnter the type of race leg you would like to create 1 for steep, 2 for flat, and 3 for trail: "))
        while leg_type not in (1, 2, 3):
            leg_type = int(input("Enter a valid choice, 1, 2, or 3: "))

        order = int(input("Enter the race leg's order in the race as an integer: "))
        distance = int(input("Enter the race leg's distance in miles: "))

        if(leg_type == 1):
            elevation_gain = int(input("Enter the steep leg's elevation gain in feet: "))
            elevation_loss = int(input("Enter the steep leg's elevation loss in feet: "))
            slip = int(input("Enter 1 if the steep leg causes the runner to slip, 2 if not: "))

            if(slip == 1): slip_arg = True
            else: slip_arg = False

            race_leg = steep(order, distance, elevation_gain, elevation_loss, slip_arg)
        elif(leg_type == 2):
            traffic = int(input("Enter in minutes the traffic delay the team van will run into on this leg: "))
            water = int(input("Enter 1 if this flat leg will have water support, 2 if not: "))

            if(water == 1): water_arg = True
            else: water_arg = False

            race_leg = flat(order, distance, traffic, water_arg)
        else:
            difficulty = int(input("Enter the level of difficulty for this trail as 1, 2, or 3: "))
            while difficulty is not (1 or 2 or 3): difficulty = int(input("Enter a valid number 1, 2, or 3"))
            twist = int(input("Enter 1 to have this trial twist the runners ankle or 2 to not: "))
            bear = int(input("Enter 1 for the runner to be attacked by a bear on this trail or 2 to not: "))

            if(twist == 1): twist_arg = True
            else: twist_arg = False

            if(bear == 1): bear_arg = True
            else: bear_arg = False

            race_leg = trail(order, distance, twist_arg, bear_arg)

        print("Here is the race leg you have created: ")
        print(race_leg)

        self._tree.insert(race_leg)

        print("The race leg has now been inserted into the tree.")


            
                    


        






        
        
