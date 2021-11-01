import unittest

from gedutil import US10, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS10(unittest.TestCase):
    """
    This test checks to see that marriage is at least 14 years after birth of both spouses (parents must be at least 14 years old)

    """

    def test_marr14(self):
        u = US10()
        path = stabilize("us10", "early_marriage")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US10.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "years of marriage" in doc["message"].lower()
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US10()
        path = stabilize("us10", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("No error should have been raised")
