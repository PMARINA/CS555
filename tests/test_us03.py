import unittest

from gedutil import US03, GED_Line, GED_Tag, Parser, errors
from gedutil.base import Error_Type, User_Story

from .path_util import stabilize


class TestUS03(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_invalid(self):
        u = US03()
        path = stabilize("us03", "deathBeforeBirth")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US03.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "after death date" in doc["message"].lower()

    def test_valid(self):
        u = US03()
        path = stabilize("us03", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception(
                "This test should not have created any errors in the database"
            )
