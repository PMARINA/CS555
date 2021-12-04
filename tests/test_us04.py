import unittest

from gedutil import US04, GED_Line, GED_Tag, Parser, errors
from gedutil.base import Error_Type, User_Story

from .path_util import stabilize

TESTFILE_CONTROL = stabilize("US04", "control")
TESTFILE_DIV_BEFORE_MARR = stabilize("US04", "div_before_marr")
TESTFILE_DIV_WITHOUT_MARR = stabilize("US04", "div_without_marr")


class TestUS04(unittest.TestCase):
    """
    The assignment:

    > Marriage should occur before divorce of spouses, and divorce can only occur after marriage

    The family I'm messing with: F6000000178633463856 (because no death occurs)
    """

    def test_control(self):
        u = US04()
        p = Parser(TESTFILE_CONTROL)
        p.read()
        p.parse()
        u.run()
        for _ in errors.find():
            raise Exception("Error was raised in control file")

    def test_div_before_marr(self):
        u = US04()
        p = Parser(TESTFILE_DIV_BEFORE_MARR)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            num_raised += 1
            # No other errors should be raised
            assert doc["user story"] == User_Story.US04.name
            # They should only be errors
            assert doc["error type"] == Error_Type.ERROR.name
        # Div 3 APR 1997
        # Marr 4 APR 1997
        assert num_raised == 1

    def test_div_without_marr(self):
        u = US04()
        p = Parser(TESTFILE_DIV_WITHOUT_MARR)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            num_raised += 1
            # No other errors should be raised
            assert doc["user story"] == User_Story.US04.name
            # They should only be errors
            assert doc["error type"] == Error_Type.ERROR.name
        # DIV without marr on family specified above
        assert num_raised == 1
