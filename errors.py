#errors.py
#Drake Wheeler
#CS302
#Program 4-5
#Karla Fant
#8/13/2024
#This file holds the the custom error classes that are all derived from the built-in Exception class. This allows me to raise errors with custom variable names.

class MissingDataError(Exception):
    #This Error is for when there is missing data

    pass


class RedundancyError(Exception):
    #Raise when something was done redundantly, unnecessarily
    pass