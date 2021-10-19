import unittest

from gedutil import US06, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS06(unittest.TestCase):
    """
    This test checks to see that death only occurred after marriage.

    """

    def test_deat(self):
        u = US06()
        path = stabilize("us06", "deat_before_div")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            num_raised += 1
            assert doc["user story"] == User_Story.US06.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "before divorce" in doc["message"].lower()
        assert num_raised == 1

    def test_valid(self):
        u = US06()
        path = stabilize("us06", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Nothing should've been added to the errors collection")
