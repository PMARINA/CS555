import unittest

from gedutil import US16, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS16(unittest.TestCase):
    """
    Assignment:

    > All male members of a family should have the same last name
    """

    def test_changed_lname(self):
        u = US16()
        path = stabilize("us16", "wrong_last_name")
        p = Parser(path)
        p.read()
        p.parse()
        raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US16.name
            assert doc["error type"] == Error_Type.ANOMALY.name
            assert "family name" in doc["message"].lower()
            raised += 1
        assert raised == 1

    def test_valid(self):
        u = US16()
        path = stabilize("us16", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Errors were raised")


if __name__ == "__main__":
    TestUS16().test_valid()
