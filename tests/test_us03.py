import unittest

from gedutil import US03, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS03(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_invalid(self):
        u = US03()
        path = stabilize("us03", "deathBeforeBirth")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US03()
        path = stabilize("us03", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
