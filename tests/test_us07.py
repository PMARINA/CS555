import unittest

from path_util import stabilize

from gedutil import US07, GED_Line, GED_Tag, Parser


class TestUS07(unittest.TestCase):
    """
    This User Story verifies that death should be less than 150 years
    """

    def test_deat(self):
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
