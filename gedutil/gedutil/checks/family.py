#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 19:12:47 2021

@author: manthan
"""

import date_diff_calculator
import dateutil.relativedelta
import ErrorLogger
import individual


class Family:
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

    def toString(self):
        if self.marriageDate is not None:
            self.marriageDateStr = self.marriageDate.strftime("%d %b %Y")
        if self.divorcedDate is not None:
            self.divorcedDateStr = self.divorcedDate.strftime("%d %b %Y")
