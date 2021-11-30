import unittest

from gedutil import US14, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS14(unittest.TestCase):
    """
    This test checks to see that there are less than 5 siblings born at the same time.

    """

    def test_many_same_time_siblings(self):
        u = US14()
        path = stabilize("us14", "many_same_time_siblings")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US14.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "5" in doc["message"]
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US14()
        path = stabilize("us14", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("An error should not have been raised")
