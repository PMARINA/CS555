import unittest

from gedutil import US05, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS05(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.
    """

    def test_deat(self):
        u = US05()
        path = stabilize("us05", "deat_before_marr")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US05.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "before marriage" in doc["message"].lower()
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US05()
        path = stabilize("us05", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("This test case should not have raised errors")
