#main.py
#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/13/2024
#This file contains the main function of the program. 
#It initializes the race by creating the race legs and athletes, estimating race times, conducting the race, 
#and summarizing the results. It also allows for testing the functionality of the 2-3 tree used in the program.

from race_log import race_log


def main():
    app = race_log()

    app.create_race()

    app.create_athletes()

    app.estimate_race()

    app.conduct_race()
    
    app.race_summary()

    print("\nNow that the race is over, would you like to..")
    print("1) Test the functionality of the 2-3 tree")
    print("2) End the program")
    choice = int(input("Enter your choice as an integer: "))

    if choice is not 2:
        app.use_23_functionality()

    print("\nThe program has ended.")




if __name__ == "__main__":
    main()