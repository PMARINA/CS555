import unittest

from gedutil import US02, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS02(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_deat(self):
        u = US02()
        path = stabilize("us02", "marr_before_birth")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US02.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "before birth" in doc["message"].lower()
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US02()
        path = stabilize("us02", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("This test case should not have raised errors")
