#test_race_legs.py
#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/13/2024
#This file holds the test functions which test the public methods of the race legs in the core hierarchy. 

import pytest
from errors import MissingDataError
from errors import RedundancyError
from athlete import athlete
from race_leg import race_leg
from trail import trail
from steep import steep
from flat import flat


#tests the get_order function of the race_leg class
def test_race_leg_get_order():
    leg1 = race_leg(10) #create race legs with positive, zero and negative order
    leg2 = race_leg(0)
    leg3 = race_leg(-5)

    #check that get_order returns the order in all cases
    assert leg1.get_order() == 10 
    assert leg2.get_order() == 0
    assert leg3.get_order () == -5


#tests all the getter functions of the athlete class
def test_athlete_get_functions():
    athlete1 = athlete() #create an athlete with default values
    athlete2 = athlete("drake", 7) #create an athlete named drake that runs at 7 mph

    #test all the get functions
    assert athlete1.get_name() == ""
    assert athlete2.get_name() == "drake"
    assert athlete1.get_speed() == -1
    assert athlete2.get_speed() == 7
    assert athlete1.get_injury() == False
    athlete1.set_injury(True)
    assert athlete1.get_injury() == True


#tests the set speed function of the athlete class
def test_athlete_set_speed():
    athlete1 = athlete('drake', 8) #create an athlete named drake with a running speed of 8 mph

    athlete1.set_speed(9) #set speed to 9
    assert athlete1._speed == 9 #test that the speed was updated to 9

    with pytest.raises(ValueError) as error:
        athlete1.set_speed(-3) #set speed to a negative number, then test that the correct error was thrown
    assert str(error.value) == "Value Error. drake's speed was attempted to be set to less than or equal to zero, the speed has not been updated."
    assert athlete1._speed #test that the speed was not updated after it was attempted to be set to an invalid speed

    

#tests the set injury function of the athlete class
def test_athlete_set_injury():
    athlete1 = athlete('guy', 8) #injury stats is always set to False on the instantiation of an athlete

    with pytest.raises(RedundancyError) as error:
        athlete1.set_injury(False) #check the correct error is thrown when set injury is called to update injury to the value it already was
    assert str(error.value) == "Redundancy Error. Athlete's injured status was 'updated' to the value it already was."
    assert athlete1._injured == False #check that injured is still false

    athlete1.set_injury(True) #set injured to true
    assert athlete1._injured == True #check set_injury did update injured to true


#test all the functions to do with runners time in the trail class
def test_trail_running_time_functions(monkeypatch):
    athlete1 = athlete("Drake", 6) #create an athlete named drake with a running speed of 6 mph
    trail_leg = trail(1, 2, 3, False, False) #create a trail leg that is the first leg, 2 miles, difficult 3, doesn't twist ankle, no bear attack
    trail_leg2 = trail(1, 2, 3, True, True) #same but does twist ankle and there is a bear attack

    assert trail_leg.estimate_time(athlete1) == 30 #the estimated time for an athlete that runs 6 mph on flat for this trail is 30 minutes

    #simulates the input of 40 for runners actual time when input is called in log_actual_time
    monkeypatch.setattr('builtins.input', lambda _: "40")
    assert trail_leg.log_actual_time(athlete1) == 40 #gets actual time from user, returns it, also sets runners new current flat running speed

    assert athlete1.get_speed() == 4.5 #checks runners new current flat running speed, 4.5 makes sense since the runner ran slower than estimated with previous current running speed, so they slowed down
    assert trail_leg2.log_actual_time(athlete1) == 96 #checks that a runner twists their ankle and then getting attacked by a bear increase their time by 20% and then another 100%

    
#tests the update bear meal function of the trail leg class. The function updates the eaten_by_bear status. Pass in whether the trail section twists
#the runners ankle and the function returns the classes updated ankle twisting status
def test_trail_update_bear_meal(monkeypatch):
    trail_leg_1 = trail(1, 2, 3, False, True) #create a trail leg object that is the first leg, is two miles, has a difficulty of three, does not twist the runners ankle, and does get eaten by a bear
    trail_leg_2 = trail(1, 2, 3, False, False)

    #test that regardless of _bear_attack, the class's data member, initial value and combination of change, it returns the correctly updated value
    
    with pytest.raises(RedundancyError) as error: #tests that correct error is thrown for updating stat to what it already was
        trail_leg_1.update_bear_meal(True)
    assert str(error.value) == "Redundancy Error. Trail's bear attack status was 'updated' to the value it already was."
    assert trail_leg_1._bear_attack == True #tests that the bear attack value correctly stays the same

    trail_leg_1.update_bear_meal(False) #update bear attack from true to false
    assert trail_leg_1._bear_attack == False #test bear attack is now false

    with pytest.raises(RedundancyError) as error:
        trail_leg_2.update_bear_meal(False) #update bear attack from false to false
    assert str(error.value) == "Redundancy Error. Trail's bear attack status was 'updated' to the value it already was." #test it throws correct error for redundancy
    assert trail_leg_2._bear_attack == False #test bear attack is still false
    
    trail_leg_2.update_bear_meal(True) #update bear attack from false to true
    assert trail_leg_2._bear_attack == True #test bear attack is now true


#tests the twist ankle function of the trail leg class. The function updates the trails twist ankle status. Pass in whether the trail section twists
#the runners ankle and the function returns the classes updated ankle twisting status
def test_trail_twist_ankle():
    trail_leg_1 = trail(1, 2, 3, False, False) #create a trail leg object that is the first leg, is two miles, has a difficulty of three, and does not twist the runners ankle, and does not get eaten by a bear
    trail_leg_2 = trail(1, 2, 3, True, False)

    #test that regardless of _twists_ankle, the class's data member's initial value and combination of change it updates correctly and throws correct errors

    with pytest.raises(RedundancyError) as error:
        trail_leg_1.update_twist_ankle(False) #update twists ankle from false to false
    assert str(error.value) == "Redundancy Error. Trail's twits ankle stats was 'updated' to the value it already was." #test correct error is thrown 
    assert trail_leg_1._twists_ankle == False #test twists ankle is still false

    trail_leg_1.update_twist_ankle(True)  #update twists ankle from false to true
    assert trail_leg_1._twists_ankle == True #test twists ankle is now true

    with pytest.raises(RedundancyError) as error:
        trail_leg_2.update_twist_ankle(True) #update twists ankle from true to true
    assert str(error.value) == "Redundancy Error. Trail's twits ankle stats was 'updated' to the value it already was." #test correct error is thrown for redundancy 
    assert trail_leg_2._twists_ankle == True #test twists ankle is still true
        
    trail_leg_2.update_twist_ankle(False) #update twists ankle from true to false
    assert trail_leg_2._twists_ankle == False #test twists ankle is now false


#test the overloaded __str__ function from the trail leg class. The function is used to print the class object details. 
def test_trail__check_difficulty():
    trail_leg1 = trail(1, 2, -1, False, False) #create a trail leg object that is the first leg, is two miles, has a difficulty of -1(meaning it has not been logged), and does not twist the runners ankle, and does not get eaten by a bear
    trail_leg2 = trail(1, 2, 1, False, False) #creates one object for each edge case and and middle cases. Difficulty can be from 1-3
    trail_leg3 = trail(1, 2, 2, False, False)
    trail_leg4 = trail(1, 2, 3, False, False)
    trail_leg5 = trail(1, 2, 4, False, False)

    #checks each possible case for correct output
    assert trail_leg1.check_difficulty() == "No difficulty level has been logged"
    assert trail_leg2.check_difficulty() == "Easy"
    assert trail_leg3.check_difficulty() == "Medium"
    assert trail_leg4.check_difficulty() == "Hard"
    assert trail_leg5.check_difficulty() == "The difficulty is set to something invalid"


#test the overloaded string function of the trail class
def test_trail__str__():
    trail_leg = trail(1, 2, 3, False, False) #create a trail leg object that is the first leg, is two miles, has a difficulty of three, and does not twist the runners ankle, and does not get eaten by a bear
    trail_leg2 = trail()

    #tests output format for correctness 
    assert str(trail_leg) == "Leg #1,   Distance: 2 miles,   Type: Trail,   Difficulty: Hard,   Twists ankle: No,   Bear attack: No"

    with pytest.raises(MissingDataError) as error:
        print(trail_leg2) #tests error is thrown when string is used but the object is missing data
    assert str(error.value) == "Missing Data Error. Data displayed with __str__ is still at a default value."




#test all the functions to do with runners time in the trail class
def test_steep_running_time_functions(monkeypatch):
    athlete1 = athlete("Drake", 7) #create an athlete named drake that runs at 7 mph
    steep_leg1 = steep(2, 5, 1000, 200, False) #create a steep leg that is order #2, 5 miles, 1000 ft elevation gain, 200ft elevation loss and does not make the runner slip
    steep_leg2 = steep(2, 5, 1000, 200, True)

    assert steep_leg1.estimate_time(athlete1) == 55.84 #checks time estimate based on leg distance, athlete speed, and trails average incline

    #simulates the input of 60 for runners actual time when input is called in log_actual_time
    monkeypatch.setattr('builtins.input', lambda _: "60")
    assert steep_leg1.log_actual_time(athlete1) == 60

    assert athlete1.get_speed() == 6.51 #checks the athlete's updated 'flat speed' which was updated by log_actual_time using the runners actual time input from user

    assert steep_leg2.log_actual_time(athlete1) == 65 #checks that slip = true adds 5 minutes to actual time


#test teh calc_elevation_change function from the steep class.
def test_steep_calc_elevation_change():
    steep_leg1 = steep(5, 6, 400, 100, False) #create a steep object that is the 5th leg, is 6 miles, has 400 feet elevation gain and 100 feet elevation loss, slip is false
    steep_leg2 = steep(5, 6, 0, 0, False) #creates object for all different cases of elevation data members
    steep_leg3 = steep(5, 6, -100, -400, False)
    steep_leg4 = steep(5, 6, 100, 500, False)

    #test that the output is correct with valid data and returns 0 with invalid data
    assert steep_leg1.calc_elevation_change() == 300
    assert steep_leg2.calc_elevation_change() == 0
    assert steep_leg3.calc_elevation_change() == 0
    assert steep_leg4.calc_elevation_change() == -400


#tests teh calc_ave_incline function from the steep class
def test_steep_calc_ave_incline():
    steep_leg1 = steep(12, 5, 300, 200, False) #create a steep object that is the 12th leg, 5 miles, 300ft elevation gain, 200ft elevation loss, slip is false
    steep_leg2 = steep(12, 5, 0, 0, False) #creates object for all different cases of elevation data members
    steep_leg3 = steep(12, 5, 100, 500, False)
    steep_leg4 = steep(12, 5, -20, -50, False)

    #test that the output is the correct incline for legs with valid data and that it returns 0 for leg with invalid data
    assert steep_leg1.calc_ave_incline() == 0.38
    assert steep_leg2.calc_ave_incline() == 0
    assert steep_leg3.calc_ave_incline() == -1.52
    assert steep_leg4.calc_ave_incline() == 0


#test the update_slip function of the steep class
def test_steep_update_slip():
    steep_leg1 = steep(10, 8, 200, 300, True) #create a steep object that is the 10th leg, 8 miles, 200ft elevation gain, 300 feet elevation loss, slip is false
    steep_leg2 = steep(10, 8, 200, 300, False)

    #checks that the function properly updates the class's slip data member regardless of it's previous state and what it is changed to and throws the correct 
    #error when a redundant update occurs
    with pytest.raises(RedundancyError) as error:
        steep_leg1.update_slip(True)
    assert str(error.value) == "Redundancy Error. A steep object's slip status was 'updated' to the value it already was."
    assert steep_leg1._slip == True

    steep_leg1.update_slip(False)
    assert steep_leg1._slip == False

    with pytest.raises(RedundancyError) as error:
        steep_leg2.update_slip(False)
    assert str(error.value) == "Redundancy Error. A steep object's slip status was 'updated' to the value it already was."
    assert steep_leg2._slip == False

    steep_leg2.update_slip(True)
    assert steep_leg2._slip == True


#test the overloaded string function of the steep class
def test_steep__str__():
    steep_leg = steep(10, 8, 200, 300, True) #create a steep object that is the 10th leg, 8 miles, 200ft elevation gain, 300 feet elevation loss, slip is false
    steep_leg2 = steep()

    assert str(steep_leg) == "Leg #10,   Distance: 8 miles,   Type: Steep,   Elevation gain: 200ft,   Elevation loss: 300ft,   Slip: Yes"

    with pytest.raises(MissingDataError) as error:
        print(steep_leg2)
    assert str(error.value) == "Missing Data Error. Data displayed with __str__ is still at a default value."




#this function test all the time related functions of the flat class
def test_flat_running_time_functions(monkeypatch):
    athlete1 = athlete("Drake", 4) #create an athlete named drake that runs at 4 mph
    athlete2 = athlete("Grace", 6)
    flat_leg1 = flat(2, 3, 10, False) #create a flat race leg that is the second leg, 3 miles, has a 10 min traffic delay, and no water support
    flat_leg2 = flat(3, 3, 0, True)

    #check the estimate time functions for two athletes with different running speeds
    assert flat_leg1.estimate_time(athlete1) == 49.5
    assert flat_leg2.estimate_time(athlete2) == 27

    #simulates the input of 40 for each runners actual time when input is called in log_actual_time
    monkeypatch.setattr('builtins.input', lambda _: "40")
    assert flat_leg1.log_actual_time(athlete1) == 50
    assert flat_leg2.log_actual_time(athlete2) == 40

    #checks athlete's updated speeds after actual time was logged
    assert athlete1.get_speed() == 4.5
    assert athlete2.get_speed() == 4.5


#tests the iadd or += overloaded operator of the flat class. 
def test_flat__iadd__():
    flat_leg1 = flat(20, 5, 0, False) #create a flat object that is leg 20, 5 miles, has 0 mins traffic delay, and does not have water support

    #test the overloaded += function to add time to traffic delay
    flat_leg1 += 0
    assert flat_leg1._traffic_delay == 0
    flat_leg1 += 5
    assert flat_leg1._traffic_delay == 5

    with pytest.raises(ValueError) as error: #Using += with a negative number should raise an error
        flat_leg1 += -10 #this test that if a negative number is added it doesn't change the traffic delay
    assert str(error.value) == "Value Error. A negative number was attempted to be added to traffic delay using the += operator. Not allowed!" #checks the error thrown
    assert flat_leg1._traffic_delay == 5 #+= a negative number should not chang the traffic delay so it should still be what it previously was


#tests the update_water function of the flat class
def test_flat_update_water():
    flat_leg1 = flat(5, 4, 0, False) #creates a flat object that is leg 5, 4 miles, 0 traffic delay, no water support
    flat_leg2 = flat(5, 4, 0, True) 

    #tests that the water support data member it properly updated in all cases and throws error when function call is redundant

    with pytest.raises(RedundancyError) as error:
        flat_leg1.update_water(False)
    assert str(error.value) == "Redundancy Error. The water support function 'updated' water support to the same value it already was."
    assert flat_leg1._water_support == False

    flat_leg1.update_water(True)
    assert flat_leg1._water_support == True

    with pytest.raises(RedundancyError) as error:
        flat_leg2.update_water(True)
    assert str(error.value) == "Redundancy Error. The water support function 'updated' water support to the same value it already was."
    assert flat_leg2._water_support == True

    flat_leg2.update_water(False)
    assert flat_leg2._water_support == False


#tests the reset_traffic function of the flat class
def test_flat_reset_traffic():
    flat_leg1 = flat(5, 4, 0, False) #creates flat object that is leg 5, 4 miles, 0 traffic delay, no water support
    flat_leg2 = flat(5, 4, 10, False)
    flat_leg3 = flat(5, 4, -4, False)

    #checks that the function resets the traffic delay regardless of previous value and throws error when function call was redundant

    with pytest.raises(RedundancyError) as error:
        flat_leg1.reset_traffic()
    assert str(error.value) == "Redundancy Error. The traffic delay was already 0 minutes when it was reset."
    assert flat_leg1._traffic_delay == 0

    flat_leg2.reset_traffic()
    assert flat_leg2._traffic_delay == 0

    flat_leg3.reset_traffic()
    assert flat_leg3._traffic_delay == 0
    

#tests the overloaded string function of the flat class
def test_flat__str__():
    flat_leg = flat(5, 4, 0, False) #creates flat object that is leg 5, 4 miles, 0 traffic delay, no water support
    flat_leg1 = flat() #creates flat object with data members set to default values

    assert str(flat_leg) == "Leg #5,   Distance: 4 miles,   Type: Flat,   Traffic delay: 0 mins,   Water support: No"

    with pytest.raises(MissingDataError) as error:
        print(flat_leg1)
    assert str(error.value) == "Missing Data Error. Data displayed with __str__ is still at a default value."