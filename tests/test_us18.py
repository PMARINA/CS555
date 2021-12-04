import unittest

from gedutil import US18, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS18(unittest.TestCase):
    """
    Assignment:

    > Siblings should not marry one another
    """

    def test_married_descendant(self):
        u = US18()
        path = stabilize("US18", "sibling")
        p = Parser(path)
        p.read()
        p.parse()
        raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US18.name
            assert doc["error type"] == Error_Type.ERROR.name
            raised += 1
        assert raised == 1

    def test_valid(self):
        u = US18()
        path = stabilize("US18", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Errors were raised")


if __name__ == "__main__":
    TestUS18().test_valid()
