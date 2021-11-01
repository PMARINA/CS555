import unittest

from gedutil import US37, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS37(unittest.TestCase):
    """
    Assignment:

    > List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days

    """

    def test_recent_death(self):
        # Note that the input file to this test will have to be modified
        # As the 30 days ago deadline means that unless I programmatically
        # edit the date (which could mask potential errors), it is
        # impossible to make this test case always valid
        u = US37()
        path = stabilize("us37", "recent_death")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        results = 0
        for e in errors.find():
            results += 1
        assert results == 1

    def test_valid(self):
        u = US37()
        path = stabilize("us37", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("No errors should have been raised")
