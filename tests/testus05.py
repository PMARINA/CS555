import unittest

from gedutil import US05, GED_Line, GED_Tag, Parser


class TestUS05(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_deat(self):
        u = US05()
        p = Parser("input_files/US05/deat_before_marr.ged")
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US05()
        p = Parser("input_files/US05/control.ged")
        p.read()
        p.parse()
        u.run()
