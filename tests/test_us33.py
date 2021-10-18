import unittest

from gedutil import US33, GED_Line, GED_Tag, Parser

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
        res = u.run()
        assert len(res) == 1

    def test_valid(self):
        u = US33()
        path = stabilize("us33", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
