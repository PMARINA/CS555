import unittest

from gedutil import US14, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS14(unittest.TestCase):
    """
    Many children at once

    Family:
    F6000000178632081948
    Original Child: I6000000178633633868
    Changed to: Imany%d
    """

    def test_6_children_at_once(self):
        u = US14()
        path = stabilize("US14", "6_children_at_once")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US14.name
            assert doc["error type"] == Error_Type.ERROR.name
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US14()
        path = stabilize("US14", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("An error should not have been raised")
