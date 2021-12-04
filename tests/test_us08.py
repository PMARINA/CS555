import unittest

from gedutil import US08, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS08(unittest.TestCase):
    """
    Birth too far away from divorce/marriage

    """

    def test_birth_after_div(self):
        u = US08()
        path = stabilize("US08", "birt_after_div")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            num_raised += 1
            assert doc["user story"] == User_Story.US08.name
            assert doc["error type"] == Error_Type.ANOMALY.name
        assert num_raised == 1

    def test_birth_before_marr(self):
        u = US08()
        path = stabilize("US08", "birt_before_marr")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            num_raised += 1
            assert doc["user story"] == User_Story.US08.name
            assert doc["error type"] == Error_Type.ANOMALY.name
        assert num_raised == 1

    def test_valid(self):
        u = US08()
        path = stabilize("US08", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Nothing should've been added to the errors collection")
