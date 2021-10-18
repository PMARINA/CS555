import unittest

from gedutil import US20, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS20(unittest.TestCase):
    """
    This test checks to see that all IDs in the database/input file are unique

    """

    def test_cyclic(self):
        u = US20()
        path = stabilize("us20", "cyclic")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US20()
        path = stabilize("us20", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
