import unittest

from gedutil import US02, GED_Line, GED_Tag, Parser, errors
from gedutil.base import Error_Type, User_Story

from .path_util import stabilize


class TestUS02(unittest.TestCase):
    """
    This test checks to see that birth only occurred before marriage.

    """

    def test_invalid(self):
        u = US02()
        path = stabilize("us02", "birthBeforeMarr")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US02.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "after marriage date" in doc["message"].lower()
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
            raise Exception(
                "This test should not have created any errors in the database"
            )
