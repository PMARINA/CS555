import unittest

from gedutil import US05, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS05(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_deat(self):
        u = US05()
        path = stabilize("us05", "deat_before_marr")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US05()
        path = stabilize("us05", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
