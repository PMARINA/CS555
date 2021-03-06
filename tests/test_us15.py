import unittest

from gedutil import US15, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS15(unittest.TestCase):
    """
    Many children at once

    Family:
    F6000000178632081948
    Original Child: I6000000178633633868
    Changed to: Imany%d
    """

    def test_15_children(self):
        u = US15()
        path = stabilize("US15", "15_children")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US15.name
            assert doc["error type"] == Error_Type.ERROR.name
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US15()
        path = stabilize("US15", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("An error should not have been raised")
