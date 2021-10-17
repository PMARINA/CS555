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
def less_than_15_siblings(the_family):
    """
    ---------------------------------------------------------------------------
    This function checks whether the family contains less than 15 siblings.
    User Story #15.
    Parameters
    ----------
    the_family:      The family object to test whether there are less than 15
                     siblings.
    Returns
    -------
    True:  When there are less than 15 siblings in the family.
    False: When there are 15 or more siblings in the family.
    ---------------------------------------------------------------------------
    """
    result = True

    if len(the_family.children) >= 15:
        result = False
        ErrorLogger.__logError__(ErrorLogger._FAMILY, "US15", the_family.id, \
            "There are too many (" + str(len(the_family.children)) + ") siblings.")

    return result