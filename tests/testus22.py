import unittest

from gedutil import US22, GED_Line, GED_Tag, Parser


class TestUS22(unittest.TestCase):
    """
    This test checks to see that all IDs in the database/input file are unique

    """

    def test_nonunique_fam(self):
        u = US22()
        p = Parser("input_files/US22/nonunique_family.ged")
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_nonunique_id(self):
        u = US22()
        p = Parser("input_files/US22/nonunique_individual.ged")
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US22()
        p = Parser("input_files/US22/control.ged")
        p.read()
        p.parse()
        u.run()
