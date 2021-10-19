import unittest

from gedutil import US25, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS25(unittest.TestCase):
    """
    Assignment:

    > No more than one child with the same name and birth date should appear in a family

    """

    def test_duplicate(self):
        u = US25()
        path = stabilize("us25", "duplicate_child")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US25.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "Duplicate child" in doc["message"]
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US25()
        path = stabilize("us25", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("No errors should've been found")
