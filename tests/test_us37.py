import unittest

from gedutil import US37, GED_Line, GED_Tag, Parser

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
        res = u.run()
        assert len(res) == 1
        key = [k for k in res.keys()][0]
        assert len(res[key]["children"]) == 2
        assert len(res[key]["spouses"]) == 1

    def test_valid(self):
        u = US37()
        path = stabilize("us37", "control")
        p = Parser(path)
        p.read()
        p.parse()
        res = u.run()
        assert len(res) == 0
