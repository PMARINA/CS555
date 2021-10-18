import unittest

from gedutil import US12, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS12(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_dad_too_old(self):
        u = US12()
        path = stabilize("us12", "man_too_old")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_mom_too_old(self):
        u = US12()
        path = stabilize("us12", "woman_too_old")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US12()
        path = stabilize("us12", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
