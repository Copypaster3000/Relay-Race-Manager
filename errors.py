#errors.py
#Drake Wheeler
#8/13/2024
#This file holds the custom error classes that are all derived from the built-in Exception class. This allows me to raise errors with custom variable names.

class MissingDataError(Exception):
    #This Error is for when there is missing data

    pass


class RedundancyError(Exception):
    #Raise when something was done redundantly, unnecessarily
    pass
