import unittest

from gedutil import US22, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

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
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US22.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "non unique" in doc["message"].lower()
            num_raised += 1
        assert num_raised == 1

    def test_nonunique_id(self):
        u = US22()
        path = stabilize("us22", "nonunique_individual")
        p = Parser(path)
        p.read()
        p.parse()
        num_raised = 0
        u.run()
        for doc in errors.find():
            assert doc["user story"] == User_Story.US22.name
            assert doc["error type"] == Error_Type.ERROR.name
            assert "non unique" in doc["message"].lower()
            num_raised += 1
        assert num_raised == 1

    def test_valid(self):
        u = US22()
        path = stabilize("us22", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("Shouldn't have errored")
