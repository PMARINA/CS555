import unittest

from gedutil import US29, GED_Line, GED_Tag, Parser

from .path_util import stabilize


class TestUS29(unittest.TestCase):
    """
    Assignment:

    > List all deceased individuals in a GEDCOM file

    """

    def test_valid(self):
        u = US29()
        path = stabilize("us29", "control")
        p = Parser(path)
        p.read()
        p.parse()
        output = u.run()
        assert len(output) == 1
