#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 17:35:32 2021

@author: manthan
"""

import logging
import logging.config
from logging import FileHandler


# -----------------------------------------------------------------------------
# User Story #15: A family must have less than 15 siblings.
# -----------------------------------------------------------------------------
class US15:

    logger = logging.getLogger("gedcomLogger")
    fileHandler = logging.FileHandler("gedcomError.log", "w")

    _logMessages = [""]
    _ANOMALY = "ANOMALY"
    _ERROR = "ERROR"
    _INDIVIDUAL = "INDIVIDUAL"
    _FAMILY = "FAMILY"
    _GENERAL = "GENERAL"

    def __initLogger__(default=""):
        #        logger.config.dictConfig(GEDCOM_LOGGER)
        US15.logger.addHandler(US15.fileHandler)
        US15.logger.setLevel(logging.DEBUG)

    def __logAnomaly__(recordType, userStory, id, messsage):
        msg = (
            US15._ANOMALY
            + ": "
            + recordType
            + ": "
            + userStory
            + ": "
            + str(id)
            + ": "
            + messsage
        )
        US15.logger.info(msg)
        US15._logMessages.append(msg)

    def __logError__(recordType, userStory, id, messsage):
        msg = (
            US15._ERROR
            + ": "
            + recordType
            + ": "
            + userStory
            + ": "
            + str(id)
            + ": "
            + messsage
        )
        US15.logger.error(msg)
        US15._logMessages.append(msg)

    def __printLogMessages__(default=""):
        for message in US15._logMessages:
            print(message)

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(the_family):

        result = True

        if len(the_family.children) >= 15:
            result = False
            US15.__logError__(
                US15._FAMILY,
                "US15",
                the_family.id,
                "There are too many (" + str(len(the_family.children)) + ") siblings.",
            )

        return result
