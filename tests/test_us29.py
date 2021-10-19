import unittest

from gedutil import US29, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

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
        u.run()
        num_found = 0
        for doc in errors.find():
            num_found += 1
        assert num_found == 1
