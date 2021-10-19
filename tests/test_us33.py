import unittest

from gedutil import US33, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS33(unittest.TestCase):
    """
    Assignment:

    > List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file

    """

    def test_one_orphan(self):
        u = US33()
        path = stabilize("us33", "orphan")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            num_raised += 1
            assert doc["user story"] == User_Story.US33.name
            assert doc["error type"] == Error_Type.RESULT.name
        assert num_raised == 1

    def test_valid(self):
        u = US33()
        path = stabilize("us33", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for err in errors.find():
            raise Exception("No orphans should've been found")
