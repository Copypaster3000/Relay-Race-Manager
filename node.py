#node.py
#Drake Wheeler
#This file contains the node class, which is used in the 2-3 tree structure that organizes the race legs. Each node can hold up to two 
#race legs and manages its children. The class provides methods to add, sort, and retrieve data, as well as handle node splitting when necessary.

from race_leg import race_leg
from steep import steep
from trail import trail
from flat import flat


class node:
    #constructor, sets data members to empty lists or ensure everything passed in is stored as lists
    def __init__(self, data = None, child = None):
        if data is None: #if no data was passed in
            data = [] #set data to empty list
        elif not isinstance(data, list): #else if data is not a list, meaning a single data object was passed in
            data = [data] #wrap it in a list

        if child is None: #if no children were passed in 
            child = [] #set children to empty list
        elif not isinstance(child, list): #if child is not a list, meaning a single child object was passed in
            child = [child] #convert object to a one element list
        
        #set private data members with values passed in which were turned to lists, as the lists passed in or as empty lists
        self._data = data 
        self._child = child


    #returns the number of data objects stored in node
    def get_num_data(self):
        return len(self._data)

    
    #returns the number of children the node has
    def get_num_child(self):
        return len(self._child)
    

    #set a child of the node at the index passed in with the node that was passed in, raises TypeError is non node object is passed in to_add
    def set_child(self, index, to_add):
        if not isinstance(to_add, node): #if object to set isn't a node, raise error
            raise TypeError("Type Error. A non node object was attempted to be added as a child to a node.")

        self._child[index] = to_add

    #returns true if the node has room for new data without being split
    def room_for_data(self):
        if(len(self._data) <= 1): return True

        return False

    #returns the data member of the index passed in
    def get_data(self, index):
        return self._data[index]


    #add's new child to node and sorts the child nodes in order
    def add_n_sort_child(self, child_node):
        if not isinstance(child_node, node): #if object to add it's a node, raise error
            raise TypeError("Type Error. A non node object was attempted to be added as a child to a node.")

        self._child.append(child_node) #add child node to the list of child pointers

        #use the sort function of lists to sort the list of child nodes base on their first data objects key, gotten
        #by using a lambda function that for every node in the child list returns the node's first data member's key
        self._child.sort(key = lambda node: node.get_data(0).get_order())


    #removes child of index passed in, for case that a split happened and need to delete old child, throws IndexError is there's no child at the index
    def remove_child(self, index):
        if(index < 0 or index > len(self._child)):
            raise IndexError("Index Error. There is no child in the index that remove child was called on.")

        del self._child[index]


    #returns the child with the correlating index passed in
    def get_child(self, index):
        return self._child[index]
        


    #returns true if this node is a leaf, false if it is not
    def is_leaf(self):
        if not self._child: return True #checks if the child list is empty, returns true if it is
        
        return False #return false if list is not empty


    #returns the element of the child node that should be traversed to next to insert the leg_object based on it's order number
    def next_traversal_child(self, leg_object):
        if(leg_object.get_order() < self._data[0].get_order()): return 0 #if the key being added is less than the key of the first data in the node, return left child index

        #if the key being added is greater than the smallest key of this node and there is no second data or is also less than or equal to the second data's order, return middle child index
        if((len(self._data) == 1) or (leg_object.get_order() <= self._data[1].get_order())): return 1

        #else the key being added is greater than the second data's key, return the right child index
        return 2


    #adds leg_object to nodes data members and sorts them, returns true if after adding the node has more than 2 data members and needs to be split
    #throws TypeError if object passed in is not a race leg
    def add_n_sort_data(self, leg_object):
        if not isinstance(leg_object, race_leg):
            raise TypeError("Type Error. The data object that was attempted to be added to a node is not a race leg.")

        self._data.append(leg_object) #add new data to the end of the list

        #using the list's sort function with a lambda function that gets the data's key to sort the data members in order
        self._data.sort(key = lambda data: data.get_order())



    #returns true if there are more than 2 data objects or three children, meaning it need to be spilt
    def split_me(self):
        if(len(self._data) > 2 or len(self._child) > 3): return True

        return False


    #replaces the child node of this node at the index passed in with the new child replacement passed in
    #organizes other functions, returns True for success or False for issue 
    def integrate_split(self, index, replacement):
        try:
            self.remove_child(index)  # removes old child that will be reintegrated as the new split node's child

            self.add_n_sort_data(replacement.get_data(0)) #add data of new node to current node's data, (a new node's data will always be in index 0)

            self.add_n_sort_child(replacement.get_child(0)) #adds and sorts the left child of replacement to the current node's children
            self.add_n_sort_child(replacement.get_child(1)) #the root of a split subtree wil always have two children

            return True  # If all operations are successful, return True
        except (IndexError, TypeError) as e:
            print(e)  # Display the error
            return False  # If an error is raised, return False

        

