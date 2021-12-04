import unittest

from gedutil import US11, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS11(unittest.TestCase):
    """
    This test checks to see that marriage is at least 14 years after birth of both spouses (parents must be at least 14 years old)

    """

    def test_current_bigamy(self):
        u = US11()
        path = stabilize("US11", "current_bigamy")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US11.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "current" in doc["message"]
            num_raised += 1
        assert num_raised == 1

    def test_past_bigamy(self):
        u = US11()
        path = stabilize("US11", "past_bigamy")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US11.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "past" in doc["message"]
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US11()
        path = stabilize("US11", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("No error should have been raised")
