import unittest

from gedutil import US12, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS12(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_dad_too_old(self):
        u = US12()
        path = stabilize("us12", "man_too_old")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US12.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "AMAB" in doc["message"]
            num_raised += 1
        assert num_raised == 1

    def test_mom_too_old(self):
        u = US12()
        path = stabilize("us12", "woman_too_old")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US12.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "AFAB" in doc["message"]
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US12()
        path = stabilize("us12", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("An error should not have been raised")
