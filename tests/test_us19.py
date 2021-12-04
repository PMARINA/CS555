import unittest

from gedutil import US19, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS19(unittest.TestCase):
    """
    Assignment:

    > First Cousins should not marry one another
    """

    def test_married_cousins(self):
        u = US19()
        path = stabilize("US19", "cousin")
        p = Parser(path)
        p.read()
        p.parse()
        raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US19.name
            assert doc["error type"] == Error_Type.ERROR.name
            raised += 1
        assert raised == 1

    def test_valid(self):
        u = US19()
        path = stabilize("US19", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Errors were raised")


if __name__ == "__main__":
    TestUS19().test_valid()
