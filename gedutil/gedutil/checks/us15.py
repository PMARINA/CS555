#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 17:35:32 2021

@author: manthan
"""

import ErrorLogger


# -----------------------------------------------------------------------------
# User Story #15: A family must have less than 15 siblings.
# -----------------------------------------------------------------------------
class US15:
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(the_family):

        result = True

        if len(the_family.children) >= 15:
            result = False
            ErrorLogger.__logError__(
                ErrorLogger._FAMILY,
                "US15",
                the_family.id,
                "There are too many (" + str(len(the_family.children)) + ") siblings.",
            )

        return result
