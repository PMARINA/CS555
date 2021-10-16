import unittest

from gedutil import US16, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS16(unittest.TestCase):
    """
    Assignment:

    > All male members of a family should have the same last name
    """

    def test_changed_lname(self):
        u = US16()
        path = stabilize("us16", "wrong_last_name")
        p = Parser(path)
        p.read()
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_valid(self):
        u = US16()
        path = stabilize("us16", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()


if __name__ == "__main__":
    TestUS16().test_valid()
