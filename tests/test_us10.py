import unittest

from gedutil import US10, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS10(unittest.TestCase):
    """
    This test checks to see that marriage is at least 14 years after birth of both spouses (parents must be at least 14 years old)

    """

    def test_marr14(self):
        u = US10()
        path = stabilize("us10", "early_marriage")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US10()
        path = stabilize("us10", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
