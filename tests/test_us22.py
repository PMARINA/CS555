import unittest

from gedutil import US22, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS22(unittest.TestCase):
    """
    This test checks to see that all IDs in the database/input file are unique

    """

    def test_nonunique_fam(self):
        u = US22()
        path = stabilize("us22", "nonunique_family")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_nonunique_id(self):
        u = US22()
        path = stabilize("us22", "nonunique_individual")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US22()
        path = stabilize("us22", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
