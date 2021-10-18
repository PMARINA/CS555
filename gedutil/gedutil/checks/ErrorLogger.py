#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 16:49:54 2021

@author: manthan
"""

import logging
import logging.config
from logging import FileHandler

logger = logging.getLogger("gedcomLogger")
fileHandler = logging.FileHandler("gedcomError.log", "w")

_logMessages = []
_ANOMALY = "ANOMALY"
_ERROR = "ERROR"
_INDIVIDUAL = "INDIVIDUAL"
_FAMILY = "FAMILY"
_GENERAL = "GENERAL"


def __initLogger__():
    #        logger.config.dictConfig(GEDCOM_LOGGER)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)


def __logAnomaly__(recordType, userStory, id, messsage):
    msg = (
        _ANOMALY
        + ": "
        + recordType
        + ": "
        + userStory
        + ": "
        + str(id)
        + ": "
        + messsage
    )
    logger.info(msg)
    _logMessages.append(msg)


def __logError__(recordType, userStory, id, messsage):
    msg = (
        _ERROR + ": " + recordType + ": " + userStory + ": " + str(id) + ": " + messsage
    )
    logger.error(msg)
    _logMessages.append(msg)


def __printLogMessages__():
    for message in _logMessages:
        print(message)
