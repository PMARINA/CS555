import unittest

from gedutil import US02, GED_Line, GED_Tag, Parser, errors
from gedutil.base import Error_Type, User_Story

from .path_util import stabilize

TESTFILE_CONTROL = stabilize("US02", "control")
TESTFILE_SHOULD_FAIL = stabilize("US02", "should_fail")


class TestUS02(unittest.TestCase):
    """
    The assignment:

    > Birth should occur before marriage of an individual
    """

    def test_control(self):
        u = US02()
        p = Parser(TESTFILE_CONTROL)
        p.read()
        p.parse()
        u.run()
        for _ in errors.find():
            raise Exception("Error was raised in control file")

    def test_marr_before_birth(self):
        u = US02()
        p = Parser(TESTFILE_SHOULD_FAIL)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            num_raised += 1
            # No other errors should be raised
            assert doc["user story"] == User_Story.US02.name
            # They should only be errors
            assert doc["error type"] == Error_Type.ERROR.name
        # Wife born 28 Jan 1948
        # Husb born 20 May 1952
        # Marr 4 Dec 1947
        assert num_raised == 2
