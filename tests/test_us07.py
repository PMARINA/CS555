import unittest

from gedutil import US07, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS07(unittest.TestCase):
    def test_yearsAlive(self):
        u = US07()
        path = stabilize("us07", "yearsAlive")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US07()
        path = stabilize("us07", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
