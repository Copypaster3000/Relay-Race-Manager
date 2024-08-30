#test_two_three_tree.py
#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/13/2024
#This file provides unit tests for the two_three_tree class. It checks the insertion, retrieval, and display functions of the tree, ensuring that the tree correctly manages and organizes the race legs.

import pytest
from errors import MissingDataError
from errors import RedundancyError
from node import node
from two_three_tree import two_three_tree
from flat import flat
from steep import steep
from trail import trail
from athlete import athlete


@pytest.fixture
def setup_tree():
    #initialize the two_three_tree object and some race legs and an athlete for testing
    tree = two_three_tree()
    leg1 = flat(order=1, distance=10.0, traffic_delay=5, water_support=False)
    leg2 = steep(order=2, distance=8.0, elevation_gain=1000, elevation_loss=500, slip=False)
    leg3 = trail(order=3, distance=12.0, difficulty=2, twists_ankle=False, bear_attack=False)
    leg4 = flat(order=4, distance=10.0, traffic_delay=5, water_support=True)
    leg5 = steep(order=5, distance=8.0, elevation_gain=1000, elevation_loss=500, slip=True)
    leg6 = trail(order=6, distance=12.0, difficulty=2, twists_ankle=True, bear_attack=True)
    athlete1 = athlete(name='Drake', speed=7.5)
    return tree, leg1, leg2, leg3, leg4, leg5, leg6, athlete1



#tests the 2-3 tree's insert function
def test_insert(setup_tree):
    tree, leg1, leg2, leg3, leg4, leg5, leg6, athlete1 = setup_tree #unpack fixture
    
    #insert legs into the tree, goes through all paths in function, causes split
    tree.insert(leg1)
    tree.insert(leg2)
    tree.insert(leg3)
    tree.insert(leg4)
    tree.insert(leg5)
    tree.insert(leg6)
    
    #tests if the root exists and the legs are in the correct places in the tree after insertion
    assert tree._root is not None
    assert tree._root.get_data(0) == leg2
    assert tree._root.get_data(1) == leg4
    assert tree._root.get_child(0).get_data(0) == leg1
    assert tree._root.get_child(1).get_data(0) == leg3
    assert tree._root.get_child(2).get_data(0) == leg5
    assert tree._root.get_child(2).get_data(1) == leg6

    #tests error raises

    #test insertion of a non-race_leg object to trigger TypeError
    with pytest.raises(TypeError) as error:
        tree.insert(athlete1)  #passing an athlete object instead of a race_leg object
    assert str(error.value) == "Type Error. A non race leg object was attempted to be inserted to the 2-3 tree."
    assert tree._root.get_data(0) == leg2  #ensuring tree state hasn't changed

    #test insertion of None to trigger TypeError
    with pytest.raises(TypeError) as error:
        tree.insert(None)  #passing None instead of a race_leg object
    assert str(error.value) == "Type Error. A non race leg object was attempted to be inserted to the 2-3 tree."
    assert tree._root.get_data(0) == leg2  #ensuring tree state hasn't changed

    #test insertion of an incorrect type object to trigger TypeError
    with pytest.raises(TypeError) as error:
        tree.insert("This is a string, not a race_leg")  #passing a string instead of a race_leg object
    assert str(error.value) == "Type Error. A non race leg object was attempted to be inserted to the 2-3 tree."
    assert tree._root.get_data(0) == leg2  #ensuring tree state hasn't changed





#test the retrieve function from the 2-3 tree
def test_retrieve(setup_tree):
    tree, leg1, leg2, leg3, leg4, leg5, leg6, _ = setup_tree #unpack fixture
    
    #insert race legs into the tree
    tree.insert(leg1)
    tree.insert(leg2)
    tree.insert(leg3)
    tree.insert(leg4)
    tree.insert(leg5)
    tree.insert(leg6)
    
    #test retrieving the inserted legs, returns leg of order # passed into function
    assert tree.retrieve(1) == leg1
    assert tree.retrieve(2) == leg2
    assert tree.retrieve(3) == leg3
    assert tree.retrieve(4) == leg4
    assert tree.retrieve(5) == leg5
    assert tree.retrieve(6) == leg6
    
    #test retrieving a non-existent leg
    assert tree.retrieve(7) is False


#tests the log_time function of the tree which take the user input actual time and returns adjusted time for issue the runner faced on race leg
def test_log_time(setup_tree, monkeypatch):
    tree, leg1, leg2, leg3, leg4, leg5, leg6, athlete1 = setup_tree #unpack fixture
    
    #insert legs and test logging time
    tree.insert(leg1)
    tree.insert(leg2)
    tree.insert(leg3)
    tree.insert(leg4)
    tree.insert(leg5)
    tree.insert(leg6)
    
    #mock the input for log_actual_time
    monkeypatch.setattr('builtins.input', lambda _: "20")

    #tests the correct output for log_time where the runner encounters each possible scenario on the trail
    #check that the actual time gotten from user is updated and returned correctly 
    actual_time = tree.log_time(1, athlete1)
    assert actual_time == 20 + leg1._traffic_delay 

    actual_time = tree.log_time(2, athlete1)
    assert actual_time == 20 + (5 if leg2._slip else 0)  #adjust for slip time if applicable

    actual_time = tree.log_time(3, athlete1)
    assert actual_time == 20 * (2 if leg3._bear_attack else 1) * (1.2 if leg3._twists_ankle else 1)

    actual_time = tree.log_time(4, athlete1)
    assert actual_time == 20 + leg4._traffic_delay  

    actual_time = tree.log_time(5, athlete1)
    assert actual_time == 20 + (5 if leg5._slip else 0)  

    actual_time = tree.log_time(6, athlete1)
    assert actual_time == 20 * (2 if leg6._bear_attack else 1) * (1.2 if leg6._twists_ankle else 1)



#tests the display_pre_race_estimate function of the two_three_tree class
def test_display_pre_race_estimate(setup_tree):
    tree, leg1, leg2, leg3, leg4, leg5, leg6, athlete1 = setup_tree #unpack fixture
    
    #insert legs and test the display of pre-race estimates
    tree.insert(leg1)
    tree.insert(leg2)
    tree.insert(leg3)
    tree.insert(leg4)
    tree.insert(leg5)
    tree.insert(leg6)
    
    #tests that the estimated time returned from the tree function matches the estimated time for the specific athlete and leg
    estimated_time = tree.display_pre_race_estimate(1, athlete1)
    assert estimated_time == leg1.estimate_time(athlete1)

    estimated_time = tree.display_pre_race_estimate(2, athlete1)
    assert estimated_time == leg2.estimate_time(athlete1)

    estimated_time = tree.display_pre_race_estimate(3, athlete1)
    assert estimated_time == leg3.estimate_time(athlete1)

    estimated_time = tree.display_pre_race_estimate(4, athlete1)
    assert estimated_time == leg4.estimate_time(athlete1)

    estimated_time = tree.display_pre_race_estimate(5, athlete1)
    assert estimated_time == leg5.estimate_time(athlete1)

    estimated_time = tree.display_pre_race_estimate(6, athlete1)
    assert estimated_time == leg6.estimate_time(athlete1)

    estimated_time = tree.display_pre_race_estimate(7, athlete1)
    assert estimated_time == None #should be None if there is no matching leg in the tree


#tests the create_tree function of the two_three_tree class
def test_create_tree(setup_tree):
    tree, *_ = setup_tree #unpack fixture
    
    #test creating a tree with random legs
    success = tree.create_tree(5)
    assert success is True #test the function returns true for successful creation
    assert tree._root is not None #tests that root is now not None

    #tests there are now 5 race legs in the tree 1-5
    assert tree.retrieve(1) is not False
    assert tree.retrieve(2) is not False
    assert tree.retrieve(3) is not False
    assert tree.retrieve(4) is not False
    assert tree.retrieve(5) is not False



#tests the display_all_details function of the two_three_tree class
def test_display_all_details(setup_tree, capsys):
    tree, leg1, leg2, leg3, leg4, leg5, leg6, _ = setup_tree #unpack fixture
    
    #insert legs and test displaying all details
    #insert legs and test the display of pre-race estimates
    tree.insert(leg1)
    tree.insert(leg2)
    tree.insert(leg3)
    tree.insert(leg4)
    tree.insert(leg5)
    tree.insert(leg6)

    #call the display function and hold it's return value
    result = tree.display_all_details()

    #capture the output that was printed
    captured = capsys.readouterr()

    #define expected display
    expected_display = (
    "Leg #1,   Distance: 10.0 miles,   Type: Flat,   Traffic delay: 5 mins,   Water support: No\n"
    "Leg #2,   Distance: 8.0 miles,   Type: Steep,   Elevation gain: 1000ft,   Elevation loss: 500ft,   Slip: No\n"
    "Leg #3,   Distance: 12.0 miles,   Type: Trail,   Difficulty: Medium,   Twists ankle: No,   Bear attack: No\n"
    "Leg #4,   Distance: 10.0 miles,   Type: Flat,   Traffic delay: 5 mins,   Water support: Yes\n"
    "Leg #5,   Distance: 8.0 miles,   Type: Steep,   Elevation gain: 1000ft,   Elevation loss: 500ft,   Slip: Yes\n"
    "Leg #6,   Distance: 12.0 miles,   Type: Trail,   Difficulty: Medium,   Twists ankle: Yes,   Bear attack: Yes\n"
    )

    #compare the captured output with the expected output
    assert captured.out == expected_display
    assert result is True