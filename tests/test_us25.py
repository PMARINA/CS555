import unittest

from gedutil import US25, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS25(unittest.TestCase):
    """
    Assignment:

    > No more than one child with the same name and birth date should appear in a family

    """

    def test_duplicate(self):
        u = US25()
        path = stabilize("us25", "duplicate_child")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US25()
        path = stabilize("us25", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
