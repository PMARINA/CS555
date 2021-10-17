#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 16:45:47 2021

@author: manthan
"""


import individual
import dateutil.relativedelta
import ErrorLogger
import date_diff_calculator

class Family:

    def setup(self):  # pragma: no cover
        pass
    
    def __init__(self):
        self.type = "F"
        self.id = ""
        self.marriageDate = None
        self.marriageDateStr = "NA"
        self.divorcedDate = None
        self.divorcedDateStr = "NA"
        self.husbandId = ""
        self.husbandName = ""
        self.wifeId = ""
        self.wifeName = ""
        self.children = []
        ##Adding Lastname and for US16
        self.lastName = ""
        self.gender = ""
        pass

    def toString(self):
        if self.marriageDate is not None:
            self.marriageDateStr = self.marriageDate.strftime('%d %b %Y')
        if self.divorcedDate is not None:
            self.divorcedDateStr = self.divorcedDate.strftime('%d %b %Y')
            
    def run(self,individuals,child):
        result = True
        marriageDate = None
        divorceDate = None

        # Validate the mother record
        if self.wifeId is not None:
            mother = individuals[self.wifeId]
            marriageDate = self.marriageDate
            divorceDate = self.divorcedDate
           
        # Validate the father record
        if self.husbandId is not None:
            father = individuals[self.husbandId]
        
        # Validate the child record and compare dates
        if child.birthDate is not None:
            if marriageDate is not None:
                marriageDiff = date_diff_calculator.calculateDateDifference(marriageDate, child.birthDate, "months")
                if marriageDiff < 9:
                    ErrorLogger.__logError__(ErrorLogger._FAMILY,"US08", self.id, str("Child " + child.id + " born on " + str(child.birthDate) + " is before marriage date of " + str(marriageDate)))
                    result = False
            if divorceDate is not None:
                divorceDiff = date_diff_calculator.calculateDateDifference(divorceDate, child.birthDate, "months")
                if divorceDiff > 9:
                    ErrorLogger.__logError__(ErrorLogger._FAMILY,"US08", self.id, str("Child " + child.id + " born on " + str(child.birthDate) + " is more than 9 months after divorce date of " + str(divorceDate)))
                    result = False
        else:
            ErrorLogger.__logError__(ErrorLogger._FAMILY,"US08", self.id, str("Child " + child.id + " has no birth date."))
            result = "error"

        return result   
