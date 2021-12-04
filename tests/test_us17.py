import unittest

from gedutil import US17, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS17(unittest.TestCase):
    """
    Assignment:

    > Parents should not marry any of their descendants
    """

    def test_married_descendant(self):
        u = US17()
        path = stabilize("US17", "descendant")
        p = Parser(path)
        p.read()
        p.parse()
        raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US17.name
            assert doc["error type"] == Error_Type.ERROR.name
            raised += 1
        assert raised == 1

    def test_valid(self):
        u = US17()
        path = stabilize("US17", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Errors were raised")


if __name__ == "__main__":
    TestUS17().test_valid()
