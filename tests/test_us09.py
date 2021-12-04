import unittest

from gedutil import US09, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS09(unittest.TestCase):
    """
    People born after death of parents:

    The family to suffer: F6000000178633463856
    Wife: I6000000178632590889
    Husb: I6000000178633463852
    Chil: I6000000178633772854 BORN 5 AUG 1997
    """

    def test_birth_after_paternal_death(self):
        u = US09()
        path = stabilize("US09", "birth_after_father_death")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            num_raised += 1
            assert doc["user story"] == User_Story.US09.name
            assert doc["error type"] == Error_Type.ERROR.name
        assert num_raised == 1

    def test_birth_after_maternal_deat(self):
        u = US09()
        path = stabilize("US09", "birth_after_mother_death")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            num_raised += 1
            assert doc["user story"] == User_Story.US09.name
            assert doc["error type"] == Error_Type.ERROR.name
        assert num_raised == 1

    def test_valid(self):
        u = US09()
        path = stabilize("US09", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Nothing should've been added to the errors collection")
