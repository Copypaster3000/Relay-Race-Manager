#2_3_tree.py
#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/13/2024
#This file implements the two_three_tree class, which manages a 2-3 tree structure to store and organize race legs. The class provides methods to insert race legs, retrieve them based on their order, 
#and display all the details of the race in sequence. The 2-3 tree ensures that the race legs are efficiently managed and accessible.

import random
from node import node
from race_leg import race_leg
from trail import trail
from steep import steep
from flat import flat

class two_three_tree:
    #constructor
    def __init__(self):
        self._root = None #Initialize root of the tree with null

    #returns the race leg object that matches the order passed in
    def retrieve(self, order):
        if self._root is None: return False

        return self._retrieve(self._root, order)


    #recursive part
    #returns the race leg object that matches the order passed in
    def _retrieve(self, root, order):
        if(order == root._data[0].get_order()):  #if the first data matches the order passed in
            return root._data[0] #return the data object

        if(len(root._child) >= 1 and order < root._data[0].get_order()): #if there is a left child, and the order passed in less than this node's left data
            return self._retrieve(root._child[0], order) #traverse to the left child

        if(len(root._data) >= 2 and order == root._data[1].get_order()): #if there is a second data and it matches the order passed in
            return root._data[1] #return the data object

        #if there is a second child, and there is not a second data member in this node, or order is less than or equal to the order of the second data
        if((len(root._child) >= 2) and (len(root._data) < 2 or order <= root._data[1].get_order())):
            return self._retrieve(root._child[1], order) #traverse to the second child

        #else if the other cases weren't  hit and there is a third child
        if(len(root._child) >= 3):
            return self._retrieve(root._child[2], order) #traverse to the third child

        return False #if it made it here, return false for no match
        



    #pass in the leg order the athlete is running and the athlete to log the time they ran the race leg
    def log_time(self, order, athlete):
        return self._log_time(self._root, order, athlete)


    def _log_time(self, root, order, athlete):
        if(order == root._data[0].get_order()):  #if the first data matches the order passed in
            return root._data[0].log_actual_time(athlete) #log the athlete's time for that leg

        if(len(root._child) >= 1 and order < root._data[0].get_order()): #if there is a left child, and the order passed in less than this node's left data
            return self._log_time(root._child[0], order, athlete) #traverse to the left child

        if(len(root._data) >= 2 and order == root._data[1].get_order()): #if there is a second data and it matches the order passed in
            return root._data[1].log_actual_time(athlete) #log the athlete's time for that leg

        #if there is a second child, and there is not a second data member in this node, or order is less than or equal to the order of the second data
        if((len(root._child) >= 2) and (len(root._data) < 2 or order <= root._data[1].get_order())):
            return self._log_time(root._child[1], order, athlete) #traverse to the second child

        #else if the other cases weren't  hit and there is a third child
        if(len(root._child) >= 3):
            return self._log_time(root._child[2], order, athlete) #traverse to the third child
        


    #goes to the leg # passed in with order, and displays the leg estimate with the athlete passed in, returns the estimated time for the leg
    #returns None if there is no matching leg in the tree
    def display_pre_race_estimate(self, order, athlete):
        return self._display_pre_race_estimate(self._root, order, athlete)


    #recursive part of display_race estimate
    def _display_pre_race_estimate(self, root, order, athlete):
        if(order == root._data[0].get_order()):  #if the first data matches the order passed in
            return root._data[0].display_estimate(athlete) #display the estimate for that leg

        if(len(root._child) >= 1 and order < root._data[0].get_order()): #if there is a left child, and the order passed in less than this node's left data
            return self._display_pre_race_estimate(root._child[0], order, athlete) #traverse to the left child

        if(len(root._data) >= 2 and order == root._data[1].get_order()): #if there is a second data and it matches the order passed in
            return root._data[1].display_estimate(athlete) #display the estimate for that leg

        #if there is a second child, and there is not a second data member in this node, or order is less than or equal to the order of the second data
        if((len(root._child) >= 2) and (len(root._data) < 2 or order <= root._data[1].get_order())):
            return self._display_pre_race_estimate(root._child[1], order, athlete) #traverse to the second child

        #else if the other cases weren't  hit and there is a third child
        if(len(root._child) >= 3):
            return self._display_pre_race_estimate(root._child[2], order, athlete) #traverse to the third child

        return None

            

    #displays all the nodes in race leg order with all of their details, returns true for success, False if there is nothing to display
    def display_all_details(self):
        if self._root is None: return False #nothing to display

        self._display_all_details(self._root) #displays tree

        return True #returns true for success


    #recursive part of in order display
    def _display_all_details(self, node):
        if(node.get_num_child() > 0): #if the node has children
            self._display_all_details(node.get_child(0)) #traverse to the left first

        print(node.get_data(0)) #display first data element

        if(node.get_num_child() > 1): #if the node has more than one child
            self._display_all_details(node.get_child(1)) #traverse to second child

        if(node.get_num_data() == 2): #if the node has two data
            print(node.get_data(1)) #display second data element

        if(node.get_num_child() == 3): #if the node has three children
            self._display_all_details(node.get_child(2))


    #this function creates an entire 2-3 tree with as many nodes as the int passed in
    #it creates each leg randomly and with random statistics in appropriate ranges
    #returns true for success, false if there is still no tree at classes root data member after the function ran
    def create_tree(self, legs):
        leg_orders = list(range(1, legs + 1)) #creates a list of numbers, one for each leg in the race
        random.shuffle(leg_orders) #shuffles their order to randomize the order of race leg types so the race isn't in a pattern of each race leg type every third leg

        #creates each type of race leg 1/3 of the time, and sets them with a random order
        for i in range(legs):
            if(i % 3 == 0):
                race_leg = trail(leg_orders[i])
            elif(i % 3 == 1): 
                race_leg = steep(leg_orders[i])
            elif(i % 3 == 2):
                race_leg = flat(leg_orders[i])

            try:
                race_leg.randomize() #randomizes the race leg
            except ValueError as e:
                print(e) #displays error if the race legs order was not already set when it was randomized

            try:
                self.insert(race_leg) #inserts the race leg properly into the 2-3 tree
            except TypeError as e:
                print(e) #display error if wrong object type was attempted to be added to the tree

        if self._root is not None: return True #there is a tree successfully created a stored at root

        return False #something went wrong there is no tree at root


    #given a race leg object, this function inserts it into the tree properly, throws TypeError is non race leg object was attempted to be inserted
    def insert(self, leg_object):
        if not isinstance(leg_object, race_leg):
            raise TypeError("Type Error. A non race leg object was attempted to be inserted to the 2-3 tree.")

        if self._root is None: #if there is no node in the tree yet
            self._root = node(leg_object) #set root to new node, with new data passed in
        else: #otherwise, call recursive insert function at add new data at proper leaf
            self._root = self._insert(self._root, leg_object)


    #recursive part of insert function, returns the root of the new tree after insertion
    def _insert(self, current, leg_object):
        #if this node is not a leaf
        if not current.is_leaf():
            next_index = current.next_traversal_child(leg_object) #get the index of the next child to be traversed to

            child = self._insert(current.get_child(next_index), leg_object) #hold onto the node returned by the next frame of the recursive call into the proper child

            #check if child is a child of this current node, if not, it's a new node resulting from a split and needs to be added to the current one
            if child is not current.get_child(next_index): #if the child returned is a new node, not the one that was traversed to
                #replaces child traversed into with new child return and caught on line 98
                if current.integrate_split(next_index, child) is not True: print("Error. Issue integrating a split back into the tree.")

                if(current.split_me()): return self._split(current) #return the root of the split subtree
            else: 
                #set current's child pointer that was traversed into with the child that was returned and held onto on line 64
                try:
                    current.set_child(next_index, child) #propagates any changes back up as function unwinds
                except TypeError as e:
                    print(e) #displays error is non node object is attempted to be set as a child
             
            return current

        #if current node is leaf
        try:
            current.add_n_sort_data(leg_object) #adds and sorts new data object to current node
        except TypeError as e:
            print (e) #display error about wrong data type attempted to be added to node's data

        #if the node needs to be spilt, meaning it has three data members now, return the root of the subtree created by splitting it
        if(current.split_me()): return self._split(current)

        #returns the current node after insertion happened, without a split having occurred 
        return current
            

    #pass in the node to be split, returns the root of the new split node subtree
    def _split(self, node_to_split):
        #hold onto the middle data of the original node to split to make it the data of the root of this subtree
        middle_data = node_to_split.get_data(1)
        left_child = node(node_to_split.get_data(0)) #creates a left child node with the node_to_splits left data as it's only data
        right_child = node(node_to_split.get_data(2)) #creates a right child node with the node_to_splits right data as it's only data

        #CHECK THIS
        #if the node to split is not a leaf node
        if not node_to_split.is_leaf():
            try:
                #reassign the node_to_split's children as children to the children node's of the new right and left children of the new root of the subtree
                left_child.add_n_sort_child(node_to_split.get_child(0)) 
                left_child.add_n_sort_child(node_to_split.get_child(1))
                right_child.add_n_sort_child( node_to_split.get_child(2))
                right_child.add_n_sort_child(node_to_split.get_child(3))
            except TypeError as e:
                print(e) #display error if no node data type was attempted to be added as a node's child

        #create new root node of the split node subtree
        root_of_split = node([middle_data], [left_child, right_child])
        
        return root_of_split #return the root of this split subtree to be used by the node_to_split's parent





