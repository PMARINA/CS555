import unittest

from gedutil import US20, GED_Line, GED_Tag, Parser, errors
from gedutil.base import Error_Type, User_Story

from .path_util import stabilize


class TestUS20(unittest.TestCase):
    """
    This test checks to see that all IDs in the database/input file are unique

    """

    def test_cyclic(self):
        u = US20()
        path = stabilize("us20", "cyclic")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US20.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "generation" in doc["message"].lower()
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US20()
        path = stabilize("us20", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Error shouldn't have been raised")
