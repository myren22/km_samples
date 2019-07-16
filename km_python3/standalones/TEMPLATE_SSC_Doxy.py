#!/usr/bin/python3
##############################################################################
# $Header$
#
# Copyright (c) 2003 - 2018 Shared Spectrum Company.
# All rights reserved.
#
# This information is Shared Spectrum Company proprietary and
# may be protected by patents or pending patents.
#
# The Government"s rights to use, modify, reproduce, release, perform, display,
# or disclose this software are restricted by the Rights in Noncommercial
# Computer Software and Noncommercial Computer Software Documentation clause
# contained in the contract and the restrictions and markings set forth in the
# software documentation and other accompanying printed material.
# Any reproduction of the software or portions thereof marked with this legend
# must also reproduce the markings.
#
# Filename      : TEMPLATE_SSC_Doxy.py
# Author        : Shared Spectrum Company - Kyle Myren
# Creation Date : (c) 20018 - 2019
#
# Description   : A class that does XXX by reading the input from YYYY
#
#
# Classification: UNCLASSIFIED
#############################################################################
import os
import sys
import time
import argparse
import unittest

##@class MyClas - quick description class purpse.
#
#Long form description of class and its role.
class MyClass():
    """
    classdocs. This is captured by most IDEs
    """

    ##Initialize the class.
    #
    #This initializes the class with default values.
    def __init__(self, param1, param2):
        """
        Constructor
        """
        self.someValue=None
        pass
        
    ##Brief summary of aMethod
    #
    #This a filler long form description of what could occur in aMethod. 
    #This description will be captured by Doxygen.
    def aMethod(self):
        """
        aMethod notes
        """
        pass
        
    ##Print Hello to the user
    #
    #This is a method to print "hello!" followed by an optional 2nd string.
    #@param extraStr Optional String input that will be printed after "hello!"
    #           The "@param is necessary to be captured and formatted with doxygen.
    def printHello(self, extraStr=""):
        """
        printHello prints hello!, and maybe some extra info if provided
        """
        print("hello!",extraStr)
        
if __name__ == "__main__":
    """
    This is only called if the file is called directly by user when running python.
    if imported by other classes it does not run.
    """
    aClassObj = MyClass(1, "aStr")
    aClassObj.printHello()
    