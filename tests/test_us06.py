import unittest

from gedutil import US06, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS06(unittest.TestCase):
    """
    This test checks to see that death only occurred after marriage.

    """

    def test_deat(self):
        u = US06()
        path = stabilize("us06", "deat_before_div")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US06()
        path = stabilize("us06", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
