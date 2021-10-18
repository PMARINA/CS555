#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 16:45:47 2021

@author: manthan
"""
import datetime
import logging
import logging.config
from logging import FileHandler

import dateutil.relativedelta
from dateutil import relativedelta


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

    logger = logging.getLogger("gedcomLogger")
    fileHandler = logging.FileHandler("gedcomError.log", "w")

    _logMessages = [""]
    _ANOMALY = "ANOMALY"
    _ERROR = "ERROR"
    _INDIVIDUAL = "INDIVIDUAL"
    _FAMILY = "FAMILY"
    _GENERAL = "GENERAL"

    def __initLogger__(default=""):
        Family.logger.addHandler(Family.fileHandler)
        Family.logger.setLevel(logging.DEBUG)

    def __logAnomaly__(recordType, userStory, id, messsage):
        msg = (
            Family._ANOMALY
            + ": "
            + recordType
            + ": "
            + userStory
            + ": "
            + str(id)
            + ": "
            + messsage
        )
        Family.logger.info(msg)
        Family._logMessages.append(msg)

    def __logError__(recordType, userStory, id, messsage):
        msg = (
            Family._ERROR
            + ": "
            + recordType
            + ": "
            + userStory
            + ": "
            + str(id)
            + ": "
            + messsage
        )
        Family.logger.error(msg)
        Family._logMessages.append(msg)

    def __printLogMessages__(default=""):
        for message in Family._logMessages:
            print(message)

        # calculates the delta between two dates in requested units years, days, months, hours with the units as a string otherwise it will just return the datedelta object

    def calculateDateDifference(calcStartDate, calcEndDate, requestedDateUnit):
        startDate = calcStartDate
        endDate = calcEndDate
        if startDate is None:
            startDate = datetime.datetime.now()
        if endDate is None:
            endDate = datetime.datetime.now()
        dateDelta = relativedelta.relativedelta(endDate, startDate)

        if requestedDateUnit is "years":
            return dateDelta.years

        elif requestedDateUnit is "days":
            return dateDelta.days

        elif requestedDateUnit is "months":
            deltaMonths = dateDelta.years * 12 + dateDelta.months
            return deltaMonths

        elif requestedDateUnit is "hours":
            return dateDelta.hours

        else:
            return dateDelta

    def isSecondNumberBigger(firstNumber, secondNumber):
        return secondNumber > firstNumber

    def toString(self):
        if self.marriageDate is not None:
            self.marriageDateStr = self.marriageDate.strftime("%d %b %Y")
        if self.divorcedDate is not None:
            self.divorcedDateStr = self.divorcedDate.strftime("%d %b %Y")

    def run(self, individuals, child):
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
                marriageDiff = Family.calculateDateDifference(
                    marriageDate, child.birthDate, "months"
                )
                if marriageDiff < 9:
                    ErrorLogger.__logError__(
                        ErrorLogger._FAMILY,
                        "US08",
                        self.id,
                        str(
                            "Child "
                            + child.id
                            + " born on "
                            + str(child.birthDate)
                            + " is before marriage date of "
                            + str(marriageDate)
                        ),
                    )
                    result = False
            if divorceDate is not None:
                divorceDiff = Family.calculateDateDifferencecalculateDateDifference(
                    divorceDate, child.birthDate, "months"
                )
                if divorceDiff > 9:
                    ErrorLogger.__logError__(
                        ErrorLogger._FAMILY,
                        "US08",
                        self.id,
                        str(
                            "Child "
                            + child.id
                            + " born on "
                            + str(child.birthDate)
                            + " is more than 9 months after divorce date of "
                            + str(divorceDate)
                        ),
                    )
                    result = False
        else:
            ErrorLogger.__logError__(
                ErrorLogger._FAMILY,
                "US08",
                self.id,
                str("Child " + child.id + " has no birth date."),
            )
            result = "error"

        return result
