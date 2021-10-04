import unittest

from gedutil import US06, GED_Line, GED_Tag, Parser


class TestUS06(unittest.TestCase):
    """
    This test checks to see that death only occurred after divorce.

    """

    def test_deat(self):
        u = US06()
        p = Parser("input_files/US06/deat_before_div.ged")
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US06()
        p = Parser("input_files/US06/control.ged")
        p.read()
        p.parse()
        u.run()
